"""
Sila Virtual Machine (Sivm) Interpreter.

.. contents:: Table of Contents
    :backlinks: none
    :local:

Introduction
------------

A straightforward interpreter that executes Sivm code.
"""

from dataclasses import dataclass
from typing import Optional, Set, Tuple, final

from sila_types.bytes import Bytes
from sila_types.numeric import U256, Uint, ulen

from sila.exceptions import SilaException
from sila.state import EMPTY_ACCOUNT, Address
from sila.trace import (
    OpEnd,
    OpException,
    OpStart,
    PrecompileEnd,
    PrecompileStart,
    SivmStop,
    TransactionEnd,
    sivm_trace,
)
from sila.utils.numeric import ceil32

from ..blocks import Log
from ..fork_types import ExecutionGas, StateGas
from ..state_tracker import (
    TransactionState,
    account_deployable,
    copy_tx_state,
    destroy_storage,
    get_account,
    get_code,
    get_pre_state_account,
    increment_nonce,
    is_account_alive,
    mark_account_created,
    move_sila,
    restore_tx_state,
    set_code,
)
from ..vm.gas import (
    GasCosts,
    GasMeter,
    StateGasCosts,
    charge_gas,
    charge_state_gas,
    charge_state_gas_from_meter,
    commit_state_gas,
    forfeit_remaining_gas,
    restore_state_gas,
    restore_state_gas_to_entry,
    tx_state_gas_used,
)
from ..vm.precompiled_contracts.mapping import PRE_COMPILED_CONTRACTS
from . import (
    BlockEnvironment,
    Sivm,
    TransactionEnvironment,
    emit_transfer_log,
)
from .eoa_delegation import resolve_delegated_code_address, set_delegation
from .exceptions import (
    AddressCollision,
    ExceptionalHalt,
    InvalidContractPrefix,
    InvalidOpcode,
    OutOfGasError,
    Revert,
    StackDepthLimitError,
)
from .instructions import Ops, op_implementation
from .runtime import get_valid_jump_destinations

STACK_DEPTH_LIMIT = Uint(1024)
MAX_CODE_SIZE = 0x10000
MAX_INIT_CODE_SIZE = 2 * MAX_CODE_SIZE


@final
@dataclass
class TransactionOutput:
    """
    Settled output of a transaction's top-level call.

    Carry the figures fee settlement and the receipt need, so the
    frame itself never leaves the interpreter.
    """

    gas_left: ExecutionGas
    """Execution gas remaining after execution."""

    refund_counter: U256
    """Gas eligible for refund at the end of the transaction."""

    logs: Tuple[Log, ...]
    """Logs emitted during execution; empty when it failed."""

    accounts_to_delete: Set[Address]
    """Accounts self-destructed during execution; empty when it failed."""

    error: Optional[SilaException]
    """The error the execution halted with, if any."""

    return_data: Bytes
    """The output of the execution."""

    state_gas_left: StateGas
    """State gas remaining in the reservoir after execution."""

    state_gas_used: int
    """Net state gas consumed; negative when refunds exceed charges."""


def charge_value_transfer_to_non_alive_account(
    state: TransactionState,
    gas_meter: GasMeter,
    recipient: Address,
    value: U256,
) -> None:
    """
    Charge the state gas for creating `recipient` when a value
    transfer revives an account that is not alive.
    """
    if value > U256(0) and not is_account_alive(state, recipient):
        charge_state_gas_from_meter(gas_meter, StateGasCosts.NEW_ACCOUNT)


