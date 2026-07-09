"""
Common procedures to test
[SIP-7685: General purpose execution
layer requests](https://sips.sila.org/SIPS/sip-7685).
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ReferenceSpec:
    """Defines the reference spec version and git path."""

    git_path: str
    version: str


ref_spec_7685 = ReferenceSpec(
    "SIPS/sip-7685.md", "67ecb425d78f1d40c4f1cb957f3214afd0ece945"
)
