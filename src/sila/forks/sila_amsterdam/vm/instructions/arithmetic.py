"""
Sila Virtual Machine (Sivm) Arithmetic Instructions.

.. contents:: Table of Contents
    :backlinks: none
    :local:

Introduction
------------

Implementations of the Sivm Arithmetic instructions.
"""

from sila_types.bytes import Bytes
from sila_types.numeric import U256, Uint

from sila.utils.numeric import get_sign

from ...fork_types import ExecutionGas
from .. import Sivm
from ..gas import (
    GasCosts,
    charge_gas,
)
from ..stack import pop, push


def add(sivm: Sivm) -> None:
    """
    Adds the top two elements of the stack togsiler, and pushes the result back
    on the stack.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    x = pop(sivm.stack)
    y = pop(sivm.stack)

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_ADD)

    # OPERATION
    result = x.wrapping_add(y)

    push(sivm.stack, result)

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def sub(sivm: Sivm) -> None:
    """
    Subtracts the top two elements of the stack, and pushes the result back
    on the stack.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    x = pop(sivm.stack)
    y = pop(sivm.stack)

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_SUB)

    # OPERATION
    result = x.wrapping_sub(y)

    push(sivm.stack, result)

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def mul(sivm: Sivm) -> None:
    """
    Multiplies the top two elements of the stack, and pushes the result back
    on the stack.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    x = pop(sivm.stack)
    y = pop(sivm.stack)

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_MUL)

    # OPERATION
    result = x.wrapping_mul(y)

    push(sivm.stack, result)

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def div(sivm: Sivm) -> None:
    """
    Integer division of the top two elements of the stack. Pushes the result
    back on the stack.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    dividend = pop(sivm.stack)
    divisor = pop(sivm.stack)

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_DIV)

    # OPERATION
    if divisor == 0:
        quotient = U256(0)
    else:
        quotient = dividend // divisor

    push(sivm.stack, quotient)

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


U255_CEIL_VALUE = 2**255


def sdiv(sivm: Sivm) -> None:
    """
    Signed integer division of the top two elements of the stack. Pushes the
    result back on the stack.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    dividend = pop(sivm.stack).to_signed()
    divisor = pop(sivm.stack).to_signed()

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_SDIV)

    # OPERATION
    if divisor == 0:
        quotient = 0
    elif dividend == -U255_CEIL_VALUE and divisor == -1:
        quotient = -U255_CEIL_VALUE
    else:
        sign = get_sign(dividend * divisor)
        quotient = sign * (abs(dividend) // abs(divisor))

    push(sivm.stack, U256.from_signed(quotient))

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def mod(sivm: Sivm) -> None:
    """
    Modulo remainder of the top two elements of the stack. Pushes the result
    back on the stack.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    x = pop(sivm.stack)
    y = pop(sivm.stack)

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_MOD)

    # OPERATION
    if y == 0:
        remainder = U256(0)
    else:
        remainder = x % y

    push(sivm.stack, remainder)

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def smod(sivm: Sivm) -> None:
    """
    Signed modulo remainder of the top two elements of the stack. Pushes the
    result back on the stack.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    x = pop(sivm.stack).to_signed()
    y = pop(sivm.stack).to_signed()

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_SMOD)

    # OPERATION
    if y == 0:
        remainder = 0
    else:
        remainder = get_sign(x) * (abs(x) % abs(y))

    push(sivm.stack, U256.from_signed(remainder))

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def addmod(sivm: Sivm) -> None:
    """
    Modulo addition of the top 2 elements with the 3rd element. Pushes the
    result back on the stack.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    x = Uint(pop(sivm.stack))
    y = Uint(pop(sivm.stack))
    z = Uint(pop(sivm.stack))

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_ADDMOD)

    # OPERATION
    if z == 0:
        result = U256(0)
    else:
        result = U256((x + y) % z)

    push(sivm.stack, result)

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def mulmod(sivm: Sivm) -> None:
    """
    Modulo multiplication of the top 2 elements with the 3rd element. Pushes
    the result back on the stack.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    x = Uint(pop(sivm.stack))
    y = Uint(pop(sivm.stack))
    z = Uint(pop(sivm.stack))

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_MULMOD)

    # OPERATION
    if z == 0:
        result = U256(0)
    else:
        result = U256((x * y) % z)

    push(sivm.stack, result)

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def exp(sivm: Sivm) -> None:
    """
    Exponential operation of the top 2 elements. Pushes the result back on
    the stack.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    base = Uint(pop(sivm.stack))
    exponent = Uint(pop(sivm.stack))

    # GAS
    # This is equivalent to 1 + floor(log(y, 256)). But in python the log
    # function is inaccurate leading to wrong results.
    exponent_bits = exponent.bit_length()
    exponent_bytes = (exponent_bits + Uint(7)) // Uint(8)
    charge_gas(
        sivm,
        ExecutionGas(
            GasCosts.OPCODE_EXP_BASE
            + GasCosts.OPCODE_EXP_PER_BYTE * exponent_bytes
        ),
    )

    # OPERATION
    result = U256(pow(base, exponent, Uint(U256.MAX_VALUE) + Uint(1)))

    push(sivm.stack, result)

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def signextend(sivm: Sivm) -> None:
    """
    Sign extend operation. In other words, extend a signed number which
    fits in N bytes to 32 bytes.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    byte_num = pop(sivm.stack)
    value = pop(sivm.stack)

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_SIGNEXTEND)

    # OPERATION
    if byte_num > U256(31):
        # Can't extend any further
        result = value
    else:
        # U256(0).to_be_bytes() gives b'' instead of b'\x00'.
        value_bytes = Bytes(value.to_be_bytes32())
        # Now among the obtained value bytes, consider only
        # N `least significant bytes`, where N is `byte_num + 1`.
        value_bytes = value_bytes[31 - int(byte_num) :]
        sign_bit = value_bytes[0] >> 7
        if sign_bit == 0:
            result = U256.from_be_bytes(value_bytes)
        else:
            num_bytes_prepend = U256(32) - (byte_num + U256(1))
            result = U256.from_be_bytes(
                bytearray([0xFF] * num_bytes_prepend) + value_bytes
            )

    push(sivm.stack, result)

    # PROGRAM COUNTER
    sivm.pc += Uint(1)
