"""Reference spec for [SIP-8246](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-8246.md)."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ReferenceSpec:
    """Reference specification."""

    git_path: str
    version: str


ref_spec_8246 = ReferenceSpec(
    git_path="SIPS/sip-8246.md",
    version="8be64cf6a01350938b93332cf0062ab7a3166f23",
)
