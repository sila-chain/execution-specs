"""Reference spec for [SIP-2780: Resource-based intrinsic transaction gas.](https://sips.sila.org/SIPS/sip-2780)."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ReferenceSpec:
    """Reference specification."""

    git_path: str
    version: str


ref_spec_2780 = ReferenceSpec(
    git_path="SIPS/sip-2780.md",
    version="7243c92ba812437c64bae9fc6524ee269b29daa9",
)
