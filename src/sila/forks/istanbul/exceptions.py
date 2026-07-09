"""
Exceptions specific to this fork.
"""

from sila_types.numeric import U64

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
