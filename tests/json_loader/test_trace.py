"""Test sivm tracing functionality."""

from typing import Optional, cast

from sila_types.numeric import Uint

import sila.trace


def test_modify_sivm_trace() -> None:
    """Tests that Sivm trace handlers can be modified and work correctly."""
    trace1: Optional[sila.trace.TraceEvent] = None
    trace2: Optional[sila.trace.TraceEvent] = None

    def tracer1(
        sivm: object,
        event: sila.trace.TraceEvent,
    ) -> None:
        del sivm
        nonlocal trace1
        trace1 = event

    def tracer2(
        sivm: object,
        event: sila.trace.TraceEvent,
    ) -> None:
        del sivm
        nonlocal trace2
        trace2 = event

    sila.trace.set_sivm_trace(tracer1)

    from sila.forks.sila_prague.vm import Message, Sivm
    from sila.forks.sila_prague.vm.gas import charge_gas

    sivm = Sivm(
        pc=Uint(1),
        stack=[],
        memory=bytearray(),
        code=b"",
        gas_left=Uint(100),
        valid_jump_destinations=set(),
        logs=(),
        refund_counter=0,
        running=True,
        message=cast(Message, object()),
        output=b"",
        accounts_to_delete=set(),
        return_data=b"",
        error=None,
        accessed_addresses=set(),
        accessed_storage_keys=set(),
    )

    charge_gas(sivm, Uint(5))

    assert trace2 is None
    assert isinstance(trace1, sila.trace.GasAndRefund)
    assert trace1.gas_cost == 5

    sila.trace.set_sivm_trace(tracer2)

    charge_gas(sivm, Uint(6))

    # Check that the old event is unmodified.
    assert isinstance(trace1, sila.trace.GasAndRefund)
    assert trace1.gas_cost == 5

    # Check that the new event is populated.
    assert isinstance(trace2, sila.trace.GasAndRefund)
    assert trace2.gas_cost == 6
