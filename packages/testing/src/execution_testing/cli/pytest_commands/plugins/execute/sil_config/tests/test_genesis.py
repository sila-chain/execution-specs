"""Test parsing a genesis file to generate a network configuration."""

from os.path import realpath
from pathlib import Path

import pytest

from execution_testing.base_types import Hash
from execution_testing.forks import (
    BPO1,
    BPO2,
    BPO3,
    BPO4,
    BPO5,
    SilaBerlin,
    SilaByzantium,
    SilaCancun,
    SilaConstantinople,
    SilaHomestead,
    SilaIstanbul,
    SilaLondon,
    SilaOsaka,
    SilaParis,
    SilaPrague,
    SilaShanghai,
)
from execution_testing.rpc import (
    ForkConfigBlobSchedule,
)

from ..execute_types import ForkActivationTimes, Genesis, NetworkConfig

CURRENT_FILE = Path(realpath(__file__))
CURRENT_FOLDER = CURRENT_FILE.parent


@pytest.fixture
def genesis_contents(genesis_file_name: str) -> str:
    """Read the genesis file contents."""
    genesis_path = CURRENT_FOLDER / genesis_file_name
    return genesis_path.read_text()


@pytest.mark.parametrize(
    "genesis_file_name,expected_hash,expected_network_config",
    [
        pytest.param(
            "genesis_example.json",
            Hash(
                0x3A8C8CEF63859865AA1D40DED77B083EEF06A1702B8188D5586434B9C3ADC4BE
            ),
            NetworkConfig(
                chain_id=7023102237,
                genesis_hash=Hash(
                    0x3A8C8CEF63859865AA1D40DED77B083EEF06A1702B8188D5586434B9C3ADC4BE
                ),
                fork_activation_times=ForkActivationTimes(
                    root={
                        SilaHomestead: 0,
                        SilaByzantium: 0,
                        SilaConstantinople: 0,
                        SilaIstanbul: 0,
                        SilaBerlin: 0,
                        SilaLondon: 0,
                        SilaParis: 0,
                        SilaShanghai: 0,
                        SilaCancun: 0,
                        SilaPrague: 0,
                        SilaOsaka: 1753379304,
                        BPO1: 1753477608,
                        BPO2: 1753575912,
                        BPO3: 1753674216,
                        BPO4: 1753772520,
                        BPO5: 1753889256,
                    },
                ),
                blob_schedule={
                    SilaCancun: ForkConfigBlobSchedule(
                        target_blobs_per_block=3,
                        max_blobs_per_block=6,
                        base_fee_update_fraction=3338477,
                    ),
                    SilaPrague: ForkConfigBlobSchedule(
                        target_blobs_per_block=6,
                        max_blobs_per_block=9,
                        base_fee_update_fraction=5007716,
                    ),
                    SilaOsaka: ForkConfigBlobSchedule(
                        target_blobs_per_block=6,
                        max_blobs_per_block=9,
                        base_fee_update_fraction=5007716,
                    ),
                    BPO1: ForkConfigBlobSchedule(
                        target_blobs_per_block=9,
                        max_blobs_per_block=12,
                        base_fee_update_fraction=5007716,
                    ),
                    BPO2: ForkConfigBlobSchedule(
                        target_blobs_per_block=12,
                        max_blobs_per_block=15,
                        base_fee_update_fraction=5007716,
                    ),
                    BPO3: ForkConfigBlobSchedule(
                        target_blobs_per_block=15,
                        max_blobs_per_block=18,
                        base_fee_update_fraction=5007716,
                    ),
                    BPO4: ForkConfigBlobSchedule(
                        target_blobs_per_block=6,
                        max_blobs_per_block=9,
                        base_fee_update_fraction=5007716,
                    ),
                    BPO5: ForkConfigBlobSchedule(
                        target_blobs_per_block=15,
                        max_blobs_per_block=20,
                        base_fee_update_fraction=5007716,
                    ),
                },
            ),
        ),
    ],
)
def test_genesis_parsing(
    genesis_contents: str,
    expected_hash: Hash,
    expected_network_config: NetworkConfig,
) -> None:
    """
    Verify genesis config file is parsed and correctly converted into a network
    configuration.
    """
    parsed_genesis = Genesis.model_validate_json(genesis_contents)
    assert parsed_genesis.hash == expected_hash, (
        f"Unexpected genesis hash: {parsed_genesis.hash}, "
        f"expected: {expected_hash}"
    )
    network_config = parsed_genesis.network_config()
    assert network_config == expected_network_config, (
        f"Unexpected network config: {network_config}, "
        f"expected: {expected_network_config}"
    )
