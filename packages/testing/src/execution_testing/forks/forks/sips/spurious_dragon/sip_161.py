"""
SIP-161: State trie clearing (invariant-preserving alternative).

https://sips.sila.org/SIPS/sip-161
"""

from execution_testing.vm import OpcodeBase

from ....base_fork import BaseFork, GasCosts


class SIP161(BaseFork):
    """SIP-161 class."""

    @classmethod
    def _calculate_call_gas(
        cls, opcode: OpcodeBase, gas_costs: GasCosts
    ) -> int:
        """
        Couple the new account charge to a value transfer, per the dead
        account rules. The charge itself applies from Frontier.
        """
        metadata = opcode.metadata
        if "value_transfer" in metadata:
            if metadata["account_new"] and not metadata["value_transfer"]:
                raise ValueError("Account new requires value transfer")

        return super(SIP161, cls)._calculate_call_gas(opcode, gas_costs)
