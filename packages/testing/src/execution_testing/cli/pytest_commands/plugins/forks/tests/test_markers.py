"""Test fork markers and their effect on test parametrization."""

from typing import List

import pytest


def generate_test(**kwargs: str) -> str:
    """Generate a test function with the given fork markers."""
    markers = [f"@pytest.mark.{key}({value})" for key, value in kwargs.items()]
    marker_lines = "\n".join(markers)
    return f"""
import pytest
{marker_lines}
@pytest.mark.state_test_only
def test_case(state_test):
    pass
"""


@pytest.mark.parametrize(
    "test_function,pytest_args,outcomes",
    [
        pytest.param(
            """
import pytest
@pytest.mark.valid_from("SilaParis")
@pytest.mark.valid_from("SilaBerlin")
@pytest.mark.state_test_only
def test_case(state_test):
    pass
""",
            [],
            {"passed": 5, "failed": 0, "skipped": 0, "errors": 0},
            id="two_valid_from",
        ),
        pytest.param(
            generate_test(
                valid_until='"SilaCancun"',
            ),
            [],
            # All deployed forks from Frontier through SilaCancun, except
            # SilaConstantinople (filled as SilaConstantinopleFix): Frontier,
            # SilaHomestead, TangerineWhistle, SpuriousDragon, SilaByzantium,
            # SilaConstantinopleFix, SilaIstanbul, SilaBerlin, SilaLondon,
            # SilaParis, SilaShanghai,
            # SilaCancun = 12 forks.
            {"passed": 12, "failed": 0, "skipped": 0, "errors": 0},
            id="valid_until",
        ),
        pytest.param(
            generate_test(
                valid_until='"SilaCancun"',
            ),
            ["--from=SilaBerlin"],
            {"passed": 5, "failed": 0, "skipped": 0, "errors": 0},
            id="valid_until,--from",
        ),
        pytest.param(
            generate_test(
                valid_from='"SilaParis"',
            ),
            ["--until=SilaPrague"],
            {"passed": 4, "failed": 0, "skipped": 0, "errors": 0},
            id="valid_from",
        ),
        pytest.param(
            generate_test(
                valid_from='"SIP3675"',
            ),
            ["--until=SilaPrague"],
            {"passed": 4, "failed": 0, "skipped": 0, "errors": 0},
            id="valid_from_sip",
        ),
        pytest.param(
            generate_test(
                valid_from='"SilaParis"',
                valid_until='"SilaCancun"',
            ),
            [],
            {"passed": 3, "failed": 0, "skipped": 0, "errors": 0},
            id="valid_from_until",
        ),
        pytest.param(
            generate_test(
                valid_from='"SIP3675"',
                valid_until='"SIP4844"',
            ),
            [],
            {"passed": 3, "failed": 0, "skipped": 0, "errors": 0},
            id="valid_from_sip_until_sip",
        ),
        pytest.param(
            generate_test(
                valid_from='"SilaParis"',
                valid_until='"SIP4844"',
            ),
            [],
            {"passed": 3, "failed": 0, "skipped": 0, "errors": 0},
            id="valid_from_fork_until_sip",
        ),
        pytest.param(
            generate_test(
                valid_from='"SIP3675"',
                valid_until='"SilaCancun"',
            ),
            [],
            {"passed": 3, "failed": 0, "skipped": 0, "errors": 0},
            id="valid_from_sip_until_fork",
        ),
        pytest.param(
            generate_test(
                valid_from='"SilaParis"',
                valid_until='"SilaCancun"',
            ),
            ["--until=SilaPrague"],
            {"passed": 3, "failed": 0, "skipped": 0, "errors": 0},
            id="valid_from_until,--until=SilaPrague",
        ),
        pytest.param(
            generate_test(
                valid_from='"SilaParis"',
                valid_until='"SilaCancun"',
            ),
            ["--until=SilaShanghai"],
            {"passed": 2, "failed": 0, "skipped": 0, "errors": 0},
            id="valid_from_until,--until=SilaShanghai",
        ),
        pytest.param(
            generate_test(
                valid_at_transition_to='"SilaShanghai"',
            ),
            [],
            {"passed": 1, "failed": 0, "skipped": 0, "errors": 0},
            id="valid_at_transition_to",
        ),
        pytest.param(
            generate_test(
                valid_at_transition_to='"SilaShanghai"',
            ),
            ["--until=SilaPrague"],
            {"passed": 1, "failed": 0, "skipped": 0, "errors": 0},
            id="valid_at_transition_to,--until=SilaPrague",
        ),
        pytest.param(
            generate_test(
                valid_at_transition_to='"SilaShanghai"',
            ),
            ["--until=SilaBerlin"],
            {"passed": 0, "failed": 0, "skipped": 0, "errors": 0},
            id="valid_at_transition_to,--until=SilaBerlin",
        ),
        pytest.param(
            generate_test(
                valid_at_transition_to='"SilaParis", subsequent_forks=True',
            ),
            ["--until=SilaPrague"],
            {"passed": 3, "failed": 0, "skipped": 0, "errors": 0},
            id="valid_at_transition_to,subsequent_forks=True",
        ),
        pytest.param(
            generate_test(
                valid_at_transition_to=(
                    '"SilaParis", subsequent_forks=True, until="SilaCancun"'
                ),
            ),
            ["--until=SilaPrague"],
            {"passed": 2, "failed": 0, "skipped": 0, "errors": 0},
            id="valid_at_transition_to,subsequent_forks=True,until",
        ),
        pytest.param(
            generate_test(
                valid_at_transition_to='"SilaCancun"',
            ),
            ["--fork=SilaShanghaiToSilaCancunAtTime15k"],
            {"passed": 1, "failed": 0, "skipped": 0, "errors": 0},
            id="valid_at_transition_to,--fork=transition_fork_only",
        ),
        pytest.param(
            generate_test(
                valid_before='"SilaCancun"',
            ),
            ["--from=SilaBerlin", "--until=SilaPrague"],
            {"passed": 4, "failed": 0, "skipped": 0, "errors": 0},
            id="valid_before",
        ),
        pytest.param(
            generate_test(
                valid_from='"SilaParis"',
                valid_before='"SilaCancun"',
            ),
            ["--until=SilaPrague"],
            {"passed": 2, "failed": 0, "skipped": 0, "errors": 0},
            id="valid_from_before",
        ),
        pytest.param(
            generate_test(
                valid_before='"SIP4844"',
            ),
            ["--from=SilaBerlin", "--until=SilaPrague"],
            {"passed": 4, "failed": 0, "skipped": 0, "errors": 0},
            id="valid_before_sip",
        ),
        pytest.param(
            generate_test(
                valid_from='"SIP3675"',
                valid_before='"SIP4844"',
            ),
            ["--until=SilaPrague"],
            {"passed": 2, "failed": 0, "skipped": 0, "errors": 0},
            id="valid_from_sip_before_sip",
        ),
        pytest.param(
            generate_test(
                valid_from='"SilaOsaka"',
                valid_until='"BPO1"',
            ),
            ["--until=BPO1"],
            {"passed": 1, "failed": 0, "skipped": 0, "errors": 0},
            id="valid_until_bpo_fork_without_bpo_test_marker",
            marks=pytest.mark.skip(reason="BPO tests are not supported yet"),
        ),
        pytest.param(
            generate_test(
                valid_from='"SilaOsaka"',
                valid_until='"BPO1"',
                valid_for_bpo_forks="",
            ),
            ["--until=BPO1"],
            {"passed": 2, "failed": 0, "skipped": 0, "errors": 0},
            id="valid_until_bpo_fork_with_bpo_test_marker",
            marks=pytest.mark.skip(reason="BPO tests are not supported yet"),
        ),
        pytest.param(
            generate_test(
                valid_at_transition_to=(
                    '"SilaOsaka", subsequent_forks=True, until="BPO1"'
                ),
            ),
            ["--until=BPO1"],
            {"passed": 1, "failed": 0, "skipped": 0, "errors": 0},
            id="valid_at_transition_without_bpo_test_marker",
            marks=pytest.mark.skip(reason="BPO tests are not supported yet"),
        ),
        pytest.param(
            generate_test(
                valid_at_transition_to=(
                    '"SilaOsaka", subsequent_forks=True, until="BPO1"'
                ),
                valid_for_bpo_forks="",
            ),
            ["--until=BPO1"],
            {"passed": 2, "failed": 0, "skipped": 0, "errors": 0},
            id="valid_at_transition_with_bpo_test_marker",
            marks=pytest.mark.skip(reason="BPO tests are not supported yet"),
        ),
        pytest.param(
            generate_test(
                valid_at_transition_to='"SilaCancun"',
            ),
            ["--fork=SilaCancun"],
            {"passed": 1, "failed": 0, "skipped": 0, "errors": 0},
            id="valid_at_transition_to_with_exact_fork",
        ),
        pytest.param(
            generate_test(
                valid_at_transition_to='"SilaCancun"',
            ),
            ["--from=SilaCancun", "--until=SilaPrague"],
            {"passed": 1, "failed": 0, "skipped": 0, "errors": 0},
            id="valid_at_transition_to_from_fork_until_later_fork",
        ),
        pytest.param(
            generate_test(
                valid_at_transition_to='"BPO1"',
                valid_for_bpo_forks="",
            ),
            ["--fork=SilaOsaka"],
            {"passed": 0, "failed": 0, "skipped": 0, "errors": 0},
            id="valid_at_transition_with_bpo_test_marker_fork_parent",
            marks=pytest.mark.skip(reason="BPO tests are not supported yet"),
        ),
        pytest.param(
            generate_test(
                valid_at_transition_to='"BPO1"',
                valid_for_bpo_forks="",
            ),
            ["--from=SilaOsaka", "--until=SilaOsaka"],
            {"passed": 0, "failed": 0, "skipped": 0, "errors": 0},
            id="valid_at_transition_with_bpo_test_marker_from_parent",
            marks=pytest.mark.skip(reason="BPO tests are not supported yet"),
        ),
    ],
)
def test_fork_markers(
    pytester: pytest.Pytester,
    test_function: str,
    outcomes: dict,
    pytest_args: List[str],
) -> None:
    """
    Test fork markers in an isolated test session, i.e., in
    a `fill` execution.

    In the case of an error, check that the expected error string is in the
    console output.
    """
    pytester.makepyfile(test_function)
    pytester.copy_example(
        name="src/execution_testing/cli/pytest_commands/pytest_ini_files/pytest-fill.ini"
    )
    result = pytester.runpytest(
        "-c",
        "pytest-fill.ini",
        "-v",
        *pytest_args,
    )
    result.assert_outcomes(**outcomes)


