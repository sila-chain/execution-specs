"""Defines SIP-161 specification constants and functions."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ReferenceSpec:
    """Defines the reference spec version and git path."""

    git_path: str
    version: str


ref_spec_161 = ReferenceSpec(
    "SIPS/sip-161.md", "47e52a8d916af4ca6d5a0dbf8d8892b0f35eddcf"
)
