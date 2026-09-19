"""
abstract: Crafted tests for sila-mainnet of [SIP-6110: Supply validator deposits on chain](https://sips.sila.org/SIPS/sip-6110).
"""  # noqa: E501

from typing import List

import pytest
from execution_testing import (
    Alloc,
    Block,
    BlockchainTestFiller,
    SystemContractInteractionTransaction,
)

from .helpers import DepositRequest
from .spec import ref_spec_6110

REFERENCE_SPEC_GIT_PATH = ref_spec_6110.git_path
REFERENCE_SPEC_VERSION = ref_spec_6110.version

pytestmark = [pytest.mark.valid_at("Prague"), getattr(pytest.mark, "sila-mainnet")]


@pytest.mark.parametrize(
    "requests",
    [
        pytest.param(
            [
                SystemContractInteractionTransaction(
                    # TODO: Use a real public key to allow recovery of
                    #  the funds.
                    requests=[
                        DepositRequest(
                            pubkey=0x01,
                            withdrawal_credentials=0x02,
                            amount=1_000_000_000,
                            signature=0x03,
                            index=0x0,
                        )
                    ],
                ),
            ],
            id="single_deposit_from_eoa_minimum",
        ),
    ],
)
def test_sip_6110(
    blockchain_test: BlockchainTestFiller,
    pre: Alloc,
    blocks: List[Block],
) -> None:
    """Test making a deposit to the beacon chain deposit contract."""
    blockchain_test(
        pre=pre,
        post={},
        blocks=blocks,
    )
