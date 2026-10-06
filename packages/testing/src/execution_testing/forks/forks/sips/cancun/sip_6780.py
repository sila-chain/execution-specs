"""
SIP-6780: SELFDESTRUCT only in same transaction.

SELFDESTRUCT will recover all funds to the target but not delete the account,
except when called in the same transaction as creation.

https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-6780.md
"""

from ....base_fork import BaseFork


class SIP6780(BaseFork):
    """SIP-6780 class."""

    pass
