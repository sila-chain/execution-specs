"""
SIP-7951: Precompile for secp256r1 curve support.

Add precompiled contract for secp256r1 ECDSA signature verification with proper
security checks.

https://sips.sila.org/SIPS/sip-7951
"""

from dataclasses import replace
from typing import List

from execution_testing.base_types import Address

from ....base_fork import BaseFork
from ....gas_costs import GasCosts


class SIP7951(BaseFork):
    """SIP-7951 class."""

    @classmethod
    def precompiles(cls) -> List[Address]:
        """
        Add a precompile for P256 signature verification.

        P256VERIFY = 0x100
        """
        return [
            Address(0x100, label="P256VERIFY"),
        ] + super(SIP7951, cls).precompiles()

    @classmethod
    def gas_costs(cls) -> GasCosts:
        """Set the P256VERIFY precompile gas cost."""
        return replace(
            super(SIP7951, cls).gas_costs(),
            PRECOMPILE_P256VERIFY=6_900,
        )
