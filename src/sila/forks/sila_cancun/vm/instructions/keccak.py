"""
Sila Virtual Machine (Sivm) Keccak Instructions.

.. contents:: Table of Contents
    :backlinks: none
    :local:

Introduction
------------

Implementations of the Sivm keccak instructions.
"""

from sila_types.numeric import U256, Uint

from sila.crypto.hash import keccak256
from sila.utils.numeric import ceil32

from .. import Sivm
from ..gas import (
    GasCosts,
    calculate_gas_extend_memory,
    charge_gas,
)
from ..memory import memory_read_bytes
from ..stack import pop, push


def keccak(sivm: Sivm) -> None:
    """
    Pushes to the stack the Keccak-256 hash of a region of memory.

    This also expands the memory, in case the memory is insufficient to
    access the data's memory location.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    memory_start_index = pop(sivm.stack)
    size = pop(sivm.stack)

    # GAS
    words = ceil32(Uint(size)) // Uint(32)
    word_gas_cost = GasCosts.OPCODE_KECCAK256_PER_WORD * words
    extend_memory = calculate_gas_extend_memory(
        sivm.memory, [(memory_start_index, size)]
    )
    charge_gas(
        sivm,
        GasCosts.OPCODE_KECCAK256_BASE + word_gas_cost + extend_memory.cost,
    )

    # OPERATION
    sivm.memory += b"\x00" * extend_memory.expand_by
    data = memory_read_bytes(sivm.memory, memory_start_index, size)
    hashed = keccak256(data)

    push(sivm.stack, U256.from_be_bytes(hashed))

    # PROGRAM COUNTER
    sivm.pc += Uint(1)
