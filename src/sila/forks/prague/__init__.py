"""
The Prague fork enables deploying code into externally owned accounts (EOAs)
via the [`SetCodeTransaction`][t], increases the blob throughput, increases the
cost of calldata-heavy transactions, introduces general execution layer
requests (and two request types: [consolidation][c], and [withdrawal][w]),
appends validator deposits to execution layer blocks, creates BLS12-381
precompiles, and exposes historical block hashes through [a system
contract][b].

### Changes

- [SIP-2537: Precompile for BLS12-381 curve operations][SIP-2537]
- [SIP-2935: Serve historical block hashes from state][SIP-2935]
- [SIP-6110: Supply validator deposits on chain][SIP-6110]
- [SIP-7002: Execution layer triggerable withdrawals][SIP-7002]
- [SIP-7251: Increase the MAX_EFFECTIVE_BALANCE][SIP-7251]
- [SIP-7549: Move committee index outside Attestation][SIP-7549]
- [SIP-7623: Increase calldata cost][SIP-7623]
- [SIP-7685: General purpose execution layer requests][SIP-7685]
- [SIP-7691: Blob throughput increase][SIP-7691]
- [SIP-7840: Add blob schedule to EL config files][SIP-7840]
- [SIP-7702: Set Code for EOAs][SIP-7702]

### Upgrade Schedule

| Network | Timestamp    | Date & Time (UTC)   | Fork Hash    | Beacon Chain Epoch |
| ------- | ------------ | ------------------- | ------------ | ------------------ |
| Holesky | `1740434112` | 2025-02-24 21:55:12 |              | 115,968            |
| Sepolia | `1741159776` | 2025-03-05 07:29:36 |              | 222,464            |
| Hoodi   | `1742999832` | 2025-03-26 14:37:12 |              |   2,048            |
| SilaMainnet | `1746612311` | 2025-05-07 10:05:11 | `0xc376cf8b` | 364,032            |

### Releases

[t]: ref:sila.forks.prague.transactions.SetCodeTransaction
[c]: ref:sila.forks.prague.requests.CONSOLIDATION_REQUEST_TYPE
[w]: ref:sila.forks.prague.requests.WITHDRAWAL_REQUEST_TYPE
[b]: ref:sila.forks.prague.fork.HISTORY_STORAGE_ADDRESS
[SIP-7702]: https://sips.sila.org/SIPS/sip-7702
[SIP-7691]: https://sips.sila.org/SIPS/sip-7691
[SIP-7623]: https://sips.sila.org/SIPS/sip-7623
[SIP-7840]: https://sips.sila.org/SIPS/sip-7840
[SIP-7251]: https://sips.sila.org/SIPS/sip-7251
[SIP-7002]: https://sips.sila.org/SIPS/sip-7002
[SIP-7685]: https://sips.sila.org/SIPS/sip-7685
[SIP-6110]: https://sips.sila.org/SIPS/sip-6110
[SIP-2537]: https://sips.sila.org/SIPS/sip-2537
[SIP-2935]: https://sips.sila.org/SIPS/sip-2935
[SIP-7549]: https://sips.sila.org/SIPS/sip-7549
"""  # noqa: E501

from sila.fork_criteria import ByTimestamp, ForkCriteria

FORK_CRITERIA: ForkCriteria = ByTimestamp(1746612311)
