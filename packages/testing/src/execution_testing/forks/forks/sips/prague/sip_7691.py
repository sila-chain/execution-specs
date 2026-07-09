"""
SIP-7691: Blob throughput increase.

Increase the number of blobs to reach a new target and max of 6 and 9
blobs per block respectively.

https://sips.sila.org/SIPS/sip-7691
"""

from ....base_fork import BaseFork


class SIP7691(
    BaseFork,
    update_blob_constants={
        "MAX_BLOBS_PER_BLOCK": 9,
        "TARGET_BLOBS_PER_BLOCK": 6,
        "BLOB_BASE_FEE_UPDATE_FRACTION": 5007716,
    },
):
    """SIP-7691 class."""

    pass
