"""Defines SIP-214 specification reference."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ReferenceSpec:
    """Defines the reference spec version and git path."""

    git_path: str
    version: str


ref_spec_214 = ReferenceSpec(
    git_path="SIPS/sip-214.md",
    version="d3eae087ab7a6bd3690b4e3be2bd0301879f8f79",
)
