"""Defines SIP-6110 specification constants and functions."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ReferenceSpec:
    """Defines the reference spec version and git path."""

    git_path: str
    version: str


ref_spec_6110 = ReferenceSpec(
    "SIPS/sip-6110.md", "cbe8bf6a28fa1d096f9756af3513675849c4158e"
)


class Spec:
    """
    Parameters from the SIP-6110 specifications as defined at
    https://sips.sila.org/SIPS/sip-6110.
    """

    DEPOSIT_CONTRACT_ADDRESS = (
        0x00000000219AB540356CBB839CBE05303D7705FA  # SilaMainnet
    )
    DEPOSIT_EVENT_SIGNATURE_HASH = (
        0x649BBC62D0E31342AFEA4E5CD82D4049E7E1EE912FC0889AA790803BE39038C5
    )
