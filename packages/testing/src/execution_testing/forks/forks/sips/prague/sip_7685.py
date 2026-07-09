"""
SIP-7685: General purpose execution layer requests.

A general purpose bus for sharing EL triggered requests with the CL.

https://sips.sila.org/SIPS/sip-7685
"""

from ....base_fork import BaseFork


class SIP7685(
    BaseFork,
    engine_new_payload_version_bump=True,
    engine_get_payload_version_bump=True,
):
    """SIP-7685 class."""

    @classmethod
    def max_request_type(cls) -> int:
        """
        Three request types are introduced: deposits, withdrawal requests,
        and consolidation requests.
        """
        return 2

    @classmethod
    def header_requests_required(cls) -> bool:
        """
        Header must contain the beacon chain requests hash.
        """
        return True

    @classmethod
    def engine_new_payload_requests(cls) -> bool:
        """
        New payloads include the requests hash as a parameter.
        """
        return True
