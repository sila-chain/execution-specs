"""
SIP-649: Metropolis difficulty bomb delay and block reward reduction.

Delay the difficulty bomb and reduce the block reward to 3 SIL.

https://sips.sila.org/SIPS/sip-649
"""

from ....base_fork import BaseFork


class SIP649(BaseFork):
    """SIP-649 class."""

    @classmethod
    def get_reward(cls) -> int:
        """Block reward is reduced to 3 SIL."""
        return 3_000_000_000_000_000_000
