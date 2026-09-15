"""Reference spec for [SIP-7843: SLOTNUM](https://sips.sila.org/SIPS/sip-7843)."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ReferenceSpec:
    """Reference specification."""

    git_path: str
    version: str


ref_spec_7843 = ReferenceSpec(
    git_path="SIPS/sip-7843.md",
    version="c3bfd4ba41cf0fcbfe8c404f33ba89f5174971e0",
)
