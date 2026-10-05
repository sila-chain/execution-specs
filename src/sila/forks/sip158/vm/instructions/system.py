"""
Sila Virtual Machine (Sivm) System Instructions.

.. contents:: Table of Contents
    :backlinks: none
    :local:

Introduction
------------

Implementations of the Sivm system related instructions.
"""

from dataclasses import dataclass
from typing import final

from sila_types.bytes import Bytes0
from sila_types.numeric import U256, Uint

from sila.state import Address

from ...state_tracker import (
    account_deployable,
    account_exists_and_is_empty,
    get_account,
    get_code,
    increment_nonce,
    is_account_alive,
    set_account_balance,
)
from ...utils.address import compute_contract_address, to_address_masked
from .. import (
    Message,
    Sivm,
    incorporate_child_on_error,
    incorporate_child_on_success,
)
from ..gas import (
    GasCosts,
    calculate_gas_extend_memory,
    calculate_message_call_gas,
    charge_gas,
    max_message_call_gas,
)
from ..memory import memory_read_bytes, memory_write
from ..stack import pop, push


def create(sivm: Sivm) -> None:
    """
    Creates a new account with associated code.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # This import causes a circular import error
    # if it's not moved inside this method
    from ...vm.interpreter import STACK_DEPTH_LIMIT, process_create_message

    # STACK
    endowment = pop(sivm.stack)
    memory_start_position = pop(sivm.stack)
    memory_size = pop(sivm.stack)

    # GAS
    extend_memory = calculate_gas_extend_memory(
        sivm.memory, [(memory_start_position, memory_size)]
    )

    charge_gas(sivm, GasCosts.OPCODE_CREATE_BASE + extend_memory.cost)

    create_message_gas = max_message_call_gas(Uint(sivm.gas_left))
    sivm.gas_left -= create_message_gas

    # OPERATION
    sivm.memory += b"\x00" * extend_memory.expand_by
    sender_address = sivm.message.current_target
    sender = get_account(sivm.message.tx_env.state, sender_address)

    contract_address = compute_contract_address(
        sivm.message.current_target,
        get_account(
            sivm.message.tx_env.state, sivm.message.current_target
        ).nonce,
    )

    if (
        sender.balance < endowment
        or sender.nonce == Uint(2**64 - 1)
        or sivm.message.depth + Uint(1) > STACK_DEPTH_LIMIT
    ):
        push(sivm.stack, U256(0))
        sivm.gas_left += create_message_gas
    elif not account_deployable(sivm.message.tx_env.state, contract_address):
        increment_nonce(sivm.message.tx_env.state, sivm.message.current_target)
        push(sivm.stack, U256(0))
    else:
        call_data = memory_read_bytes(
            sivm.memory, memory_start_position, memory_size
        )

        increment_nonce(sivm.message.tx_env.state, sivm.message.current_target)

        child_message = Message(
            block_env=sivm.message.block_env,
            tx_env=sivm.message.tx_env,
            caller=sivm.message.current_target,
            target=Bytes0(),
            gas=create_message_gas,
            value=endowment,
            data=b"",
            code=call_data,
            current_target=contract_address,
            depth=sivm.message.depth + Uint(1),
            code_address=None,
            should_transfer_value=True,
            parent_sivm=sivm,
        )
        child_sivm = process_create_message(child_message)

        if child_sivm.error:
            incorporate_child_on_error(sivm, child_sivm)
            push(sivm.stack, U256(0))
        else:
            incorporate_child_on_success(sivm, child_sivm)
            push(
                sivm.stack,
                U256.from_be_bytes(child_sivm.message.current_target),
            )

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def return_(sivm: Sivm) -> None:
    """
    Halts execution returning output data.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    memory_start_position = pop(sivm.stack)
    memory_size = pop(sivm.stack)

    # GAS
    extend_memory = calculate_gas_extend_memory(
        sivm.memory, [(memory_start_position, memory_size)]
    )

    charge_gas(sivm, GasCosts.ZERO + extend_memory.cost)

    # OPERATION
    sivm.memory += b"\x00" * extend_memory.expand_by
    sivm.output = memory_read_bytes(
        sivm.memory, memory_start_position, memory_size
    )

    sivm.running = False

    # PROGRAM COUNTER
    pass


@final
@dataclass
class GenericCall:
    """
    Parameters for the core logic of the `CALL*` family of opcodes.
    """

    gas: Uint
    value: U256
    caller: Address
    to: Address
    code_address: Address
    should_transfer_value: bool
    memory_input_start_position: U256
    memory_input_size: U256
    memory_output_start_position: U256
    memory_output_size: U256


