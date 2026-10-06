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

from sila_types.bytes import Bytes, Bytes0
from sila_types.numeric import U256, Uint

from sila.state import Address
from sila.utils.numeric import ceil32

from ...state_tracker import (
    account_deployable,
    get_account,
    increment_nonce,
    is_account_alive,
    move_sila,
    set_account_balance,
)
from ...utils.address import (
    compute_contract_address,
    compute_create2_contract_address,
    to_address_masked,
)
from ...vm.eoa_delegation import access_delegation
from .. import (
    Message,
    Sivm,
    incorporate_child_on_error,
    incorporate_child_on_success,
)
from ..exceptions import OutOfGasError, Revert, WriteInStaticContext
from ..gas import (
    GasCosts,
    calculate_gas_extend_memory,
    calculate_message_call_gas,
    charge_gas,
    init_code_cost,
    max_message_call_gas,
)
from ..memory import memory_read_bytes, memory_write
from ..stack import pop, push


def generic_create(
    sivm: Sivm,
    endowment: U256,
    contract_address: Address,
    memory_start_position: U256,
    memory_size: U256,
) -> None:
    """
    Core logic used by the `CREATE*` family of opcodes.
    """
    # This import causes a circular import error
    # if it's not moved inside this method
    from ...vm.interpreter import (
        MAX_INIT_CODE_SIZE,
        STACK_DEPTH_LIMIT,
        process_create_message,
    )

    call_data = memory_read_bytes(
        sivm.memory, memory_start_position, memory_size
    )
    if len(call_data) > MAX_INIT_CODE_SIZE:
        raise OutOfGasError

    create_message_gas = max_message_call_gas(Uint(sivm.gas_left))
    sivm.gas_left -= create_message_gas
    if sivm.message.is_static:
        raise WriteInStaticContext
    sivm.return_data = b""

    sender_address = sivm.message.current_target
    sender = get_account(sivm.message.tx_env.state, sender_address)

    if (
        sender.balance < endowment
        or sender.nonce == Uint(2**64 - 1)
        or sivm.message.depth + Uint(1) > STACK_DEPTH_LIMIT
    ):
        sivm.gas_left += create_message_gas
        push(sivm.stack, U256(0))
        return

    sivm.accessed_addresses.add(contract_address)

    if not account_deployable(sivm.message.tx_env.state, contract_address):
        increment_nonce(sivm.message.tx_env.state, sivm.message.current_target)
        push(sivm.stack, U256(0))
        return

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
        is_static=False,
        accessed_addresses=sivm.accessed_addresses.copy(),
        accessed_storage_keys=sivm.accessed_storage_keys.copy(),
        disable_precompiles=False,
        parent_sivm=sivm,
    )
    child_sivm = process_create_message(child_message)

    if child_sivm.error:
        incorporate_child_on_error(sivm, child_sivm)
        sivm.return_data = child_sivm.output
        push(sivm.stack, U256(0))
    else:
        incorporate_child_on_success(sivm, child_sivm)
        sivm.return_data = b""
        push(sivm.stack, U256.from_be_bytes(child_sivm.message.current_target))