# --- Tests for param-level validity markers --- #


def generate_param_level_marker_test() -> str:
    """Generate a test function with param-level fork validity markers."""
    return """
import pytest

@pytest.mark.parametrize(
    "value",
    [
        pytest.param(
            True,
            id="from_tangerine",
            marks=pytest.mark.valid_from("TangerineWhistle"),
        ),
        pytest.param(
            False,
            id="from_paris",
            marks=pytest.mark.valid_from("SilaParis"),
        ),
    ],
)
@pytest.mark.state_test_only
def test_param_level_valid_from(state_test, value):
    pass
"""


def generate_param_level_valid_until_test() -> str:
    """Generate a test function with param-level valid_until markers."""
    return """
import pytest

@pytest.mark.parametrize(
    "value",
    [
        pytest.param(
            True,
            id="until_cancun",
            marks=pytest.mark.valid_until("SilaCancun"),
        ),
        pytest.param(
            False,
            id="until_paris",
            marks=pytest.mark.valid_until("SilaParis"),
        ),
    ],
)
@pytest.mark.state_test_only
def test_param_level_valid_until(state_test, value):
    pass
"""


def generate_param_level_valid_before_test() -> str:
    """Generate a test with param-level valid_before markers."""
    return """
import pytest

@pytest.mark.parametrize(
    "value",
    [
        pytest.param(
            True,
            id="before_cancun",
            marks=pytest.mark.valid_before("SilaCancun"),
        ),
        pytest.param(
            False,
            id="before_paris",
            marks=pytest.mark.valid_before("SilaParis"),
        ),
    ],
)
@pytest.mark.state_test_only
def test_param_level_valid_before(state_test, value):
    pass
"""


