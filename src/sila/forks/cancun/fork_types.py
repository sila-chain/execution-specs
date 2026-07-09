"""
Sila Types.

.. contents:: Table of Contents
    :backlinks: none
    :local:

Introduction
------------

Types reused throughout the specification, which are specific to Sila.
"""

from sila_rlp import rlp
from sila_types.bytes import Bytes, Bytes20, Bytes256

from sila.crypto.hash import Hash32
from sila.state import Account

Address = Bytes20

VersionedHash = Hash32

Root = Hash32

Bloom = Bytes256


def encode_account(raw_account_data: Account, storage_root: Bytes) -> Bytes:
    """
    Encode `Account` dataclass.

    Storage is not stored in the `Account` dataclass, so `Accounts` cannot be
    encoded without providing a storage root.
    """
    return rlp.encode(
        (
            raw_account_data.nonce,
            raw_account_data.balance,
            storage_root,
            raw_account_data.code_hash,
        )
    )
