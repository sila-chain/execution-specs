"""Reference spec for [SIP-2780: Resource-based intrinsic transaction gas.](https://sips.sila.org/SIPS/sip-2780)."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ReferenceSpec:
    """Reference specification."""

    git_path: str
    version: str


ref_spec_2780 = ReferenceSpec(
    git_path="SIPS/sip-2780.md",
    version="992074053f12f24fed9e6d6bf6099d3a44707dca",
)
