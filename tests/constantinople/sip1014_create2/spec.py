"""Defines SIP-1014 specification constants and functions."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ReferenceSpec:
    """Defines the reference spec version and git path."""

    git_path: str
    version: str


ref_spec_1014 = ReferenceSpec(
    "SIPS/sip-1014.md", "12bc3939666bce5182f485e401fe915bde0c7ca3"
)


class Spec:
    """
    Parameters from the SIP-1014 specifications as defined at
    https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-1014.md.
    """
