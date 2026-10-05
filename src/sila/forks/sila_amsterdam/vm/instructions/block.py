"""
Sila Virtual Machine (Sivm) Block Instructions.

.. contents:: Table of Contents
    :backlinks: none
    :local:

Introduction
------------

Implementations of the Sivm block instructions.
"""

from sila_types.numeric import U256, Uint

from .. import Sivm
from ..gas import GasCosts, charge_gas
from ..stack import pop, push


def block_hash(sivm: Sivm) -> None:
    """
    Push the hash of one of the 256 most recent complete blocks onto the
    stack. The block number to hash is present at the top of the stack.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    Raises
    ------
    :py:class:`~sila.forks.sila_amsterdam.vm.exceptions.StackUnderflowError`
        If `len(stack)` is less than `1`.
    :py:class:`~sila.forks.sila_amsterdam.vm.exceptions.OutOfGasError`
        If `sivm.gas_left` is less than `20`.

    """
    # STACK
    block_number = Uint(pop(sivm.stack))

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_BLOCKHASH)

    # OPERATION
    max_block_number = block_number + Uint(256)
    current_block_number = sivm.block_env.number
    if (
        current_block_number <= block_number
        or current_block_number > max_block_number
    ):
        # Default hash to 0, if the block of interest is not yet on the chain
        # (including the block which has the current executing transaction),
        # or if the block's age is more than 256.
        current_block_hash = b"\x00"
    else:
        current_block_hash = sivm.block_env.block_hashes[
            -(current_block_number - block_number)
        ]

    push(sivm.stack, U256.from_be_bytes(current_block_hash))

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def coinbase(sivm: Sivm) -> None:
    """
    Push the current block's beneficiary address (address of the block miner)
    onto the stack.

    Here the current block refers to the block in which the currently
    executing transaction/call resides.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    Raises
    ------
    :py:class:`~sila.forks.sila_amsterdam.vm.exceptions.StackOverflowError`
        If `len(stack)` is equal to `1024`.
    :py:class:`~sila.forks.sila_amsterdam.vm.exceptions.OutOfGasError`
        If `sivm.gas_left` is less than `2`.

    """
    # STACK
    pass

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_COINBASE)

    # OPERATION
    push(sivm.stack, U256.from_be_bytes(sivm.block_env.coinbase))

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def timestamp(sivm: Sivm) -> None:
    """
    Push the current block's timestamp onto the stack. Here the timestamp
    being referred to is actually the unix timestamp in seconds.

    Here the current block refers to the block in which the currently
    executing transaction/call resides.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    Raises
    ------
    :py:class:`~sila.forks.sila_amsterdam.vm.exceptions.StackOverflowError`
        If `len(stack)` is equal to `1024`.
    :py:class:`~sila.forks.sila_amsterdam.vm.exceptions.OutOfGasError`
        If `sivm.gas_left` is less than `2`.

    """
    # STACK
    pass

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_TIMESTAMP)

    # OPERATION
    push(sivm.stack, sivm.block_env.time)

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def number(sivm: Sivm) -> None:
    """
    Push the current block's number onto the stack.

    Here the current block refers to the block in which the currently
    executing transaction/call resides.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    Raises
    ------
    :py:class:`~sila.forks.sila_amsterdam.vm.exceptions.StackOverflowError`
        If `len(stack)` is equal to `1024`.
    :py:class:`~sila.forks.sila_amsterdam.vm.exceptions.OutOfGasError`
        If `sivm.gas_left` is less than `2`.

    """
    # STACK
    pass

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_NUMBER)

    # OPERATION
    push(sivm.stack, U256(sivm.block_env.number))

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def prev_randao(sivm: Sivm) -> None:
    """
    Push the `prev_randao` value onto the stack.

    The `prev_randao` value is the random output of the beacon chain's
    randomness oracle for the previous block.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    Raises
    ------
    :py:class:`~sila.forks.sila_amsterdam.vm.exceptions.StackOverflowError`
        If `len(stack)` is equal to `1024`.
    :py:class:`~sila.forks.sila_amsterdam.vm.exceptions.OutOfGasError`
        If `sivm.gas_left` is less than `2`.

    """
    # STACK
    pass

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_PREVRANDAO)

    # OPERATION
    push(sivm.stack, U256.from_be_bytes(sivm.block_env.prev_randao))

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def gas_limit(sivm: Sivm) -> None:
    """
    Push the current block's gas limit onto the stack.

    Here the current block refers to the block in which the currently
    executing transaction/call resides.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    Raises
    ------
    :py:class:`~sila.forks.sila_amsterdam.vm.exceptions.StackOverflowError`
        If `len(stack)` is equal to `1024`.
    :py:class:`~sila.forks.sila_amsterdam.vm.exceptions.OutOfGasError`
        If `sivm.gas_left` is less than `2`.

    """
    # STACK
    pass

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_GASLIMIT)

    # OPERATION
    push(sivm.stack, U256(sivm.block_env.block_gas_limit))

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def chain_id(sivm: Sivm) -> None:
    """
    Push the chain id onto the stack.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    Raises
    ------
    :py:class:`~sila.forks.sila_amsterdam.vm.exceptions.StackOverflowError`
        If `len(stack)` is equal to `1024`.
    :py:class:`~sila.forks.sila_amsterdam.vm.exceptions.OutOfGasError`
        If `sivm.gas_left` is less than `2`.

    """
    # STACK
    pass

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_CHAINID)

    # OPERATION
    push(sivm.stack, U256(sivm.block_env.chain_id))

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def slot_number(sivm: Sivm) -> None:
    """
    Push the current slot number onto the stack.

    The slot number is provided by the consensus layer and passed to the
    execution layer through the engine API.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    Raises
    ------
    :py:class:`~sila.forks.sila_amsterdam.vm.exceptions.StackOverflowError`
        If `len(stack)` is equal to `1024`.
    :py:class:`~sila.forks.sila_amsterdam.vm.exceptions.OutOfGasError`
        If `sivm.gas_left` is less than `2`.

    """
    # STACK
    pass

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_SLOTNUM)

    # OPERATION
    push(sivm.stack, U256(sivm.block_env.slot_number))

    # PROGRAM COUNTER
    sivm.pc += Uint(1)
