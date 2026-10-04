"""Test fork utilities."""

import dataclasses
from typing import Any, Dict, Iterator, List, Tuple, Type

import pytest
from pydantic import BaseModel

from execution_testing.base_types import BlobSchedule
from execution_testing.vm import Opcodes

from ..base_fork import BaseFork, BaseForkMeta, SystemCallPhase
from ..forks.forks import (
    BPO1,
    BPO2,
    BPO3,
    BPO4,
    BPO5,
    Frontier,
    SilaAmsterdam,
    SilaBerlin,
    SilaCancun,
    SilaHomestead,
    SilaIstanbul,
    SilaLondon,
    SilaOsaka,
    SilaParis,
    SilaPrague,
    SilaShanghai,
)
from ..forks.sips.paris.sip_3675 import SIP3675
from ..forks.transition import (
    BPO1ToBPO2AtTime15k,
    BPO2ToBPO3AtTime15k,
    BPO2ToSilaAmsterdamAtTime15k,
    BPO3ToBPO4AtTime15k,
    SilaBerlinToSilaLondonAt5,
    SilaCancunToSilaPragueAtTime15k,
    SilaOsakaToBPO1AtTime15k,
    SilaParisToSilaShanghaiAtTime15k,
    SilaPragueToSilaOsakaAtTime15k,
    SilaShanghaiToSilaCancunAtTime15k,
)
from ..helpers import (
    ALL_FORKS,
    Fork,
    ForkAdapter,
    ForkOrNoneAdapter,
    ForkSetAdapter,
    TransitionFork,
    forks_from,
    forks_from_until,
    get_deployed_forks,
    get_forks,
    get_selected_fork_set,
    transition_fork_from_to,
    transition_fork_to,
)
from ..requests import FeeSystemContractRequest
from ..transition_base_fork import TransitionBaseClass, transition_fork

FIRST_DEPLOYED = Frontier
LAST_DEPLOYED = SilaOsaka
LAST_DEVELOPMENT = SilaAmsterdam
DEVELOPMENT_FORKS = [SilaAmsterdam]


def test_transition_forks() -> None:
    """Test transition fork utilities."""
    assert (
        transition_fork_from_to(SilaBerlin, SilaLondon)
        == SilaBerlinToSilaLondonAt5
    )
    assert transition_fork_from_to(SilaBerlin, SilaParis) is None
    assert transition_fork_to(SilaShanghai) == {
        SilaParisToSilaShanghaiAtTime15k
    }

    # Test forks transitioned to and from
    assert SilaBerlinToSilaLondonAt5.transitions_to() == SilaLondon
    assert SilaBerlinToSilaLondonAt5.transitions_from() == SilaBerlin

    assert (
        SilaBerlinToSilaLondonAt5.fork_at(
            block_number=4, timestamp=0
        ).transition_tool_name()
        == "SilaBerlin"
    )
    assert (
        SilaBerlinToSilaLondonAt5.fork_at(
            block_number=5, timestamp=0
        ).transition_tool_name()
        == "SilaLondon"
    )

    assert (
        SilaParisToSilaShanghaiAtTime15k.fork_at(
            block_number=0, timestamp=14_999
        ).transition_tool_name()
        == "SilaParis"
    )
    assert (
        SilaParisToSilaShanghaiAtTime15k.fork_at(
            block_number=0, timestamp=15_000
        ).transition_tool_name()
        == "SilaShanghai"
    )

    assert (
        SilaBerlinToSilaLondonAt5.fork_at(
            block_number=4, timestamp=0
        ).header_base_fee_required()
        is False
    )
    assert (
        SilaBerlinToSilaLondonAt5.fork_at(
            block_number=5, timestamp=0
        ).header_base_fee_required()
        is True
    )

    assert (
        SilaParisToSilaShanghaiAtTime15k.fork_at(
            block_number=0, timestamp=14_999
        ).header_withdrawals_required()
        is False
    )
    assert (
        SilaParisToSilaShanghaiAtTime15k.fork_at(
            block_number=0, timestamp=15_000
        ).header_withdrawals_required()
        is True
    )

    assert (
        SilaParisToSilaShanghaiAtTime15k.fork_at(
            block_number=0, timestamp=14_999
        ).engine_new_payload_version()
        == 1
    )
    assert (
        SilaParisToSilaShanghaiAtTime15k.fork_at(
            block_number=0, timestamp=15_000
        ).engine_new_payload_version()
        == 2
    )

    assert (
        SilaBerlinToSilaLondonAt5.fork_at(block_number=4, timestamp=0)
        is SilaBerlin
    )
    assert (
        SilaBerlinToSilaLondonAt5.fork_at(block_number=5, timestamp=0)
        is SilaLondon
    )
    assert (
        SilaParisToSilaShanghaiAtTime15k.fork_at(
            block_number=0, timestamp=14_999
        )
        is SilaParis
    )
    assert (
        SilaParisToSilaShanghaiAtTime15k.fork_at(
            block_number=0, timestamp=15_000
        )
        is SilaShanghai
    )
    assert SilaParisToSilaShanghaiAtTime15k.fork_at() is SilaParis
    assert (
        SilaParisToSilaShanghaiAtTime15k.fork_at(
            block_number=10_000_000, timestamp=14_999
        )
        is SilaParis
    )


