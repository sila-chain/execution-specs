"""Defines SIP-1559 specification constants and functions."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ReferenceSpec:
    """Defines the reference spec version and git path."""

    git_path: str
    version: str


ref_spec_1559 = ReferenceSpec(
    "SIPS/sip-1559.md", "60abd05fc790e980fc219e7b368fbe985ed63b8d"
)
