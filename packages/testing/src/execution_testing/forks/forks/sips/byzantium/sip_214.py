"""
SIP-214: New opcode STATICCALL.

https://sips.sila.org/SIPS/sip-214
"""

from typing import Callable, Dict, List

from execution_testing.vm import OpcodeBase, Opcodes

from ....base_fork import BaseFork


class SIP214(BaseFork):
    """SIP-214 class."""

    @classmethod
    def call_opcodes(cls) -> List[Opcodes]:
        """Add STATICCALL opcode."""
        return [
            Opcodes.STATICCALL,
        ] + super(SIP214, cls).call_opcodes()

    @classmethod
    def opcode_gas_map(
        cls,
    ) -> Dict[OpcodeBase, int | Callable[[OpcodeBase], int]]:
        """Add STATICCALL opcode gas cost."""
        gas_costs = cls.gas_costs()
        memory_expansion_calculator = cls.memory_expansion_gas_calculator()
        base_map = super(SIP214, cls).opcode_gas_map()
        return {
            **base_map,
            Opcodes.STATICCALL: cls._with_memory_expansion(
                lambda op: cls._calculate_call_gas(op, gas_costs),
                memory_expansion_calculator,
            ),
        }

    @classmethod
    def valid_opcodes(cls) -> List[Opcodes]:
        """Add STATICCALL to valid opcodes."""
        return [
            Opcodes.STATICCALL,
        ] + super(SIP214, cls).valid_opcodes()
