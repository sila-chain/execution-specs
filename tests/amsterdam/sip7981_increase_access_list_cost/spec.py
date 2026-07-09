"""Defines SIP-7981 specification constants and functions."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ReferenceSpec:
    """Defines the reference spec version and git path."""

    git_path: str
    version: str


ref_spec_7981 = ReferenceSpec(
    "SIPS/sip-7981.md", "954963fb6315dffadd9c40d48e4dae313e20cff5"
)


# Constants
class Spec:
    """
    Parameters from the SIP-7981 specifications as defined at
    https://sips.sila.org/SIPS/sip-7981.
    """

    ACCESS_LIST_ADDRESS_COST = 2400
    ACCESS_LIST_STORAGE_KEY_COST = 1900