def generate_param_level_mixed_test() -> str:
    """Generate a test with both function-level and param-level markers."""
    return """
import pytest

@pytest.mark.parametrize(
    "value",
    [
        pytest.param(
            True,
            id="all_forks",
            marks=pytest.mark.valid_from("TangerineWhistle"),
        ),
        pytest.param(
            False,
            id="paris_only",
            marks=pytest.mark.valid_from("SilaParis"),
        ),
    ],
)
@pytest.mark.valid_until("SilaCancun")
@pytest.mark.state_test_only
def test_mixed_function_and_param_markers(state_test, value):
    pass
"""


@pytest.mark.parametrize(
    "test_function,pytest_args,outcomes",
    [
        pytest.param(
            generate_param_level_marker_test(),
            ["--from=SilaParis", "--until=SilaCancun"],
            # from_tangerine: SilaParis, SilaShanghai, SilaCancun = 3 forks
            # from_paris: SilaParis, SilaShanghai, SilaCancun = 3 forks
            # Total: 6 tests
            {"passed": 6, "failed": 0, "skipped": 0, "errors": 0},
            id="param_level_valid_from_paris_to_cancun",
        ),
        pytest.param(
            generate_param_level_marker_test(),
            ["--from=SilaBerlin", "--until=SilaShanghai"],
            # from_tangerine: SilaBerlin, SilaLondon, SilaParis, SilaShanghai =
            # 4 forks
            # from_paris: SilaParis, SilaShanghai = 2 forks
            # Total: 6 tests
            {"passed": 6, "failed": 0, "skipped": 0, "errors": 0},
            id="param_level_valid_from_berlin_to_shanghai",
        ),
        pytest.param(
            generate_param_level_marker_test(),
            ["--from=SilaBerlin", "--until=SilaLondon"],
            # from_tangerine: SilaBerlin, SilaLondon = 2 forks
            # from_paris: none (SilaParis > SilaLondon)
            # Total: 2 tests
            {"passed": 2, "failed": 0, "skipped": 0, "errors": 0},
            id="param_level_valid_from_berlin_to_london",
        ),
        pytest.param(
            generate_param_level_valid_until_test(),
            ["--from=SilaParis", "--until=SilaPrague"],
            # until_cancun: SilaParis, SilaShanghai, SilaCancun = 3 forks
            # until_paris: SilaParis = 1 fork
            # Total: 4 tests
            {"passed": 4, "failed": 0, "skipped": 0, "errors": 0},
            id="param_level_valid_until_paris_to_prague",
        ),
        pytest.param(
            generate_param_level_valid_until_test(),
            ["--from=SilaShanghai", "--until=SilaPrague"],
            # until_cancun: SilaShanghai, SilaCancun = 2 forks
            # until_paris: none (SilaShanghai > SilaParis)
            # Total: 2 tests
            {"passed": 2, "failed": 0, "skipped": 0, "errors": 0},
            id="param_level_valid_until_shanghai_to_prague",
        ),
        pytest.param(
            generate_param_level_mixed_test(),
            ["--from=SilaBerlin", "--until=SilaPrague"],
            # Function marker: valid_until("SilaCancun") limits to <=
            # SilaCancun
            # all_forks (TangerineWhistle):
            #   SilaBerlin, SilaLondon, SilaParis, SilaShanghai, SilaCancun = 5
            # paris_only: SilaParis, SilaShanghai, SilaCancun = 3
            # Total: 8 tests
            {"passed": 8, "failed": 0, "skipped": 0, "errors": 0},
            id="mixed_markers_berlin_to_prague",
        ),
        pytest.param(
            generate_param_level_mixed_test(),
            ["--from=SilaParis", "--until=SilaShanghai"],
            # Function marker: valid_until("SilaCancun") limits to <=
            # SilaCancun
            # Command line: --until=SilaShanghai further limits to <=
            # SilaShanghai
            # all_forks: SilaParis, SilaShanghai = 2 forks
            # paris_only: SilaParis, SilaShanghai = 2 forks
            # Total: 4 tests
            {"passed": 4, "failed": 0, "skipped": 0, "errors": 0},
            id="mixed_markers_paris_to_shanghai",
        ),
        pytest.param(
            generate_param_level_valid_before_test(),
            ["--from=SilaParis", "--until=SilaPrague"],
            # before_cancun: SilaParis, SilaShanghai = 2 forks
            # before_paris: none (SilaParis is not < SilaParis)
            # Total: 2 tests
            {"passed": 2, "failed": 0, "skipped": 0, "errors": 0},
            id="param_level_valid_before_paris_to_prague",
        ),
        pytest.param(
            generate_param_level_valid_before_test(),
            ["--from=SilaBerlin", "--until=SilaPrague"],
            # before_cancun: SilaBerlin, SilaLondon, SilaParis, SilaShanghai =
            # 4
            # before_paris: SilaBerlin, SilaLondon = 2
            # Total: 6 tests
            {"passed": 6, "failed": 0, "skipped": 0, "errors": 0},
            id="param_level_valid_before_berlin_to_prague",
        ),
    ],
)
def test_param_level_validity_markers(
    pytester: pytest.Pytester,
    test_function: str,
    outcomes: dict,
    pytest_args: List[str],
) -> None:
    """
    Test param-level validity markers (valid_from, valid_until, valid_before).

    The pytest_collection_modifyitems hook filters tests based on param-level
    markers after parametrization, allowing different parameter values to have
    different fork validity ranges.
    """
    pytester.makepyfile(test_function)
    pytester.copy_example(
        name="src/execution_testing/cli/pytest_commands/pytest_ini_files/pytest-fill.ini"
    )
    result = pytester.runpytest(
        "-c",
        "pytest-fill.ini",
        "-v",
        *pytest_args,
    )
    result.assert_outcomes(**outcomes)
