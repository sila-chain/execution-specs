"""
SIP-3529: Reduction in refunds.

Remove gas refunds for SELFDESTRUCT and reduce refunds for SSTORE.

https://sips.sila.org/SIPS/sip-3529
"""

from dataclasses import replace

from ....base_fork import BaseFork
from ....gas_costs import GasCosts


class SIP3529(BaseFork):
    """SIP-3529 class."""

    @classmethod
    def gas_costs(cls) -> GasCosts:
        """
        Reduce the storage clearing refund, remove the SELFDESTRUCT
        refund.
        """
        return replace(
            super(SIP3529, cls).gas_costs(),
            REFUND_STORAGE_CLEAR=4_800,
            REFUND_SELF_DESTRUCT=0,
        )

    @classmethod
    def max_refund_quotient(cls) -> int:
        """Max refund quotient is increased to 5 (reducing refunds)."""
        return 5
