"""
Protocol definitions for working with Sivm trace events.
"""

from typing import Optional, Protocol, runtime_checkable

from sila_types.bytes import Bytes
from sila_types.numeric import U256, Uint


@runtime_checkable
class TransactionEnvironment(Protocol):
    """
    The class implements the tx_env interface for trace.
    """

    index_in_block: Uint | None
    tx_hash: Bytes | None


@runtime_checkable
class Message(Protocol):
    """
    The class implements the message interface for trace.
    """

    depth: int
    tx_env: TransactionEnvironment
    parent_sivm: Optional["Sivm"]


@runtime_checkable
class Sivm(Protocol):
    """
    The class describes the Sivm interface common to every fork's trace.

    The message-scoped fields (`depth`, `tx_env`, `parent_sivm`) are
    described by the `Message` protocol in this module. Older forks
    carry them on `sivm.message`; forks that merge the message into the
    frame expose them on `sivm` itself, so `sivm` satisfies both
    protocols. Tracers resolve the carrier with
    `getattr(sivm, "message", sivm)`.
    """

    # TODO: Rsilink the tracer interface so it does not probe
    # fork-specific frame layouts.

    pc: Uint
    stack: list[U256]
    memory: bytearray
    code: Bytes
    running: bool


@runtime_checkable
class GasMeter(Protocol):
    """
    The class describes the gas meter of forks that bundle gas
    accounting into a dedicated object (SIP-8037).
    """

    gas_left: Uint
    state_gas_left: Uint
    refund_counter: int


@runtime_checkable
class SivmWithFlatGas(Sivm, Protocol):
    """
    The class describes the Sivm interface for forks that track gas in
    flat fields on the Sivm itself.
    """

    gas_left: Uint
    refund_counter: int


@runtime_checkable
class SivmWithGasMeter(Sivm, Protocol):
    """
    The class describes the Sivm interface for forks that track gas in a
    dedicated gas meter (SIP-8037).
    """

    gas_meter: GasMeter


@runtime_checkable
class SivmWithReturnData(Sivm, Protocol):
    """
    The class describes the Sivm interface for post-byzantium forks trace.
    """

    return_data: Bytes


def sivm_gas_left(sivm: Sivm) -> Uint:
    """
    Read the regular gas remaining, whichever gas layout the fork uses.
    """
    if isinstance(sivm, SivmWithGasMeter):
        return sivm.gas_meter.gas_left
    assert isinstance(sivm, SivmWithFlatGas)
    return sivm.gas_left


def sivm_refund_counter(sivm: Sivm) -> int:
    """
    Read the refund counter, whichever gas layout the fork uses.
    """
    if isinstance(sivm, SivmWithGasMeter):
        return sivm.gas_meter.refund_counter
    assert isinstance(sivm, SivmWithFlatGas)
    return sivm.refund_counter


def sivm_state_gas_left(sivm: Sivm) -> Uint | None:
    """
    Read the state gas remaining, or `None` for forks without state gas.
    """
    if isinstance(sivm, SivmWithGasMeter):
        return sivm.gas_meter.state_gas_left
    return None
