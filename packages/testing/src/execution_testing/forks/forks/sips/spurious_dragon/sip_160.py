"""
SIP-160: EXP cost increase.

Raise the per-byte charge for EXP's exponent operand from 10 to 50.

https://sips.sila.org/SIPS/sip-160
"""

from dataclasses import replace

from ....base_fork import BaseFork
from ....gas_costs import GasCosts


class SIP160(BaseFork):
    """SIP-160 class."""

    @classmethod
    def gas_costs(cls) -> GasCosts:
        """Raise the EXP per-exponent-byte gas cost to 50."""
        return replace(
            super(SIP160, cls).gas_costs(),
            OPCODE_EXP_PER_BYTE=50,
        )
