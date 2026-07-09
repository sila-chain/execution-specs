"""
SIP-198: Big integer modular exponentiation.

Precompile for modular exponentiation.

https://sips.sila.org/SIPS/sip-198
"""

from typing import List

from execution_testing.base_types import Address

from ....base_fork import BaseFork


class SIP198(BaseFork):
    """SIP-198 class."""

    @classmethod
    def precompiles(cls) -> List[Address]:
        """Add modular exponentiation precompile."""
        return [
            Address(5, label="MODEXP"),
        ] + super(SIP198, cls).precompiles()