def test_forks_from() -> None:  # noqa: D103
    assert forks_from(SilaParis)[0] == SilaParis
    assert forks_from(SilaParis)[-1] == LAST_DEPLOYED
    assert forks_from(SilaParis, deployed_only=True)[0] == SilaParis
    assert forks_from(SilaParis, deployed_only=True)[-1] == LAST_DEPLOYED
    assert forks_from(SilaParis, deployed_only=False)[0] == SilaParis
    # Too flaky
    # assert forks_from(SilaParis, deployed_only=False)[-1] == LAST_DEVELOPMENT


def test_forks() -> None:
    """Test fork utilities."""
    assert forks_from_until(SilaBerlin, SilaBerlin) == [SilaBerlin]
    assert forks_from_until(SilaBerlin, SilaLondon) == [SilaBerlin, SilaLondon]
    assert forks_from_until(SilaBerlin, SilaParis) == [
        SilaBerlin,
        SilaLondon,
        SilaParis,
    ]

    # Test fork names
    assert SilaLondon.name() == "SilaLondon"
    assert (
        SilaParisToSilaShanghaiAtTime15k.name()
        == "SilaParisToSilaShanghaiAtTime15k"
    )
    assert f"{SilaLondon}" == "SilaLondon"
    assert (
        f"{SilaParisToSilaShanghaiAtTime15k}"
        == "SilaParisToSilaShanghaiAtTime15k"
    )

    assert SilaParis.transition_tool_name() == "SilaParis"
    assert SilaShanghai.transition_tool_name() == "SilaShanghai"
    assert f"{SilaParis}" == "SilaParis"
    assert f"{SilaShanghai}" == "SilaShanghai"
    assert (
        f"{SilaParisToSilaShanghaiAtTime15k}"
        == "SilaParisToSilaShanghaiAtTime15k"
    )

    # Test some fork properties
    assert SilaBerlin.header_base_fee_required() is False
    assert SilaLondon.header_base_fee_required() is True
    assert SilaParis.header_base_fee_required() is True
    # Default values of normal forks if the genesis block
    assert SilaParis.header_base_fee_required() is True

    # Transition forks too
    assert (
        SilaBerlinToSilaLondonAt5.fork_at(
            block_number=4, timestamp=0
        ).header_base_fee_required()
        is False
    )
    assert (
        SilaBerlinToSilaLondonAt5.fork_at(
            block_number=5, timestamp=0
        ).header_base_fee_required()
        is True
    )
    assert (
        SilaParisToSilaShanghaiAtTime15k.fork_at(
            block_number=0, timestamp=14_999
        ).header_withdrawals_required()
        is False
    )
    assert (
        SilaParisToSilaShanghaiAtTime15k.fork_at(
            block_number=0, timestamp=15_000
        ).header_withdrawals_required()
        is True
    )
    assert (
        SilaParisToSilaShanghaiAtTime15k.fork_at().header_withdrawals_required()
        is False
    )


class ForkInPydanticModel(BaseModel):
    """Fork in pydantic model."""

    fork_1: Fork | TransitionFork
    fork_2: Fork | TransitionFork
    fork_3: Fork | TransitionFork | None


def test_fork_in_pydantic_model() -> None:
    """Test fork in pydantic model."""
    model = ForkInPydanticModel(
        fork_1=SilaParis, fork_2=SilaParisToSilaShanghaiAtTime15k, fork_3=None
    )
    assert model.model_dump() == {
        "fork_1": "SilaParis",
        "fork_2": "SilaParisToSilaShanghaiAtTime15k",
        "fork_3": None,
    }
    assert model.model_dump_json() == (
        '{"fork_1":"SilaParis","fork_2":"SilaParisToSilaShanghaiAtTime15k","fork_3":null}'
    )
    model = ForkInPydanticModel.model_validate_json(
        '{"fork_1": "SilaParis", '
        '"fork_2": "SilaParisToSilaShanghaiAtTime15k", '
        '"fork_3": null}'
    )
    assert model.fork_1 is SilaParis
    assert model.fork_2 is SilaParisToSilaShanghaiAtTime15k
    assert model.fork_3 is None


