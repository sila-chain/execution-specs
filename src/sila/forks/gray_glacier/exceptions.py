"""
Exceptions specific to this fork.
"""

from typing import Final

from sila_types.numeric import U64, Uint

from sila.exceptions import InvalidTransaction


class WrongChainIdError(InvalidTransaction):
    """
    Chain identifier from a transaction does not match the executing chain. See
    [SIP-155].

    [SIP-155]: https://sips.sila.org/SIPS/sip-155
    """

    def __init__(self, expected: U64, actual: U64):
        super().__init__(f"expected chain_id `{expected}` but got `{actual}`")
        self.expected = expected
        self.actual = actual


class TransactionTypeError(InvalidTransaction):
    """
    Unknown [SIP-2718] transaction type byte.

    [SIP-2718]: https://sips.sila.org/SIPS/sip-2718
    """

    transaction_type: Final[int]
    """
    The type byte of the transaction that caused the error.
    """

    def __init__(self, transaction_type: int):
        super().__init__(f"unknown transaction type `{transaction_type}`")
        self.transaction_type = transaction_type


class InsufficientMaxFeePerGasError(InvalidTransaction):
    """
    The maximum fee per gas is insufficient for the transaction.
    """

    transaction_max_fee_per_gas: Final[Uint]
    """
    The maximum fee per gas specified in the transaction.
    """

    block_base_fee_per_gas: Final[Uint]
    """
    The base fee per gas of the block in which the transaction is included.
    """

    def __init__(
        self, transaction_max_fee_per_gas: Uint, block_base_fee_per_gas: Uint
    ):
        super().__init__(
            f"Insufficient max fee per gas "
            f"({transaction_max_fee_per_gas} < {block_base_fee_per_gas})"
        )
        self.transaction_max_fee_per_gas = transaction_max_fee_per_gas
        self.block_base_fee_per_gas = block_base_fee_per_gas


class PriorityFeeGreaterThanMaxFeeError(InvalidTransaction):
    """
    The priority fee is greater than the maximum fee per gas.
    """
