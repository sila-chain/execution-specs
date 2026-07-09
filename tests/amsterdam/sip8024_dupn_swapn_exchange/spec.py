"""Reference spec for [SIP-8024: Stack Access Instructions](https://sips.sila.org/SIPS/sip-8024)."""

from dataclasses import dataclass
from typing import Tuple

from sila_types.numeric import U8

from sila.forks.amsterdam.vm.stack import decode_pair as _decode_pair
from sila.forks.amsterdam.vm.stack import decode_single as _decode_single


@dataclass(frozen=True)
class ReferenceSpec:
    """Reference specification."""

    git_path: str
    version: str


ref_spec_8024 = ReferenceSpec(
    git_path="SIPS/sip-8024.md",
    version="380cb02832a6ed5310bfde51591e580ca6d1f3cd",
)


class Spec:
    """Constants and parameters from SIP-8024."""

    # Gas cost for DUPN, SWAPN, and EXCHANGE
    GAS_COST: int = 3

    # DUPN/SWAPN stack index range (after decoding)
    MIN_STACK_INDEX: int = 17
    MAX_STACK_INDEX: int = 235

    # EXCHANGE constraints: 1 <= n < m <= 29, n + m <= 30
    EXCHANGE_MIN_N: int = 1
    EXCHANGE_MAX_N: int = 14
    EXCHANGE_MAX_M: int = 29
    EXCHANGE_MAX_SUM: int = 30


def decode_pair(x: int) -> Tuple[int, int]:
    """Decode a pair with proper typing for tests."""
    n, m = _decode_pair(U8(x))
    return int(n), int(m)


def decode_single(x: int) -> int:
    """Decode single with proper typing for tests."""
    return int(_decode_single(U8(x)))
