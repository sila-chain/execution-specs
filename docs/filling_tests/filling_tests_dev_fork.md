# Filling Tests for Features under Development

## Requirements

By default, the execution-testing framework only generates fixtures for forks that have been deployed to sila-mainnet. In order to generate fixtures for evm features that are actively under development:

1. A version of the `evm` and `solc` tools that implement the feature must be available (although, typically only a developer version of the `evm` tool is required, usually the latest stable release of `solc` is adequate), and,
2. The development fork to test must be explicitly specified on the command-line:

    === "via the `--fork` flag"

          ```console
          uv run fill -k 4844 --fork=SilaCancun -v
          ```

    === "via the `--from` flag"

          ```console
          uv run fill -k 4844 --from=SilaCancun -v
          ```

    === "via the `--until` flag"

          ```console
          uv run fill -k 4844 --until=SilaCancun -v
          ```

!!! note "Specifying the `evm` binary via `sivm-bin`"
     It is possible to explicitly specify the `evm` binary used to generate fixtures via the `--sivm-bin` flag, for example,

     ```console
     uv run fill --fork=SilaCancun --sivm-bin=/opt/bin/sivm -v
     ```

## Further Help

1. [`gsil`/`sivm` build documentation](https://github.com/sila-chain/go-sila#building-the-source).
2. [`solc` build documentation](https://docs.soliditylang.org/en/v0.8.20/installing-solidity.html#building-from-source).

!!! note "Verifying `evm` and `solc` versions used"
     The versions used to generate fixtures are displayed in the console output:
     <figure markdown>  <!-- markdownlint-disable MD033 (MD033=no-inline-html) -->
          ![Screenshot of pytest test collection console output](./img/pytest_run_example.png){align=center}
     </figure>
