"""
SIP-197: Precompiled contracts for optimal ate pairing check on the
elliptic curve alt_bn128.

https://sips.sila.org/SIPS/sip-197
"""

from dataclasses import replace
from typing import List

from execution_testing.base_types import Address

from ....base_fork import BaseFork
from ....gas_costs import GasCosts


class SIP197(BaseFork):
    """SIP-197 class."""

    @classmethod
    def precompiles(cls) -> List[Address]:
        """Add BN254 pairing check precompile."""
        return [
            Address(8, label="BN254_PAIRING"),
        ] + super(SIP197, cls).precompiles()

    @classmethod
    def gas_costs(cls) -> GasCosts:
        """Set gas costs for BN254 pairing check."""
        return replace(
            super(SIP197, cls).gas_costs(),
            PRECOMPILE_ECPAIRING_BASE=100_000,
            PRECOMPILE_ECPAIRING_PER_POINT=80_000,
        )
