"""
Merge the sharded benchmark fill with the framework's own merges.

`groups <dir>...`: every shard's phase-1 `pre_alloc/<hash>.json` becomes a
`<hash>.partial.<shard>.json` and `merge_partial_group_files` merges them,
exactly as it merges the partial files of the xdist workers of one run.

`fixtures <out> <dir>...`: every shard's fixture file becomes a
`<name>.partial.<shard>.jsonl` with the lines a worker writes
(`json.dumps(fixture, indent=4)` per fixture) and
`merge_partial_fixture_files` merges them into the final files.
"""

import json
import shutil
import sys
from pathlib import Path

from execution_testing.fixtures.collector import merge_partial_fixture_files
from execution_testing.fixtures.pre_alloc_groups import (
    merge_partial_group_files,
)

PRE_ALLOC = Path("blockchain_tests_engine_x") / "pre_alloc"


def merge_groups(out: Path, shards: list[Path]) -> None:
    """Merge the phase-1 pre-allocation groups of all shards."""
    target = out / PRE_ALLOC
    target.mkdir(parents=True, exist_ok=True)
    for index, shard in enumerate(shards):
        for group in sorted((shard / PRE_ALLOC).glob("*.json")):
            name = group.name[: -len(".json")]
            shutil.copyfile(group, target / f"{name}.partial.s{index}.json")
    merge_partial_group_files(target)


def merge_fixtures(out: Path, shards: list[Path]) -> None:
    """Merge the phase-2 fixture files of all shards."""
    for index, shard in enumerate(shards):
        for fixture_file in sorted(shard.rglob("*.json")):
            relative = fixture_file.relative_to(shard)
            if relative.parts[0] == ".meta" or PRE_ALLOC in relative.parents:
                continue
            fixtures = json.loads(fixture_file.read_text())
            partial = (out / relative).with_suffix(f".partial.s{index}.jsonl")
            partial.parent.mkdir(parents=True, exist_ok=True)
            with open(partial, "w") as f:
                for key, value in fixtures.items():
                    line = {"k": key, "v": json.dumps(value, indent=4)}
                    f.write(json.dumps(line) + "\n")
    merge_partial_fixture_files(out)


if __name__ == "__main__":
    mode, out, *dirs = sys.argv[1:]
    shard_dirs = [Path(d) for d in dirs]
    if mode == "groups":
        merge_groups(Path(out), shard_dirs)
    elif mode == "fixtures":
        merge_fixtures(Path(out), shard_dirs)
    else:
        raise SystemExit(f"unknown mode {mode}")
