"""
SIP-170: Contract code size limit.

https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-170.md
"""

from ....base_fork import BaseFork


class SIP170(BaseFork):
    """SIP-170 class."""

    @classmethod
    def max_code_size(cls) -> int:
        """Upper bound is introduced for max contract code size."""
        return 0x6000
