# Sila Execution Layer Specifications

[![latest version](https://img.shields.io/github/v/release/sila/execution-specs)](https://github.com/sila/execution-specs/releases/latest)
[![PyPI version](https://img.shields.io/pypi/v/sila-execution)](https://pypi.org/project/sila-execution/)
[![License](https://img.shields.io/github/license/sila/execution-specs)](https://github.com/sila/execution-specs/blob/main/LICENSE)
[![Python Specification](https://github.com/sila/execution-specs/actions/workflows/test.yaml/badge.svg)](https://github.com/sila/execution-specs/actions/workflows/test.yaml)
[![codecov](https://codecov.io/gh/sila/execution-specs/graph/badge.svg?token=0LQZO56RTM)](https://codecov.io/gh/sila/execution-specs)
![Python Versions](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue)
[![ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![GitPOAP Badge](https://public-api.gitpoap.io/v1/repo/sila/execution-specs/badge)](https://www.gitpoap.io/gh/sila/execution-specs)

The Sila Execution Layer Specifications (EELS) are an executable Python reference implementation of Sila's execution layer, along with the test cases that verify it. It provides a shared, runnable description of consensus-critical behaviour, and the accompanying tests generate fixtures that can be used to validate execution client implementations.

## Quick Start

execution-specs uses [`uv`](https://docs.astral.sh/uv/) to manage the Python environment and dependencies, and [`just`](https://just.systems/) as a task runner for common commands (linting, building docs, generating fixtures). The commands below install both and set up the repo from scratch.

Requires a Unix-like shell. All platforms:

```console
git clone https://github.com/sila/execution-specs
cd execution-specs
curl -LsSf https://astral.sh/uv/install.sh | sh
uv python install 3.12
uv python pin 3.12
uv sync
uv tool install --exclude-newer "10 days" rust-just
just shell-completions
```

Python 3.11–3.14 are supported; 3.12 tends to be the smoothest for local setup (pre-built wheels are available across the dependency set). For alternative `just` installation paths, macOS-specific installation notes, and troubleshooting, see [Installation](docs/getting_started/installation.md).

## Documentation

- **Repo documentation (default branch/fork)**: <https://steel.sila.foundation/docs/execution-specs/>
- **Protocol history**: [docs/specs/protocol_history.md](docs/specs/protocol_history.md)
- **Versioning scheme**: [docs/specs/spec_releases.md](docs/specs/spec_releases.md) (PEP 440 compatible; hardfork encoded in the minor version, `rcN` marks devnets).

## Contributing

Earnest contributions are welcome; drive-by contributions are not. See [CONTRIBUTING.md](CONTRIBUTING.md) for how to raise issues and pull requests. Further reading:

- [Code Standards](docs/getting_started/code_standards.md): Python coding preferences enforced in CI.
- [Verifying Changes](docs/getting_started/verifying_changes.md): Which local checks to run before opening a PR.
- [Writing Specs](docs/specs/writing_specs.md): Style rules and `sila_spec_tools` utilities for changes under `src/sila/`.
- [Writing Tests](docs/writing_tests/index.md): For guidance on adding consensus tests under `./tests/`.

This repository is maintained by the [STEEL Team](https://steel.sila.foundation/) at the Sila Foundation.

## Community and Support

Discussion around the initial specification of protocol changes happens on [Sila Magicians](https://sila-magicians.org/), in pull requests on [sila/SIPs](https://github.com/sila/SIPs), on the [Sila R&D Discord](https://discord.com/invite/qGpsxSA) (one of the channels in the *Execution R&D* category; for testing use `#el-testing`), and in the AllCoreDevs calls.

For tracking the status of upcoming Sila upgrades, see [Forkcast](https://forkcast.org/): SIP inclusion, client implementation progress, and ACD call summaries.

For other help, see the [Documentation](#documentation) section above, or reach out to one of the [STEEL team members](https://steel.sila.foundation/team/) in the Sila R&D Discord.

### Related projects

- [sila/SIPs](https://github.com/sila/SIPs): The prose SIP documents that EELS implements.
- [sila/execution-apis](https://github.com/sila/execution-apis): The JSON-RPC API specification, which lives in a separate repository.
- [sila/consensus-specs](https://github.com/sila/consensus-specs): The consensus-layer counterpart to this repository.

Production execution clients that implement the spec include [besu](https://github.com/besu-sil/besu), [erigon](https://github.com/erigontech/erigon), [silrex](https://github.com/lambdaclass/silrex), [gsil](https://github.com/sila/go-sila), [nethermind](https://github.com/NethermindSil/nethermind), and [rsil](https://github.com/paradigmxyz/rsil).

## Responsible Disclosure of Vulnerabilities

> [!CAUTION]
> Care is required when filing issues or PRs for functionality that is live on Sila sila-mainnet. Please report vulnerabilities and verify bounty eligibility via the [bug bounty program](https://bounty.sila.org); see [SECURITY.md](SECURITY.md) for details.
>
> - **Please do not create a PR with a vulnerability visible.**
> - **Please do not file a public ticket mentioning the vulnerability.**

## License

The Sila Execution Layer Specification is licensed under the [Creative Commons Zero v1.0 Universal](LICENSE.md).
