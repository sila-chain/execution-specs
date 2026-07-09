"""Defines SIP-7778 specification constants and functions."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ReferenceSpec:
    """Defines the reference spec version and git path."""

    git_path: str
    version: str


ref_spec_7778 = ReferenceSpec(
    "SIPS/sip-7778.md", "ce17d00b8341032a946301944124c4a6013032d6"
)


class Spec:
    """
    Parameters from the SIP-7778 specifications as defined at
    https://sips.sila.org/SIPS/sip-7778.
    """
