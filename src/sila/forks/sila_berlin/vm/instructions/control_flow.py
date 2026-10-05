"""
Sila Virtual Machine (Sivm) Control Flow Instructions.

.. contents:: Table of Contents
    :backlinks: none
    :local:

Introduction
------------

Implementations of the Sivm control flow instructions.
"""

from sila_types.numeric import U256, Uint

from ...vm.gas import (
    GasCosts,
    charge_gas,
)
from .. import Sivm
from ..exceptions import InvalidJumpDestError
from ..stack import pop, push


def stop(sivm: Sivm) -> None:
    """
    Stop further execution of Sivm code.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    pass

    # GAS
    pass

    # OPERATION
    sivm.running = False

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def jump(sivm: Sivm) -> None:
    """
    Alter the program counter to the location specified by the top of the
    stack.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    jump_dest = Uint(pop(sivm.stack))

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_JUMP)

    # OPERATION
    if jump_dest not in sivm.valid_jump_destinations:
        raise InvalidJumpDestError

    # PROGRAM COUNTER
    sivm.pc = Uint(jump_dest)


def jumpi(sivm: Sivm) -> None:
    """
    Alter the program counter to the specified location if and only if a
    condition is true. If the condition is not true, then the program counter
    would increase only by 1.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    jump_dest = Uint(pop(sivm.stack))
    conditional_value = pop(sivm.stack)

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_JUMPI)

    # OPERATION
    if conditional_value == 0:
        destination = sivm.pc + Uint(1)
    elif jump_dest not in sivm.valid_jump_destinations:
        raise InvalidJumpDestError
    else:
        destination = jump_dest

    # PROGRAM COUNTER
    sivm.pc = destination


def pc(sivm: Sivm) -> None:
    """
    Push onto the stack the value of the program counter after reaching the
    current instruction and without increasing it for the next instruction.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    pass

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_PC)

    # OPERATION
    push(sivm.stack, U256(sivm.pc))

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def gas_left(sivm: Sivm) -> None:
    """
    Push the amount of available gas (including the corresponding reduction
    for the cost of this instruction) onto the stack.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    pass

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_GAS)

    # OPERATION
    push(sivm.stack, U256(sivm.gas_left))

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def jumpdest(sivm: Sivm) -> None:
    """
    Mark a valid destination for jumps. This is a noop, present only
    to be used by `JUMP` and `JUMPI` opcodes to verify that their jump is
    valid.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    pass

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_JUMPDEST)

    # OPERATION
    pass

    # PROGRAM COUNTER
    sivm.pc += Uint(1)
