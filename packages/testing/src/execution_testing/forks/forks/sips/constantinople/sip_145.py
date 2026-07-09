"""
SIP-145: Bitwise shifting instructions in EVM.

Add SHL, SHR, and SAR instructions to the EVM.

https://sips.sila.org/SIPS/sip-145
"""

from typing import Callable, Dict, List

from execution_testing.vm import OpcodeBase, Opcodes

from ....base_fork import BaseFork


class SIP145(BaseFork):
    """SIP-145 class."""

    @classmethod
    def opcode_gas_map(
        cls,
    ) -> Dict[OpcodeBase, int | Callable[[OpcodeBase], int]]:
        """Add SHL, SHR, and SAR opcode gas costs."""
        gas_costs = cls.gas_costs()
        base_map = super(SIP145, cls).opcode_gas_map()
        return {
            **base_map,
            Opcodes.SHL: gas_costs.VERY_LOW,
            Opcodes.SHR: gas_costs.VERY_LOW,
            Opcodes.SAR: gas_costs.VERY_LOW,
        }

    @classmethod
    def valid_opcodes(cls) -> List[Opcodes]:
        """Add SHL, SHR, and SAR to valid opcodes."""
        return [
            Opcodes.SHL,
            Opcodes.SHR,
            Opcodes.SAR,
        ] + super(SIP145, cls).valid_opcodes()