def test_fork_comparison() -> None:
    """Test fork comparison operators."""
    # Test fork comparison
    assert SilaParis > SilaBerlin
    assert not SilaBerlin > SilaParis
    assert SilaBerlin < SilaParis
    assert not SilaParis < SilaBerlin

    assert SilaParis >= SilaBerlin
    assert not SilaBerlin >= SilaParis
    assert SilaBerlin <= SilaParis
    assert not SilaParis <= SilaBerlin

    assert SilaLondon > SilaBerlin
    assert not SilaBerlin > SilaLondon
    assert SilaBerlin < SilaLondon
    assert not SilaLondon < SilaBerlin

    assert SilaLondon >= SilaBerlin
    assert not SilaBerlin >= SilaLondon
    assert SilaBerlin <= SilaLondon
    assert not SilaLondon <= SilaBerlin

    assert SilaBerlin >= SilaBerlin
    assert SilaBerlin <= SilaBerlin
    assert not SilaBerlin > SilaBerlin
    assert not SilaBerlin < SilaBerlin

    fork = SilaBerlin
    assert fork >= SilaBerlin
    assert fork <= SilaBerlin
    assert not fork > SilaBerlin
    assert not fork < SilaBerlin
    assert fork == SilaBerlin


def test_transition_fork_comparison() -> None:
    """
    Test comparing to a transition fork.

    The comparison logic is based on the logic we use to generate the tests.

    E.g. given transition fork A->B, when filling, and given the from/until
    markers, we expect the following logic:

    Marker    Comparison   A->B Included
    --------- ------------ ---------------
    From A    fork >= A    True
    Until A   fork <= A    False
    From B    fork >= B    True
    Until B   fork <= B    True
    """
    assert SilaBerlinToSilaLondonAt5 >= SilaBerlin
    assert not SilaBerlinToSilaLondonAt5 <= SilaBerlin
    assert SilaBerlinToSilaLondonAt5 >= SilaLondon
    assert SilaBerlinToSilaLondonAt5 <= SilaLondon

    # Comparisons between transition forks is done against the `transitions_to`
    # fork
    assert SilaBerlinToSilaLondonAt5 < SilaParisToSilaShanghaiAtTime15k
    assert SilaParisToSilaShanghaiAtTime15k > SilaBerlinToSilaLondonAt5
    assert SilaBerlinToSilaLondonAt5 == SilaBerlinToSilaLondonAt5
    assert SilaBerlinToSilaLondonAt5 != SilaParisToSilaShanghaiAtTime15k
    assert SilaBerlinToSilaLondonAt5 <= SilaParisToSilaShanghaiAtTime15k
    assert SilaParisToSilaShanghaiAtTime15k >= SilaBerlinToSilaLondonAt5

    assert sorted(
        {
            SilaPragueToSilaOsakaAtTime15k,
            SilaCancunToSilaPragueAtTime15k,
            SilaParisToSilaShanghaiAtTime15k,
            SilaShanghaiToSilaCancunAtTime15k,
            SilaBerlinToSilaLondonAt5,
        }
    ) == [
        SilaBerlinToSilaLondonAt5,
        SilaParisToSilaShanghaiAtTime15k,
        SilaShanghaiToSilaCancunAtTime15k,
        SilaCancunToSilaPragueAtTime15k,
        SilaPragueToSilaOsakaAtTime15k,
    ]


def test_get_forks() -> None:  # noqa: D103
    all_forks = get_forks()
    assert all_forks[0] == FIRST_DEPLOYED
    # assert all_forks[-1] == LAST_DEVELOPMENT  # Too flaky


def test_deployed_forks() -> None:  # noqa: D103
    deployed_forks = get_deployed_forks()
    assert deployed_forks[0] == FIRST_DEPLOYED
    assert deployed_forks[-1] == LAST_DEPLOYED


class PrePreAllocFork(SilaShanghai):
    """Dummy fork used for testing."""

    @classmethod
    def pre_allocation(cls) -> Dict:
        """Return some starting point for allocation."""
        return {"test": "test"}


class PreAllocFork(PrePreAllocFork):
    """Dummy fork used for testing."""

    @classmethod
    def pre_allocation(cls) -> Dict:
        """Add allocation to the pre-existing one from previous fork."""
        return {"test2": "test2"} | super(PreAllocFork, cls).pre_allocation()


