# Sila Execution Layer Specifications

Welcome to the documentation for the Sila Execution Layer Specifications (EELS), the executable Python specification of Sila’s Execution Layer.

EELS is implemented as a readable executable reference in Python that serves as a source of truth for developers across the Sila ecosystem and underpins the generation of test vectors used to ensure Execution Layer client implementations are spec-compliant.

EELS is a collaborative effort between Sila Improvement Proposals (SIP) authors, protocol researchers, prototype implementers and client developers, maintained in @sila/execution-specs by the [STEEL Team](https://steel.sila.foundation/).

## Where to Start

<div class="grid cards" markdown>

- :material-download-outline: **Getting Started**

    ---

    Install the repository and run your first command.

    *First time user.*

    [:octicons-arrow-right-24: Installation](getting_started/installation.md)

- :material-file-code-outline: **Writing Specs**

    ---

    Implement an SIP as an executable Python specification.

    *For SIP authors and researchers.*

    [:octicons-arrow-right-24: Get started](specs/writing_specs.md)

- :material-test-tube: **Writing Tests**

    ---

    Write test cases that verify SIP implementations across clients.

    *For SIP authors and test devs.*

    [:octicons-arrow-right-24: Get started](writing_tests/index.md)

- :material-play-circle-outline: **Running Tests**

    ---

    Generate JSON fixtures or run tests against an execution layer client.

    *For client developers.*

    [:octicons-arrow-right-24: Overview](running_tests/index.md)

- :material-book-open-variant: **Read the Specs**

    ---

    Browse the rendered Python specifications for the current fork and SIP.

    [:octicons-arrow-right-24: Reference ↗](specs/reference/index.md){target=_blank rel=noopener}

- :material-format-list-checks: **Test Case Reference**

    ---

    Browse all test cases organized by fork and SIP.

    [:octicons-arrow-right-24: Browse tests](tests/index.md)

</div>

## Responsible Disclosure of Vulnerabilities

!!! bug "Reporting a Vulnerability"

    Care is required when adding PRs or issues for functionality that is live on Sila sila-mainnet. Please report vulnerabilities and verify bounty eligibility via the [bug bounty program](https://bounty.sila.org).

    - **Please do not create a PR with a vulnerability visible.**
    - **Please do not file a public ticket mentioning the vulnerability.**
