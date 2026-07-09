"""Defines SIP-7976 specification constants and functions."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ReferenceSpec:
    """Defines the reference spec version and git path."""

    git_path: str
    version: str


ref_spec_7976 = ReferenceSpec(
    "SIPS/sip-7976.md", "83d473b0504d316a06ce58ae581e7f03b5d54fe1"
)


# Constants
class Spec:
    """
    Parameters from the SIP-7976 specifications as defined at
    https://sips.sila.org/SIPS/sip-7976.
    """

    STANDARD_TOKEN_COST = 4
    TOTAL_COST_FLOOR_PER_TOKEN = 16
