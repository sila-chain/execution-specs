"""Test that withdrawal amounts decode as 64-bit unsigned integers."""

import pytest
import sila_rlp as rlp
from sila_rlp.exceptions import SILA_RLPException as RLPException
from sila_types.numeric import U64, U256

from sila.forks.amsterdam.blocks import Withdrawal
from sila.state import Address


def test_decode_max_withdrawal_amount() -> None:
    """Round-trip a withdrawal with the largest valid amount."""
    withdrawal = Withdrawal(
        index=U64(0),
        validator_index=U64(0),
        address=Address(b"\x00" * 20),
        amount=U64(2**64 - 1),
    )
    encoded = rlp.encode(withdrawal)
    assert rlp.decode_to(Withdrawal, encoded) == withdrawal


def test_decode_oversized_withdrawal_amount() -> None:
    """Reject a withdrawal whose amount does not fit in 64 bits."""
    encoded = rlp.encode((U64(0), U64(0), Address(b"\x00" * 20), U256(2**64)))
    with pytest.raises(RLPException):
        rlp.decode_to(Withdrawal, encoded)
