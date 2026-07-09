"""
SIP-7843: SLOTNUM opcode.

Opcode to get the current slot number.

https://sips.sila.org/SIPS/sip-7843
"""

from typing import Callable, Dict, List

from execution_testing.vm import (
    OpcodeBase,
    Opcodes,
)

from ....base_fork import BaseFork


class SIP7843(
    BaseFork,
    # Engine API method version bumps
    # New field `slotNumber` in ExecutionPayload
    engine_new_payload_version_bump=True,
    engine_get_payload_version_bump=True,
    engine_forkchoice_updated_version_bump=True,
):
    """SIP-7843 class."""

    @classmethod
    def header_slot_number_required(cls) -> bool:
        """Slot number in header required."""
        return True

    @classmethod
    def engine_payload_attribute_slot_number(cls) -> bool:
        """Payload attributes include the slot number."""
        return True

    @classmethod
    def opcode_gas_map(
        cls,
    ) -> Dict[OpcodeBase, int | Callable[[OpcodeBase], int]]:
        """Add SLOTNUM opcode gas cost."""
        gas_costs = cls.gas_costs()
        base_map = super(SIP7843, cls).opcode_gas_map()
        return {
            **base_map,
            Opcodes.SLOTNUM: gas_costs.BASE,
        }

    @classmethod
    def valid_opcodes(cls) -> List[Opcodes]:
        """Add SLOTNUM opcode."""
        return [Opcodes.SLOTNUM] + super(SIP7843, cls).valid_opcodes()
