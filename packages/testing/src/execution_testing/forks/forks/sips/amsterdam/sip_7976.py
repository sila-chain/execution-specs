"""
SIP-7976: Increase Calldata Floor Cost.

Increase the calldata floor cost to 64/64 gas per byte to reduce maximum block
size.

https://sips.sila.org/SIPS/sip-7976
"""

from dataclasses import replace

from execution_testing.base_types import Bytes
from execution_testing.base_types.conversions import BytesConvertible

from ....base_fork import BaseFork, CalldataGasCalculator
from ....gas_costs import GasCosts


class SIP7976(BaseFork):
    """SIP-7976 class."""

    @classmethod
    def gas_costs(cls) -> GasCosts:
        """Transaction data floor token cost is increased from 10 to 16."""
        return replace(
            super(SIP7976, cls).gas_costs(),
            TX_DATA_TOKEN_FLOOR=16,
        )

    @classmethod
    def calldata_gas_calculator(cls) -> CalldataGasCalculator:
        """
        In floor mode, count four tokens per calldata byte uniformly so
        the data floor cost becomes ``4 * bytes * TX_DATA_TOKEN_FLOOR``
        (64/64 gas per byte). Standard mode keeps SIP-7623 semantics so
        that composition with downstream SIPs (e.g. SIP-7981) stays
        intact via ``super().transaction_data_floor_cost_calculator()``.
        """
        super_fn = super(SIP7976, cls).calldata_gas_calculator()
        gas_costs = cls.gas_costs()

        def fn(*, data: BytesConvertible, floor: bool = False) -> int:
            if floor:
                return len(Bytes(data)) * 4 * gas_costs.TX_DATA_TOKEN_FLOOR
            return super_fn(data=data, floor=False)

        return fn
