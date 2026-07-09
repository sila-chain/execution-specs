"""
SIP-7: DELEGATECALL.

A new opcode that is similar to CALLCODE but propagates the sender and
value from the parent scope.

https://sips.sila.org/SIPS/sip-7
"""

from typing import Callable, Dict, List

from execution_testing.vm import OpcodeBase, Opcodes

from ....base_fork import BaseFork


class SIP7(BaseFork):
    """SIP-7 class."""

    @classmethod
    def call_opcodes(cls) -> List[Opcodes]:
        """Add DELEGATECALL opcode."""
        return [Opcodes.DELEGATECALL] + super(SIP7, cls).call_opcodes()

    @classmethod
    def opcode_gas_map(
        cls,
    ) -> Dict[OpcodeBase, int | Callable[[OpcodeBase], int]]:
        """Add DELEGATECALL opcode gas cost."""
        gas_costs = cls.gas_costs()
        memory_expansion_calculator = cls.memory_expansion_gas_calculator()
        base_map = super(SIP7, cls).opcode_gas_map()
        return {
            **base_map,
            Opcodes.DELEGATECALL: cls._with_memory_expansion(
                lambda op: cls._calculate_call_gas(op, gas_costs),
                memory_expansion_calculator,
            ),
        }

    @classmethod
    def valid_opcodes(cls) -> List[Opcodes]:
        """Add DELEGATECALL to valid opcodes."""
        return [
            Opcodes.DELEGATECALL,
        ] + super(SIP7, cls).valid_opcodes()
