"""
Run one phase of a two-phase fill: `sila_benchmark_phase.py <1|2> <args>`.

The arguments are those of `fill --generate-all-formats ...`; the phase run
is the execution the `fill` command itself builds for them (phase 1
generates the pre-allocation groups, phase 2 fills the fixtures with
`--use-pre-alloc-groups`).
"""

import sys

from execution_testing.cli.pytest_commands.base import PytestRunner
from execution_testing.cli.pytest_commands.fill import FillCommand, fill

if __name__ == "__main__":
    phase, args = int(sys.argv[1]), sys.argv[2:]
    with fill.make_context("fill", list(args)):
        executions = FillCommand().create_executions(args)
        assert len(executions) == 2, "expected a two-phase fill"
        sys.exit(PytestRunner().run_single(executions[phase - 1]))
