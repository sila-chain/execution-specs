"""Defines SIP-7623 specification constants and functions."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ReferenceSpec:
    """Defines the reference spec version and git path."""

    git_path: str
    version: str


ref_spec_7623 = ReferenceSpec(
    "SIPS/sip-7623.md", "744f2075ba5deee9c1040eb089104d55bd89960d"
)


# Constants
class Spec:
    """
    Parameters from the SIP-7623 specifications as defined at
    https://sips.sila.org/SIPS/sip-7623.
    """

    TX_DATA_TOKEN_STANDARD = 4
    TX_DATA_TOKEN_FLOOR = 10
