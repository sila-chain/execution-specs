"""Defines SIP-4895 specification constants and functions."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ReferenceSpec:
    """Defines the reference spec version and git path."""

    git_path: str
    version: str


ref_spec_4895 = ReferenceSpec(
    "SIPS/sip-4895.md", "714f24271ad7732dfe4cb7bcd4c0fd7391e6cfe1"
)
