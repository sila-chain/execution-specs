"""
SIP-155: Simple replay attack protection.

https://sips.sila.org/SIPS/sip-155
"""

from ....base_fork import BaseFork


class SIP155(BaseFork):
    """SIP-155 class."""

    @classmethod
    def supports_protected_txs(cls) -> bool:
        """
        Enables support for protected transactions.
        """
        return True
