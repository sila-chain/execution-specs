"""Defines SIP-211 specification reference."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ReferenceSpec:
    """Defines the reference spec version and git path."""

    git_path: str
    version: str


ref_spec_211 = ReferenceSpec(
    git_path="SIPS/sip-211.md",
    version="N/A",
)