def create_sivm(
    block_env: BlockEnvironment,
    tx_env: TransactionEnvironment,
    gas_meter: GasMeter,
) -> Sivm:
    """
    Build the transaction's top-level frame.

    Apply the SIP-7702 authorizations, charge the state-dependent
    dispatch costs to `gas_meter`, and resolve the code the frame
    runs. A preparation failure -- a creation-address collision or
    insufficient gas -- raises instead of building a frame, leaving
    the caller to roll back the state and gas the preparation charged
    and settle the transaction without dispatching.
    """
    current_target = tx_env.recipient
    if tx_env.is_create:
        call_data = Bytes(b"")
    else:
        call_data = tx_env.data

    code_address: Optional[Address] = None
    disable_precompiles = False
    accessed_addresses: Set[Address] = set()
    accessed_storage_keys = set(tx_env.access_list_storage_keys)

    ## Apply the 7702 delegations
    if tx_env.authorizations != ():
        accessed_authorities = set_delegation(block_env, tx_env, gas_meter)
        accessed_addresses.update(accessed_authorities)
        commit_state_gas(gas_meter)

    ## Warm up the access sets
    accessed_addresses.add(block_env.coinbase)
    accessed_addresses.update(PRE_COMPILED_CONTRACTS.keys())
    accessed_addresses.add(tx_env.origin)
    accessed_addresses.update(tx_env.access_list_addresses)
    accessed_addresses.add(current_target)

    ## Resolve dispatch and charge its state-dependent costs
    if tx_env.is_create:
        if not account_deployable(tx_env.state, current_target):
            raise AddressCollision()

        if (
            get_pre_state_account(tx_env.state, current_target)
            == EMPTY_ACCOUNT
        ):
            charge_state_gas_from_meter(gas_meter, StateGasCosts.NEW_ACCOUNT)

        code = tx_env.data
    else:
        charge_value_transfer_to_non_alive_account(
            tx_env.state, gas_meter, current_target, tx_env.value
        )

        code_address, disable_precompiles = resolve_delegated_code_address(
            tx_env.state, gas_meter, accessed_addresses, tx_env.recipient
        )

        code = get_code(
            tx_env.state,
            get_account(tx_env.state, code_address).code_hash,
        )

    ## Build the frame
    return Sivm(
        # Context
        block_env=block_env,
        tx_env=tx_env,
        parent_sivm=None,
        depth=Uint(0),
        # Call Parameters
        caller=tx_env.origin,
        current_target=current_target,
        value=tx_env.value,
        call_data=call_data,
        should_transfer_value=True,
        is_static=False,
        disable_precompiles=disable_precompiles,
        # Code
        code_address=code_address,
        code=code,
        valid_jump_destinations=get_valid_jump_destinations(code),
        # Machine State
        gas_meter=gas_meter,
        pc=Uint(0),
        stack=[],
        memory=bytearray(),
        return_data=b"",
        # Accrued Effects
        logs=(),
        accounts_to_delete=set(),
        accessed_addresses=accessed_addresses,
        accessed_storage_keys=accessed_storage_keys,
        # Outcome
        running=True,
        output=b"",
        error=None,
    )


def process_top_level(
    block_env: BlockEnvironment,
    tx_env: TransactionEnvironment,
) -> TransactionOutput:
    """
    Execute the top level of a transaction.

    Prepare the transaction's top-level Sivm frame and dispatch it: a
    contract creation or a call, per the transaction environment. A
    preparation failure rolls back everything the preparation changed
    and never dispatches; the transaction then settles as if
    execution halted at entry, forfeiting its entire gas grant.

    Parameters
    ----------
    block_env :
        Environment for the Sila Virtual Machine.
    tx_env :
        Environment for the transaction.

    Returns
    -------
    tx_output : `TransactionOutput`
        The settled output of the top-level execution.

    """
    gas_meter = GasMeter(
        gas_left=tx_env.execution_gas_grant,
        state_gas_left=tx_env.state_gas_reservoir,
        state_gas_baseline=tx_env.state_gas_reservoir,
    )

    prep_snapshot = copy_tx_state(tx_env.state)
    try:
        sivm = create_sivm(block_env, tx_env, gas_meter)
    except ExceptionalHalt as halt:
        # The rollback also reverts any applied delegations, so their
        # state gas commit is undone with it: roll state gas back to
        # frame entry, refilling every state charge.
        restore_tx_state(tx_env.state, prep_snapshot)
        restore_state_gas_to_entry(gas_meter, tx_env.state_gas_reservoir)
        forfeit_remaining_gas(gas_meter)
        return TransactionOutput(
            gas_left=gas_meter.gas_left,
            refund_counter=U256(gas_meter.refund_counter),
            logs=(),
            accounts_to_delete=set(),
            error=halt,
            return_data=Bytes(b""),
            state_gas_left=gas_meter.state_gas_left,
            state_gas_used=tx_state_gas_used(
                gas_meter, tx_env.state_gas_reservoir
            ),
        )

    if tx_env.is_create:
        process_create(sivm)
    else:
        process_call(sivm)

    # A failed execution contributes no logs or self-destructs.
    if sivm.error:
        logs: Tuple[Log, ...] = ()
        accounts_to_delete: Set[Address] = set()
    else:
        logs = sivm.logs
        accounts_to_delete = sivm.accounts_to_delete

    tx_end = TransactionEnd(
        int(tx_env.execution_gas_grant) - int(gas_meter.gas_left),
        sivm.output,
        sivm.error,
    )
    sivm_trace(sivm, tx_end)

    return TransactionOutput(
        gas_left=gas_meter.gas_left,
        refund_counter=U256(gas_meter.refund_counter),
        logs=logs,
        accounts_to_delete=accounts_to_delete,
        error=sivm.error,
        return_data=sivm.output,
        state_gas_left=gas_meter.state_gas_left,
        state_gas_used=tx_state_gas_used(
            gas_meter, tx_env.state_gas_reservoir
        ),
    )


