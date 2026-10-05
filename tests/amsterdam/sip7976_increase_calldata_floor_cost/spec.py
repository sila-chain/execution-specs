"""Defines SIP-7976 specification constants and functions."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ReferenceSpec:
    """Defines the reference spec version and git path."""

    git_path: str
    version: str


ref_spec_7976 = ReferenceSpec(
    "SIPS/sip-7976.md", "6ef30f528b700398ef1b878b93463fff9ecc728c"
)


# Constants
class Spec:
    """
    Parameters from the SIP-7976 specifications as defined at
    https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-7976.md.
    """

    STANDARD_TOKEN_COST = 4
    TOTAL_COST_FLOOR_PER_TOKEN = 16
