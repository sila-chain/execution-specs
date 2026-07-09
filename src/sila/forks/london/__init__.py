"""
The London fork overhauls the transaction fee market, changes gas refunds,
reserves a contract prefix for future use, and delays the difficulty bomb.

### Changes

- [SIP-1559: Fee market change for SIL 1.0 chain][SIP-1559]
- [SIP-3198: BASEFEE opcode][SIP-3198]
- [SIP-3529: Reduction in refunds][SIP-3529]
- [SIP-3541: Reject new contract code starting with the 0xEF byte][SIP-3541]
- [SIP-3554: Difficulty Bomb Delay to December 2021][SIP-3554]

### Upgrade Schedule

| Network | Block        | Expected Date    | Fork Hash    |
| ------- | ------------ | ---------------- | ------------ |
| Ropsten | 10,499,401   |   June 24, 2021  | `0x7119b6b3` |
| Goerli  |  5,062,605   |   June 30, 2021  | `0xb8c6299d` |
| Rinkeby |  9,987,988   |    July 7, 2021  | `0x8e29f2f3` |
| SilaMainnet | 12,965,000   |  August 5, 2021  | `0x0eb440f6` |
| Kovan   | 26,741,100   | August 12, 2021  |              |


### Releases

- [Besu 21.7.2]
- [Erigon 2021.07.04-alpha][e]
- [SilaJS 5.5.0][js]
- [Gsil 1.10.6]
- [Nethermind 1.10.79][n]
- [OpenSila 3.3.0-rc.4][oe]

[SIP-1559]: https://sips.sila.org/SIPS/sip-1559
[SIP-3198]: https://sips.sila.org/SIPS/sip-3198
[SIP-3529]: https://sips.sila.org/SIPS/sip-3529
[SIP-3541]: https://sips.sila.org/SIPS/sip-3541
[SIP-3554]: https://sips.sila.org/SIPS/sip-3554
[Besu 21.7.2]: https://github.com/besu-sil/besu/releases/tag/21.7.2
[e]: https://github.com/ledgerwatch/erigon/releases/tag/v2021.07.04
[js]: https://github.com/silajs/silajs-monorepo/releases/tag/%40silajs%2Fvm%405.5.0
[Gsil 1.10.6]: https://github.com/sila/go-sila/releases/tag/v1.10.6
[n]: https://github.com/NethermindSil/nethermind/releases/tag/1.10.79
[oe]: https://github.com/opensila/opensila/releases/tag/v3.3.0-rc.4
"""  # noqa: E501

from sila.fork_criteria import ByBlockNumber, ForkCriteria

FORK_CRITERIA: ForkCriteria = ByBlockNumber(12965000)