@transition_fork(
    to_fork=PreAllocFork, from_fork=PrePreAllocFork, at_timestamp=15_000
)
class PreAllocTransitionFork(TransitionBaseClass):
    """PrePreAllocFork to PreAllocFork transition at Timestamp 15k."""

    pass


def test_pre_alloc() -> None:  # noqa: D103
    assert PrePreAllocFork.pre_allocation() == {"test": "test"}
    assert PreAllocFork.pre_allocation() == {"test": "test", "test2": "test2"}
    assert PreAllocTransitionFork.transitions_to().pre_allocation() == {
        "test": "test",
        "test2": "test2",
    }
    assert PreAllocTransitionFork.transitions_from().pre_allocation() == {
        "test": "test",
    }


def test_precompiles() -> None:  # noqa: D103
    assert sorted(SilaCancun.precompiles()) == list(range(1, 11))


@pytest.mark.parametrize("fork", sorted(ALL_FORKS, key=str), ids=str)
def test_system_contract_request_types(fork: Fork) -> None:
    """
    Every request type is a request class whose system contract is one of
    the fork's system contracts.
    """
    request_classes = fork.system_contract_request_types()
    assert sorted(cls.type for cls in request_classes) == list(
        range(0, fork.max_request_type() + 1)
    )
    assert {cls.system_contract_address for cls in request_classes} <= set(
        fork.system_contracts()
    )


@pytest.mark.parametrize("fork", sorted(ALL_FORKS, key=str), ids=str)
def test_system_contract_call_phases(fork: Fork) -> None:
    """
    Every system contract declares when the block calls it, and every
    queued request predeploy is called after the transactions.
    """
    phases = fork.system_contract_call_phases()
    assert set(phases) == set(fork.system_contracts())
    for request_class in fork.system_contract_request_types():
        if issubclass(request_class, FeeSystemContractRequest):
            assert (
                phases[request_class.system_contract_address]
                is SystemCallPhase.AFTER_TRANSACTIONS
            )


def test_tx_types() -> None:  # noqa: D103
    assert SilaCancun.tx_types() == list(reversed(range(4)))


@pytest.mark.parametrize(
    "fork",
    [
        pytest.param(SilaShanghai, id="SilaShanghai"),
        pytest.param(SilaBerlin, id="SilaBerlin"),
        pytest.param(SilaIstanbul, id="SilaIstanbul"),
        pytest.param(SilaHomestead, id="SilaHomestead"),
        pytest.param(Frontier, id="Frontier"),
    ],
)
@pytest.mark.parametrize(
    "calldata",
    [
        pytest.param(b"\0", id="zero-data"),
        pytest.param(b"\1", id="non-zero-data"),
    ],
)
@pytest.mark.parametrize(
    "create_tx",
    [False, True],
)
def test_tx_intrinsic_gas_functions(  # noqa: D103
    fork: Fork, calldata: bytes, create_tx: bool
) -> None:
    intrinsic_gas = 21_000
    if calldata == b"\0":
        intrinsic_gas += 4
    else:
        if fork >= SilaIstanbul:
            intrinsic_gas += 16
        else:
            intrinsic_gas += 68

    if create_tx:
        if fork >= SilaHomestead:
            intrinsic_gas += 32000
        if fork >= SilaShanghai:
            intrinsic_gas += 2
    assert (
        fork.transaction_intrinsic_cost_calculator()(
            calldata=calldata,
            contract_creation=create_tx,
        )
        == intrinsic_gas
    )


class FutureFork(SilaOsaka):
    """
    Dummy fork used for testing.

    Contains no changes to the blob parameters from the parent fork in order to
    confirm that it's added to the blob schedule even if it doesn't have any
    changes.
    """

    pass


