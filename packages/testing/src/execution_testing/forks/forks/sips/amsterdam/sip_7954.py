"""
SIP-7954: Increase Maximum Contract Size.

Raise the maximum contract code size from 24KiB to 64KiB and initcode size from
48KiB to 128KiB.

https://sips.sila.org/SIPS/sip-7954
"""

from ....base_fork import BaseFork


class SIP7954(BaseFork):
    """SIP-7954 class."""

    @classmethod
    def max_code_size(cls) -> int:
        """Max contract code size is 64 KiB."""
        return 64 * 1024

    @classmethod
    def max_initcode_size(cls) -> int:
        """Max initcode size is 128 KiB."""
        return 128 * 1024
