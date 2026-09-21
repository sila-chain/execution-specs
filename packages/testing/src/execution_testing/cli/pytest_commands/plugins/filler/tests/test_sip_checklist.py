"""Test the SIP checklist plugin functionality."""

import re
import textwrap
from typing import Any

import pytest

from ..sip_checklist import SIP, TEMPLATE_CONTENT


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


def test_generator_built_test_is_credited_to_its_directory(
    testdir: Any,
) -> None:
    """
    A test built by a decorator that lives outside the SIP directory is
    credited to the SIP of the module that collected it, not to the module
    that defines the wrapper.
    """
    tests_dir = testdir.mkdir("tests")
    # An empty conftest puts `tests/` on the import path for the builder.
    tests_dir.join("conftest.py").write("")
    tests_dir.join("generated.py").write(
        textwrap.dedent(
            """
            def build(func):
                def wrapper(state_test):
                    pass

                wrapper.__name__ = func.__name__
                return wrapper
            """
        )
    )
    sip_dir = tests_dir.mkdir("prague").mkdir("sip7702_set_code_tx")
    sip_dir.join("test_sip7702.py").write(
        textwrap.dedent(
            """
            import pytest
            from execution_testing import StateTestFiller
            from execution_testing.checklists import SIPChecklist
            from generated import build

            REFERENCE_SPEC_GIT_PATH = "N/A"
            REFERENCE_SPEC_VERSION = "N/A"

            @pytest.mark.valid_at("Prague")
            @SIPChecklist.TransactionType.Test.IntrinsicValidity.GasLimit.Exact()
            @build
            def test_generated(state_test: StateTestFiller) -> None:
                pass
            """
        )
    )
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
    result.assert_outcomes(passed=0, failed=0, skipped=0, errors=0)

    checklist_file = testdir.tmpdir / "checklists" / "sip7702_checklist.md"
    assert checklist_file.exists()
    content = checklist_file.readlines()
    assert any(re.search(r"✅.*test_generated", line) for line in content)


@pytest.mark.parametrize(
    "coverage_kind", ["tests", "external", "not_applicable"]
)
def test_repeated_checklist_rows(coverage_kind: str) -> None:
    """Render coverage on every repeated row while counting its ID once."""
    item_id = (
        "transaction_type/test/intrinsic_validity/"
        "data_floor_above_intrinsic_gas_cost"
    )
    sip = SIP(number=7981)
    total = sip.total_items
    item = sip.items[item_id]
    evidence = "Evidence for both floor outcomes"
    if coverage_kind == "tests":
        item.tests.add(evidence)
    elif coverage_kind == "external":
        item.external_coverage_reason = evidence
    else:
        item.not_applicable_reason = evidence

    prefix = f"| `{item_id}` |"
    original_rows = [
        line
        for line in TEMPLATE_CONTENT.splitlines()
        if line.startswith(prefix)
    ]
    rows = [
        line
        for line in sip.generate_filled_checklist_lines()
        if line.startswith(prefix)
    ]
    assert len(rows) == len(original_rows) == 2
    status = "N/A" if coverage_kind == "not_applicable" else "✅"
    for original, rendered in zip(original_rows, rows, strict=True):
        assert original.split("|")[2].strip() == rendered.split("|")[2].strip()
        assert f"| {status} | {evidence} |" in rendered
    assert sip.covered_items == (0 if coverage_kind == "not_applicable" else 1)
    assert sip.total_items == total - (coverage_kind == "not_applicable")
