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
