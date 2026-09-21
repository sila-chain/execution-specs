# AGENTS.md

Sila Execution Layer Specification written in Python. This is a **specification**, not production code — readability over performance.

## Tooling

- **uv** is the package manager. **just** is the command runner (`just --list`).
- The `execution_testing` package under `packages/testing/` is a UV workspace member.

## Linting

When done with changes, ask the user if they'd like to run `/lint` before committing. Don't skip this unless the user explicitly says to.

## Code Style

- 79 char lines, strict mypy, `pathlib` over `os.path`
- `snake_case` for variables/functions, `PascalCase` for classes, `UPPER_CASE` for constants
- Docstrings: imperative mood ("Return" not "Returns"), blank line after summary for multi-line
- Descriptive English names — avoid SIP numbers in identifiers
- Custom spell-check dictionary: `whitelist.txt`

## Architecture

- Each fork under `src/sila/forks/` is a **complete copy** of its predecessor (WET principle). Do NOT abstract across forks.
- Import isolation (enforced by `sila-spec-lint`): relative imports within a fork, absolute from previous fork only, shared modules (`sila.crypto`, `sila.utils`) always OK. Never import from future or ancient (2+ back) forks.

## Branches

- **There is no `main` branch.** Default branch = most active fork (currently `forks/amsterdam`). Run `git remote show origin | grep HEAD` to check.
- `sila-mainnet` = stable specs for forks live on sila-mainnet
- PRs target the default branch
- PRs strictly follow the template in `.github/PULL_REQUEST_TEMPLATE.md`.
- Never add Claude attribution links (`Claude-Session:` trailers or `claude.ai` URLs) to commit messages or PR descriptions.

## PR Reviews

Reviews are strictly read-only. Never submit a GitHub review, post review
findings as a PR or issue comment, approve, request changes, or react to review
threads. Return findings in chat or write them to a local draft instead.

When reviewing PRs that implement or test SIPs:

1. Identify the SIP number(s) from the branch name, PR title, or changed file paths
2. Fetch each SIP spec from `https://sips.sila.org/SIPS/sip-<number>` before starting the review
3. Verify the implementation matches the SIP's specification requirements

## When to Use Skills

The skills below are canonical under `.agents/skills/`. Claude exposes the same
skills as `/name` commands through symlinked folders in `.claude/skills/`.

- Writing or modifying tests → run `/write-test` first
- Cleaning up or future-proofing a `tests/ported_static/` test → run `/enhance-ported-test` first
- Writing or modifying pytester-based plugin tests → run `/pytester` first
- Filling test fixtures → run `/fill-tests` first
- Implementing an SIP or modifying fork code in `src/` → run `/implement-sip` first
- Modifying GitHub Actions workflows → run `/edit-workflow` first
- Assessing SIP complexity or scope → run `/assess-sip`
- Working on SIP test coverage or checklists → run `/sip-checklist` first
- Checking if config/skills are stale → run `/audit-config`
- Writing or modifying docstrings in `src/sila/` → run `/write-docstring` first
- Done with changes and ready to lint → run `/lint`

## Available Skills

- `/write-test` — test writing patterns, fixtures, markers, bytecode helpers
- `/enhance-ported-test` — ordered methodology to clean up & future-proof `tests/ported_static/` tests
- `/pytester` — pytester execution modes, isolation, output handling for plugin tests
- `/fill-tests` — `fill` CLI reference, flags, debugging, benchmark tests
- `/implement-sip` — fork structure, import rules, adding opcodes/precompiles/tx types
- `/edit-workflow` — GitHub Actions conventions and version pinning
- `/assess-sip` — structured SIP complexity assessment
- `/sip-checklist` — SIP testing checklist system for tracking coverage
- `/lint` — full static analysis suite with auto-fix workflow
- `/audit-config` — verify AGENTS.md and skills are still accurate
- `/write-docstring` — narrative Markdown docstring conventions for the spec
- `/grammar-check` — audit grammar in documentation and code comments
