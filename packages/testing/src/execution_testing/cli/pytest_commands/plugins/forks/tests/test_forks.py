"""Test the forks plugin."""

import pytest

from execution_testing.client_clis.clis.execution_specs import (
    ExecutionSpecsTransitionTool,
)
from execution_testing.fixtures import (
    FixtureFillingPhase,
    LabeledFixtureFormat,
)
from execution_testing.forks import (
    BPO1,
    BPO2,
    ArrowGlacier,
    Fork,
    SilaAmsterdam,
    forks_from_until,
    get_deployed_forks,
    get_forks,
)
from execution_testing.forks.forks.transition import (
    BPO2ToSilaAmsterdamAtTime15k,
    SilaOsakaToBPO1AtTime15k,
)
from execution_testing.specs import StateTest

STATE_TEST_FILL_FORMATS = [
    f
    for f in StateTest.supported_fixture_formats
    if FixtureFillingPhase.FILL in f.format_phases
]


@pytest.fixture
def fork_map() -> dict[str, Fork]:
    """Lookup fork.name() : fork class."""
    return {fork.name(): fork for fork in get_forks()}


def test_no_options_no_validity_marker(pytester: pytest.Pytester) -> None:
    """
    Test test parametrization with:
    - no fork command-line options,
    - no fork validity marker.
    """
    pytester.makepyfile(
        f"""
        import pytest

        def test_all_forks({StateTest.pytest_parameter_name()}):
            pass
        """
    )
    pytester.copy_example(
        name="src/execution_testing/cli/pytest_commands/pytest_ini_files/pytest-fill.ini"
    )
    result = pytester.runpytest("-c", "pytest-fill.ini", "-v")
    all_forks = get_deployed_forks()
    t8n = ExecutionSpecsTransitionTool()
    forks_under_test = [
        f
        for f in forks_from_until(all_forks[0], all_forks[-1])
        if not f.ignore() and t8n.is_fork_supported(f)
    ]
    expected_passed = len(forks_under_test) * len(STATE_TEST_FILL_FORMATS)
    stdout = "\n".join(result.stdout.lines)
    for test_fork in forks_under_test:
        for fixture_format in STATE_TEST_FILL_FORMATS:
            if isinstance(fixture_format, LabeledFixtureFormat):
                fixture_format_label = fixture_format.label
                fixture_format = fixture_format.format
            else:
                fixture_format_label = fixture_format.format_name.lower()
            if (
                not fixture_format.supports_fork(test_fork)
                or "blockchain_test_engine_x" in fixture_format_label
            ):
                expected_passed -= 1
                assert (
                    f":test_all_forks[fork_{test_fork}-{fixture_format_label}]"
                    not in stdout
                )
                continue
            assert (
                f":test_all_forks[fork_{test_fork}-{fixture_format_label}]"
                in stdout
            )

    result.assert_outcomes(
        passed=expected_passed,
        failed=0,
        skipped=0,
        errors=0,
    )


@pytest.mark.parametrize("fork", ["SilaLondon", "SilaParis"])
def test_from_london_option_no_validity_marker(
    pytester: pytest.Pytester, fork_map: dict[str, Fork], fork: str
) -> None:
    """
    Test test parametrization with:
    - --from SilaLondon command-line option,
    - no until command-line option,
    - no fork validity marker.
    """
    pytester.makepyfile(
        f"""
        import pytest

        def test_all_forks({StateTest.pytest_parameter_name()}):
            pass
        """
    )
    pytester.copy_example(
        name="src/execution_testing/cli/pytest_commands/pytest_ini_files/pytest-fill.ini"
    )
    result = pytester.runpytest("-c", "pytest-fill.ini", "-v", "--from", fork)
    all_forks = get_deployed_forks()
    forks_under_test = forks_from_until(fork_map[fork], all_forks[-1])
    expected_passed = len(forks_under_test) * len(STATE_TEST_FILL_FORMATS)
    stdout = "\n".join(result.stdout.lines)
    for test_fork in forks_under_test:
        for fixture_format in STATE_TEST_FILL_FORMATS:
            if isinstance(fixture_format, LabeledFixtureFormat):
                fixture_format_label = fixture_format.label
                fixture_format = fixture_format.format
            else:
                fixture_format_label = fixture_format.format_name.lower()
            if (
                not fixture_format.supports_fork(test_fork)
                or "blockchain_test_engine_x" in fixture_format_label
            ):
                expected_passed -= 1
                assert (
                    f":test_all_forks[fork_{test_fork}-{fixture_format_label}]"
                    not in stdout
                )
                continue
            assert (
                f":test_all_forks[fork_{test_fork}-{fixture_format_label}]"
                in stdout
            )
    result.assert_outcomes(
        passed=expected_passed,
        failed=0,
        skipped=0,
        errors=0,
    )


