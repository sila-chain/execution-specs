"""Defines SIP-7981 specification constants and functions."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ReferenceSpec:
    """Defines the reference spec version and git path."""

    git_path: str
    version: str


ref_spec_7981 = ReferenceSpec(
    "SIPS/sip-7981.md", "747b78c0edfdf04e9e2933ad1bec592d3318e1d9"
)
