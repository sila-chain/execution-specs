"""Test fork range descriptor parsing from string."""

import pytest

from ..forks.forks import SilaOsaka, SilaPrague
from ..helpers import ForkRangeDescriptor


@pytest.mark.parametrize(
    "fork_range_descriptor_string,expected_fork_range_descriptor",
    [
        (
            ">=SilaOsaka",
            ForkRangeDescriptor(
                greater_equal=SilaOsaka,
                less_than=None,
            ),
        ),
        (
            ">= SilaPrague < SilaOsaka",
            ForkRangeDescriptor(
                greater_equal=SilaPrague,
                less_than=SilaOsaka,
            ),
        ),
    ],
)
def test_parsing_fork_range_descriptor_from_string(
    fork_range_descriptor_string: str,
    expected_fork_range_descriptor: ForkRangeDescriptor,
) -> None:
    """
    Test multiple strings used as fork range descriptors in
    sila-chain/sila-tests.
    """
    assert (
        ForkRangeDescriptor.model_validate(fork_range_descriptor_string)
        == expected_fork_range_descriptor
    )
