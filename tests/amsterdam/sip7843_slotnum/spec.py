"""Reference spec for [SIP-7843: SLOTNUM](https://sips.sila.org/SIPS/sip-7843)."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ReferenceSpec:
    """Reference specification."""

    git_path: str
    version: str


ref_spec_7843 = ReferenceSpec(
    git_path="SIPS/sip-7843.md",
    version="6bc5d6b7acbc016a79fa573f98975093b5c2ca52",
)


class Spec:
    """Constants and parameters from SIP-7843."""
