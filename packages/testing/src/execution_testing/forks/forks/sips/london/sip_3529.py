"""
SIP-3529: Reduction in refunds.

Remove gas refunds for SELFDESTRUCT and reduce refunds for SSTORE.

https://sips.sila.org/SIPS/sip-3529
"""

from ....base_fork import BaseFork


class SIP3529(BaseFork):
    """SIP-3529 class."""

    @classmethod
    def max_refund_quotient(cls) -> int:
        """Max refund quotient is increased to 5 (reducing refunds)."""
        return 5
