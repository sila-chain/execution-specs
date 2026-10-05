"""
Sivm trace implementation that fans out to many concrete trace implementations.
"""

from typing import Final

from sila.trace import SivmTracer, TraceEvent
from typing_extensions import override


class GroupTracer(SivmTracer):
    """
    Sivm trace implementation that fans out to many concrete trace
    implementations.
    """

    tracers: Final[set[SivmTracer]]

    def __init__(self) -> None:
        self.tracers = set()

    def add(self, tracer: SivmTracer) -> None:
        """
        Insert a new tracer.
        """
        self.tracers.add(tracer)

    @override
    def __call__(
        self,
        sivm: object,
        event: TraceEvent,
    ) -> None:
        """
        Record a trace event.
        """
        for tracer in self.tracers:
            tracer(sivm, event)
