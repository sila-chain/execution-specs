"""Test the SIP checklist plugin functionality."""

import re
import textwrap
from typing import Any


def test_sip_checklist_collection(testdir: Any) -> None:
    """Test that checklist markers are collected correctly."""
    # Create the test in an SIP-specific directory
    tests_dir = testdir.mkdir("tests")

    prague_tests_dir = tests_dir.mkdir("prague")
    sip_7702_tests_dir = prague_tests_dir.mkdir("sip7702_set_code_tx")
    test_7702_module = sip_7702_tests_dir.join("test_sip7702.py")
    test_7702_module.write(
        textwrap.dedent(
            """
            import pytest
            from execution_testing import  StateTestFiller

            from execution_testing.checklists import SIPChecklist

            REFERENCE_SPEC_GIT_PATH = "N/A"
            REFERENCE_SPEC_VERSION = "N/A"

            @pytest.mark.valid_at("Prague")
            @SIPChecklist.TransactionType.Test.IntrinsicValidity.GasLimit.Exact()
            def test_exact_gas(state_test: StateTestFiller) -> None:
                pass

            @pytest.mark.valid_at("Prague")
            @SIPChecklist.TransactionType.Test.Signature.Invalid.V.Two(sip=[2930])
            def test_invalid_v(state_test: StateTestFiller) -> None:
                pass
            """
        )
    )
    sip_7702_external_coverage_file = sip_7702_tests_dir.join(
        "sip_checklist_external_coverage.txt"
    )
    sip_7702_external_coverage_file.write(
        textwrap.dedent(
            """
            general/code_coverage/eels = DEBUG EXTERNAL COVERAGE REASON
            """
        )
    )

    berlin_tests_dir = tests_dir.mkdir("berlin")
    sip_2930_tests_dir = berlin_tests_dir.mkdir("sip2930_access_list")
    test_2930_module = sip_2930_tests_dir.join("test_sip2930.py")
    test_2930_module.write(
        textwrap.dedent(
            """
            import pytest
            from execution_testing import  StateTestFiller

            REFERENCE_SPEC_GIT_PATH = "N/A"
            REFERENCE_SPEC_VERSION = "N/A"

            @pytest.mark.valid_at("Berlin")
            def test_berlin_one(state_test: StateTestFiller) -> None:
                pass
            """
        )
    )
    test_2930_n_a_file = sip_2930_tests_dir.join(
        "sip_checklist_not_applicable.txt"
    )
    test_2930_n_a_file.write(
        textwrap.dedent(
            """
            system_contract = DEBUG NOT APPLICABLE REASON
            """
        )
    )
    # Run pytest with checklist-only mode
    testdir.copy_example(
        name="src/execution_testing/cli/pytest_commands/pytest_ini_files/pytest-fill.ini"
    )
    result = testdir.runpytest(
        "-c",
        "pytest-fill.ini",
        "-p",
        "execution_testing.cli.pytest_commands.plugins.filler.sip_checklist",
        "--collect-only",
        "--checklist-output",
        str(testdir.tmpdir / "checklists"),
        str(tests_dir),
    )
    result.assert_outcomes(
        passed=0,
        failed=0,
        skipped=0,
        errors=0,
    )

    # Check that checklists were generated
    checklist_dir = testdir.tmpdir / "checklists"
    assert checklist_dir.exists()

    checklist_file = checklist_dir / "sip7702_checklist.md"
    assert checklist_file.exists()

    # Verify the checklist contains the expected markers
    content = checklist_file.readlines()
    assert any(re.search(r"✅.*test_exact_gas", line) for line in content)
    assert any(re.search(r"✅.*test_invalid_v", line) for line in content)
    assert any(
        re.search(r"✅.*DEBUG EXTERNAL COVERAGE REASON", line)
        for line in content
    )

    checklist_file = checklist_dir / "sip2930_checklist.md"
    assert checklist_file.exists()
    content = checklist_file.readlines()
    assert not any(re.search(r"✅.*test_exact_gas", line) for line in content)
    assert any(re.search(r"✅.*test_invalid_v", line) for line in content)
    assert any(
        re.search(r"N/A.*DEBUG NOT APPLICABLE REASON", line)
        for line in content
    )
