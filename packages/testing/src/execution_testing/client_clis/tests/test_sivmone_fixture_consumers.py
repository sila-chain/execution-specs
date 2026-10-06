"""Test the `sivmone test` state and blockchain fixture consumers."""

import json
import shutil
from pathlib import Path
from typing import Any, Dict, Type

import pytest

from execution_testing.base_types import (
    Account,
    Address,
    TestAddress,
    TestPrivateKey,
)
from execution_testing.client_clis import (
    SivmoneBlockchainFixtureConsumer,
    SivmoneStateFixtureConsumer,
    TransitionTool,
)
from execution_testing.client_clis.fixture_consumer_tool import (
    FixtureConsumerTool,
)
from execution_testing.fixtures import (
    BlockchainFixture,
    FixtureFormat,
    StateFixture,
)
from execution_testing.forks import SilaCancun
from execution_testing.specs import StateTest
from execution_testing.test_types import (
    Environment,
    Transaction,
)
from execution_testing.vm import Op

SIVMONE = shutil.which("sivmone")

pytestmark = pytest.mark.skipif(
    SIVMONE is None, reason="sivmone binary not found in PATH"
)

CONSUMERS: Dict[FixtureFormat, Type[FixtureConsumerTool]] = {
    StateFixture: SivmoneStateFixtureConsumer,
    BlockchainFixture: SivmoneBlockchainFixtureConsumer,
}


def test_sivmone_binary_provides_both_consumers() -> None:
    """A single `sivmone` binary provides both fixture consumers."""
    assert SIVMONE is not None
    consumers = FixtureConsumerTool.all_from_binary_path(
        binary_path=Path(SIVMONE)
    )
    assert {type(consumer) for consumer in consumers} == {
        SivmoneStateFixtureConsumer,
        SivmoneBlockchainFixtureConsumer,
    }


def write_fixture(
    tmp_path: Path,
    default_t8n: TransitionTool,
    fixture_format: FixtureFormat,
    corrupt: bool,
) -> Path:
    """Fill a two-fixture file and optionally corrupt the second fixture."""
    contract = Address(0x1000)
    fixtures: Dict[str, Any] = {}
    for value in (1, 2):
        result = StateTest(
            env=Environment(),
            pre={
                TestAddress: Account(balance=10**18),
                contract: Account(code=Op.SSTORE(0, value)),
            },
            post={contract: Account(storage={0: value})},
            tx=Transaction(
                to=contract, gas_limit=100_000, secret_key=TestPrivateKey
            ),
            fork=SilaCancun,
        ).generate(t8n=default_t8n, fixture_format=fixture_format)
        fixtures[f"fixture_{value}"] = result.fixture.json_dict_with_info()
    if corrupt:
        fixture_json = fixtures["fixture_2"]
        if fixture_format == StateFixture:
            fixture_json["post"]["SilaCancun"][0]["hash"] = "0x" + "11" * 32
        else:
            fixture_json["lastblockhash"] = "0x" + "11" * 32
    path = tmp_path / f"{fixture_format.format_name}.json"
    path.write_text(json.dumps(fixtures, indent=2))
    return path


@pytest.mark.parametrize("fixture_format", [StateFixture, BlockchainFixture])
@pytest.mark.parametrize("corrupt", [False, True], ids=["valid", "corrupt"])
def test_sivmone_consumes_fixture(
    tmp_path: Path,
    default_t8n: TransitionTool,
    fixture_format: FixtureFormat,
    corrupt: bool,
) -> None:
    """Consume a valid and a corrupted fixture of each format."""
    assert SIVMONE is not None
    path = write_fixture(tmp_path, default_t8n, fixture_format, corrupt)
    consumer = CONSUMERS[fixture_format](binary=Path(SIVMONE))
    consumer.consume_fixture(fixture_format, path, "fixture_1")
    if corrupt:
        with pytest.raises(AssertionError, match="Test failed"):
            consumer.consume_fixture(fixture_format, path, "fixture_2")
    else:
        consumer.consume_fixture(fixture_format, path, "fixture_2")
