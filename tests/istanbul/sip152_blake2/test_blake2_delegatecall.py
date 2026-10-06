"""
Test delegatecall to Blake2B Precompile before and after being added.
"""

import pytest
from execution_testing import (
    Account,
    Alloc,
    Fork,
    Op,
    StateTestFiller,
    Transaction,
)
from execution_testing.forks.forks.forks import SilaIstanbul

from .spec import Spec

REFERENCE_SPEC_GIT_PATH = "SIPS/sip-152.md"
REFERENCE_SPEC_VERSION = "2d29eb21229e23ee0a05bf2d0ec5e55dfb4691c1"


@pytest.mark.valid_from("SilaConstantinopleFix")
def test_blake2_precompile_delegatecall(
    state_test: StateTestFiller, pre: Alloc, fork: Fork
) -> None:
    """
    Test delegatecall consumes specified gas for the Blake2B precompile when it
    exists.
    """
    account = pre.deploy_contract(
        Op.SSTORE(
            0,
            Op.DELEGATECALL(
                gas=1,
                address=Spec.BLAKE2_PRECOMPILE_ADDRESS,
            ),
        )
        + Op.STOP,
        storage={0: 0xDEADBEEF},
    )

    tx = Transaction(to=account, sender=pre.fund_eoa())

    # If precompile exists, DELEGATECALL will fail, otherwise DELEGATECALL will
    # succeed
    post = {
        account: Account(
            storage={
                0: "0x00" if fork >= SilaIstanbul else "0x01",
            }
        )
    }

    state_test(pre=pre, post=post, tx=tx)
