"""
The Shanghai fork brings staking withdrawals to the execution layer, adds a
push-zero EVM instruction, limits the maximum size of initialization
bytecode, and deprecates the self-destruct EVM instruction.

### Notices

- [SIP-6049: Deprecate SELFDESTRUCT][SIP-6049]

### Changes

- [SIP-3651: Warm COINBASE][SIP-3651]
- [SIP-3855: PUSH0 instruction][SIP-3855]
- [SIP-3860: Limit and meter initcode][SIP-3860]
- [SIP-4895: Beacon chain push withdrawals as operations][SIP-4895]

### Upgrade Schedule

| Network | Timestamp    | Date & Time (UTC)   | Fork Hash    | Beacon Chain Epoch |
| ------- | ------------ | ------------------- | ------------ | ------------------ |
| SilaSepolia | `1677557088` | 2023-02-28 04:04:48 | `0xf7f9bc08` |  56,832            |
| Goerli  | `1678832736` | 2023-03-14 22:25:36 | `0xf9843abf` | 162,304            |
| SilaMainnet | `1681338455` | 2023-04-12 22:27:35 | `0xdce96c2d` | 194,048            |


### Releases

- [Besu 23.1.2]
- [Gsil 1.11.5]
- [Erigon 2.41.0][e]
- [SilaJS 6.4.0][js]
- [Nethermind 1.17.3][n]

[SIP-3651]: https://sips.sila.org/SIPS/sip-3651
[SIP-3855]: https://sips.sila.org/SIPS/sip-3855
[SIP-3860]: https://sips.sila.org/SIPS/sip-3860
[SIP-4895]: https://sips.sila.org/SIPS/sip-4895
[Gsil 1.11.5]: https://github.com/sila/go-sila/releases/tag/v1.11.5
[Besu 23.1.2]: https://github.com/besu-sil/besu/releases/tag/23.1.2
[n]: https://github.com/NethermindEth/nethermind/releases/tag/1.17.3
[e]: https://github.com/ledgerwatch/erigon/releases/tag/v2.41.0
[js]: https://github.com/silajs/silajs-monorepo/releases/tag/%40silajs%2Fvm%406.4.0
"""  # noqa: E501

from sila.fork_criteria import ByTimestamp, ForkCriteria

FORK_CRITERIA: ForkCriteria = ByTimestamp(1681338455)
