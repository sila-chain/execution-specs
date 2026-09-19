"""
abstract: Crafted tests for sila-mainnet of [SIP-7251: Increase the MAX_EFFECTIVE_BALANCE](https://sips.sila.org/SIPS/sip-7251).
"""  # noqa: E501

from typing import List

import pytest
from execution_testing import (
    Alloc,
    Block,
    BlockchainTestFiller,
    SystemContractInteractionTransaction,
)

from .helpers import ConsolidationRequest
from .spec import ref_spec_7251

REFERENCE_SPEC_GIT_PATH = ref_spec_7251.git_path
REFERENCE_SPEC_VERSION = ref_spec_7251.version

pytestmark = [pytest.mark.valid_at("Prague"), getattr(pytest.mark, "sila-mainnet")]


@pytest.mark.parametrize(
    "system_contract_interactions_per_block",
    [
        pytest.param(
            [
                [
                    SystemContractInteractionTransaction(
                        requests=[
                            ConsolidationRequest(
                                source_pubkey=0x01,
                                target_pubkey=0x02,
                            )
                        ],
                    ),
                ],
            ],
            id="single_consolidation_request",
        ),
    ],
)
def test_sip_7251(
    blockchain_test: BlockchainTestFiller,
    blocks: List[Block],
    pre: Alloc,
) -> None:
    """Test making a consolidation request."""
    blockchain_test(
        pre=pre,
        post={},
        blocks=blocks,
    )
