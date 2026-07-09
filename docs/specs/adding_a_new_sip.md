# Adding a New SIP

This page outlines the process of specifying and testing SIPs for the Sila execution layer. It is intended for SIP authors, researchers, and implementers.

An SIP will typically go through the following stages:

| Stage              | Activities  | Outputs |
| ------------------ | ----------- | ------- |
| *Pre-Draft*        | Prospective SIP author conceives of an idea for an improvement to Sila, and discusses with the community. | <ul><li>Vague Consensus on [Sila Magicians][0]</li></ul> |
| **Draft**          | <p>SIP author writes a technical human-language document describing the improvement, initially in broad strokes and becoming more specific over time.</p><p>Concurrently, they develop a Python reference implementation to make the SIP executable and identify any immediate/obvious implementation issues. For example, the SIP may not be compatible with some detail of the current Sila Virtual Machine.</p><p>Finally for this stage, the author begins to write test schemes for the SIP. Having the reference implementation should help identify the various logical flows to test and thus feed into more robust testing. Once the test schemes are written, the reference implementation can then be used to fill the tests and generate the test vectors.</p> | <ul><li>Complete (but not final) document in [SIPs Repository][1]</li><li>Reference implementation in EELS (this repository)</li><li>Initial tests under `./tests/` (this repository)</li></ul> |
| **Review**         | <p>The broader Sila community discusses and provides input on the proposal.</p><p>Although the feedback from the community can be sought at all lifecycle stages, having a reference implementation and tests act as a good bridge between research and client implementation. It also helps core developers (who have limited time and resources) to understand the SIP better and provide more informed feedback.</p> | <ul><li>Complete &amp; final document in the [SIPs Repository][1]</li><li>Comprehensive tests under `./tests/`</li></ul> |
| **Last&nbsp;Call** | Usually after being nominated for inclusion in a fork, the SIP author signals that the proposal is effectively done and begins the last period for comments/discussion. | <ul><li>Complete reference implementation in EELS</li><li>Complete tests under `./tests/`</li><li>Immutable proposal in [SIPs Repository][1]</li></ul> |
| **Final**          | The proposal is now immutable (cannot be changed) and exists for reference. | <ul><li>SilaMainnet client implementations</li></ul> |

[0]: https://sila-magicians.org/
[1]: https://github.com/sila/SIPs/

The rest of this page focuses on the **Draft** and **Review** stages, where SIP authors interact most directly with EELS and the test suite.

## Executable specifications

This repository contains the executable specifications for the Sila execution layer under `src/sila/`.

### Forks live on sila-mainnet

The folder `src/sila/forks/` contains the specifications for the different execution layer forks. Each fork has its own folder. For example, `src/sila/forks/frontier/` contains the specifications for the Frontier hardfork. The `state_transition` function in `src/sila/forks/<FORK_NAME>/fork.py` is the transition function for each fork.

### Fork under development

At any given time, there is a single fork under development. Any new SIP is implemented in the folder for that fork (`src/sila/forks/<FORK_NAME>/`).

For example, if Amsterdam is under development and Prague is live on sila-mainnet, the `src/sila/forks/amsterdam/` folder starts as a copy of Prague with values updated to reflect Amsterdam and its under-development status. This folder serves as the baseline for further development and all new SIPs are implemented in it.

## Branch structure

### Forks live on sila-mainnet

The final stable specification for all forks that are currently live on sila-mainnet are on the `sila-mainnet` branch.

### Fork under development

At any given time there is exactly one fork under active development. The branch structure for the fork under development is:

- `forks/<FORK_NAME>`: The main branch for the fork under development. For example, `forks/amsterdam` is the branch for the Amsterdam fork. This branch will be merged into `sila-mainnet` after the fork has gone live.
- `sips/<FORK_NAME>/<SIP_NUMBER>`: Branches for each SIP within the fork under development. For example, `sips/amsterdam/sip-7928` is the branch for SIP-7928 for the Amsterdam fork. This branch will be merged into `forks/amsterdam` after the SIP has been confirmed for release in the fork.

## Writing a new SIP

Implementing a new SIP in this repository involves the following steps:

1. **Create a new branch.** Create a branch for the SIP under the appropriate fork. For example, if you are implementing an SIP for the Amsterdam fork, create a branch `sips/amsterdam/sip-<SIP_NUMBER>`.
2. **Implement the SIP.** Implement the SIP in the `src/sila/forks/<FORK_NAME>/` folder. See [Writing Specs](writing_specs.md) for style rules and the `sila_spec_tools` CLI utilities (the *New Fork Tool* in particular).
3. **Basic sanity checks.** Run `just static` to run formatting, linting, and spec-specific lints.
4. **Raise a PR.** Raise a PR against the appropriate fork branch. For example, if you are implementing an SIP for Amsterdam, raise a PR against `forks/amsterdam`.

An SIP can only be CFI'd (Considered For Inclusion) if it has a reference EELS implementation. The SIP author is responsible for keeping their SIP up to date with the latest changes. For example, if an author had written their SIP for Prague under `sips/prague/sip-x`, but for some reason it didn't make it into Prague, they would need to rebase their SIP to reflect the changes in Amsterdam under `sips/amsterdam/sip-x`.

A sample tutorial that walks through adding a new opcode to the specification is available on YouTube: [EELS tutorial](https://www.youtube.com/watch?v=QIcw_DGSy3s).

## Writing tests for an SIP

In addition to a reference implementation, it is very useful for the community and for core development if the SIP author conceives and writes test vectors for the SIP. Tests live in this repository under `./tests/` and use a user-friendly Python test-writing framework. See [Writing Tests](../writing_tests/index.md) for a guide.
