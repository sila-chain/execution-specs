"""Defines SIP-1153 specification constants and functions."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ReferenceSpec:
    """Defines the reference spec version and git path."""

    git_path: str
    version: str


ref_spec_1153 = ReferenceSpec(
    "SIPS/sip-1153.md", "71af630706495decd26dec6ab63648cce0055da3"
)


class Spec:
    """
    Parameters from the SIP-1153 specifications as defined at
    https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-1153.md.
    """

    TLOAD_OPCODE_BYTE = 0x5C
    TSTORE_OPCODE_BYTE = 0x5D
    TLOAD_GAS_COST = 100
    TSTORE_GAS_COST = 100
