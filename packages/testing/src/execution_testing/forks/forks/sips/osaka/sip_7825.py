"""
SIP-7825: Transaction gas limit cap.

Introduce a protocol-level cap on the maximum gas used by a transaction to
16,777,216 (2^24).

https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-7825.md
"""

from ....base_fork import BaseFork


class SIP7825(BaseFork):
    """SIP-7825 class."""

    @classmethod
    def transaction_gas_limit_cap(cls) -> int | None:
        """Transaction gas limit is capped at 16 million (2**24)."""
        return 16_777_216
