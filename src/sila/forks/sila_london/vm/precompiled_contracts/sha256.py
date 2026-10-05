"""
Sila Virtual Machine (Sivm) SHA256 PRECOMPILED CONTRACT.

.. contents:: Table of Contents
    :backlinks: none
    :local:

Introduction
------------

Implementation of the `SHA256` precompiled contract.
"""

import hashlib

from sila_types.numeric import Uint, ulen

from sila.utils.numeric import ceil32

from ...vm import Sivm
from ...vm.gas import (
    GasCosts,
    charge_gas,
)


def sha256(sivm: Sivm) -> None:
    """
    Writes the sha256 hash to output.

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
        GasCosts.PRECOMPILE_SHA256_BASE
        + GasCosts.PRECOMPILE_SHA256_PER_WORD * word_count,
    )

    # OPERATION
    sivm.output = hashlib.sha256(data).digest()
