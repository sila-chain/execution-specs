"""
SIP-1884: Repricing for trie-size-dependent opcodes.

Introduces SELFBALANCE opcode.

https://sips.sila.org/SIPS/sip-1884
"""

from typing import Callable, Dict, List

from execution_testing.vm import OpcodeBase, Opcodes

from ....base_fork import BaseFork


class SIP1884(BaseFork):
    """SIP-1884 class."""

    @classmethod
    def opcode_gas_map(
        cls,
    ) -> Dict[OpcodeBase, int | Callable[[OpcodeBase], int]]:
        """Add SELFBALANCE opcode gas cost."""
        gas_costs = cls.gas_costs()
        base_map = super(SIP1884, cls).opcode_gas_map()
        return {**base_map, Opcodes.SELFBALANCE: gas_costs.LOW}

    @classmethod
    def valid_opcodes(cls) -> List[Opcodes]:
        """Add SELFBALANCE to valid opcodes."""
        return [
            Opcodes.SELFBALANCE,
        ] + super(SIP1884, cls).valid_opcodes()
