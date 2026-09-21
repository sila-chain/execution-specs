"""Defines SIP-7778 specification constants and functions."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ReferenceSpec:
    """Defines the reference spec version and git path."""

    git_path: str
    version: str


ref_spec_7778 = ReferenceSpec(
    "SIPS/sip-7778.md", "4897aec97160c72d2080acf928b132f2efc1a886"
)


class Spec:
    """
    Parameters from the SIP-7778 specifications as defined at
    https://sips.sila.org/SIPS/sip-7778.
    """
