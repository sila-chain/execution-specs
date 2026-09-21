"""Tests for scheduling the activating fork of a fork-transition fixture."""

from contextlib import ExitStack

from sila.fork_criteria import ByBlockNumber, ByTimestamp
from sila_spec_tools.loaders.fixture_loader import Load

from .helpers.load_blockchain_tests import BlockchainTestFixture


def test_schedule_fork_patches_the_fork_module_binding() -> None:
    """Patch the fork module's own `FORK_CRITERIA` binding and restore it."""
    load = Load("london")
    hardfork = load.fork.hardfork
    fork_module = hardfork.module("fork")
    sila_mainnet = hardfork.criteria
    criteria = ByBlockNumber(5)
    assert fork_module.FORK_CRITERIA == sila_mainnet

    with ExitStack() as stack:
        BlockchainTestFixture._schedule_fork(stack, load, criteria)
        assert hardfork.criteria == criteria
        assert fork_module.FORK_CRITERIA == criteria

    assert hardfork.criteria == sila_mainnet
    assert fork_module.FORK_CRITERIA == sila_mainnet


def test_schedule_fork_patches_the_package_without_module_binding() -> None:
    """Patch the fork package when the fork module does not bind the name."""
    load = Load("cancun")
    hardfork = load.fork.hardfork
    sila_mainnet = hardfork.criteria
    criteria = ByTimestamp(15_000)
    assert not hasattr(hardfork.module("fork"), "FORK_CRITERIA")

    with ExitStack() as stack:
        BlockchainTestFixture._schedule_fork(stack, load, criteria)
        assert hardfork.criteria == criteria
        assert not hasattr(hardfork.module("fork"), "FORK_CRITERIA")

    assert hardfork.criteria == sila_mainnet
