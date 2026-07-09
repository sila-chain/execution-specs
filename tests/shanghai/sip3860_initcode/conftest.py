"""Fixtures for the SIP-3860 initcode tests."""

import pytest
from execution_testing import Alloc


@pytest.fixture
def post() -> Alloc:
    """Post state fixture."""
    return Alloc()
