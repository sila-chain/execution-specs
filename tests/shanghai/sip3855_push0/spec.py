"""Defines SIP-3855 specification constants and functions."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ReferenceSpec:
    """Defines the reference spec version and git path."""

    git_path: str
    version: str


ref_spec_3855 = ReferenceSpec(
    "SIPS/sip-3855.md", "4422eae1cdf9a3e3507e0c666579ae95e19dd0a0"
)
