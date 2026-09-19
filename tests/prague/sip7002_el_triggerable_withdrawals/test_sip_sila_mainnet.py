"""
abstract: Crafted tests for sila-mainnet of [SIP-7002: Execution layer triggerable withdrawals](https://sips.sila.org/SIPS/sip-7002).
"""  # noqa: E501

from typing import List

import pytest
from execution_testing import (
    Alloc,
    Block,
    BlockchainTestFiller,
    SystemContractInteractionTransaction,
)

from .helpers import WithdrawalRequest
from .spec import ref_spec_7002

REFERENCE_SPEC_GIT_PATH = ref_spec_7002.git_path
REFERENCE_SPEC_VERSION = ref_spec_7002.version

pytestmark = [pytest.mark.valid_at("Prague"), getattr(pytest.mark, "sila-mainnet")]


@pytest.mark.parametrize(
    "system_contract_interactions_per_block",
    [
        pytest.param(
            [
                [
                    SystemContractInteractionTransaction(
                        requests=[
                            WithdrawalRequest(
                                validator_pubkey=0x01,
                                amount=0,
                            )
                        ],
                    ),
                ],
            ],
            id="single_withdrawal_request",
        ),
    ],
)
def test_sip_7002(
    blockchain_test: BlockchainTestFiller,
    pre: Alloc,
    blocks: List[Block],
) -> None:
    """Test making a withdrawal request."""
    blockchain_test(
        pre=pre,
        post={},
        blocks=blocks,
    )
