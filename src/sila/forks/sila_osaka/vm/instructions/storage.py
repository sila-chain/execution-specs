"""
Sila Virtual Machine (Sivm) Storage Instructions.

.. contents:: Table of Contents
    :backlinks: none
    :local:

Introduction
------------

Implementations of the Sivm storage related instructions.
"""

from sila_types.numeric import Uint

from ...state_tracker import (
    get_storage,
    get_storage_original,
    get_transient_storage,
    set_storage,
    set_transient_storage,
)
from .. import Sivm
from ..exceptions import OutOfGasError, WriteInStaticContext
from ..gas import (
    GasCosts,
    charge_gas,
)
from ..stack import pop, push


def sload(sivm: Sivm) -> None:
    """
    Loads to the stack, the value corresponding to a certain key from the
    storage of the current account.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    key = pop(sivm.stack).to_be_bytes32()

    # GAS
    if (sivm.message.current_target, key) in sivm.accessed_storage_keys:
        charge_gas(sivm, GasCosts.WARM_ACCESS)
    else:
        sivm.accessed_storage_keys.add((sivm.message.current_target, key))
        charge_gas(sivm, GasCosts.COLD_STORAGE_ACCESS)

    # OPERATION
    tx_state = sivm.message.tx_env.state
    value = get_storage(tx_state, sivm.message.current_target, key)

    push(sivm.stack, value)

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def sstore(sivm: Sivm) -> None:
    """
    Stores a value at a certain key in the current context's storage.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    key = pop(sivm.stack).to_be_bytes32()
    new_value = pop(sivm.stack)
    if sivm.gas_left <= GasCosts.CALL_STIPEND:
        raise OutOfGasError

    tx_state = sivm.message.tx_env.state
    original_value = get_storage_original(
        tx_state, sivm.message.current_target, key
    )
    current_value = get_storage(tx_state, sivm.message.current_target, key)

    gas_cost = Uint(0)

    if (sivm.message.current_target, key) not in sivm.accessed_storage_keys:
        sivm.accessed_storage_keys.add((sivm.message.current_target, key))
        gas_cost += GasCosts.COLD_STORAGE_ACCESS

    if original_value == current_value and current_value != new_value:
        if original_value == 0:
            gas_cost += GasCosts.STORAGE_SET
        else:
            gas_cost += (
                GasCosts.COLD_STORAGE_WRITE - GasCosts.COLD_STORAGE_ACCESS
            )
    else:
        gas_cost += GasCosts.WARM_ACCESS

    # Refund Counter Calculation
    if current_value != new_value:
        if original_value != 0 and current_value != 0 and new_value == 0:
            sivm.refund_counter += GasCosts.REFUND_STORAGE_CLEAR

        if original_value != 0 and current_value == 0:
            sivm.refund_counter -= GasCosts.REFUND_STORAGE_CLEAR

        if original_value == new_value:
            if original_value == 0:
                sivm.refund_counter += int(
                    GasCosts.STORAGE_SET - GasCosts.WARM_ACCESS
                )
            else:
                sivm.refund_counter += int(
                    GasCosts.COLD_STORAGE_WRITE
                    - GasCosts.COLD_STORAGE_ACCESS
                    - GasCosts.WARM_ACCESS
                )

    charge_gas(sivm, gas_cost)
    if sivm.message.is_static:
        raise WriteInStaticContext
    set_storage(tx_state, sivm.message.current_target, key, new_value)

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def tload(sivm: Sivm) -> None:
    """
    Loads to the stack, the value corresponding to a certain key from the
    transient storage of the current account.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    key = pop(sivm.stack).to_be_bytes32()

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_TLOAD)

    # OPERATION
    value = get_transient_storage(
        sivm.message.tx_env.state, sivm.message.current_target, key
    )
    push(sivm.stack, value)

    # PROGRAM COUNTER
    sivm.pc += Uint(1)


def tstore(sivm: Sivm) -> None:
    """
    Stores a value at a certain key in the current context's transient storage.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    # STACK
    key = pop(sivm.stack).to_be_bytes32()
    new_value = pop(sivm.stack)

    # GAS
    charge_gas(sivm, GasCosts.OPCODE_TSTORE)
    if sivm.message.is_static:
        raise WriteInStaticContext
    set_transient_storage(
        sivm.message.tx_env.state,
        sivm.message.current_target,
        key,
        new_value,
    )

    # PROGRAM COUNTER
    sivm.pc += Uint(1)
