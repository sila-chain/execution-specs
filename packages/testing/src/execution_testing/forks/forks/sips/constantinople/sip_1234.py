"""
SIP-1234: Constantinople difficulty bomb delay and block reward adjustment.

Delay the difficulty bomb and reduce the block reward to 2 SIL.

https://sips.sila.org/SIPS/sip-1234
"""

from ....base_fork import BaseFork


class SIP1234(BaseFork):
    """SIP-1234 class."""

    @classmethod
    def get_reward(cls) -> int:
        """Block reward is reduced to 2 SIL."""
        return 2_000_000_000_000_000_000
