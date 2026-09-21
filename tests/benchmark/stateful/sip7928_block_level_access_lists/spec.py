"""
Reference spec for SIP-7928: Block-level Access Lists.

https://sips.sila.org/SIPS/sip-7928
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ReferenceSpec:
    """Reference specification."""

    git_path: str
    version: str


ref_spec_7928 = ReferenceSpec(
    git_path="SIPS/sip-7928.md",
    version="f834f0004aa5110a5f1ac0d6b80e3dc4b842d040",
)