@pytest.mark.parametrize(
    "fork,expected_schedule",
    [
        pytest.param(Frontier, None, id="Frontier"),
        pytest.param(
            SilaCancun,
            {
                "SilaCancun": {
                    "target_blobs_per_block": 3,
                    "max_blobs_per_block": 6,
                    "baseFeeUpdateFraction": 3338477,
                },
            },
            id="SilaCancun",
        ),
        pytest.param(
            SilaPrague,
            {
                "SilaCancun": {
                    "target_blobs_per_block": 3,
                    "max_blobs_per_block": 6,
                    "baseFeeUpdateFraction": 3338477,
                },
                "SilaPrague": {
                    "target_blobs_per_block": 6,
                    "max_blobs_per_block": 9,
                    "baseFeeUpdateFraction": 5007716,
                },
            },
            id="SilaPrague",
        ),
        pytest.param(
            SilaOsaka,
            {
                "SilaCancun": {
                    "target_blobs_per_block": 3,
                    "max_blobs_per_block": 6,
                    "baseFeeUpdateFraction": 3338477,
                },
                "SilaPrague": {
                    "target_blobs_per_block": 6,
                    "max_blobs_per_block": 9,
                    "baseFeeUpdateFraction": 5007716,
                },
                "SilaOsaka": {
                    "target_blobs_per_block": 6,
                    "max_blobs_per_block": 9,
                    "baseFeeUpdateFraction": 5007716,
                },
            },
            id="SilaOsaka",
        ),
        pytest.param(
            SilaCancunToSilaPragueAtTime15k,
            {
                "SilaCancun": {
                    "target_blobs_per_block": 3,
                    "max_blobs_per_block": 6,
                    "baseFeeUpdateFraction": 3338477,
                },
                "SilaPrague": {
                    "target_blobs_per_block": 6,
                    "max_blobs_per_block": 9,
                    "baseFeeUpdateFraction": 5007716,
                },
            },
            id="SilaCancunToSilaPragueAtTime15k",
        ),
        pytest.param(
            SilaPragueToSilaOsakaAtTime15k,
            {
                "SilaCancun": {
                    "target_blobs_per_block": 3,
                    "max_blobs_per_block": 6,
                    "baseFeeUpdateFraction": 3338477,
                },
                "SilaPrague": {
                    "target_blobs_per_block": 6,
                    "max_blobs_per_block": 9,
                    "baseFeeUpdateFraction": 5007716,
                },
                "SilaOsaka": {
                    "target_blobs_per_block": 6,
                    "max_blobs_per_block": 9,
                    "baseFeeUpdateFraction": 5007716,
                },
            },
            id="SilaPragueToSilaOsakaAtTime15k",
        ),
        pytest.param(
            FutureFork,
            {
                "SilaCancun": {
                    "target_blobs_per_block": 3,
                    "max_blobs_per_block": 6,
                    "baseFeeUpdateFraction": 3338477,
                },
                "SilaPrague": {
                    "target_blobs_per_block": 6,
                    "max_blobs_per_block": 9,
                    "baseFeeUpdateFraction": 5007716,
                },
                "SilaOsaka": {
                    "target_blobs_per_block": 6,
                    "max_blobs_per_block": 9,
                    "baseFeeUpdateFraction": 5007716,
                },
                "FutureFork": {
                    "target_blobs_per_block": 6,
                    "max_blobs_per_block": 9,
                    "baseFeeUpdateFraction": 5007716,
                },
            },
            id="FutureFork",
        ),
    ],
)
def test_blob_schedules(
    fork: Fork | TransitionFork, expected_schedule: Dict | None
) -> None:
    """Test blob schedules for different forks."""
    if expected_schedule is None:
        assert fork.transitions_to().blob_schedule() is None
    else:
        assert fork.transitions_to().blob_schedule() == BlobSchedule(
            **expected_schedule
        )


def test_bpo_fork() -> None:  # noqa: D103
    assert SilaOsaka.bpo_fork() is False
    assert BPO1.bpo_fork() is True
    assert BPO2.bpo_fork() is True
    assert BPO3.bpo_fork() is True
    assert BPO4.bpo_fork() is True
    assert SilaOsakaToBPO1AtTime15k.fork_at().bpo_fork() is False
    assert BPO1ToBPO2AtTime15k.fork_at().bpo_fork() is True
    assert BPO2ToBPO3AtTime15k.fork_at().bpo_fork() is True
    assert BPO3ToBPO4AtTime15k.fork_at().bpo_fork() is True


def test_fork_adapters() -> None:  # noqa: D103
    assert SilaOsaka == ForkAdapter.validate_python("SilaOsaka")
    assert SilaOsaka == ForkOrNoneAdapter.validate_python("SilaOsaka")
    assert ForkOrNoneAdapter.validate_python(None) is None
    assert {SilaOsaka, SilaPrague} == ForkSetAdapter.validate_python(
        "SilaOsaka, SilaPrague"
    )
    assert {SilaOsaka, SilaPrague} == ForkSetAdapter.validate_python(
        "silaosaka, SilaPrague"
    )
    assert {SilaOsaka, SilaPrague} == ForkSetAdapter.validate_python(
        {"silaosaka", "SilaPrague"}
    )
    assert {SilaOsaka} == ForkSetAdapter.validate_python("SilaOsaka")
    assert {SilaOsaka} == ForkSetAdapter.validate_python({SilaOsaka})
    assert set() == ForkSetAdapter.validate_python("")