def create(sivm: Sivm) -> None:
    """
    Creates a new account with associated code.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    endowment = pop(sivm.stack)
    memory_start_position = pop(sivm.stack)
    memory_size = pop(sivm.stack)

    # GAS
    extend_memory = calculate_gas_extend_memory(
        sivm.memory, [(memory_start_position, memory_size)]
    )
    init_code_gas = init_code_cost(Uint(memory_size))

    charge_gas(
        sivm, GasCosts.OPCODE_CREATE_BASE + extend_memory.cost + init_code_gas
    )

    # OPERATION
    sivm.memory += b"\x00" * extend_memory.expand_by
    contract_address = compute_contract_address(
        sivm.message.current_target,
        get_account(
            sivm.message.tx_env.state, sivm.message.current_target
        ).nonce,
    )

    generic_create(
        sivm,
        endowment,
        contract_address,
        memory_start_position,
        memory_size,
    )

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def create2(sivm: Sivm) -> None:
    """
    Creates a new account with associated code.

    It's similar to the CREATE opcode except that the address of the new
    account depends on the init_code instead of the nonce of sender.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    endowment = pop(sivm.stack)
    memory_start_position = pop(sivm.stack)
    memory_size = pop(sivm.stack)
    salt = pop(sivm.stack).to_be_bytes32()

    # GAS
    extend_memory = calculate_gas_extend_memory(
        sivm.memory, [(memory_start_position, memory_size)]
    )
    call_data_words = ceil32(Uint(memory_size)) // Uint(32)
    init_code_gas = init_code_cost(Uint(memory_size))
    charge_gas(
        sivm,
        GasCosts.OPCODE_CREATE_BASE
        + GasCosts.OPCODE_KECCAK256_PER_WORD * call_data_words
        + extend_memory.cost
        + init_code_gas,
    )

    # OPERATION
    sivm.memory += b"\x00" * extend_memory.expand_by
    contract_address = compute_create2_contract_address(
        sivm.message.current_target,
        salt,
        memory_read_bytes(sivm.memory, memory_start_position, memory_size),
    )

    generic_create(
        sivm,
        endowment,
        contract_address,
        memory_start_position,
        memory_size,
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
    is_staticcall: bool
    memory_input_start_position: U256
    memory_input_size: U256
    memory_output_start_position: U256
    memory_output_size: U256
    code: Bytes
    disable_precompiles: bool


def generic_call(sivm: Sivm, params: GenericCall) -> None:
    """
    Perform the core logic of the `CALL*` family of opcodes.
    """
    from ...vm.interpreter import STACK_DEPTH_LIMIT, process_message

    sivm.return_data = b""

    if sivm.message.depth + Uint(1) > STACK_DEPTH_LIMIT:
        sivm.gas_left += params.gas
        push(sivm.stack, U256(0))
        return

    call_data = memory_read_bytes(
        sivm.memory,
        params.memory_input_start_position,
        params.memory_input_size,
    )

    child_message = Message(
        block_env=sivm.message.block_env,
        tx_env=sivm.message.tx_env,
        caller=params.caller,
        target=params.to,
        gas=params.gas,
        value=params.value,
        data=call_data,
        code=params.code,
        current_target=params.to,
        depth=sivm.message.depth + Uint(1),
        code_address=params.code_address,
        should_transfer_value=params.should_transfer_value,
        is_static=params.is_staticcall or sivm.message.is_static,
        accessed_addresses=sivm.accessed_addresses.copy(),
        accessed_storage_keys=sivm.accessed_storage_keys.copy(),
        disable_precompiles=params.disable_precompiles,
        parent_sivm=sivm,
    )
    child_sivm = process_message(child_message)

    if child_sivm.error:
        incorporate_child_on_error(sivm, child_sivm)
        sivm.return_data = child_sivm.output
        push(sivm.stack, U256(0))
    else:
        incorporate_child_on_success(sivm, child_sivm)
        sivm.return_data = child_sivm.output
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

    if to in sivm.accessed_addresses:
        access_gas_cost = GasCosts.WARM_ACCESS
    else:
        sivm.accessed_addresses.add(to)
        access_gas_cost = GasCosts.COLD_ACCOUNT_ACCESS

    code_address = to
    (
        disable_precompiles,
        code_address,
        code,
        delegated_access_gas_cost,
    ) = access_delegation(sivm, code_address)
    access_gas_cost += delegated_access_gas_cost

    create_gas_cost = GasCosts.NEW_ACCOUNT
    if value == 0 or is_account_alive(sivm.message.tx_env.state, to):
        create_gas_cost = Uint(0)
    transfer_gas_cost = Uint(0) if value == 0 else GasCosts.CALL_VALUE
    message_call_gas = calculate_message_call_gas(
        value,
        gas,
        Uint(sivm.gas_left),
        memory_cost=extend_memory.cost,
        extra_gas=access_gas_cost + create_gas_cost + transfer_gas_cost,
    )
    charge_gas(sivm, message_call_gas.cost + extend_memory.cost)
    if sivm.message.is_static and value != U256(0):
        raise WriteInStaticContext
    sivm.memory += b"\x00" * extend_memory.expand_by
    sender_balance = get_account(
        sivm.message.tx_env.state, sivm.message.current_target
    ).balance
    if sender_balance < value:
        push(sivm.stack, U256(0))
        sivm.return_data = b""
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
                is_staticcall=False,
                memory_input_start_position=memory_input_start_position,
                memory_input_size=memory_input_size,
                memory_output_start_position=memory_output_start_position,
                memory_output_size=memory_output_size,
                code=code,
                disable_precompiles=disable_precompiles,
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

    if code_address in sivm.accessed_addresses:
        access_gas_cost = GasCosts.WARM_ACCESS
    else:
        sivm.accessed_addresses.add(code_address)
        access_gas_cost = GasCosts.COLD_ACCOUNT_ACCESS

    (
        disable_precompiles,
        code_address,
        code,
        delegated_access_gas_cost,
    ) = access_delegation(sivm, code_address)
    access_gas_cost += delegated_access_gas_cost

    transfer_gas_cost = Uint(0) if value == 0 else GasCosts.CALL_VALUE
    message_call_gas = calculate_message_call_gas(
        value,
        gas,
        Uint(sivm.gas_left),
        extend_memory.cost,
        access_gas_cost + transfer_gas_cost,
    )
    charge_gas(sivm, message_call_gas.cost + extend_memory.cost)

    # OPERATION
    sivm.memory += b"\x00" * extend_memory.expand_by
    sender_balance = get_account(
        sivm.message.tx_env.state, sivm.message.current_target
    ).balance
    if sender_balance < value:
        push(sivm.stack, U256(0))
        sivm.return_data = b""
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
                is_staticcall=False,
                memory_input_start_position=memory_input_start_position,
                memory_input_size=memory_input_size,
                memory_output_start_position=memory_output_start_position,
                memory_output_size=memory_output_size,
                code=code,
                disable_precompiles=disable_precompiles,
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
    if beneficiary not in sivm.accessed_addresses:
        sivm.accessed_addresses.add(beneficiary)
        gas_cost += GasCosts.COLD_ACCOUNT_ACCESS

    if (
        not is_account_alive(sivm.message.tx_env.state, beneficiary)
        and get_account(
            sivm.message.tx_env.state, sivm.message.current_target
        ).balance
        != 0
    ):
        gas_cost += GasCosts.OPCODE_SELFDESTRUCT_NEW_ACCOUNT

    charge_gas(sivm, gas_cost)
    if sivm.message.is_static:
        raise WriteInStaticContext

    originator = sivm.message.current_target
    originator_balance = get_account(
        sivm.message.tx_env.state, originator
    ).balance

    move_sila(
        sivm.message.tx_env.state,
        originator,
        beneficiary,
        originator_balance,
    )

    # register account for deletion only if it was created
    # in the same transaction
    if originator in sivm.message.tx_env.state.created_accounts:
        # If beneficiary is the same as originator, then
        # the sila is burnt.
        set_account_balance(sivm.message.tx_env.state, originator, U256(0))
        sivm.accounts_to_delete.add(originator)

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

    if code_address in sivm.accessed_addresses:
        access_gas_cost = GasCosts.WARM_ACCESS
    else:
        sivm.accessed_addresses.add(code_address)
        access_gas_cost = GasCosts.COLD_ACCOUNT_ACCESS

    (
        disable_precompiles,
        code_address,
        code,
        delegated_access_gas_cost,
    ) = access_delegation(sivm, code_address)
    access_gas_cost += delegated_access_gas_cost

    message_call_gas = calculate_message_call_gas(
        U256(0), gas, Uint(sivm.gas_left), extend_memory.cost, access_gas_cost
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
            is_staticcall=False,
            memory_input_start_position=memory_input_start_position,
            memory_input_size=memory_input_size,
            memory_output_start_position=memory_output_start_position,
            memory_output_size=memory_output_size,
            code=code,
            disable_precompiles=disable_precompiles,
        ),
    )

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def staticcall(sivm: Sivm) -> None:
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

    if to in sivm.accessed_addresses:
        access_gas_cost = GasCosts.WARM_ACCESS
    else:
        sivm.accessed_addresses.add(to)
        access_gas_cost = GasCosts.COLD_ACCOUNT_ACCESS

    code_address = to
    (
        disable_precompiles,
        code_address,
        code,
        delegated_access_gas_cost,
    ) = access_delegation(sivm, code_address)
    access_gas_cost += delegated_access_gas_cost

    message_call_gas = calculate_message_call_gas(
        U256(0),
        gas,
        Uint(sivm.gas_left),
        extend_memory.cost,
        access_gas_cost,
    )
    charge_gas(sivm, message_call_gas.cost + extend_memory.cost)

    # OPERATION
    sivm.memory += b"\x00" * extend_memory.expand_by
    generic_call(
        sivm,
        GenericCall(
            gas=message_call_gas.sub_call,
            value=U256(0),
            caller=sivm.message.current_target,
            to=to,
            code_address=code_address,
            should_transfer_value=True,
            is_staticcall=True,
            memory_input_start_position=memory_input_start_position,
            memory_input_size=memory_input_size,
            memory_output_start_position=memory_output_start_position,
            memory_output_size=memory_output_size,
            code=code,
            disable_precompiles=disable_precompiles,
        ),
    )

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def revert(sivm: Sivm) -> None:
    """
    Stop execution and revert state changes, without consuming all provided gas
    and also has the ability to return a reason.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    memory_start_index = pop(sivm.stack)
    size = pop(sivm.stack)

    # GAS
    extend_memory = calculate_gas_extend_memory(
        sivm.memory, [(memory_start_index, size)]
    )

    charge_gas(sivm, extend_memory.cost)

    # OPERATION
    sivm.memory += b"\x00" * extend_memory.expand_by
    output = memory_read_bytes(sivm.memory, memory_start_index, size)
    sivm.output = Bytes(output)
    raise Revert

    # PROGRAM COUNTER
    # no-op
