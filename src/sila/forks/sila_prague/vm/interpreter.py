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

from sila_types.bytes import Bytes, Bytes0
from sila_types.numeric import U256, Uint, ulen

from sila.exceptions import SilaException
from sila.state import Address
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

from ..blocks import Log
from ..state_tracker import (
    account_deployable,
    copy_tx_state,
    destroy_storage,
    get_account,
    get_code,
    increment_nonce,
    mark_account_created,
    move_sila,
    restore_tx_state,
    set_code,
)
from ..vm import Message
from ..vm.eoa_delegation import get_delegated_code_address, set_delegation
from ..vm.gas import GasCosts, charge_gas
from ..vm.precompiled_contracts.mapping import PRE_COMPILED_CONTRACTS
from . import Sivm
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
MAX_CODE_SIZE = 0x6000
MAX_INIT_CODE_SIZE = 2 * MAX_CODE_SIZE


@final
@dataclass
class MessageCallOutput:
    """
    Output of a particular message call.

    Contains the following:

          1. `gas_left`: remaining gas after execution.
          2. `refund_counter`: gas to refund after execution.
          3. `logs`: list of `Log` generated during execution.
          4. `accounts_to_delete`: Contracts which have self-destructed.
          5. `error`: The error from the execution if any.
          6. `return_data`: The output of the execution.
    """

    gas_left: Uint
    refund_counter: U256
    logs: Tuple[Log, ...]
    accounts_to_delete: Set[Address]
    error: Optional[SilaException]
    return_data: Bytes


def process_message_call(message: Message) -> MessageCallOutput:
    """
    If `message.target` is empty then it creates a smart contract
    else it executes a call from the `message.caller` to the `message.target`.

    Parameters
    ----------
    message :
        Transaction specific items.

    Returns
    -------
    output : `MessageCallOutput`
        Output of the message call

    """
    tx_state = message.tx_env.state
    refund_counter = U256(0)
    if message.target == Bytes0(b""):
        if account_deployable(tx_state, message.current_target):
            sivm = process_create_message(message)
        else:
            return MessageCallOutput(
                gas_left=Uint(0),
                refund_counter=U256(0),
                logs=tuple(),
                accounts_to_delete=set(),
                error=AddressCollision(),
                return_data=Bytes(b""),
            )
    else:
        if message.tx_env.authorizations != ():
            refund_counter += set_delegation(message)

        delegated_address = get_delegated_code_address(message.code)
        if delegated_address is not None:
            message.disable_precompiles = True
            message.accessed_addresses.add(delegated_address)
            message.code = get_code(
                tx_state,
                get_account(tx_state, delegated_address).code_hash,
            )
            message.code_address = delegated_address

        sivm = process_message(message)

    if sivm.error:
        logs: Tuple[Log, ...] = ()
        accounts_to_delete = set()
    else:
        logs = sivm.logs
        accounts_to_delete = sivm.accounts_to_delete
        refund_counter += U256(sivm.refund_counter)

    tx_end = TransactionEnd(
        int(message.gas) - int(sivm.gas_left), sivm.output, sivm.error
    )
    sivm_trace(sivm, tx_end)

    return MessageCallOutput(
        gas_left=sivm.gas_left,
        refund_counter=refund_counter,
        logs=logs,
        accounts_to_delete=accounts_to_delete,
        error=sivm.error,
        return_data=sivm.output,
    )


def process_create_message(message: Message) -> Sivm:
    """
    Executes a call to create a smart contract.

    Parameters
    ----------
    message :
        Transaction specific items.

    Returns
    -------
    sivm: :py:class:`~sila.forks.sila_prague.vm.Sivm`
        Items containing execution specific objects.

    """
    tx_state = message.tx_env.state
    # take snapshot of state before processing the message
    snapshot = copy_tx_state(tx_state)

    # If the address where the account is being created has storage, it is
    # destroyed. This can only happen in the following highly unlikely
    # circumstances:
    # * The address created by a `CREATE` call collides with a subsequent
    #   `CREATE` or `CREATE2` call.
    # * The first `CREATE` happened before SIP158 and left empty
    #   code.
    destroy_storage(tx_state, message.current_target)

    # In the previously mentioned edge case the preexisting storage is ignored
    # for gas refund purposes. In order to do this we must track created
    # accounts. This tracking is also needed to respect the constraints
    # added to SELFDESTRUCT by SIP-6780.
    mark_account_created(tx_state, message.current_target)

    increment_nonce(tx_state, message.current_target)
    sivm = process_message(message)
    if not sivm.error:
        contract_code = sivm.output
        contract_code_gas = (
            ulen(contract_code) * GasCosts.CODE_DEPOSIT_PER_BYTE
        )
        try:
            if len(contract_code) > 0:
                if contract_code[0] == 0xEF:
                    raise InvalidContractPrefix
            charge_gas(sivm, contract_code_gas)
            if len(contract_code) > MAX_CODE_SIZE:
                raise OutOfGasError
        except ExceptionalHalt as error:
            restore_tx_state(tx_state, snapshot)
            sivm.gas_left = Uint(0)
            sivm.output = b""
            sivm.error = error
        else:
            set_code(tx_state, message.current_target, contract_code)
    else:
        restore_tx_state(tx_state, snapshot)
    return sivm


def process_message(message: Message) -> Sivm:
    """
    Move sila and execute the relevant code.

    Parameters
    ----------
    message :
        Transaction specific items.

    Returns
    -------
    sivm: :py:class:`~sila.forks.sila_prague.vm.Sivm`
        Items containing execution specific objects

    """
    tx_state = message.tx_env.state
    if message.depth > STACK_DEPTH_LIMIT:
        raise StackDepthLimitError("Stack depth limit reached")

    code = message.code
    valid_jump_destinations = get_valid_jump_destinations(code)
    sivm = Sivm(
        pc=Uint(0),
        stack=[],
        memory=bytearray(),
        code=code,
        gas_left=message.gas,
        valid_jump_destinations=valid_jump_destinations,
        logs=(),
        refund_counter=0,
        running=True,
        message=message,
        output=b"",
        accounts_to_delete=set(),
        return_data=b"",
        error=None,
        accessed_addresses=message.accessed_addresses,
        accessed_storage_keys=message.accessed_storage_keys,
    )

    # take snapshot of state before processing the message
    snapshot = copy_tx_state(tx_state)

    if message.should_transfer_value and message.value != 0:
        move_sila(
            tx_state,
            message.caller,
            message.current_target,
            message.value,
        )

    try:
        if sivm.message.code_address in PRE_COMPILED_CONTRACTS:
            if not message.disable_precompiles:
                sivm_trace(sivm, PrecompileStart(sivm.message.code_address))
                PRE_COMPILED_CONTRACTS[sivm.message.code_address](sivm)
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
        sivm.gas_left = Uint(0)
        sivm.output = b""
        sivm.error = error
    except Revert as error:
        sivm_trace(sivm, OpException(error))
        sivm.error = error

    if sivm.error:
        restore_tx_state(tx_state, snapshot)
    return sivm
