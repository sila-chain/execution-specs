"""
SIP-4895: Beacon chain push withdrawals as operations.

Support validator withdrawals from the beacon chain to the EVM via a new
"system-level" operation type.

https://sips.sila.org/SIPS/sip-4895
"""

from ....base_fork import BaseFork


class SIP4895(
    BaseFork,
    engine_new_payload_version_bump=True,
    engine_forkchoice_updated_version_bump=True,
    engine_get_payload_version_bump=True,
):
    """SIP-4895 class."""

    @classmethod
    def header_withdrawals_required(cls) -> bool:
        """Withdrawals are required."""
        return True
