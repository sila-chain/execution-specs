"""
Reference spec for SIP-7928: Block-level Access Lists.

https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-7928.md
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ReferenceSpec:
    """Reference specification."""

    git_path: str
    version: str


ref_spec_7928 = ReferenceSpec(
    git_path="SIPS/sip-7928.md",
    version="aef85acbe069f399d6edd4d46712a560af3872e4",
)
