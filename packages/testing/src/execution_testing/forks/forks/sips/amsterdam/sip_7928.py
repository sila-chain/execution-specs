"""
SIP-7928: Block-Level Access Lists.

Enforced block access lists with state locations and post-transaction state
diffs.

https://sips.sila.org/SIPS/sip-7928
"""

from dataclasses import replace

from ....base_fork import BaseFork
from ....gas_costs import GasCosts


class SIP7928(
    BaseFork,
    # Engine API method version bumps
    # New field `blockAccessList` in ExecutionPayload
    engine_new_payload_version_bump=True,
    engine_get_payload_version_bump=True,
):
    """SIP-7928 class."""

    @classmethod
    def header_bal_hash_required(cls) -> bool:
        """
        Header must contain block access list hash (SIP-7928).
        """
        return True

    @classmethod
    def gas_costs(cls) -> GasCosts:
        """
        The cost per block access list item is introduced in SIP-7928.
        """
        return replace(
            super(SIP7928, cls).gas_costs(),
            BLOCK_ACCESS_LIST_ITEM=2000,
        )

    @classmethod
    def engine_execution_payload_block_access_list(cls) -> bool:
        """
        From SIP-7928, engine execution payload includes `block_access_list`
        as a parameter.
        """
        return True
