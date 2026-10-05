"""Test fork utilities."""

from typing import Dict, cast

import pytest
from pydantic import BaseModel

from execution_testing.base_types import BlobSchedule

from ..forks.forks import (
    BPO1,
    BPO2,
    BPO3,
    BPO4,
    SilaAmsterdam,
    SilaBerlin,
    SilaCancun,
    Frontier,
    SilaHomestead,
    SilaIstanbul,
    SilaLondon,
    SilaOsaka,
    SilaParis,
    SilaPrague,
    SilaShanghai,
)
from ..forks.transition import (
    SilaBerlinToSilaLondonAt5,
    BPO1ToBPO2AtTime15k,
    BPO2ToBPO3AtTime15k,
    BPO3ToBPO4AtTime15k,
    SilaCancunToSilaPragueAtTime15k,
    SilaOsakaToBPO1AtTime15k,
    SilaParisToSilaShanghaiAtTime15k,
    SilaPragueToSilaOsakaAtTime15k,
    SilaShanghaiToSilaCancunAtTime15k,
)
from ..helpers import (
    Fork,
    ForkAdapter,
    ForkOrNoneAdapter,
    ForkSetAdapter,
    forks_from,
    forks_from_until,
    get_deployed_forks,
    get_forks,
    transition_fork_from_to,
    transition_fork_to,
)
from ..transition_base_fork import transition_fork

FIRST_DEPLOYED = Frontier
LAST_DEPLOYED = SilaOsaka
LAST_DEVELOPMENT = SilaAmsterdam
DEVELOPMENT_FORKS = [SilaAmsterdam]


def test_transition_forks() -> None:
    """Test transition fork utilities."""
    assert transition_fork_from_to(SilaBerlin, SilaLondon) == SilaBerlinToSilaLondonAt5
    assert transition_fork_from_to(SilaBerlin, SilaParis) is None
    assert transition_fork_to(SilaShanghai) == {SilaParisToSilaShanghaiAtTime15k}

    # Test forks transitioned to and from
    assert SilaBerlinToSilaLondonAt5.transitions_to() == SilaLondon  # type: ignore
    assert SilaBerlinToSilaLondonAt5.transitions_from() == SilaBerlin  # type: ignore

    assert (
        SilaBerlinToSilaLondonAt5.transition_tool_name(block_number=4, timestamp=0)
        == "SilaBerlin"
    )
    assert (
        SilaBerlinToSilaLondonAt5.transition_tool_name(block_number=5, timestamp=0)
        == "SilaLondon"
    )
    # Default values of transition forks is the transition block
    assert SilaBerlinToSilaLondonAt5.transition_tool_name() == "SilaLondon"

    assert (
        SilaParisToSilaShanghaiAtTime15k.transition_tool_name(
            block_number=0, timestamp=14_999
        )
        == "Merge"
    )
    assert (
        SilaParisToSilaShanghaiAtTime15k.transition_tool_name(
            block_number=0, timestamp=15_000
        )
        == "SilaShanghai"
    )
    assert SilaParisToSilaShanghaiAtTime15k.transition_tool_name() == "SilaShanghai"

    assert (
        SilaBerlinToSilaLondonAt5.header_base_fee_required(block_number=4, timestamp=0)
        is False
    )
    assert (
        SilaBerlinToSilaLondonAt5.header_base_fee_required(block_number=5, timestamp=0)
        is True
    )

    assert (
        SilaParisToSilaShanghaiAtTime15k.header_withdrawals_required(
            block_number=0, timestamp=14_999
        )
        is False
    )
    assert (
        SilaParisToSilaShanghaiAtTime15k.header_withdrawals_required(
            block_number=0, timestamp=15_000
        )
        is True
    )

    assert (
        SilaParisToSilaShanghaiAtTime15k.engine_new_payload_version(
            block_number=0, timestamp=14_999
        )
        == 1
    )
    assert (
        SilaParisToSilaShanghaiAtTime15k.engine_new_payload_version(
            block_number=0, timestamp=15_000
        )
        == 2
    )

    assert SilaBerlinToSilaLondonAt5.fork_at(block_number=4, timestamp=0) == SilaBerlin
    assert SilaBerlinToSilaLondonAt5.fork_at(block_number=5, timestamp=0) == SilaLondon
    assert (
        SilaParisToSilaShanghaiAtTime15k.fork_at(block_number=0, timestamp=14_999)
        == SilaParis
    )
    assert (
        SilaParisToSilaShanghaiAtTime15k.fork_at(block_number=0, timestamp=15_000)
        == SilaShanghai
    )
    assert SilaParisToSilaShanghaiAtTime15k.fork_at() == SilaParis
    assert (
        SilaParisToSilaShanghaiAtTime15k.fork_at(
            block_number=10_000_000, timestamp=14_999
        )
        == SilaParis
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
    assert SilaParisToSilaShanghaiAtTime15k.name() == "SilaParisToSilaShanghaiAtTime15k"
    assert f"{SilaLondon}" == "SilaLondon"
    assert f"{SilaParisToSilaShanghaiAtTime15k}" == "SilaParisToSilaShanghaiAtTime15k"

    # Merge name will be changed to paris, but we need to check the inheriting
    # fork name is still the default
    assert SilaParis.transition_tool_name() == "Merge"
    assert SilaShanghai.transition_tool_name() == "SilaShanghai"
    assert f"{SilaParis}" == "SilaParis"
    assert f"{SilaShanghai}" == "SilaShanghai"
    assert f"{SilaParisToSilaShanghaiAtTime15k}" == "SilaParisToSilaShanghaiAtTime15k"

    # Test some fork properties
    assert (
        SilaBerlin.header_base_fee_required(block_number=0, timestamp=0) is False
    )
    assert SilaLondon.header_base_fee_required(block_number=0, timestamp=0) is True
    assert SilaParis.header_base_fee_required(block_number=0, timestamp=0) is True
    # Default values of normal forks if the genesis block
    assert SilaParis.header_base_fee_required() is True

    # Transition forks too
    assert (
        cast(Fork, SilaBerlinToSilaLondonAt5).header_base_fee_required(
            block_number=4, timestamp=0
        )
        is False
    )
    assert (
        cast(Fork, SilaBerlinToSilaLondonAt5).header_base_fee_required(
            block_number=5, timestamp=0
        )
        is True
    )
    assert (
        cast(Fork, SilaParisToSilaShanghaiAtTime15k).header_withdrawals_required(
            block_number=0, timestamp=14_999
        )
        is False
    )
    assert (
        cast(Fork, SilaParisToSilaShanghaiAtTime15k).header_withdrawals_required(
            block_number=0, timestamp=15_000
        )
        is True
    )
    assert (
        cast(Fork, SilaParisToSilaShanghaiAtTime15k).header_withdrawals_required()
        is True
    )


class ForkInPydanticModel(BaseModel):
    """Fork in pydantic model."""

    fork_1: Fork
    fork_2: Fork
    fork_3: Fork | None


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
        '{"fork_1": "SilaParis", "fork_2": "SilaParisToSilaShanghaiAtTime15k", '
        '"fork_3": null}'
    )
    assert model.fork_1 == SilaParis
    assert model.fork_2 == SilaParisToSilaShanghaiAtTime15k
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
    def pre_allocation(
        cls, *, block_number: int = 0, timestamp: int = 0
    ) -> Dict:
        """Return some starting point for allocation."""
        del block_number, timestamp
        return {"test": "test"}


