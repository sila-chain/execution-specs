"""
SIP-2028: Transaction data gas cost reduction.

Reduce the gas cost of non-zero transaction data bytes to 16.

https://sips.sila.org/SIPS/sip-2028
"""

from dataclasses import replace

from ....base_fork import BaseFork
from ....gas_costs import GasCosts


class SIP2028(BaseFork):
    """SIP-2028 class."""

    @classmethod
    def gas_costs(cls) -> GasCosts:
        """Reduce non-zero calldata byte gas cost to 16."""
        return replace(
            super(SIP2028, cls).gas_costs(),
            TX_DATA_PER_NON_ZERO=16,
        )
