"""
SIP-3198: BASEFEE opcode.

Add an opcode that returns the value of the base fee of the current
block.

https://sips.sila.org/SIPS/sip-3198
"""

from typing import Callable, Dict, List

from execution_testing.vm import OpcodeBase, Opcodes

from ....base_fork import BaseFork


class SIP3198(BaseFork):
    """SIP-3198 class."""

    @classmethod
    def opcode_gas_map(
        cls,
    ) -> Dict[OpcodeBase, int | Callable[[OpcodeBase], int]]:
        """Add BASEFEE opcode gas cost."""
        gas_costs = cls.gas_costs()
        base_map = super(SIP3198, cls).opcode_gas_map()
        return {**base_map, Opcodes.BASEFEE: gas_costs.BASE}

    @classmethod
    def valid_opcodes(cls) -> List[Opcodes]:
        """Add BASEFEE to valid opcodes."""
        return [Opcodes.BASEFEE] + super(SIP3198, cls).valid_opcodes()
