"""Defines SIP-3860 specification constants and functions."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ReferenceSpec:
    """Defines the reference spec version and git path."""

    git_path: str
    version: str


ref_spec_3860 = ReferenceSpec(
    "SIPS/sip-3860.md", "28ad71002098c35fd4dce811c142b668ab8759bc"
)


class Spec:
    """
    Define parameters from the SIP-3860 specifications.

    These are the parameters defined at
    https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-3860.md#parameters.
    """

    MAX_INITCODE_SIZE = 49152
    INITCODE_WORD_COST = 2
