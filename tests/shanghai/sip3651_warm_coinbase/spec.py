"""Defines SIP-3651 specification constants and functions."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ReferenceSpec:
    """Defines the reference spec version and git path."""

    git_path: str
    version: str


ref_spec_3651 = ReferenceSpec(
    "SIPS/sip-3651.md", "a0bd488b6a08b5679d7ed87f2fd5a0edf3832a89"
)
