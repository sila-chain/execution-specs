"""Defines SIP-1153 specification constants and functions."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ReferenceSpec:
    """Defines the reference spec version and git path."""

    git_path: str
    version: str


ref_spec_1153 = ReferenceSpec(
    "SIPS/sip-1153.md", "1eb863b534a5a3e19e9c196ab2a7f3db4bb9da17"
)


class Spec:
    """
    Parameters from the SIP-1153 specifications as defined at
    https://sips.sila.org/SIPS/sip-1153.
    """

    TLOAD_OPCODE_BYTE = 0x5C
    TSTORE_OPCODE_BYTE = 0x5D
    TLOAD_GAS_COST = 100
    TSTORE_GAS_COST = 100
