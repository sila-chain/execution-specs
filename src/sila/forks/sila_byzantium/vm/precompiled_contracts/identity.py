"""
Sila Virtual Machine (Sivm) IDENTITY PRECOMPILED CONTRACT.

.. contents:: Table of Contents
    :backlinks: none
    :local:

Introduction
------------

Implementation of the `IDENTITY` precompiled contract.
"""

from sila_types.numeric import Uint, ulen

from sila.utils.numeric import ceil32

from ...vm import Sivm
from ...vm.gas import GasCosts, charge_gas


def identity(sivm: Sivm) -> None:
    """
    Writes the message data to output.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    data = sivm.message.data

    # GAS
    word_count = ceil32(ulen(data)) // Uint(32)
    charge_gas(
        sivm,
        GasCosts.PRECOMPILE_IDENTITY_BASE
        + GasCosts.PRECOMPILE_IDENTITY_PER_WORD * word_count,
    )

    # OPERATION
    sivm.output = data
