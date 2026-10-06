"""
Sila Virtual Machine (Sivm) Environmental Instructions.

.. contents:: Table of Contents
    :backlinks: none
    :local:

Introduction
------------

Implementations of the Sivm environment related instructions.
"""

from sila_types.numeric import U256, Uint

from sila.utils.numeric import ceil32

from ...state_tracker import get_account, get_code
from ...utils.address import to_address_masked
from ...vm.memory import buffer_read, memory_write
from .. import Sivm
from ..gas import (
    GasCosts,
    calculate_gas_extend_memory,
    charge_gas,
)
from ..stack import pop, push


def address(sivm: Sivm) -> None:
    """
    Pushes the address of the current executing account to the stack.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    pass

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_ADDRESS)

    # OPERATION
    push(sivm.stack, U256.from_be_bytes(sivm.message.current_target))

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def balance(sivm: Sivm) -> None:
    """
    Pushes the balance of the given account onto the stack.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    address = to_address_masked(pop(sivm.stack))

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_BALANCE)

    # OPERATION
    # Non-existent accounts default to EMPTY_ACCOUNT, which has balance 0.
    tx_state = sivm.message.tx_env.state
    balance = get_account(tx_state, address).balance

    push(sivm.stack, balance)

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def origin(sivm: Sivm) -> None:
    """
    Pushes the address of the original transaction sender to the stack.
    The origin address can only be an EOA.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    pass

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_ORIGIN)

    # OPERATION
    push(sivm.stack, U256.from_be_bytes(sivm.message.tx_env.origin))

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def caller(sivm: Sivm) -> None:
    """
    Pushes the address of the caller onto the stack.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    pass

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_CALLER)

    # OPERATION
    push(sivm.stack, U256.from_be_bytes(sivm.message.caller))

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def callvalue(sivm: Sivm) -> None:
    """
    Push the value (in wei) sent with the call onto the stack.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    pass

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_CALLVALUE)

    # OPERATION
    push(sivm.stack, sivm.message.value)

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def calldataload(sivm: Sivm) -> None:
    """
    Push a word (32 bytes) of the input data belonging to the current
    environment onto the stack.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    start_index = pop(sivm.stack)

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_CALLDATALOAD)

    # OPERATION
    value = buffer_read(sivm.message.data, start_index, U256(32))

    push(sivm.stack, U256.from_be_bytes(value))

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def calldatasize(sivm: Sivm) -> None:
    """
    Push the size of input data in current environment onto the stack.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    pass

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_CALLDATASIZE)

    # OPERATION
    push(sivm.stack, U256(len(sivm.message.data)))

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def calldatacopy(sivm: Sivm) -> None:
    """
    Copy a portion of the input data in current environment to memory.

    This will also expand the memory, in case that the memory is insufficient
    to store the data.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    memory_start_index = pop(sivm.stack)
    data_start_index = pop(sivm.stack)
    size = pop(sivm.stack)

    # GAS
    words = ceil32(Uint(size)) // Uint(32)
    copy_gas_cost = GasCosts.OPCODE_COPY_PER_WORD * words
    extend_memory = calculate_gas_extend_memory(
        sivm.memory, [(memory_start_index, size)]
    )
    charge_gas(
        sivm,
        GasCosts.OPCODE_CALLDATACOPY_BASE + copy_gas_cost + extend_memory.cost,
    )

    # OPERATION
    sivm.memory += b"\x00" * extend_memory.expand_by
    value = buffer_read(sivm.message.data, data_start_index, size)
    memory_write(sivm.memory, memory_start_index, value)

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def codesize(sivm: Sivm) -> None:
    """
    Push the size of code running in current environment onto the stack.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    pass

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_CODESIZE)

    # OPERATION
    push(sivm.stack, U256(len(sivm.code)))

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def codecopy(sivm: Sivm) -> None:
    """
    Copy a portion of the code in current environment to memory.

    This will also expand the memory, in case that the memory is insufficient
    to store the data.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    memory_start_index = pop(sivm.stack)
    code_start_index = pop(sivm.stack)
    size = pop(sivm.stack)

    # GAS
    words = ceil32(Uint(size)) // Uint(32)
    copy_gas_cost = GasCosts.OPCODE_COPY_PER_WORD * words
    extend_memory = calculate_gas_extend_memory(
        sivm.memory, [(memory_start_index, size)]
    )
    charge_gas(
        sivm,
        GasCosts.OPCODE_CODECOPY_BASE + copy_gas_cost + extend_memory.cost,
    )

    # OPERATION
    sivm.memory += b"\x00" * extend_memory.expand_by
    value = buffer_read(sivm.code, code_start_index, size)
    memory_write(sivm.memory, memory_start_index, value)

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def gasprice(sivm: Sivm) -> None:
    """
    Push the gas price used in current environment onto the stack.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    pass

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_GASPRICE)

    # OPERATION
    push(sivm.stack, U256(sivm.message.tx_env.gas_price))

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def extcodesize(sivm: Sivm) -> None:
    """
    Push the code size of a given account onto the stack.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    address = to_address_masked(pop(sivm.stack))

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_EXTERNAL_BASE)

    # OPERATION
    tx_state = sivm.message.tx_env.state
    account = get_account(tx_state, address)
    code = get_code(tx_state, account.code_hash)

    codesize = U256(len(code))
    push(sivm.stack, codesize)

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def extcodecopy(sivm: Sivm) -> None:
    """
    Copy a portion of an account's code to memory.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    address = to_address_masked(pop(sivm.stack))
    memory_start_index = pop(sivm.stack)
    code_start_index = pop(sivm.stack)
    size = pop(sivm.stack)

    # GAS
    words = ceil32(Uint(size)) // Uint(32)
    copy_gas_cost = GasCosts.OPCODE_COPY_PER_WORD * words
    extend_memory = calculate_gas_extend_memory(
        sivm.memory, [(memory_start_index, size)]
    )
    charge_gas(
        sivm,
        GasCosts.OPCODE_EXTERNAL_BASE + copy_gas_cost + extend_memory.cost,
    )

    # OPERATION
    sivm.memory += b"\x00" * extend_memory.expand_by
    tx_state = sivm.message.tx_env.state
    account = get_account(tx_state, address)
    code = get_code(tx_state, account.code_hash)

    value = buffer_read(code, code_start_index, size)
    memory_write(sivm.memory, memory_start_index, value)

    # PROGRAM COUNTER
    sivm.pc += Uint(1)
