"""
SIP-7594: SilaPeerDAS - Peer Data Availability Sampling.

Introducing simple DAS utilizing gossip distribution and peer requests.

https://sips.sila.org/SIPS/sip-7594
"""

from ....base_fork import BaseFork


class SIP7594(
    BaseFork,
    engine_get_payload_version_bump=True,
    engine_get_blobs_version_bump=True,
    update_blob_constants={
        "AMOUNT_CELL_PROOFS": 128,
        "MAX_BLOBS_PER_TX": 6,
    },
):
    """SIP-7594 class."""

    @classmethod
    def full_blob_tx_wrapper_version(cls) -> int | None:
        """Full blob transaction wrapper version is defined."""
        return 1
