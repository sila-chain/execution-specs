"""
Sila Virtual Machine (Sivm) Environmental Instructions.

.. contents:: Table of Contents
    :backlinks: none
    :local:

Introduction
------------

Implementations of the Sivm environment related instructions.
"""

from sila_types.bytes import Bytes32
from sila_types.numeric import U256, Uint, ulen

from sila.state import EMPTY_ACCOUNT
from sila.utils.numeric import ceil32

from ...fork_types import ExecutionGas
from ...state_tracker import get_account, get_code
from ...utils.address import to_address_masked
from ...vm.memory import buffer_read, memory_write
from .. import Sivm
from ..exceptions import OutOfBoundsRead
from ..gas import (
    GasCosts,
    calculate_blob_gas_price,
    calculate_gas_extend_memory,
    charge_gas,
)
from ..stack import pop, push


def address(sivm: Sivm) -> None:
    """
    Pushes the address of the current executing account to the stack.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    pass

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_ADDRESS)

    # OPERATION
    push(sivm.stack, U256.from_be_bytes(sivm.current_target))

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def balance(sivm: Sivm) -> None:
    """
    Pushes the balance of the given account onto the stack.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    address = to_address_masked(pop(sivm.stack))

    # GAS
    if address in sivm.accessed_addresses:
        charge_gas(sivm, GasCosts.WARM_ACCESS)
    else:
        sivm.accessed_addresses.add(address)
        charge_gas(sivm, GasCosts.COLD_ACCOUNT_ACCESS)

    # OPERATION
    # Non-existent accounts default to EMPTY_ACCOUNT, which has balance 0.
    tx_state = sivm.tx_env.state
    balance = get_account(tx_state, address).balance

    push(sivm.stack, balance)

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def origin(sivm: Sivm) -> None:
    """
    Pushes the address of the original transaction sender to the stack.
    The origin address can only be an EOA.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    pass

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_ORIGIN)

    # OPERATION
    push(sivm.stack, U256.from_be_bytes(sivm.tx_env.origin))

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def caller(sivm: Sivm) -> None:
    """
    Pushes the address of the caller onto the stack.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    pass

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_CALLER)

    # OPERATION
    push(sivm.stack, U256.from_be_bytes(sivm.caller))

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def callvalue(sivm: Sivm) -> None:
    """
    Push the value (in wei) sent with the call onto the stack.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    pass

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_CALLVALUE)

    # OPERATION
    push(sivm.stack, sivm.value)

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def calldataload(sivm: Sivm) -> None:
    """
    Push a word (32 bytes) of the input data belonging to the current
    environment onto the stack.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    start_index = pop(sivm.stack)

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_CALLDATALOAD)

    # OPERATION
    value = buffer_read(sivm.call_data, start_index, U256(32))

    push(sivm.stack, U256.from_be_bytes(value))

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def calldatasize(sivm: Sivm) -> None:
    """
    Push the size of input data in current environment onto the stack.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    pass

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_CALLDATASIZE)

    # OPERATION
    push(sivm.stack, U256(len(sivm.call_data)))

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def calldatacopy(sivm: Sivm) -> None:
    """
    Copy a portion of the input data in current environment to memory.

    This will also expand the memory, in case that the memory is insufficient
    to store the data.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    memory_start_index = pop(sivm.stack)
    data_start_index = pop(sivm.stack)
    size = pop(sivm.stack)

    # GAS
    words = ceil32(Uint(size)) // Uint(32)
    copy_gas_cost = ExecutionGas(GasCosts.OPCODE_COPY_PER_WORD * words)
    extend_memory = calculate_gas_extend_memory(
        sivm.memory, [(memory_start_index, size)]
    )
    charge_gas(
        sivm,
        GasCosts.OPCODE_CALLDATACOPY_BASE + copy_gas_cost + extend_memory.cost,
    )

    # OPERATION
    sivm.memory += b"\x00" * extend_memory.expand_by
    value = buffer_read(sivm.call_data, data_start_index, size)
    memory_write(sivm.memory, memory_start_index, value)

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def codesize(sivm: Sivm) -> None:
    """
    Push the size of code running in current environment onto the stack.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    pass

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_CODESIZE)

    # OPERATION
    push(sivm.stack, U256(len(sivm.code)))

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def codecopy(sivm: Sivm) -> None:
    """
    Copy a portion of the code in current environment to memory.

    This will also expand the memory, in case that the memory is insufficient
    to store the data.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    memory_start_index = pop(sivm.stack)
    code_start_index = pop(sivm.stack)
    size = pop(sivm.stack)

    # GAS
    words = ceil32(Uint(size)) // Uint(32)
    copy_gas_cost = ExecutionGas(GasCosts.OPCODE_COPY_PER_WORD * words)
    extend_memory = calculate_gas_extend_memory(
        sivm.memory, [(memory_start_index, size)]
    )
    charge_gas(
        sivm,
        GasCosts.OPCODE_CODECOPY_BASE + copy_gas_cost + extend_memory.cost,
    )

    # OPERATION
    sivm.memory += b"\x00" * extend_memory.expand_by
    value = buffer_read(sivm.code, code_start_index, size)
    memory_write(sivm.memory, memory_start_index, value)

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def gasprice(sivm: Sivm) -> None:
    """
    Push the gas price used in current environment onto the stack.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    pass

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_GASPRICE)

    # OPERATION
    push(sivm.stack, U256(sivm.tx_env.effective_gas_price))

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def extcodesize(sivm: Sivm) -> None:
    """
    Push the code size of a given account onto the stack.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    address = to_address_masked(pop(sivm.stack))

    # GAS
    if address in sivm.accessed_addresses:
        access_gas_cost = GasCosts.WARM_ACCESS
    else:
        sivm.accessed_addresses.add(address)
        access_gas_cost = GasCosts.COLD_ACCOUNT_ACCESS
    access_gas_cost += GasCosts.WARM_ACCESS  # Code reading cost (SIP-8038)
    charge_gas(sivm, access_gas_cost)

    # OPERATION
    tx_state = sivm.tx_env.state
    code_hash = get_account(tx_state, address).code_hash
    code = get_code(tx_state, code_hash)

    codesize = U256(len(code))
    push(sivm.stack, codesize)

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def extcodecopy(sivm: Sivm) -> None:
    """
    Copy a portion of an account's code to memory.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    address = to_address_masked(pop(sivm.stack))
    memory_start_index = pop(sivm.stack)
    code_start_index = pop(sivm.stack)
    size = pop(sivm.stack)

    # GAS
    words = ceil32(Uint(size)) // Uint(32)
    copy_gas_cost = ExecutionGas(GasCosts.OPCODE_COPY_PER_WORD * words)
    extend_memory = calculate_gas_extend_memory(
        sivm.memory, [(memory_start_index, size)]
    )

    if address in sivm.accessed_addresses:
        access_gas_cost = GasCosts.WARM_ACCESS
    else:
        sivm.accessed_addresses.add(address)
        access_gas_cost = GasCosts.COLD_ACCOUNT_ACCESS
    access_gas_cost += GasCosts.WARM_ACCESS  # Code reading cost (SIP-8038)

    total_gas_cost = access_gas_cost + copy_gas_cost + extend_memory.cost

    charge_gas(sivm, total_gas_cost)

    # OPERATION
    sivm.memory += b"\x00" * extend_memory.expand_by
    tx_state = sivm.tx_env.state
    code_hash = get_account(tx_state, address).code_hash
    code = get_code(tx_state, code_hash)

    value = buffer_read(code, code_start_index, size)
    memory_write(sivm.memory, memory_start_index, value)

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def returndatasize(sivm: Sivm) -> None:
    """
    Pushes the size of the return data buffer onto the stack.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    pass

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_RETURNDATASIZE)

    # OPERATION
    push(sivm.stack, U256(len(sivm.return_data)))

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def returndatacopy(sivm: Sivm) -> None:
    """
    Copies data from the return data buffer to memory.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    memory_start_index = pop(sivm.stack)
    return_data_start_position = pop(sivm.stack)
    size = pop(sivm.stack)

    # GAS
    words = ceil32(Uint(size)) // Uint(32)
    copy_gas_cost = ExecutionGas(
        GasCosts.OPCODE_RETURNDATACOPY_PER_WORD * words
    )
    extend_memory = calculate_gas_extend_memory(
        sivm.memory, [(memory_start_index, size)]
    )
    charge_gas(
        sivm,
        GasCosts.OPCODE_RETURNDATACOPY_BASE
        + copy_gas_cost
        + extend_memory.cost,
    )
    if Uint(return_data_start_position) + Uint(size) > ulen(sivm.return_data):
        raise OutOfBoundsRead

    sivm.memory += b"\x00" * extend_memory.expand_by
    value = sivm.return_data[
        return_data_start_position : return_data_start_position + size
    ]
    memory_write(sivm.memory, memory_start_index, value)

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def extcodehash(sivm: Sivm) -> None:
    """
    Returns the keccak256 hash of a contract’s bytecode.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    address = to_address_masked(pop(sivm.stack))

    # GAS
    if address in sivm.accessed_addresses:
        access_gas_cost = GasCosts.WARM_ACCESS
    else:
        sivm.accessed_addresses.add(address)
        access_gas_cost = GasCosts.COLD_ACCOUNT_ACCESS

    charge_gas(sivm, access_gas_cost)

    # OPERATION
    tx_state = sivm.tx_env.state
    account = get_account(tx_state, address)

    if account == EMPTY_ACCOUNT:
        codehash = U256(0)
    else:
        codehash = U256.from_be_bytes(account.code_hash)

    push(sivm.stack, codehash)

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def self_balance(sivm: Sivm) -> None:
    """
    Pushes the balance of the current address to the stack.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    pass

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_SELFBALANCE)

    # OPERATION
    # Non-existent accounts default to EMPTY_ACCOUNT, which has balance 0.
    balance = get_account(sivm.tx_env.state, sivm.current_target).balance

    push(sivm.stack, balance)

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def base_fee(sivm: Sivm) -> None:
    """
    Pushes the base fee of the current block on to the stack.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    pass

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_BASEFEE)

    # OPERATION
    push(sivm.stack, U256(sivm.block_env.base_fee_per_gas))

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def blob_hash(sivm: Sivm) -> None:
    """
    Pushes the versioned hash at a particular index on to the stack.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    index = pop(sivm.stack)

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_BLOBHASH)

    # OPERATION
    if int(index) < len(sivm.tx_env.blob_versioned_hashes):
        blob_hash = sivm.tx_env.blob_versioned_hashes[index]
    else:
        blob_hash = Bytes32(b"\x00" * 32)
    push(sivm.stack, U256.from_be_bytes(blob_hash))

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def blob_base_fee(sivm: Sivm) -> None:
    """
    Pushes the blob base fee on to the stack.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    pass

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_BLOBBASEFEE)

    # OPERATION
    blob_base_fee = calculate_blob_gas_price(sivm.block_env.excess_blob_gas)
    push(sivm.stack, U256(blob_base_fee))

    # PROGRAM COUNTER
    sivm.pc += Uint(1)