def generic_call(sivm: Sivm, params: GenericCall) -> None:
    """
    Perform the core logic of the `CALL*` family of opcodes.
    """
    from ...vm.interpreter import STACK_DEPTH_LIMIT, process_message

    if sivm.message.depth + Uint(1) > STACK_DEPTH_LIMIT:
        sivm.gas_left += params.gas
        push(sivm.stack, U256(0))
        return

    call_data = memory_read_bytes(
        sivm.memory,
        params.memory_input_start_position,
        params.memory_input_size,
    )
    account = get_account(sivm.message.tx_env.state, params.code_address)
    code = get_code(sivm.message.tx_env.state, account.code_hash)
    child_message = Message(
        block_env=sivm.message.block_env,
        tx_env=sivm.message.tx_env,
        caller=params.caller,
        target=params.to,
        gas=params.gas,
        value=params.value,
        data=call_data,
        code=code,
        current_target=params.to,
        depth=sivm.message.depth + Uint(1),
        code_address=params.code_address,
        should_transfer_value=params.should_transfer_value,
        parent_sivm=sivm,
    )
    child_sivm = process_message(child_message)

    if child_sivm.error:
        incorporate_child_on_error(sivm, child_sivm)
        push(sivm.stack, U256(0))
    else:
        incorporate_child_on_success(sivm, child_sivm)
        push(sivm.stack, U256(1))

    actual_output_size = min(
        params.memory_output_size, U256(len(child_sivm.output))
    )
    memory_write(
        sivm.memory,
        params.memory_output_start_position,
        child_sivm.output[:actual_output_size],
    )


