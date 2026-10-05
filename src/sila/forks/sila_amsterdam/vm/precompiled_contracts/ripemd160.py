"""
Sila Virtual Machine (Sivm) RIPEMD160 PRECOMPILED CONTRACT.

.. contents:: Table of Contents
    :backlinks: none
    :local:

Introduction
------------

Implementation of the `RIPEMD160` precompiled contract.
"""

import hashlib

from sila_types.numeric import Uint, ulen

from sila.utils.byte import left_pad_zero_bytes
from sila.utils.numeric import ceil32

from ...fork_types import ExecutionGas
from ...vm import Sivm
from ...vm.gas import (
    GasCosts,
    charge_gas,
)


def ripemd160(sivm: Sivm) -> None:
    """
    Writes the ripemd160 hash to output.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    data = sivm.call_data

    # GAS
    word_count = ceil32(ulen(data)) // Uint(32)
    charge_gas(
        sivm,
        ExecutionGas(
            GasCosts.PRECOMPILE_RIPEMD160_BASE
            + GasCosts.PRECOMPILE_RIPEMD160_PER_WORD * word_count
        ),
    )

    # OPERATION
    hash_bytes = hashlib.new("ripemd160", data).digest()
    padded_hash = left_pad_zero_bytes(hash_bytes, 32)
    sivm.output = padded_hash