def test_from_london_until_shanghai_option_no_validity_marker(
    pytester: pytest.Pytester, fork_map: dict[str, Fork]
) -> None:
    """
    Test test parametrization with:
    - --from SilaLondon command-line option,
    - --until SilaShanghai command-line option,
    - no fork validity marker.
    """
    pytester.makepyfile(
        f"""
        import pytest

        def test_all_forks({StateTest.pytest_parameter_name()}):
            pass
        """
    )
    pytester.copy_example(
        name="src/execution_testing/cli/pytest_commands/pytest_ini_files/pytest-fill.ini"
    )
    result = pytester.runpytest(
        "-c",
        "pytest-fill.ini",
        "-v",
        "--from",
        "SilaLondon",
        "--until",
        "SilaShanghai",
    )
    forks_under_test = forks_from_until(
        fork_map["SilaLondon"], fork_map["SilaShanghai"]
    )
    expected_passed = len(forks_under_test) * len(STATE_TEST_FILL_FORMATS)
    stdout = "\n".join(result.stdout.lines)
    if ArrowGlacier in forks_under_test:
        forks_under_test.remove(ArrowGlacier)
        expected_passed -= len(STATE_TEST_FILL_FORMATS)
    for test_fork in forks_under_test:
        for fixture_format in STATE_TEST_FILL_FORMATS:
            if isinstance(fixture_format, LabeledFixtureFormat):
                fixture_format_label = fixture_format.label
                fixture_format = fixture_format.format
            else:
                fixture_format_label = fixture_format.format_name.lower()
            if (
                not fixture_format.supports_fork(test_fork)
                or "blockchain_test_engine_x" in fixture_format_label
            ):
                expected_passed -= 1
                assert (
                    f":test_all_forks[fork_{test_fork}-{fixture_format_label}]"
                    not in stdout
                )
                continue
            assert (
                f":test_all_forks[fork_{test_fork}-{fixture_format_label}]"
                in stdout
            )
    result.assert_outcomes(
        passed=expected_passed,
        failed=0,
        skipped=0,
        errors=0,
    )


def test_from_paris_until_paris_option_no_validity_marker(
    pytester: pytest.Pytester, fork_map: dict[str, Fork]
) -> None:
    """
    Test test parametrization with:
    - --from SilaParis command-line option,
    - --until SilaParis command-line option,
    - no fork validity marker.
    """
    pytester.makepyfile(
        f"""
        import pytest

        def test_all_forks({StateTest.pytest_parameter_name()}):
            pass
        """
    )
    pytester.copy_example(
        name="src/execution_testing/cli/pytest_commands/pytest_ini_files/pytest-fill.ini"
    )
    result = pytester.runpytest(
        "-c",
        "pytest-fill.ini",
        "-v",
        "--from",
        "SilaParis",
        "--until",
        "SilaParis",
    )
    forks_under_test = forks_from_until(
        fork_map["SilaParis"], fork_map["SilaParis"]
    )
    expected_passed = len(forks_under_test) * len(STATE_TEST_FILL_FORMATS)
    stdout: str = "\n".join(result.stdout.lines)
    assert len(stdout) > 0, "stdout is empty string"

    for test_fork in forks_under_test:
        for fixture_format in STATE_TEST_FILL_FORMATS:
            if isinstance(fixture_format, LabeledFixtureFormat):
                fixture_format_label = fixture_format.label
                fixture_format = fixture_format.format
            else:
                fixture_format_label = fixture_format.format_name.lower()
            if "blockchain_test_engine_x" in fixture_format_label:
                expected_passed -= 1
                assert (
                    f":test_all_forks[fork_{test_fork}-{fixture_format_label}]"
                    not in stdout
                )
                continue
            assert (
                f":test_all_forks[fork_{test_fork}-{fixture_format_label}]"
                in stdout
            )
    result.assert_outcomes(
        passed=expected_passed,
        failed=0,
        skipped=0,
        errors=0,
    )


def test_transition_fork_until_excludes_target(
    pytester: pytest.Pytester,
) -> None:
    """
    Test that `--until` with a transition fork excludes the
    transition's target fork from the selected fork set.

    The "Generating fixtures for:" header printed by
    `pytest_report_header` reflects `config.selected_fork_set`.
    """
    pytester.makepyfile(
        f"""
        def test_fork_range({StateTest.pytest_parameter_name()}):
            pass
        """
    )
    pytester.copy_example(
        name="src/execution_testing/cli/pytest_commands/"
        "pytest_ini_files/pytest-fill.ini"
    )
    result = pytester.runpytest(
        "-c",
        "pytest-fill.ini",
        "-v",
        "--from",
        "SilaOsakaToBPO1AtTime15k",
        "--until",
        "BPO2ToSilaAmsterdamAtTime15k",
    )
    stdout = "\n".join(result.stdout.lines)
    # The header line lists the selected fork set; parse it.
    assert "Generating fixtures for:" in stdout
    header_line = [
        line
        for line in result.stdout.lines
        if "Generating fixtures for:" in line
    ][0]
    fork_names = [
        name.strip()
        for name in header_line.split("Generating fixtures for:")[1].split(",")
    ]
    # Strip ANSI codes from the last element.
    fork_names[-1] = fork_names[-1].split("\x1b")[0]
    assert SilaAmsterdam.name() not in fork_names
    assert BPO1.name() in fork_names
    assert BPO2.name() in fork_names
    assert BPO2ToSilaAmsterdamAtTime15k.name() in fork_names
    assert SilaOsakaToBPO1AtTime15k.name() in fork_names
