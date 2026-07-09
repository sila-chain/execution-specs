"""Defines SIP-1014 specification constants and functions."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ReferenceSpec:
    """Defines the reference spec version and git path."""

    git_path: str
    version: str


ref_spec_1014 = ReferenceSpec(
    "SIPS/sip-1014.md", "31d4d62ec1dfc9f2bb26ca648f05d4cc2f47da09"
)


class Spec:
    """
    Parameters from the SIP-1014 specifications as defined at
    https://sips.sila.org/SIPS/sip-1014.
    """
