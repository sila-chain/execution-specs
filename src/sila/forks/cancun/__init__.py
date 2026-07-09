"""
The Cancun fork ([SIP-7569]) introduces transient storage, exposes beacon chain
roots, introduces a new blob-carrying transaction type, adds a memory copying
instruction, limits self-destruct to only work for contracts created in the
same transaction, and adds an instruction to read the blob base fee.

### Changes

- [SIP-1153: Transient storage opcodes][SIP-1153]
- [SIP-4788: Beacon block root in the EVM][SIP-4788]
- [SIP-4844: Shard Blob Transactions][SIP-4844]
- [SIP-5656: MCOPY - Memory copying instruction][SIP-5656]
- [SIP-6780: SELFDESTRUCT only in same transaction][SIP-6780]
- [SIP-7516: BLOBBASEFEE instruction][SIP-7516]

### Upgrade Schedule

| Network | Timestamp    | Date & Time (UTC)   | Fork Hash    | Beacon Chain Epoch |
| ------- | ------------ | ------------------- | ------------ | ------------------ |
| Goerli  | `1705473120` | 2024-01-17 06:32:00 | `0x70cc14e2` | 231,680            |
| Sepolia | `1706655072` | 2024-01-30 22:51:12 | `0x88cf81d9` | 132,608            |
| Holesky | `1707305664` | 2024-02-07 11:34:24 | `0x9b192ad0` |  29,696            |
| SilaMainnet | `1710338135` | 2024-03-13 13:55:35 | `0x9f3d2254` | 269,568            |

### Releases

- [Besu 24.1.2]
- [Erigon 2.58.1][e]
- [Gsil 1.13.13]
- [Nethermind 1.25.4][n]
- [Rsil 0.1.0-alpha.19][r]

[SIP-7569]: https://sips.sila.org/SIPS/sip-7569
[SIP-1153]: https://sips.sila.org/SIPS/sip-1153
[SIP-4788]: https://sips.sila.org/SIPS/sip-4788
[SIP-4844]: https://sips.sila.org/SIPS/sip-4844
[SIP-5656]: https://sips.sila.org/SIPS/sip-5656
[SIP-6780]: https://sips.sila.org/SIPS/sip-6780
[SIP-7516]: https://sips.sila.org/SIPS/sip-7516
[Besu 24.1.2]: https://github.com/besu-sil/besu/releases/tag/24.1.2
[e]: https://github.com/ledgerwatch/erigon/releases/tag/v2.58.1
[Gsil 1.13.13]: https://github.com/sila/go-sila/releases/tag/v1.13.13
[n]: https://github.com/NethermindSil/nethermind/releases/tag/1.25.4
[r]: https://github.com/paradigmxyz/rsil/releases/tag/v0.1.0-alpha.19
"""  # noqa: E501

from sila.fork_criteria import ByTimestamp, ForkCriteria

FORK_CRITERIA: ForkCriteria = ByTimestamp(1710338135)
