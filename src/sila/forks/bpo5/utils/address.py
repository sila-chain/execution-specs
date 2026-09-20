"""
Hardfork Utility Functions For Addresses.

.. contents:: Table of Contents
    :backlinks: none
    :local:

Introduction
------------

Address specific functions used in this bpo5 version of
specification.
"""

import sila_rlp as rlp
from sila_types.bytes import Bytes, Bytes32
from sila_types.numeric import U256, Uint

from sila.crypto.hash import keccak256
from sila.state import Address
from sila.utils.byte import left_pad_zero_bytes


def to_address_masked(data: Uint | U256) -> Address:
    """
    Convert a Uint or U256 value to a valid address (20 bytes).

    Parameters
    ----------
    data :
        The numeric value to be converted to address.

    Returns
    -------
    address : `Address`
        The obtained address.

    """
    return Address(data.to_be_bytes32()[-20:])


def compute_contract_address(address: Address, nonce: Uint) -> Address:
    """
    Computes address of the new account that needs to be created.

    Parameters
    ----------
    address :
        The address of the account that wants to create the new account.
    nonce :
        The transaction count of the account that wants to create the new
        account.

    Returns
    -------
    address: `Address`
        The computed address of the new account.

    """
    computed_address = keccak256(rlp.encode([address, nonce]))
    canonical_address = computed_address[-20:]
    padded_address = left_pad_zero_bytes(canonical_address, 20)
    return Address(padded_address)


def compute_create2_contract_address(
    address: Address, salt: Bytes32, call_data: Bytes
) -> Address:
    """
    Computes address of the new account that needs to be created, which is
    based on the sender address, salt and the call data as well.

    Parameters
    ----------
    address :
        The address of the account that wants to create the new account.
    salt :
        Address generation salt.
    call_data :
        The code of the new account which is to be created.

    Returns
    -------
    address: `sila.forks.bpo5.fork_types.Address`
        The computed address of the new account.

    """
    preimage = b"\xff" + address + salt + keccak256(call_data)
    computed_address = keccak256(preimage)
    canonical_address = computed_address[-20:]
    padded_address = left_pad_zero_bytes(canonical_address, 20)

    return Address(padded_address)
