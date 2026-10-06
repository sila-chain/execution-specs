"""
Sila Virtual Machine (Sivm) Comparison Instructions.

.. contents:: Table of Contents
    :backlinks: none
    :local:

Introduction
------------

Implementations of the Sivm Comparison instructions.
"""

from sila_types.numeric import U256, Uint

from .. import Sivm
from ..gas import GasCosts, charge_gas
from ..stack import pop, push


def less_than(sivm: Sivm) -> None:
    """
    Checks if the top element is less than the next top element. Pushes the
    result back on the stack.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    left = pop(sivm.stack)
    right = pop(sivm.stack)

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_LT)

    # OPERATION
    result = U256(left < right)

    push(sivm.stack, result)

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def signed_less_than(sivm: Sivm) -> None:
    """
    Signed less-than comparison.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    left = pop(sivm.stack).to_signed()
    right = pop(sivm.stack).to_signed()

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_SLT)

    # OPERATION
    result = U256(left < right)

    push(sivm.stack, result)

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def greater_than(sivm: Sivm) -> None:
    """
    Checks if the top element is greater than the next top element. Pushes
    the result back on the stack.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    left = pop(sivm.stack)
    right = pop(sivm.stack)

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_GT)

    # OPERATION
    result = U256(left > right)

    push(sivm.stack, result)

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def signed_greater_than(sivm: Sivm) -> None:
    """
    Signed greater-than comparison.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    left = pop(sivm.stack).to_signed()
    right = pop(sivm.stack).to_signed()

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_SGT)

    # OPERATION
    result = U256(left > right)

    push(sivm.stack, result)

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def equal(sivm: Sivm) -> None:
    """
    Checks if the top element is equal to the next top element. Pushes
    the result back on the stack.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    left = pop(sivm.stack)
    right = pop(sivm.stack)

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_EQ)

    # OPERATION
    result = U256(left == right)

    push(sivm.stack, result)

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def is_zero(sivm: Sivm) -> None:
    """
    Checks if the top element is equal to 0. Pushes the result back on the
    stack.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    x = pop(sivm.stack)

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_ISZERO)

    # OPERATION
    result = U256(x == 0)

    push(sivm.stack, result)

    # PROGRAM COUNTER
    sivm.pc += Uint(1)
