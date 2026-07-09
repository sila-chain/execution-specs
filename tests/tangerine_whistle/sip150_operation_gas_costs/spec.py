"""
[SIP-150: Operation Gas Costs](https://sips.sila.org/SIPS/sip-150)
introduced changes to the gas costs of certain EVM operations to mitigate DOS
attacks. This module contains tests that verify the correct implementation
of these gas cost changes in the Sila Virtual Machine (EVM).
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ReferenceSpec:
    """Defines the reference spec version and git path."""

    git_path: str
    version: str


ref_spec_150 = ReferenceSpec(
    "SIPS/sip-150.md", "34acf72522b989d86e76efcaf42eba4cdb0b31ad"
)
