"""
Sila Virtual Machine (Sivm) Bitwise Instructions.

.. contents:: Table of Contents
    :backlinks: none
    :local:

Introduction
------------

Implementations of the Sivm bitwise instructions.
"""

from sila_types.numeric import U256, Uint

from .. import Sivm
from ..gas import (
    GasCosts,
    charge_gas,
)
from ..stack import pop, push


def bitwise_and(sivm: Sivm) -> None:
    """
    Bitwise AND operation of the top 2 elements of the stack. Pushes the
    result back on the stack.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    x = pop(sivm.stack)
    y = pop(sivm.stack)

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_AND)

    # OPERATION
    push(sivm.stack, x & y)

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def bitwise_or(sivm: Sivm) -> None:
    """
    Bitwise OR operation of the top 2 elements of the stack. Pushes the
    result back on the stack.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    x = pop(sivm.stack)
    y = pop(sivm.stack)

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_OR)

    # OPERATION
    push(sivm.stack, x | y)

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def bitwise_xor(sivm: Sivm) -> None:
    """
    Bitwise XOR operation of the top 2 elements of the stack. Pushes the
    result back on the stack.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    x = pop(sivm.stack)
    y = pop(sivm.stack)

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_XOR)

    # OPERATION
    push(sivm.stack, x ^ y)

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def bitwise_not(sivm: Sivm) -> None:
    """
    Bitwise NOT operation of the top element of the stack. Pushes the
    result back on the stack.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    x = pop(sivm.stack)

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_NOT)

    # OPERATION
    push(sivm.stack, ~x)

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def get_byte(sivm: Sivm) -> None:
    """
    For a word (defined by next top element of the stack), retrieve the
    Nth byte (0-indexed and defined by top element of stack) from the
    left (most significant) to right (least significant).

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    byte_index = pop(sivm.stack)
    word = pop(sivm.stack)

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_BYTE)

    # OPERATION
    if byte_index >= U256(32):
        result = U256(0)
    else:
        extra_bytes_to_right = U256(31) - byte_index
        # Remove the extra bytes in the right
        word = word >> (extra_bytes_to_right * U256(8))
        # Remove the extra bytes in the left
        word = word & U256(0xFF)
        result = word

    push(sivm.stack, result)

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def bitwise_shl(sivm: Sivm) -> None:
    """
    Logical shift left (SHL) operation of the top 2 elements of the stack.
    Pushes the result back on the stack.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    shift = Uint(pop(sivm.stack))
    value = Uint(pop(sivm.stack))

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_SHL)

    # OPERATION
    if shift < Uint(256):
        result = U256((value << shift) & Uint(U256.MAX_VALUE))
    else:
        result = U256(0)

    push(sivm.stack, result)

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def bitwise_shr(sivm: Sivm) -> None:
    """
    Logical shift right (SHR) operation of the top 2 elements of the stack.
    Pushes the result back on the stack.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    shift = pop(sivm.stack)
    value = pop(sivm.stack)

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_SHR)

    # OPERATION
    if shift < U256(256):
        result = value >> shift
    else:
        result = U256(0)

    push(sivm.stack, result)

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def bitwise_sar(sivm: Sivm) -> None:
    """
    Arithmetic shift right (SAR) operation of the top 2 elements of the stack.
    Pushes the result back on the stack.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    shift = int(pop(sivm.stack))
    signed_value = pop(sivm.stack).to_signed()

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_SAR)

    # OPERATION
    if shift < 256:
        result = U256.from_signed(signed_value >> shift)
    elif signed_value >= 0:
        result = U256(0)
    else:
        result = U256.MAX_VALUE

    push(sivm.stack, result)

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def count_leading_zeros(sivm: Sivm) -> None:
    """
    Count the number of leading zero bits in a 256-bit word.

    Pops one value from the stack and pushes the number of leading zero bits.
    If the input is zero, pushes 256.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    x = pop(sivm.stack)

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_CLZ)

    # OPERATION
    bit_length = U256(x.bit_length())
    result = U256(256) - bit_length

    push(sivm.stack, result)

    # PROGRAM COUNTER
    sivm.pc += Uint(1)
