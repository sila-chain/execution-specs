"""
Sila Virtual Machine (Sivm) Blake2 PRECOMPILED CONTRACT.

.. contents:: Table of Contents
    :backlinks: none
    :local:

Introduction
------------

Implementation of the `Blake2` precompiled contract.
"""

from sila.crypto.blake2 import Blake2b

from ...vm import Sivm
from ...vm.gas import GasCosts, charge_gas
from ..exceptions import InvalidParameter


def blake2f(sivm: Sivm) -> None:
    """
    Writes the Blake2 hash to output.

    Parameters
    ----------
    sivm :
        The current Sivm frame.

    """
    data = sivm.message.data
    if len(data) != 213:
        raise InvalidParameter

    blake2b = Blake2b()
    rounds, h, m, t_0, t_1, f = blake2b.get_blake2_parameters(data)

    charge_gas(sivm, GasCosts.PRECOMPILE_BLAKE2F_PER_ROUND * rounds)
    if f not in [0, 1]:
        raise InvalidParameter

    sivm.output = blake2b.compress(rounds, h, m, t_0, t_1, f)
