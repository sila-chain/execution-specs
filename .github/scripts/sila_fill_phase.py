"""
Run one phase of a two-phase fill: `sila_fill_phase.py <1|2> <fill args>`.

The phase run is the execution the `fill` command itself builds for the
arguments. Phase 1 of a shard skips the master's packing of the
pre-allocation groups: packing needs every group, so it runs once, after
the groups of all shards are merged (`sila_fill_merge.py groups`). The
phase-1 summary then counts the accounts of the unpacked (builder format)
group files.
"""

import sys
from pathlib import Path

from execution_testing.cli.pytest_commands.base import PytestRunner
from execution_testing.cli.pytest_commands.fill import FillCommand, fill
from execution_testing.cli.pytest_commands.plugins.filler import filler
from execution_testing.fixtures.pre_alloc_groups import PreAllocGroupBuilder


class _UnpackedGroup:
    """Account count of a phase-1 group file in builder format."""

    def __init__(self, builder: PreAllocGroupBuilder) -> None:
        self.pre_account_count = builder.get_pre_account_count()

    @classmethod
    def from_file(cls, file: Path) -> "_UnpackedGroup":
        return cls(PreAllocGroupBuilder.from_file(file))


def _skip_packing(folder: Path) -> None:
    """Leave the phase-1 groups of a shard unpacked."""
    del folder


if __name__ == "__main__":
    phase, args = int(sys.argv[1]), sys.argv[2:]
    if phase == 1:
        filler.pack_pre_alloc_groups = _skip_packing
        filler.PreAllocGroup = _UnpackedGroup  # type: ignore[misc,assignment]
    with fill.make_context("fill", list(args)):
        executions = FillCommand().create_executions(args)
        assert len(executions) == 2, "expected a two-phase fill"
        sys.exit(PytestRunner().run_single(executions[phase - 1]))