class TestSelectedForkSetWithTransitionBoundaries:
    """Test `get_selected_fork_set` with transition fork boundaries."""

    @staticmethod
    def _normal_forks(fork_set: set) -> set:
        """Return the set of normal (non-transition) forks."""
        return {f for f in fork_set if not issubclass(f, TransitionBaseClass)}

    @staticmethod
    def _transition_forks(fork_set: set) -> set:
        """Return the set of transition forks."""
        return {f for f in fork_set if issubclass(f, TransitionBaseClass)}

    def test_transition_from_and_until(self) -> None:
        """Test range with transition forks as both boundaries."""
        result = get_selected_fork_set(
            single_fork=set(),
            forks_from={SilaOsakaToBPO1AtTime15k},  # type: ignore[arg-type]
            forks_until={BPO2ToSilaAmsterdamAtTime15k},  # type: ignore[arg-type]
        )
        assert self._normal_forks(result) == {BPO1, BPO2}
        assert self._transition_forks(result) == {
            SilaOsakaToBPO1AtTime15k,
            BPO1ToBPO2AtTime15k,
            BPO2ToSilaAmsterdamAtTime15k,
        }

    def test_transition_until_excludes_target(self) -> None:
        """Transition fork `--until` must not include `transitions_to()`."""
        result = get_selected_fork_set(
            single_fork=set(),
            forks_from={SilaOsakaToBPO1AtTime15k},  # type: ignore[arg-type]
            forks_until={BPO2ToSilaAmsterdamAtTime15k},  # type: ignore[arg-type]
        )
        assert SilaAmsterdam not in result

    def test_non_bpo_transition_boundaries(self) -> None:
        """Test non-BPO transition fork boundaries."""
        result = get_selected_fork_set(
            single_fork=set(),
            forks_from={SilaCancunToSilaPragueAtTime15k},  # type: ignore[arg-type]
            forks_until={SilaPragueToSilaOsakaAtTime15k},  # type: ignore[arg-type]
        )
        assert self._normal_forks(result) == {SilaPrague}
        assert self._transition_forks(result) == {
            SilaCancunToSilaPragueAtTime15k,
            SilaPragueToSilaOsakaAtTime15k,
        }
        assert SilaOsaka not in result

    def test_normal_boundaries_unchanged(self) -> None:
        """Normal fork boundaries still work as before."""
        result = get_selected_fork_set(
            single_fork=set(),
            forks_from={SilaPrague},
            forks_until={SilaOsaka},
        )
        assert self._normal_forks(result) == {SilaPrague, SilaOsaka}
        assert SilaCancunToSilaPragueAtTime15k in result
        assert SilaPragueToSilaOsakaAtTime15k in result

    def test_transition_from_normal_until(self) -> None:
        """Test transition `--from` with normal `--until`."""
        result = get_selected_fork_set(
            single_fork=set(),
            forks_from={SilaOsakaToBPO1AtTime15k},  # type: ignore[arg-type]
            forks_until={BPO2},
        )
        assert self._normal_forks(result) == {BPO1, BPO2}
        assert SilaOsakaToBPO1AtTime15k in result
        assert BPO1ToBPO2AtTime15k in result
        assert BPO2ToSilaAmsterdamAtTime15k not in result

    def test_until_amsterdam_includes_bpo_siblings(self) -> None:
        """`--until=SilaAmsterdam` pulls in the parallel BPO branch."""
        result = get_selected_fork_set(
            single_fork=set(),
            forks_from=set(),
            forks_until={SilaAmsterdam},
        )
        normal = self._normal_forks(result)
        assert {BPO1, BPO2, BPO3, BPO4, BPO5, SilaAmsterdam} <= normal
        assert BPO2ToBPO3AtTime15k in result
        assert BPO3ToBPO4AtTime15k in result

    def test_from_osaka_until_amsterdam_spans_bpo_branch(self) -> None:
        """
        `--from=SilaOsaka --until=SilaAmsterdam` spans the full BPO branch.
        """
        result = get_selected_fork_set(
            single_fork=set(),
            forks_from={SilaOsaka},
            forks_until={SilaAmsterdam},
        )
        assert self._normal_forks(result) == {
            SilaOsaka,
            BPO1,
            BPO2,
            BPO3,
            BPO4,
            BPO5,
            SilaAmsterdam,
        }

    def test_until_amsterdam_bpo_siblings_disabled(self) -> None:
        """`bpo_siblings=False` keeps the parallel BPO branch out."""
        result = get_selected_fork_set(
            single_fork=set(),
            forks_from=set(),
            forks_until={SilaAmsterdam},
            bpo_siblings=False,
        )
        normal = self._normal_forks(result)
        assert {BPO1, BPO2, SilaAmsterdam} <= normal
        assert not ({BPO3, BPO4, BPO5} & normal)

    def test_until_bpo2_excludes_later_bpo_siblings(self) -> None:
        """`--until=BPO2` must not pull in the later BPO branch."""
        result = get_selected_fork_set(
            single_fork=set(),
            forks_from=set(),
            forks_until={BPO2},
        )
        normal = self._normal_forks(result)
        assert {BPO1, BPO2} <= normal
        assert not ({BPO3, BPO4, BPO5} & normal)

    def test_from_amsterdam_until_amsterdam_excludes_bpos(self) -> None:
        """
        `--from=SilaAmsterdam --until=SilaAmsterdam` stays SilaAmsterdam-only.
        """
        result = get_selected_fork_set(
            single_fork=set(),
            forks_from={SilaAmsterdam},
            forks_until={SilaAmsterdam},
        )
        assert self._normal_forks(result) == {SilaAmsterdam}


