"""Sivmone Transition tool interface."""

import re
from pathlib import Path
from typing import ClassVar, Dict, Optional

from execution_testing.exceptions import (
    ExceptionBase,
    ExceptionMapper,
    TransactionException,
)
from execution_testing.exceptions.exceptions.block import BlockException
from execution_testing.forks import Fork

from ..transition_tool import TransitionTool


class SivmoneTransitionTool(TransitionTool):
    """Sivmone `sivmone t8n` Transition tool interface wrapper class."""

    default_binary = Path("sivmone")
    # Match the `sivmone` binary's version banner (`sivmone <version>`) while
    # excluding other `sivmone-*` binaries.
    detect_binary_pattern = re.compile(r"^sivmone\b(?!-)")
    version_flag = "--version"
    subcommand = "t8n"
    t8n_use_stream = False

    binary: Path
    cached_version: Optional[str] = None
    trace: bool
    supports_opcode_count: ClassVar[bool] = True
    supports_blob_params: ClassVar[bool] = True

    def __init__(
        self,
        *,
        binary: Optional[Path] = None,
        trace: bool = False,
    ):
        """Initialize the Sivmone Transition tool interface."""
        super().__init__(
            exception_mapper=SivmoneExceptionMapper(),
            binary=binary,
            trace=trace,
        )

    def is_fork_supported(self, fork: Fork) -> bool:
        """
        Return True if the fork is supported by the tool. Currently, sivmone
        provides no way to determine supported forks.
        """
        del fork
        return True


class SivmoneExceptionMapper(ExceptionMapper):
    """
    Translate between SEST exceptions and error strings returned by Sivmone.
    """

    mapping_substring: ClassVar[Dict[ExceptionBase, str]] = {
        TransactionException.SENDER_NOT_EOA: "sender not an eoa:",
        TransactionException.GAS_ALLOWANCE_EXCEEDED: "gas limit reached",
        TransactionException.PRIORITY_GREATER_THAN_MAX_FEE_PER_GAS: (
            "max priority fee per gas higher than max fee per gas"
        ),
        TransactionException.NONCE_IS_MAX: "nonce has max value:",
        TransactionException.TYPE_4_TX_CONTRACT_CREATION: (
            "set code transaction must "
        ),
        TransactionException.TYPE_4_INVALID_AUTHORITY_SIGNATURE: (
            "invalid authorization signature"
        ),
        TransactionException.TYPE_4_INVALID_AUTHORITY_SIGNATURE_S_TOO_HIGH: (
            "authorization signature s value too high"
        ),
        TransactionException.TYPE_4_EMPTY_AUTHORIZATION_LIST: (
            "empty authorization list"
        ),
        TransactionException.INTRINSIC_GAS_TOO_LOW: "intrinsic gas too low",
        TransactionException.INTRINSIC_GAS_BELOW_FLOOR_GAS_COST: (
            "intrinsic gas too low"
        ),
        TransactionException.TYPE_3_TX_MAX_BLOB_GAS_ALLOWANCE_EXCEEDED: (
            "blob gas limit exceeded"
        ),
        TransactionException.INITCODE_SIZE_EXCEEDED: (
            "max initcode size exceeded"
        ),
        TransactionException.INSUFFICIENT_ACCOUNT_FUNDS: (
            "insufficient funds for gas * price + value"
        ),
        TransactionException.INSUFFICIENT_MAX_FEE_PER_GAS: (
            "max fee per gas less than block base fee"
        ),
        TransactionException.INSUFFICIENT_MAX_FEE_PER_BLOB_GAS: (
            "max blob fee per gas less than block base fee"
        ),
        TransactionException.TYPE_4_TX_PRE_FORK: (
            "transaction type not supported"
        ),
        TransactionException.TYPE_3_TX_PRE_FORK: (
            "transaction type not supported"
        ),
        TransactionException.TYPE_2_TX_PRE_FORK: (
            "transaction type not supported"
        ),
        TransactionException.TYPE_1_TX_PRE_FORK: (
            "transaction type not supported"
        ),
        TransactionException.TYPE_3_TX_INVALID_BLOB_VERSIONED_HASH: (
            "invalid blob hash version"
        ),
        TransactionException.TYPE_3_TX_BLOB_COUNT_EXCEEDED: (
            "blob gas limit exceeded"
        ),
        TransactionException.TYPE_3_TX_ZERO_BLOBS: "empty blob hashes list",
        TransactionException.TYPE_3_TX_CONTRACT_CREATION: (
            "blob transaction must not be a create transaction"
        ),
        TransactionException.NONCE_MISMATCH_TOO_LOW: "nonce too low",
        TransactionException.NONCE_MISMATCH_TOO_HIGH: "nonce too high",
        TransactionException.GAS_LIMIT_EXCEEDS_MAXIMUM: (
            "max gas limit exceeded"
        ),
        BlockException.INVALID_DEPOSIT_EVENT_LAYOUT: (
            "invalid deposit event layout"
        ),
        # TODO sivmone needs to differentiate when the system contract is
        # missing or failing
        BlockException.SYSTEM_CONTRACT_EMPTY: (
            "system contract empty or failed"
        ),
        BlockException.SYSTEM_CONTRACT_CALL_FAILED: (
            "system contract empty or failed"
        ),
    }
    mapping_regex: ClassVar[Dict[ExceptionBase, str]] = {}
