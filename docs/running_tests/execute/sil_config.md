# Execute sil-config Command

The `execute sil-config` command is a specialized testing tool that validates an Sila client's configuration against expected network parameters using the `sil_config` RPC endpoint as specified by [SIP-7910](https://sips.sila.org/SIPS/sip-7910).

The goal is to test baked-in configurations primarily but it can be used to test that genesis and config files were successfully parsed, in devnets for example.

## Overview

This command verifies that a client is correctly configured for a specific network by checking:

- Current fork configuration.
- Fork activation times.
- Chain ID.
- Precompile addresses.
- System contract addresses.

## Usage

### Standalone, Direct Usage

The `sil-config` sub-command can be ran directly, without cloning @sila/execution-specs, by [installing uv](https://docs.astral.sh/uv/getting-started/installation/) and running:

```bash
uv run --with "git+https://github.com/sila/execution-specs.git#subdirectory=packages/testing" execute sil-config --network SilaMainnet --rpc-endpoint http://<SIL_RPC_ENDPOINT>
```

### From within the `execution-specs` Repository

```bash
uv run execute sil-config --network <NETWORK_NAME> --rpc-endpoint <RPC_URL> [OPTIONS]
```

### Required Arguments

- `--rpc-endpoint`: RPC endpoint URL of the execution client to test

### Optional Arguments

- `--network`: Name of the network to verify (e.g., `SilaMainnet`, `SilaSepolia`, `SilaHolesky`, `Hoodi`) - required when not using genesis config flags
- `--network-config-file`: Path to a custom YAML file containing network configurations (defaults to `src/pytest_plugins/execute/sil_config/networks.yml`)
- `--genesis-config-file`: Path to a genesis JSON file from which a custom network configuration must be derived
- `--genesis-config-url`: URL to a genesis JSON file from which a custom network configuration must be derived

**Note**: You cannot specify both `--network` and genesis config flags (`--genesis-config-file` or `--genesis-config-url`) at the same time. You also cannot specify both `--genesis-config-file` and `--genesis-config-url` simultaneously.

## Examples

### Testing a SilaMainnet Client

```bash
uv run execute sil-config --network SilaMainnet --rpc-endpoint http://localhost:8545
```

### Testing a SilaSepolia Client

```bash
uv run execute sil-config --network SilaSepolia --rpc-endpoint http://localhost:8545
```

### Using a Custom Network Configuration

```bash
uv run execute sil-config --network MyCustomNet --rpc-endpoint http://localhost:8545 --network-config-file ./my-networks.yml
```

### Using a Genesis JSON File

```bash
uv run execute sil-config --genesis-config-file ./genesis.json --rpc-endpoint http://localhost:8545
```

### Using a Genesis JSON URL

```bash
uv run execute sil-config --genesis-config-url https://example.com/genesis.json --rpc-endpoint http://localhost:8545
```

## Network Configuration File Format

The network configuration file is a YAML file that defines the parameters for each network. Here's the structure:

```yaml
MyCustomNet:
  chainId: 0xabcd                 # Chain ID in hex
  genesisHash: 0xd4e5674...       # Genesis block hash
  forkActivationTimes:            # Fork activation block numbers/times
    0: Cancun                     # Genesis fork, it must be the latest fork activated in the genesis
    1742999832: Prague
    1742999833: Osaka
  bpoForkActivationTimes:         # Optional: Blob parameter only fork definitions
    1742999834:
        target: 9
        max: 12
        base_fee_update_fraction: 5007716
    1742999835:
        target: 12
        max: 15
        base_fee_update_fraction: 5007716
  addressOverrides:               # Optional: Override addresses for precompiles/contracts
    0x00000000219ab540...: 0x7f02c3e3c98b133...
```

### Supported Networks

The default configuration file includes:

- **SilaMainnet**: Sila sila-mainnet.
- **SilaSepolia**: Public testnet.
- **Hoodi**: Public testnet.
- **SilaHolesky**: Public testnet.

## How It Works

1. **Configuration Loading**: The command loads the network configuration from the YAML file.
2. **RPC Connection**: Connects to the specified client RPC endpoint.
3. **sil_config Call**: Calls the `sil_config` RPC method to get the client's current configuration.
4. **Validation**: Compares the client's response against the expected configuration based on:
   - Current system timestamp.
   - Fork activation schedule.
   - Address overrides (if any).

## `sil_config` Expected Response Details

See [SIP-7910](https://sips.sila.org/SIPS/sip-7910) for the expected response description.