def process_create(sivm: Sivm) -> Sivm:
    """
    Executes a call to create a smart contract.

    Parameters
    ----------
    sivm :
        Currently running sivm.

    Returns
    -------
    sivm: :py:class:`~sila.forks.sila_amsterdam.vm.Sivm`
        Items containing execution specific objects.

    """
    tx_state = sivm.tx_env.state
    # take snapshot of state before processing the message
    snapshot = copy_tx_state(tx_state)

    # If the address where the account is being created has storage, it is
    # destroyed. This can only happen in the following highly unlikely
    # circumstances:
    # * The address created by a `CREATE` call collides with a subsequent
    #   `CREATE` or `CREATE2` call.
    # * The first `CREATE` happened before SIP158 and left empty
    #   code.
    destroy_storage(tx_state, sivm.current_target)

    # In the previously mentioned edge case the preexisting storage is ignored
    # for gas refund purposes. In order to do this we must track created
    # accounts. This tracking is also needed to respect the constraints
    # added to SELFDESTRUCT by SIP-6780.
    mark_account_created(tx_state, sivm.current_target)

    increment_nonce(tx_state, sivm.current_target)

    sivm = process_call(sivm)
    if not sivm.error:
        contract_code = sivm.output
        try:
            if len(contract_code) > 0:
                if contract_code[0] == 0xEF:
                    raise InvalidContractPrefix
            if len(contract_code) > MAX_CODE_SIZE:
                raise OutOfGasError
            # Hash cost for computing keccak256 of deployed bytecode
            code_hash_gas = ExecutionGas(
                GasCosts.OPCODE_KECCAK256_PER_WORD
                * ceil32(ulen(contract_code))
                // Uint(32)
            )
            charge_gas(sivm, code_hash_gas)
            code_deposit_state_gas = (
                ulen(contract_code) * StateGasCosts.COST_PER_STATE_BYTE
            )
            charge_state_gas(sivm, code_deposit_state_gas)
        except ExceptionalHalt as error:
            restore_tx_state(tx_state, snapshot)
            # A create frame never applies authorizations, so its
            # baseline is still the frame's entry reservoir.
            restore_state_gas(sivm.gas_meter)
            forfeit_remaining_gas(sivm.gas_meter)
            sivm.output = b""
            sivm.error = error
        else:
            set_code(tx_state, sivm.current_target, contract_code)
    else:
        restore_tx_state(tx_state, snapshot)
    return sivm


def process_call(sivm: Sivm) -> Sivm:
    """
    Move sila and execute the relevant code.

    Parameters
    ----------
    sivm :
        The Sivm frame to execute.

    Returns
    -------
    sivm: :py:class:`~sila.forks.sila_amsterdam.vm.Sivm`
        Items containing execution specific objects

    """
    tx_state = sivm.tx_env.state
    if sivm.depth > STACK_DEPTH_LIMIT:
        raise StackDepthLimitError("Stack depth limit reached")

    snapshot = copy_tx_state(tx_state)

    # Execute message code and handle errors
    try:
        if sivm.should_transfer_value and sivm.value != 0:
            move_sila(
                tx_state,
                sivm.caller,
                sivm.current_target,
                sivm.value,
            )
            if sivm.caller != sivm.current_target:
                emit_transfer_log(
                    sivm,
                    sivm.caller,
                    sivm.current_target,
                    sivm.value,
                )
        if sivm.code_address in PRE_COMPILED_CONTRACTS:
            if not sivm.disable_precompiles:
                sivm_trace(sivm, PrecompileStart(sivm.code_address))
                PRE_COMPILED_CONTRACTS[sivm.code_address](sivm)
                sivm_trace(sivm, PrecompileEnd())
        else:
            while sivm.running and sivm.pc < ulen(sivm.code):
                try:
                    op = Ops(sivm.code[sivm.pc])
                except ValueError as e:
                    raise InvalidOpcode(sivm.code[sivm.pc]) from e

                sivm_trace(sivm, OpStart(op))
                op_implementation[op](sivm)
                sivm_trace(sivm, OpEnd())

            sivm_trace(sivm, SivmStop(Ops.STOP))

    except ExceptionalHalt as error:
        sivm_trace(sivm, OpException(error))
        # Frame settlement: refill state gas to the baseline, then
        # forfeit -- a halted frame returns no execution gas to its
        # parent. After these handlers the meter states exactly what
        # the frame gives back, so parents absorb unconditionally.
        restore_state_gas(sivm.gas_meter)
        forfeit_remaining_gas(sivm.gas_meter)
        sivm.output = b""
        sivm.error = error
    except Revert as error:
        sivm_trace(sivm, OpException(error))
        # Frame settlement: refill state gas to the baseline -- a
        # reverted frame returns its unspent `gas_left` to its parent.
        restore_state_gas(sivm.gas_meter)
        sivm.error = error

    if sivm.error:
        restore_tx_state(tx_state, snapshot)
    return sivm
