"""Defines SIP-7981 specification constants and functions."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ReferenceSpec:
    """Defines the reference spec version and git path."""

    git_path: str
    version: str


ref_spec_7981 = ReferenceSpec(
    "SIPS/sip-7981.md", "dd1d024560b702833ba5c67e37f5a04712e476dc"
)