class PreAllocFork(PrePreAllocFork):
    """Dummy fork used for testing."""

    @classmethod
    def pre_allocation(
        cls, *, block_number: int = 0, timestamp: int = 0
    ) -> Dict:
        """Add allocation to the pre-existing one from previous fork."""
        del block_number, timestamp
        return {"test2": "test2"} | super(PreAllocFork, cls).pre_allocation()


@transition_fork(to_fork=PreAllocFork, at_timestamp=15_000)
class PreAllocTransitionFork(PrePreAllocFork):
    """PrePreAllocFork to PreAllocFork transition at Timestamp 15k."""

    pass


def test_pre_alloc() -> None:  # noqa: D103
    assert PrePreAllocFork.pre_allocation() == {"test": "test"}
    assert PreAllocFork.pre_allocation() == {"test": "test", "test2": "test2"}
    assert PreAllocTransitionFork.pre_allocation() == {
        "test": "test",
        "test2": "test2",
    }
    assert PreAllocTransitionFork.pre_allocation() == {
        "test": "test",
        "test2": "test2",
    }


def test_precompiles() -> None:  # noqa: D103
    SilaCancun.precompiles() == list(range(11))[1:]  # noqa: B015


def test_tx_types() -> None:  # noqa: D103
    SilaCancun.tx_types() == list(range(4))  # noqa: B015


@pytest.mark.parametrize(
    "fork",
    [
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
def test_blob_schedules(fork: Fork, expected_schedule: Dict | None) -> None:
    """Test blob schedules for different forks."""
    if expected_schedule is None:
        assert fork.blob_schedule() is None
    else:
        assert fork.blob_schedule() == BlobSchedule(**expected_schedule)


def test_bpo_fork() -> None:  # noqa: D103
    assert SilaOsaka.bpo_fork() is False
    assert BPO1.bpo_fork() is True
    assert BPO2.bpo_fork() is True
    assert BPO3.bpo_fork() is True
    assert BPO4.bpo_fork() is True
    assert SilaOsakaToBPO1AtTime15k.bpo_fork() is True
    assert BPO1ToBPO2AtTime15k.bpo_fork() is True
    assert BPO2ToBPO3AtTime15k.bpo_fork() is True
    assert BPO3ToBPO4AtTime15k.bpo_fork() is True


def test_fork_adapters() -> None:  # noqa: D103
    assert SilaOsaka == ForkAdapter.validate_python("SilaOsaka")
    assert SilaOsaka == ForkOrNoneAdapter.validate_python("SilaOsaka")
    assert ForkOrNoneAdapter.validate_python(None) is None
    assert {SilaOsaka, SilaPrague} == ForkSetAdapter.validate_python("SilaOsaka, SilaPrague")
    assert {SilaOsaka, SilaPrague} == ForkSetAdapter.validate_python("osaka, SilaPrague")
    assert {SilaOsaka, SilaPrague} == ForkSetAdapter.validate_python(
        {"osaka", "SilaPrague"}
    )
    assert {SilaOsaka} == ForkSetAdapter.validate_python("SilaOsaka")
    assert {SilaOsaka} == ForkSetAdapter.validate_python({SilaOsaka})
    assert set() == ForkSetAdapter.validate_python("")
