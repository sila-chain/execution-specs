"""
SIP-1344: ChainID opcode.

Add a new opcode that returns the current chain's SIP-155 unique
identifier.

https://sips.sila.org/SIPS/sip-1344
"""

from typing import Callable, Dict, List

from execution_testing.vm import OpcodeBase, Opcodes

from ....base_fork import BaseFork


class SIP1344(BaseFork):
    """SIP-1344 class."""

    @classmethod
    def opcode_gas_map(
        cls,
    ) -> Dict[OpcodeBase, int | Callable[[OpcodeBase], int]]:
        """Add CHAINID opcode gas cost."""
        gas_costs = cls.gas_costs()
        base_map = super(SIP1344, cls).opcode_gas_map()
        return {**base_map, Opcodes.CHAINID: gas_costs.BASE}

    @classmethod
    def valid_opcodes(cls) -> List[Opcodes]:
        """Add CHAINID to valid opcodes."""
        return [Opcodes.CHAINID] + super(SIP1344, cls).valid_opcodes()
