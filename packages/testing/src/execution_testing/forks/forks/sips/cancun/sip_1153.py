"""
SIP-1153: Transient storage opcodes.

Add opcodes for manipulating state that behaves identically to storage
but is discarded after every transaction.

https://sips.sila.org/SIPS/sip-1153
"""

from dataclasses import replace
from typing import Callable, Dict, List

from execution_testing.vm import OpcodeBase, Opcodes

from ....base_fork import BaseFork
from ....gas_costs import GasCosts


class SIP1153(BaseFork):
    """SIP-1153 class."""

    @classmethod
    def gas_costs(cls) -> GasCosts:
        """
        Set dedicated TLOAD and TSTORE gas costs. Transient storage is
        in-memory only; its cost matches a warm storage access at
        introduction but is independent of state-access pricing.
        """
        return replace(
            super(SIP1153, cls).gas_costs(),
            OPCODE_TLOAD=100,
            OPCODE_TSTORE=100,
        )

    @classmethod
    def opcode_gas_map(
        cls,
    ) -> Dict[OpcodeBase, int | Callable[[OpcodeBase], int]]:
        """Add TLOAD and TSTORE opcode gas costs."""
        gas_costs = cls.gas_costs()
        base_map = super(SIP1153, cls).opcode_gas_map()
        return {
            **base_map,
            Opcodes.TLOAD: gas_costs.OPCODE_TLOAD,
            Opcodes.TSTORE: gas_costs.OPCODE_TSTORE,
        }

    @classmethod
    def valid_opcodes(cls) -> List[Opcodes]:
        """Add TLOAD and TSTORE to valid opcodes."""
        return [
            Opcodes.TLOAD,
            Opcodes.TSTORE,
        ] + super(SIP1153, cls).valid_opcodes()
