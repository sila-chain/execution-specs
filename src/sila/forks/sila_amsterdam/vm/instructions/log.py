"""
Sila Virtual Machine (Sivm) Logging Instructions.

.. contents:: Table of Contents
    :backlinks: none
    :local:

Introduction
------------

Implementations of the Sivm logging instructions.
"""

from functools import partial
from typing import Callable

from sila_types.numeric import Uint

from ...blocks import Log
from ...fork_types import ExecutionGas
from .. import Sivm
from ..exceptions import WriteInStaticContext
from ..gas import (
    GasCosts,
    calculate_gas_extend_memory,
    charge_gas,
)
from ..memory import memory_read_bytes
from ..stack import pop


def log_n(sivm: Sivm, num_topics: int) -> None:
    """
    Appends a log entry, having `num_topics` topics, to the sivm logs.

    This will also expand the memory if the data (required by the log entry)
    corresponding to the memory is not accessible.

    Parameters
    ----------
    sivm :
        The current Sivm frame.
    num_topics :
        The number of topics to be included in the log entry.

    """
    # STACK
    memory_start_index = pop(sivm.stack)
    size = pop(sivm.stack)

    topics = []
    for _ in range(num_topics):
        topic = pop(sivm.stack).to_be_bytes32()
        topics.append(topic)

    # GAS
    extend_memory = calculate_gas_extend_memory(
        sivm.memory, [(memory_start_index, size)]
    )
    charge_gas(
        sivm,
        ExecutionGas(
            GasCosts.OPCODE_LOG_BASE
            + GasCosts.OPCODE_LOG_DATA_PER_BYTE * Uint(size)
            + GasCosts.OPCODE_LOG_TOPIC * Uint(num_topics)
            + extend_memory.cost
        ),
    )

    # OPERATION
    sivm.memory += b"\x00" * extend_memory.expand_by
    if sivm.is_static:
        raise WriteInStaticContext
    log_entry = Log(
        address=sivm.current_target,
        topics=tuple(topics),
        data=memory_read_bytes(sivm.memory, memory_start_index, size),
    )

    sivm.logs = sivm.logs + (log_entry,)

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


log0: Callable[[Sivm], None] = partial(log_n, num_topics=0)
log1: Callable[[Sivm], None] = partial(log_n, num_topics=1)
log2: Callable[[Sivm], None] = partial(log_n, num_topics=2)
log3: Callable[[Sivm], None] = partial(log_n, num_topics=3)
log4: Callable[[Sivm], None] = partial(log_n, num_topics=4)
