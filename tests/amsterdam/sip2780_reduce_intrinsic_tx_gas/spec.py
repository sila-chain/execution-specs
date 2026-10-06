"""Reference spec for [SIP-2780: Resource-based intrinsic transaction gas.](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-2780.md)."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ReferenceSpec:
    """Reference specification."""

    git_path: str
    version: str


ref_spec_2780 = ReferenceSpec(
    git_path="SIPS/sip-2780.md",
    version="079952a5d3659197dfc87a6449957e46c0acf0fd",
)
