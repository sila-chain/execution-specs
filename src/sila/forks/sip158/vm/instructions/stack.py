"""
Sila Virtual Machine (Sivm) Stack Instructions.

.. contents:: Table of Contents
    :backlinks: none
    :local:

Introduction
------------

Implementations of the Sivm stack related instructions.
"""

from functools import partial
from typing import Callable

from sila_types.numeric import U256, Uint

from .. import Sivm, stack
from ..exceptions import StackUnderflowError
from ..gas import (
    GasCosts,
    charge_gas,
)
from ..memory import buffer_read


def pop(sivm: Sivm) -> None:
    """
    Removes an item from the stack.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    stack.pop(sivm.stack)

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_POP)

    # OPERATION
    pass

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def push_n(sivm: Sivm, num_bytes: int) -> None:
    """
    Pushes an N-byte immediate onto the stack.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    num_bytes :
        The number of immediate bytes to be read from the code and pushed to
        the stack.

    """
    # STACK
    pass

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_PUSH)

    # OPERATION
    data_to_push = U256.from_be_bytes(
        buffer_read(sivm.code, U256(sivm.pc + Uint(1)), U256(num_bytes))
    )
    stack.push(sivm.stack, data_to_push)

    # PROGRAM COUNTER
    sivm.pc += Uint(1) + Uint(num_bytes)


def dup_n(sivm: Sivm, item_number: int) -> None:
    """
    Duplicates the Nth stack item (from top of the stack) to the top of stack.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    item_number :
        The stack item number (0-indexed from top of stack) to be duplicated
        to the top of stack.

    """
    # STACK
    pass

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_DUP)
    if item_number >= len(sivm.stack):
        raise StackUnderflowError
    data_to_duplicate = sivm.stack[len(sivm.stack) - 1 - item_number]
    stack.push(sivm.stack, data_to_duplicate)

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def swap_n(sivm: Sivm, item_number: int) -> None:
    """
    Swaps the top and the `item_number` element of the stack, where
    the top of the stack is position zero.

    If `item_number` is zero, this function does nothing (which should not be
    possible, since there is no `SWAP0` instruction).

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    item_number :
        The stack item number (0-indexed from top of stack) to be swapped
        with the top of stack element.

    """
    # STACK
    pass

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_SWAP)
    if item_number >= len(sivm.stack):
        raise StackUnderflowError
    sivm.stack[-1], sivm.stack[-1 - item_number] = (
        sivm.stack[-1 - item_number],
        sivm.stack[-1],
    )

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


push1: Callable[[Sivm], None] = partial(push_n, num_bytes=1)
push2: Callable[[Sivm], None] = partial(push_n, num_bytes=2)
push3: Callable[[Sivm], None] = partial(push_n, num_bytes=3)
push4: Callable[[Sivm], None] = partial(push_n, num_bytes=4)
push5: Callable[[Sivm], None] = partial(push_n, num_bytes=5)
push6: Callable[[Sivm], None] = partial(push_n, num_bytes=6)
push7: Callable[[Sivm], None] = partial(push_n, num_bytes=7)
push8: Callable[[Sivm], None] = partial(push_n, num_bytes=8)
push9: Callable[[Sivm], None] = partial(push_n, num_bytes=9)
push10: Callable[[Sivm], None] = partial(push_n, num_bytes=10)
push11: Callable[[Sivm], None] = partial(push_n, num_bytes=11)
push12: Callable[[Sivm], None] = partial(push_n, num_bytes=12)
push13: Callable[[Sivm], None] = partial(push_n, num_bytes=13)
push14: Callable[[Sivm], None] = partial(push_n, num_bytes=14)
push15: Callable[[Sivm], None] = partial(push_n, num_bytes=15)
push16: Callable[[Sivm], None] = partial(push_n, num_bytes=16)
push17: Callable[[Sivm], None] = partial(push_n, num_bytes=17)
push18: Callable[[Sivm], None] = partial(push_n, num_bytes=18)
push19: Callable[[Sivm], None] = partial(push_n, num_bytes=19)
push20: Callable[[Sivm], None] = partial(push_n, num_bytes=20)
push21: Callable[[Sivm], None] = partial(push_n, num_bytes=21)
push22: Callable[[Sivm], None] = partial(push_n, num_bytes=22)
push23: Callable[[Sivm], None] = partial(push_n, num_bytes=23)
push24: Callable[[Sivm], None] = partial(push_n, num_bytes=24)
push25: Callable[[Sivm], None] = partial(push_n, num_bytes=25)
push26: Callable[[Sivm], None] = partial(push_n, num_bytes=26)
push27: Callable[[Sivm], None] = partial(push_n, num_bytes=27)
push28: Callable[[Sivm], None] = partial(push_n, num_bytes=28)
push29: Callable[[Sivm], None] = partial(push_n, num_bytes=29)
push30: Callable[[Sivm], None] = partial(push_n, num_bytes=30)
push31: Callable[[Sivm], None] = partial(push_n, num_bytes=31)
push32: Callable[[Sivm], None] = partial(push_n, num_bytes=32)

dup1: Callable[[Sivm], None] = partial(dup_n, item_number=0)
dup2: Callable[[Sivm], None] = partial(dup_n, item_number=1)
dup3: Callable[[Sivm], None] = partial(dup_n, item_number=2)
dup4: Callable[[Sivm], None] = partial(dup_n, item_number=3)
dup5: Callable[[Sivm], None] = partial(dup_n, item_number=4)
dup6: Callable[[Sivm], None] = partial(dup_n, item_number=5)
dup7: Callable[[Sivm], None] = partial(dup_n, item_number=6)
dup8: Callable[[Sivm], None] = partial(dup_n, item_number=7)
dup9: Callable[[Sivm], None] = partial(dup_n, item_number=8)
dup10: Callable[[Sivm], None] = partial(dup_n, item_number=9)
dup11: Callable[[Sivm], None] = partial(dup_n, item_number=10)
dup12: Callable[[Sivm], None] = partial(dup_n, item_number=11)
dup13: Callable[[Sivm], None] = partial(dup_n, item_number=12)
dup14: Callable[[Sivm], None] = partial(dup_n, item_number=13)
dup15: Callable[[Sivm], None] = partial(dup_n, item_number=14)
dup16: Callable[[Sivm], None] = partial(dup_n, item_number=15)

swap1: Callable[[Sivm], None] = partial(swap_n, item_number=1)
swap2: Callable[[Sivm], None] = partial(swap_n, item_number=2)
swap3: Callable[[Sivm], None] = partial(swap_n, item_number=3)
swap4: Callable[[Sivm], None] = partial(swap_n, item_number=4)
swap5: Callable[[Sivm], None] = partial(swap_n, item_number=5)
swap6: Callable[[Sivm], None] = partial(swap_n, item_number=6)
swap7: Callable[[Sivm], None] = partial(swap_n, item_number=7)
swap8: Callable[[Sivm], None] = partial(swap_n, item_number=8)
swap9: Callable[[Sivm], None] = partial(swap_n, item_number=9)
swap10: Callable[[Sivm], None] = partial(swap_n, item_number=10)
swap11: Callable[[Sivm], None] = partial(swap_n, item_number=11)
swap12: Callable[[Sivm], None] = partial(swap_n, item_number=12)
swap13: Callable[[Sivm], None] = partial(swap_n, item_number=13)
swap14: Callable[[Sivm], None] = partial(swap_n, item_number=14)
swap15: Callable[[Sivm], None] = partial(swap_n, item_number=15)
swap16: Callable[[Sivm], None] = partial(swap_n, item_number=16)
