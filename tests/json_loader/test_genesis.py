"""Tests for genesis block creation."""

import pytest
from sila_rlp import rlp
from sila_types.numeric import U64

from sila.crypto.hash import keccak256
from sila.forks.frontier.blocks import Block, Header
from sila.forks.frontier.fork import BlockChain
from sila.forks.frontier.fork_types import Account, Bloom
from sila.forks.frontier.utils.hexadecimal import hex_to_address
from sila.genesis import (
    GenesisFork,
    add_genesis_block,
    get_genesis_configuration,
)
from sila.merkle_patricia_trie import Trie, root
from sila.state import (
    Address,
    State,
    set_account,
    set_storage,
    state_root,
    store_code,
)
from sila.utils.hexadecimal import hex_to_hash
from sila_spec_tools.forks import Hardfork

SILA_MAINNET_GENESIS_CONFIGURATION = get_genesis_configuration("sila-mainnet.json")


def test_frontier_block_hash() -> None:
    """
    Tests that the frontier genesis block hash matches the expected
    sila-mainnet hash.
    """
    description: GenesisFork[
        Address, Account, State, Trie, Bloom, Header, Block
    ] = GenesisFork(
        Address=Address,
        Account=Account,
        Trie=Trie,
        Bloom=Bloom,
        Header=Header,
        Block=Block,
        set_account=set_account,
        set_storage=set_storage,
        state_root=state_root,
        root=root,
        hex_to_address=hex_to_address,
        store_code=store_code,
    )

    chain = BlockChain([], State(), U64(1))
    add_genesis_block(description, chain, SILA_MAINNET_GENESIS_CONFIGURATION)

    assert keccak256(rlp.encode(chain.blocks[0].header)) == hex_to_hash(
        "0xd4e56740f876aef8c010b86a40d5f56745a118d0906a34e69aec8c0db1cb8fa3"
    )


def fork_name(fork: Hardfork) -> str:
    """Returns the short name of a hardfork for test identification."""
    return fork.short_name


@pytest.mark.parametrize("fork", Hardfork.discover(), ids=fork_name)
def test_genesis(fork: Hardfork) -> None:
    """Tests genesis block creation for all hardforks."""
    # TODO: remove once the changes have been back-ported
    from sila.merkle_patricia_trie import Trie
    from sila.state import (
        Address,
        State,
        root,
        set_account,
        set_storage,
        state_root,
        store_code,
    )

    try:
        _trie = fork.module("trie").Trie
        _set_account = fork.module("state").set_account
        _set_storage = fork.module("state").set_storage
        _state_root = fork.module("state").state_root
        _root = fork.module("trie").root
        _store_code = fork.module("state").store_code
        state = fork.module("state").State()
    except ModuleNotFoundError:
        _trie = Trie
        _set_account = set_account
        _set_storage = set_storage
        _state_root = state_root
        _root = root
        _store_code = store_code
        state = State()

    description: GenesisFork = GenesisFork(
        Address=Address,
        Account=fork.module("fork_types").Account,
        Trie=_trie,
        Bloom=fork.module("fork_types").Bloom,
        Header=fork.module("blocks").Header,
        Block=fork.module("blocks").Block,
        set_account=_set_account,
        set_storage=_set_storage,
        state_root=_state_root,
        root=_root,
        hex_to_address=fork.module("utils.hexadecimal").hex_to_address,
        store_code=_store_code,
    )

    chain = fork.module("fork").BlockChain([], state, U64(1))
    add_genesis_block(description, chain, SILA_MAINNET_GENESIS_CONFIGURATION)

    assert len(chain.blocks) == 1
