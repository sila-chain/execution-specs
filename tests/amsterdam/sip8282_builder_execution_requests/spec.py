"""
Reference spec and constants for [SIP-8282: Builder Execution Requests][8282].

[8282]: https://sips.sila.org/SIPS/sip-8282
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ReferenceSpec:
    """Reference specification."""

    git_path: str
    version: str


# SIP-8282 is a Draft; its addresses, request-type bytes, and predeploy
# bytecode are placeholders pending the SIP's final, audit-frozen values.
ref_spec_8282 = ReferenceSpec(
    git_path="SIPS/sip-8282.md",
    version="0000000000000000000000000000000000000000",
)


class Spec:
    """
    Constants and parameters from SIP-8282. Addresses are the
    glamsterdam-devnet-6 values; request-type bytes remain placeholders
    pending the SIP's final allocation.
    """

    BUILDER_DEPOSIT_CONTRACT_ADDRESS = (
        0x0000884D2AA32EAA155F59A2F24EFA73D9008282
    )
    BUILDER_EXIT_CONTRACT_ADDRESS = 0x000014574A74C805590AFF9499FC7A690F008282

    BUILDER_DEPOSIT_REQUEST_TYPE = 0x03
    BUILDER_EXIT_REQUEST_TYPE = 0x04

    SYSTEM_ADDRESS = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFE
    SYSTEM_CALL_GAS_LIMIT = 30_000_000

    # Shared request-bus parameters (identical to SIP-7002 / SIP-7251).
    MAX_DEPOSIT_REQUESTS_PER_BLOCK = 256
    TARGET_DEPOSIT_REQUESTS_PER_BLOCK = 32
    MAX_EXIT_REQUESTS_PER_BLOCK = 16
    TARGET_EXIT_REQUESTS_PER_BLOCK = 2
    MIN_REQUEST_FEE = 1
    REQUEST_FEE_UPDATE_FRACTION = 17
    EXCESS_INHIBITOR = 2**256 - 1

    # Minimum credited stake for a builder deposit, in wei (1 SIL).
    BUILDER_MIN_DEPOSIT = 1_000_000_000_000_000_000

    # Calldata input sizes accepted by each predeploy.
    DEPOSIT_REQUEST_INPUT_BYTES = 184
    EXIT_REQUEST_INPUT_BYTES = 48