def call(sivm: Sivm) -> None:
    """
    Message-call into an account.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    gas = Uint(pop(sivm.stack))
    to = to_address_masked(pop(sivm.stack))
    value = pop(sivm.stack)
    memory_input_start_position = pop(sivm.stack)
    memory_input_size = pop(sivm.stack)
    memory_output_start_position = pop(sivm.stack)
    memory_output_size = pop(sivm.stack)

    # GAS
    extend_memory = calculate_gas_extend_memory(
        sivm.memory,
        [
            (memory_input_start_position, memory_input_size),
            (memory_output_start_position, memory_output_size),
        ],
    )

    code_address = to

    create_gas_cost = GasCosts.NEW_ACCOUNT
    if value == 0 or is_account_alive(sivm.message.tx_env.state, to):
        create_gas_cost = Uint(0)
    transfer_gas_cost = Uint(0) if value == 0 else GasCosts.CALL_VALUE
    message_call_gas = calculate_message_call_gas(
        value,
        gas,
        Uint(sivm.gas_left),
        memory_cost=extend_memory.cost,
        extra_gas=GasCosts.OPCODE_CALL_BASE
        + create_gas_cost
        + transfer_gas_cost,
    )
    charge_gas(sivm, message_call_gas.cost + extend_memory.cost)

    # OPERATION
    sivm.memory += b"\x00" * extend_memory.expand_by
    sender_balance = get_account(
        sivm.message.tx_env.state, sivm.message.current_target
    ).balance
    if sender_balance < value:
        push(sivm.stack, U256(0))
        sivm.gas_left += message_call_gas.sub_call
    else:
        generic_call(
            sivm,
            GenericCall(
                gas=message_call_gas.sub_call,
                value=value,
                caller=sivm.message.current_target,
                to=to,
                code_address=code_address,
                should_transfer_value=True,
                memory_input_start_position=memory_input_start_position,
                memory_input_size=memory_input_size,
                memory_output_start_position=memory_output_start_position,
                memory_output_size=memory_output_size,
            ),
        )

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def callcode(sivm: Sivm) -> None:
    """
    Message-call into this account with alternative account’s code.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    gas = Uint(pop(sivm.stack))
    code_address = to_address_masked(pop(sivm.stack))
    value = pop(sivm.stack)
    memory_input_start_position = pop(sivm.stack)
    memory_input_size = pop(sivm.stack)
    memory_output_start_position = pop(sivm.stack)
    memory_output_size = pop(sivm.stack)

    # GAS
    to = sivm.message.current_target

    extend_memory = calculate_gas_extend_memory(
        sivm.memory,
        [
            (memory_input_start_position, memory_input_size),
            (memory_output_start_position, memory_output_size),
        ],
    )
    transfer_gas_cost = Uint(0) if value == 0 else GasCosts.CALL_VALUE
    message_call_gas = calculate_message_call_gas(
        value,
        gas,
        Uint(sivm.gas_left),
        extend_memory.cost,
        GasCosts.OPCODE_CALL_BASE + transfer_gas_cost,
    )
    charge_gas(sivm, message_call_gas.cost + extend_memory.cost)

    # OPERATION
    sivm.memory += b"\x00" * extend_memory.expand_by
    sender_balance = get_account(
        sivm.message.tx_env.state, sivm.message.current_target
    ).balance
    if sender_balance < value:
        push(sivm.stack, U256(0))
        sivm.gas_left += message_call_gas.sub_call
    else:
        generic_call(
            sivm,
            GenericCall(
                gas=message_call_gas.sub_call,
                value=value,
                caller=sivm.message.current_target,
                to=to,
                code_address=code_address,
                should_transfer_value=True,
                memory_input_start_position=memory_input_start_position,
                memory_input_size=memory_input_size,
                memory_output_start_position=memory_output_start_position,
                memory_output_size=memory_output_size,
            ),
        )

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def selfdestruct(sivm: Sivm) -> None:
    """
    Halt execution and register account for later deletion.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    beneficiary = to_address_masked(pop(sivm.stack))

    # GAS
    gas_cost = GasCosts.OPCODE_SELFDESTRUCT_BASE
    if (
        not is_account_alive(sivm.message.tx_env.state, beneficiary)
        and get_account(
            sivm.message.tx_env.state, sivm.message.current_target
        ).balance
        != 0
    ):
        gas_cost += GasCosts.OPCODE_SELFDESTRUCT_NEW_ACCOUNT

    originator = sivm.message.current_target

    refunded_accounts = sivm.accounts_to_delete
    parent_sivm = sivm.message.parent_sivm
    while parent_sivm is not None:
        refunded_accounts.update(parent_sivm.accounts_to_delete)
        parent_sivm = parent_sivm.message.parent_sivm

    if originator not in refunded_accounts:
        sivm.refund_counter += GasCosts.REFUND_SELF_DESTRUCT

    charge_gas(sivm, gas_cost)

    beneficiary_balance = get_account(
        sivm.message.tx_env.state, beneficiary
    ).balance
    originator_balance = get_account(
        sivm.message.tx_env.state, originator
    ).balance

    # First Transfer to beneficiary
    set_account_balance(
        sivm.message.tx_env.state,
        beneficiary,
        beneficiary_balance + originator_balance,
    )
    # Next, Zero the balance of the address being deleted (must come after
    # sending to beneficiary in case the contract named itself as the
    # beneficiary).
    set_account_balance(sivm.message.tx_env.state, originator, U256(0))

    # register account for deletion
    sivm.accounts_to_delete.add(originator)

    # mark beneficiary as touched
    if account_exists_and_is_empty(sivm.message.tx_env.state, beneficiary):
        sivm.touched_accounts.add(beneficiary)

    # HALT the execution
    sivm.running = False

    # PROGRAM COUNTER
    pass


def delegatecall(sivm: Sivm) -> None:
    """
    Message-call into an account.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    gas = Uint(pop(sivm.stack))
    code_address = to_address_masked(pop(sivm.stack))
    memory_input_start_position = pop(sivm.stack)
    memory_input_size = pop(sivm.stack)
    memory_output_start_position = pop(sivm.stack)
    memory_output_size = pop(sivm.stack)

    # GAS
    extend_memory = calculate_gas_extend_memory(
        sivm.memory,
        [
            (memory_input_start_position, memory_input_size),
            (memory_output_start_position, memory_output_size),
        ],
    )
    message_call_gas = calculate_message_call_gas(
        U256(0),
        gas,
        Uint(sivm.gas_left),
        extend_memory.cost,
        GasCosts.OPCODE_CALL_BASE,
    )
    charge_gas(sivm, message_call_gas.cost + extend_memory.cost)

    # OPERATION
    sivm.memory += b"\x00" * extend_memory.expand_by
    generic_call(
        sivm,
        GenericCall(
            gas=message_call_gas.sub_call,
            value=sivm.message.value,
            caller=sivm.message.caller,
            to=sivm.message.current_target,
            code_address=code_address,
            should_transfer_value=False,
            memory_input_start_position=memory_input_start_position,
            memory_input_size=memory_input_size,
            memory_output_start_position=memory_output_start_position,
            memory_output_size=memory_output_size,
        ),
    )

    # PROGRAM COUNTER
    sivm.pc += Uint(1)
