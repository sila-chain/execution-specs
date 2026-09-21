"""Defines SIP-2681 specification constants and functions."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ReferenceSpec:
    """Defines the reference spec version and git path."""

    git_path: str
    version: str


# SIP-2681 reference specification
ref_spec_2681 = ReferenceSpec(
    "SIPS/sip-2681.md", "9e393a79d9937f579acbdcb234a67869259d5a96"
)


class Spec:
    """Constants for the SIP-2681 account nonce limit tests."""

    max_nonce = 2**64 - 1
