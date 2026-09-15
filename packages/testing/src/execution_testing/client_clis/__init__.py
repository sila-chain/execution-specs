"""
Library of Python wrappers for the different implementations of transition
tools.
"""

from .cli_types import (
    BlockExceptionWithMessage,
    LazyAlloc,
    Result,
    TraceFieldDiff,
    Traces,
    TransactionExceptionWithMessage,
    TransitionToolOutput,
)
from .client_backend import ClientBackend, ClientBackendExceptionMapper
from .clis.besu import BesuFixtureConsumer, BesuTransitionTool

# NOTE: erigon is imported before gsil so it is registered (and thus probed)
# first. Both expose an `evm` binary printing `evm version ...`; go-sila's
# detection matches that banner unconditionally, so it would otherwise claim an
# Erigon binary. ErigonEvm.detect_binary positively fingerprints Erigon (via
# the `enginextest` subcommand) and declines anything else, so a go-sila
# binary checked here falls through to GsilEvm — the ordering only gives Erigon
# first look, it does not by itself decide identity.
from .clis.erigon import ErigonExceptionMapper, ErigonFixtureConsumer
from .clis.evmone import (
    EvmOneBlockchainFixtureConsumer,
    EvmoneExceptionMapper,
    EvmOneStateFixtureConsumer,
    EvmOneTransitionTool,
)
from .clis.execution_specs import ExecutionSpecsTransitionTool
from .clis.gsil import GsilFixtureConsumer, GsilTransitionTool
from .clis.nethermind import Nethtest, NethtestFixtureConsumer
from .clis.nimbus import NimbusTransitionTool
from .clis.silajs import SilaJSTransitionTool
from .filler_backend import FillerBackend
from .fixture_consumer_tool import FixtureConsumerTool
from .sila_cli import CLINotFoundInPathError, UnknownCLIError
from .trace_comparators import (
    FieldExclusionTraceComparator,
    GasExhaustionTraceComparator,
    TraceComparator,
    TraceComparatorType,
    TraceComparisonResult,
    TraceDifference,
    TransactionCountMismatch,
    create_comparator,
)
from .transition_tool import TransitionTool

TransitionTool.set_default_tool(ExecutionSpecsTransitionTool)
FixtureConsumerTool.set_default_tool(GsilFixtureConsumer)

__all__ = (
    "BesuFixtureConsumer",
    "BesuTransitionTool",
    "BlockExceptionWithMessage",
    "CLINotFoundInPathError",
    "ClientBackend",
    "ClientBackendExceptionMapper",
    "ErigonExceptionMapper",
    "ErigonFixtureConsumer",
    "SilaJSTransitionTool",
    "EvmoneExceptionMapper",
    "EvmOneTransitionTool",
    "EvmOneStateFixtureConsumer",
    "EvmOneBlockchainFixtureConsumer",
    "ExecutionSpecsTransitionTool",
    "FieldExclusionTraceComparator",
    "FillerBackend",
    "FixtureConsumerTool",
    "GasExhaustionTraceComparator",
    "GsilFixtureConsumer",
    "GsilTransitionTool",
    "LazyAlloc",
    "Nethtest",
    "NethtestFixtureConsumer",
    "NimbusTransitionTool",
    "Result",
    "TraceComparator",
    "TraceComparatorType",
    "TraceComparisonResult",
    "TraceDifference",
    "TraceFieldDiff",
    "Traces",
    "TransactionCountMismatch",
    "TransactionExceptionWithMessage",
    "TransitionTool",
    "TransitionToolOutput",
    "UnknownCLIError",
    "create_comparator",
)
