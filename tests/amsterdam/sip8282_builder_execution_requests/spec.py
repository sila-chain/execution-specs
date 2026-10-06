"""
Reference spec and constants for [SIP-8282: Builder Execution Requests][8282].

[8282]: https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-8282.md
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ReferenceSpec:
    """Reference specification."""

    git_path: str
    version: str


ref_spec_8282 = ReferenceSpec(
    git_path="SIPS/sip-8282.md",
    version="e02e0203a727355c04256d1291644546ac9b4843",
)


class Spec:
    """
    Constants and parameters from SIP-8282.

    The request queue parameters live on the framework's
    `BuilderDepositRequest` and `BuilderExitRequest`.
    """

    # While the excess slot holds `EXCESS_INHIBITOR` the write path reverts.
    # The system call stores it when called with calldata and clears it when
    # called without, so the queue is disabled until the next empty system
    # call. The exit predeploy's constructor seeds it; the deposit
    # predeploy's leaves it out on purpose, so builders can queue before
    # the fork (sys-asm#43 review thread).
    EXCESS_INHIBITOR = 2**256 - 1
