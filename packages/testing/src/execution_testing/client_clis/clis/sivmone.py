"""Sivmone Transition tool and fixture consumer interfaces."""

import re
import shlex
import shutil
import subprocess
import textwrap
from functools import cache
from pathlib import Path
from typing import ClassVar, Dict, List, Optional

import pytest

from execution_testing.client_clis.file_utils import (
    dump_files_to_directory,
)
from execution_testing.client_clis.fixture_consumer_tool import (
    FixtureConsumerTool,
)
from execution_testing.exceptions import (
    ExceptionBase,
    ExceptionMapper,
    TransactionException,
)
from execution_testing.exceptions.exceptions.block import BlockException
from execution_testing.fixtures.base import FixtureFormat
from execution_testing.fixtures.blockchain import BlockchainFixture
from execution_testing.fixtures.state import StateFixture
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


class SivmoneFixtureConsumerCommon:
    """Common functionality for the `sivmone test` fixture consumers."""

    binary: Path
    default_binary = Path("sivmone")
    # The same `sivmone` binary as the transition tool: `sivmone test` runs
    # both state and blockchain fixtures.
    detect_binary_pattern = re.compile(r"^sivmone\b(?!-)")
    version_flag: str = "--version"
    subcommand = "test"

    cached_version: Optional[str] = None

    def __init__(
        self,
        binary: Optional[Path] = None,
        trace: bool = False,
    ):
        """Initialize the `sivmone test` fixture consumer."""
        del trace
        self.binary = binary if binary else self.default_binary
        self._info_metadata: Optional[Dict[str, str]] = {}

    def _run_command(self, command: List[str]) -> subprocess.CompletedProcess:
        try:
            return subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
        except Exception as e:
            raise Exception("Unexpected exception calling sivmone.") from e

    def _consume_debug_dump(
        self,
        command: List[str],
        result: subprocess.CompletedProcess,
        fixture_path: Path,
        debug_output_path: Path,
    ) -> None:
        assert all(isinstance(x, str) for x in command), (
            f"Not all elements of 'command' list are strings: {command}"
        )
        assert len(command) > 0

        # Replace the fixture path with the debug copy of the fixture.
        debug_fixture_path = str(debug_output_path / "fixtures.json")
        command[-1] = debug_fixture_path

        consume_direct_call = " ".join(shlex.quote(arg) for arg in command)
        consume_direct_script = textwrap.dedent(
            f"""\
            #!/bin/bash
            {consume_direct_call}
            """
        )
        dump_files_to_directory(
            debug_output_path,
            {
                "consume_direct_args.py": command,
                "consume_direct_returncode.txt": result.returncode,
                "consume_direct_stdout.txt": result.stdout,
                "consume_direct_stderr.txt": result.stderr,
                "consume_direct.sh+x": consume_direct_script,
            },
        )
        shutil.copyfile(fixture_path, debug_fixture_path)

    def _skip_message(self, fixture_format: FixtureFormat) -> str:
        fmt_name = fixture_format.format_name
        return f"Fixture format {fmt_name} not supported by {self.binary}"

    @cache  # noqa
    def consume_test_file(
        self,
        fixture_path: Path,
        debug_output_path: Optional[Path] = None,
    ) -> Dict[str, str]:
        """
        Run `sivmone test` on an entire fixture file.

        `sivmone test` runs every fixture of a file as one test, so this
        function is cached in order to only call the command once per file.
        Returns the failure summary of each failed fixture, by name.
        """
        global_options: List[str] = []
        if debug_output_path:
            global_options += ["--trace"]
        command = (
            [str(self.binary)]
            + global_options
            + [self.subcommand, str(fixture_path)]
        )
        result = self._run_command(command)

        if debug_output_path:
            self._consume_debug_dump(
                command, result, fixture_path, debug_output_path
            )

        if result.returncode not in [0, 1]:
            cmd_str = " ".join(command)
            raise Exception(
                f"Unexpected exit code {result.returncode}:\n{cmd_str}\n\n"
                f"Output:\n{result.stdout}\n\nError:\n{result.stderr}"
            )

        # Failed fixtures are listed in the short test summary as
        # `FAILED  <file>::<fixture name> - <reason>`.
        failures: Dict[str, str] = {}
        prefix = f"{fixture_path}::"
        for line in result.stdout.splitlines():
            if not line.startswith("FAILED"):
                continue
            entry = line[len("FAILED") :].strip()
            if not entry.startswith(prefix):
                raise Exception(
                    f"Unexpected `sivmone test` failure line: {line}"
                )
            name, _, reason = entry[len(prefix) :].rpartition(" - ")
            failures[name] = reason
        if result.returncode == 1 and not failures:
            raise Exception(
                "`sivmone test` failed without a failure summary:\n"
                f"{result.stdout}\n{result.stderr}"
            )
        return failures

    def consume_test(
        self,
        fixture_path: Path,
        fixture_name: Optional[str] = None,
        debug_output_path: Optional[Path] = None,
    ) -> None:
        """
        Consume a single state or blockchain test.

        Uses the cached result from `consume_test_file` in order to not call
        the command for every fixture of the file.
        """
        assert fixture_name is not None, (
            "fixture_name must be provided for sivmone tests"
        )
        failures = self.consume_test_file(
            fixture_path=fixture_path,
            debug_output_path=debug_output_path,
        )
        assert fixture_name not in failures, (
            f"Test failed: {failures[fixture_name]}"
        )


class SivmoneStateFixtureConsumer(
    SivmoneFixtureConsumerCommon,
    FixtureConsumerTool,
    fixture_formats=[StateFixture],
):
    """Sivmone's `sivmone test` fixture consumer for state tests."""

    def consume_fixture(
        self,
        fixture_format: FixtureFormat,
        fixture_path: Path,
        fixture_name: Optional[str] = None,
        debug_output_path: Optional[Path] = None,
    ) -> None:
        """
        Execute the appropriate fixture consumer for the fixture at
        `fixture_path`.
        """
        if fixture_format == StateFixture:
            self.consume_test(
                fixture_path=fixture_path,
                fixture_name=fixture_name,
                debug_output_path=debug_output_path,
            )
        else:
            pytest.skip(self._skip_message(fixture_format))


class SivmoneBlockchainFixtureConsumer(
    SivmoneFixtureConsumerCommon,
    FixtureConsumerTool,
    fixture_formats=[BlockchainFixture],
):
    """Sivmone's `sivmone test` fixture consumer for blockchain tests."""

    def consume_fixture(
        self,
        fixture_format: FixtureFormat,
        fixture_path: Path,
        fixture_name: Optional[str] = None,
        debug_output_path: Optional[Path] = None,
    ) -> None:
        """
        Execute the appropriate fixture consumer for the fixture at
        `fixture_path`.
        """
        if fixture_format == BlockchainFixture:
            self.consume_test(
                fixture_path=fixture_path,
                fixture_name=fixture_name,
                debug_output_path=debug_output_path,
            )
        else:
            pytest.skip(self._skip_message(fixture_format))


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
