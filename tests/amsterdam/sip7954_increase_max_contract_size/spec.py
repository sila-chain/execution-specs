"""Reference spec for [SIP-7954: Increase Maximum Contract Size](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-7954.md)."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ReferenceSpec:
    """Reference specification."""

    git_path: str
    version: str


ref_spec_7954 = ReferenceSpec(
    git_path="SIPS/sip-7954.md",
    version="54653e12f68f36ed9bb8253699a5f3a48a12c4c8",
)
