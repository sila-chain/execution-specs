"""
Defines the functions required for creating Sivm traces during execution.

A _trace_ is a log of operations that took place during an event or period of
time. In the case of a Sivm trace, the log is built from a series of
[`TraceEvent`]s emitted during the execution of a transaction.

Note that this module _does not_ contain a trace implementation. Instead, it
defines only the events that can be collected into a trace by some other
package. See [`SivmTracer`].

See [SIP-3155] for more details on Sivm traces.

[`SivmTracer`]: ref:sila.trace.SivmTracer
[`TraceEvent`]: ref:sila.trace.TraceEvent
[SIP-3155]: https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-3155.md
"""

import enum
from dataclasses import dataclass
from typing import Optional, Protocol, final

from sila_types.bytes import Bytes

from sila.exceptions import SilaException


@final
@dataclass
class TransactionStart:
    """
    Trace event that is triggered at the start of a transaction.
    """


@final
@dataclass
class TransactionEnd:
    """
    Trace event that is triggered at the end of a transaction.
    """

    gas_used: int
    """
    Total gas consumed by this transaction.
    """

    output: Bytes
    """
    Return value or revert reason of the outermost frame of execution.
    """

    error: Optional[SilaException]
    """
    The exception, if any, that caused the transaction to fail.

    See [`sila.exceptions`] as well as fork-specific modules like
    [`sila.forks.frontier.vm.exceptions`][vm] for details.

    [`sila.exceptions`]: ref:sila.exceptions
    [vm]: ref:sila.forks.frontier.vm.exceptions
    """


@final
@dataclass
class PrecompileStart:
    """
    Trace event that is triggered before executing a precompile.
    """

    address: Bytes
    """
    Precompile that is about to be executed.
    """


@final
@dataclass
class PrecompileEnd:
    """
    Trace event that is triggered after executing a precompile.
    """


@final
@dataclass
class OpStart:
    """
    Trace event that is triggered before executing an opcode.
    """

    op: enum.Enum
    """
    Opcode that is about to be executed.

    Will be an instance of a fork-specific type like, for example,
    [`sila.forks.frontier.vm.instructions.Ops`][ops].

    [ops]: ref:sila.forks.frontier.vm.instructions.Ops
    """


@final
@dataclass
class OpEnd:
    """
    Trace event that is triggered after executing an opcode.
    """


@final
@dataclass
class OpException:
    """
    Trace event that is triggered when an opcode raises an exception.
    """

    error: Exception
    """
    Exception that was raised.

    See [`sila.exceptions`] as well as fork-specific modules like
    [`sila.forks.frontier.vm.exceptions`][vm] for examples of exceptions
    that might be raised.

    [`sila.exceptions`]: ref:sila.exceptions
    [vm]: ref:sila.forks.frontier.vm.exceptions
    """


@final
@dataclass
class SivmStop:
    """
    Trace event that is triggered when the Sivm stops.
    """

    op: enum.Enum
    """
    Last opcode executed.

    Will be an instance of a fork-specific type like, for example,
    [`sila.forks.frontier.vm.instructions.Ops`][ops].

    [ops]: ref:sila.forks.frontier.vm.instructions.Ops
    """


@final
@dataclass
class GasAndRefund:
    """
    Trace event that is triggered when gas is deducted.
    """

    gas_cost: int
    """
    Amount of gas charged or refunded.
    """


@final
@dataclass
class StateGasAndRefund:
    """
    Trace event that is triggered when state gas is deducted.
    """

    state_gas_cost: int
    """
    Amount of state gas charged.
    """


TraceEvent = (
    TransactionStart
    | TransactionEnd
    | PrecompileStart
    | PrecompileEnd
    | OpStart
    | OpEnd
    | OpException
    | SivmStop
    | GasAndRefund
    | StateGasAndRefund
)
"""
All possible types of events that an [`SivmTracer`] is expected to handle.

[`SivmTracer`]: ref:sila.trace.SivmTracer
"""


def discard_sivm_trace(
    sivm: object,
    event: TraceEvent,
) -> None:
    """
    An [`SivmTracer`] that discards all events.

    [`SivmTracer`]: ref:sila.trace.SivmTracer
    """
    del sivm, event


class SivmTracer(Protocol):
    """
    [`Protocol`] that describes tracer functions.

    See [`sila.trace`] for details about tracing in general, and
    [`__call__`] for more on how to implement a tracer.

    [`Protocol`]: https://docs.python.org/3/library/typing.html#typing.Protocol
    [`sila.trace`]: ref:sila.trace
    [`__call__`]: ref:sila.trace.SivmTracer.__call__
    """

    def __call__(
        self,
        sivm: object,
        event: TraceEvent,
    ) -> None:
        """
        Call `self` as a function, recording a trace event.

        `sivm` is the live state of the Sivm, and will be a fork-specific type
        like [`sila.forks.frontier.vm.Sivm`][sivm].

        `event`, a [`TraceEvent`], is the reason why the tracer was triggered.

        See [`discard_sivm_trace`] for an example function implementing this
        protocol.

        [`discard_sivm_trace`]: ref:sila.trace.discard_sivm_trace
        [sivm]: ref:sila.forks.frontier.vm.Sivm
        [`TraceEvent`]: ref:sila.trace.TraceEvent
        """
        raise NotImplementedError


_sivm_trace: SivmTracer = discard_sivm_trace
"""
Active [`SivmTracer`] that is used for generating traces.

[`SivmTracer`]: ref:sila.trace.SivmTracer
"""


def set_sivm_trace(tracer: SivmTracer) -> SivmTracer:
    """
    Change the active [`SivmTracer`] that is used for generating traces.

    [`SivmTracer`]: ref:sila.trace.SivmTracer
    """
    global _sivm_trace
    old = _sivm_trace
    _sivm_trace = tracer
    return old


def sivm_trace(
    sivm: object,
    event: TraceEvent,
) -> None:
    """
    Emit a trace to the active [`SivmTracer`].

    [`SivmTracer`]: ref:sila.trace.SivmTracer
    """
    global _sivm_trace
    _sivm_trace(
        sivm,
        event,
    )
