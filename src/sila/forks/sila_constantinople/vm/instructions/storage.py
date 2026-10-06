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

from ...state_tracker import get_storage, set_storage
from .. import Sivm
from ..exceptions import WriteInStaticContext
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
    charge_gas(sivm, GasCosts.SLOAD)

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

    # GAS
    tx_state = sivm.message.tx_env.state
    current_value = get_storage(tx_state, sivm.message.current_target, key)
    if new_value != 0 and current_value == 0:
        gas_cost = GasCosts.STORAGE_SET
    else:
        gas_cost = GasCosts.COLD_STORAGE_WRITE

    if new_value == 0 and current_value != 0:
        sivm.refund_counter += GasCosts.REFUND_STORAGE_CLEAR

    charge_gas(sivm, gas_cost)
    if sivm.message.is_static:
        raise WriteInStaticContext
    set_storage(tx_state, sivm.message.current_target, key, new_value)

    # PROGRAM COUNTER
    sivm.pc += Uint(1)
