"""
SIP-7934: RLP encoded block size limit.

Introduce a protocol-level cap on the maximum RLP-encoded block size to 10 MiB,
including a 2 MiB margin for beacon block size.

https://sips.sila.org/SIPS/sip-7934
"""

from ....base_fork import BaseFork


class SIP7934(BaseFork):
    """SIP-7934 class."""

    @classmethod
    def block_rlp_size_limit(cls) -> int | None:
        """Block RLP size is limited."""
        max_block_size = 10_485_760
        safety_margin = 2_097_152
        return max_block_size - safety_margin