def test_blob_constants() -> None:  # noqa: D103
    assert SilaOsaka.get_blob_constant("AMOUNT_CELL_PROOFS") == 128


def test_method_versions() -> None:  # noqa: D103
    assert SilaLondon.engine_get_blobs_version() is None
    assert SilaLondon.engine_get_payload_version() is None
    assert SilaLondon.engine_new_payload_version() is None
    assert SilaLondon.engine_forkchoice_updated_version() is None

    assert SilaParis.engine_get_blobs_version() is None
    assert SilaParis.engine_get_payload_version() == 1
    assert SilaParis.engine_new_payload_version() == 1
    assert SilaParis.engine_forkchoice_updated_version() == 1

    assert SilaShanghai.engine_get_blobs_version() is None
    assert SilaShanghai.engine_get_payload_version() == 2
    assert SilaShanghai.engine_new_payload_version() == 2
    assert SilaShanghai.engine_forkchoice_updated_version() == 2

    assert SilaCancun.engine_get_blobs_version() == 1
    assert SilaCancun.engine_get_payload_version() == 3
    assert SilaCancun.engine_new_payload_version() == 3
    assert SilaCancun.engine_forkchoice_updated_version() == 3

    assert SilaPrague.engine_get_blobs_version() == 1
    assert SilaPrague.engine_get_payload_version() == 4
    assert SilaPrague.engine_new_payload_version() == 4
    assert SilaPrague.engine_forkchoice_updated_version() == 3

    assert SilaOsaka.engine_get_blobs_version() == 2
    assert SilaOsaka.engine_get_payload_version() == 5
    assert SilaOsaka.engine_new_payload_version() == 4
    assert SilaOsaka.engine_forkchoice_updated_version() == 3

    assert SilaAmsterdam.engine_get_payload_version() == 6
    assert SilaAmsterdam.engine_new_payload_version() == 5


def test_sips() -> None:  # noqa: D103
    assert SIP3675.enabling_forks() == {SilaParis}
    assert SilaParis.is_sip_enabled(3675)
    assert SilaParis.is_sip_enabled(3675, 1559)
    assert SilaShanghai.is_sip_enabled(3675)
    assert not SilaParis.is_sip_enabled(3855)
    assert not SilaParis.is_sip_enabled(3675, 3855)
    assert not SilaParis.is_sip_enabled(3855, 3675)
    assert SilaShanghai.is_sip_enabled(3855)


def test_oog_budget_lift() -> None:
    """
    `Fork.oog_budget_lift` returns zero pre-SIP-8037 and the cumulative
    SSTORE-set + CREATE + code-deposit state-gas spill on SilaAmsterdam.
    """
    # Pre-SIP-8037: state_gas helpers are 0, so any lift is 0.
    assert SilaCancun.oog_budget_lift(sstores_before_oog=1) == 0
    assert SilaCancun.oog_budget_lift(creates_before_oog=1) == 0
    assert (
        SilaCancun.oog_budget_lift(
            sstores_before_oog=3, creates_before_oog=2, deploy_code_size=64
        )
        == 0
    )
    # SilaAmsterdam: lift composes the three state-gas helpers.
    sstore = Opcodes.SSTORE(new_value=1).state_cost(SilaAmsterdam)
    create = SilaAmsterdam.create_state_gas()
    code_64 = SilaAmsterdam.code_deposit_state_gas(code_size=64)
    assert SilaAmsterdam.oog_budget_lift() == 0
    assert SilaAmsterdam.oog_budget_lift(sstores_before_oog=1) == sstore
    assert SilaAmsterdam.oog_budget_lift(creates_before_oog=1) == create
    assert SilaAmsterdam.oog_budget_lift(deploy_code_size=64) == code_64
    assert (
        SilaAmsterdam.oog_budget_lift(
            sstores_before_oog=3,
            creates_before_oog=2,
            deploy_code_size=64,
        )
        == 3 * sstore + 2 * create + code_64
    )


