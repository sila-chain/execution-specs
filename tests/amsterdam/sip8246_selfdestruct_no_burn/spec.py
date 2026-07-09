"""Reference spec for [SIP-8246](https://sips.sila.org/SIPS/sip-8246)."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ReferenceSpec:
    """Reference specification."""

    git_path: str
    version: str


ref_spec_8246 = ReferenceSpec(
    git_path="SIPS/sip-8246.md",
    version="3b30ff829e5e698f1c6f69427111d194b80af38d",
)
