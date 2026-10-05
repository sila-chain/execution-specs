"""
Sila Virtual Machine (Sivm) Memory Instructions.

.. contents:: Table of Contents
    :backlinks: none
    :local:

Introduction
------------

Implementations of the Sivm Memory instructions.
"""

from sila_types.bytes import Bytes
from sila_types.numeric import U256, Uint

from sila.utils.numeric import ceil32

from .. import Sivm
from ..gas import (
    GasCosts,
    calculate_gas_extend_memory,
    charge_gas,
)
from ..memory import memory_read_bytes, memory_write
from ..stack import pop, push


def mstore(sivm: Sivm) -> None:
    """
    Stores a word to memory.
    This also expands the memory, if the memory is
    insufficient to store the word.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    start_position = pop(sivm.stack)
    value = pop(sivm.stack).to_be_bytes32()

    # GAS
    extend_memory = calculate_gas_extend_memory(
        sivm.memory, [(start_position, U256(len(value)))]
    )

    charge_gas(sivm, GasCosts.OPCODE_MSTORE_BASE + extend_memory.cost)

    # OPERATION
    sivm.memory += b"\x00" * extend_memory.expand_by
    memory_write(sivm.memory, start_position, value)

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def mstore8(sivm: Sivm) -> None:
    """
    Stores a byte to memory.
    This also expands the memory, if the memory is
    insufficient to store the word.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    start_position = pop(sivm.stack)
    value = pop(sivm.stack)

    # GAS
    extend_memory = calculate_gas_extend_memory(
        sivm.memory, [(start_position, U256(1))]
    )

    charge_gas(sivm, GasCosts.OPCODE_MSTORE8_BASE + extend_memory.cost)

    # OPERATION
    sivm.memory += b"\x00" * extend_memory.expand_by
    normalized_bytes_value = Bytes([value & U256(0xFF)])
    memory_write(sivm.memory, start_position, normalized_bytes_value)

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def mload(sivm: Sivm) -> None:
    """
    Loads a word from memory.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    start_position = pop(sivm.stack)

    # GAS
    extend_memory = calculate_gas_extend_memory(
        sivm.memory, [(start_position, U256(32))]
    )
    charge_gas(sivm, GasCosts.OPCODE_MLOAD_BASE + extend_memory.cost)

    # OPERATION
    sivm.memory += b"\x00" * extend_memory.expand_by
    value = U256.from_be_bytes(
        memory_read_bytes(sivm.memory, start_position, U256(32))
    )
    push(sivm.stack, value)

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def msize(sivm: Sivm) -> None:
    """
    Pushes the size of active memory in bytes onto the stack.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    pass

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_MSIZE)

    # OPERATION
    push(sivm.stack, U256(len(sivm.memory)))

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def mcopy(sivm: Sivm) -> None:
    """
    Copies the bytes in memory from one location to another.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    destination = pop(sivm.stack)
    source = pop(sivm.stack)
    length = pop(sivm.stack)

    # GAS
    words = ceil32(Uint(length)) // Uint(32)
    copy_gas_cost = GasCosts.OPCODE_COPY_PER_WORD * words

    extend_memory = calculate_gas_extend_memory(
        sivm.memory, [(source, length), (destination, length)]
    )
    charge_gas(
        sivm,
        GasCosts.OPCODE_MCOPY_BASE + copy_gas_cost + extend_memory.cost,
    )

    # OPERATION
    sivm.memory += b"\x00" * extend_memory.expand_by
    value = memory_read_bytes(sivm.memory, source, length)
    memory_write(sivm.memory, destination, value)

    # PROGRAM COUNTER
    sivm.pc += Uint(1)