@pytest.fixture(scope="module")
def all_fork_classes() -> List[Type[BaseFork]]:
    """Return every concrete fork class, transition forks excluded."""
    return sorted(get_forks(), key=str)


def _memoized_caches(
    fork_classes: List[Type[BaseFork]],
) -> Iterator[Tuple[Type[Any], str, Any]]:
    """Yield ``(owner, method_name, cache)`` for every memoized override."""
    owners: set = set()
    for fork in fork_classes:
        owners.update(fork.__mro__)
    for owner in owners:
        for method_name in BaseForkMeta.MEMOIZED_FORK_METHODS:
            member = owner.__dict__.get(method_name)
            if not isinstance(member, classmethod):
                continue
            function = member.__func__
            if hasattr(function, "cache_clear"):
                yield owner, method_name, function


def test_memoized_fork_methods_are_installed(
    all_fork_classes: List[Type[BaseFork]],
) -> None:
    """Every fork must resolve each memoized name to a cached override."""
    for fork in all_fork_classes:
        for method_name in BaseForkMeta.MEMOIZED_FORK_METHODS:
            resolved = getattr(fork, method_name)
            assert hasattr(resolved.__func__, "cache_info"), (
                f"{fork}.{method_name} resolves to an uncached override"
            )


def test_memoized_fork_methods_are_computed_once_per_fork(
    all_fork_classes: List[Type[BaseFork]],
) -> None:
    """The first call per fork computes, and every later one is a hit."""
    for method_name in BaseForkMeta.MEMOIZED_FORK_METHODS:
        for _, _, function in _memoized_caches(all_fork_classes):
            function.cache_clear()
        for fork in all_fork_classes:
            cache = getattr(fork, method_name).__func__
            before = cache.cache_info()
            getattr(fork, method_name)()
            getattr(fork, method_name)()
            after = cache.cache_info()
            assert after.misses == before.misses + 1, (
                f"{fork}.{method_name} recomputed on a repeat call"
            )
            assert after.hits == before.hits + 1, (
                f"{fork}.{method_name} was not served from its cache"
            )


def test_memoized_fork_methods_are_not_shared_between_forks(
    all_fork_classes: List[Type[BaseFork]],
) -> None:
    """A cache is keyed on the fork, so no fork may serve another's value."""
    for method_name in BaseForkMeta.MEMOIZED_FORK_METHODS:
        warm = {
            str(fork): getattr(fork, method_name)()
            for fork in all_fork_classes
        }
        for _, _, function in _memoized_caches(all_fork_classes):
            function.cache_clear()
        for fork in reversed(all_fork_classes):
            assert getattr(fork, method_name)() == warm[str(fork)], (
                f"{fork}.{method_name} changed when recomputed in a "
                "different order"
            )

        assert SilaAmsterdam.gas_costs() is not SilaCancun.gas_costs()
        assert SilaAmsterdam.gas_costs() != SilaCancun.gas_costs()


def test_memoized_fork_methods_return_immutable_values() -> None:
    """Callers share one object, so a mutable value could be corrupted."""
    for method_name in BaseForkMeta.MEMOIZED_FORK_METHODS:
        value = getattr(SilaAmsterdam, method_name)()
        assert dataclasses.is_dataclass(value)
        field_name = next(iter(dataclasses.fields(value))).name
        with pytest.raises(dataclasses.FrozenInstanceError):
            setattr(value, field_name, 0)


def test_abstract_memoized_declarations_are_left_alone() -> None:
    """`abc` must still see `BaseFork`'s declarations as unimplemented."""
    for method_name in BaseForkMeta.MEMOIZED_FORK_METHODS:
        declaration = BaseFork.__dict__[method_name]
        assert getattr(declaration, "__isabstractmethod__", False)
        assert not hasattr(declaration.__func__, "cache_info")
