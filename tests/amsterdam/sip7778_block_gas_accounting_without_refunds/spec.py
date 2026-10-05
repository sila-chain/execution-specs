"""Defines SIP-7778 specification constants and functions."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ReferenceSpec:
    """Defines the reference spec version and git path."""

    git_path: str
    version: str


ref_spec_7778 = ReferenceSpec(
    "SIPS/sip-7778.md", "a713ae73a9f0fc3a70a311b26e987c9e2bba76f0"
)


class Spec:
    """
    Parameters from the SIP-7778 specifications as defined at
    https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-7778.md.
    """
