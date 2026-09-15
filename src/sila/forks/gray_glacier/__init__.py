"""
The Gray Glacier fork delays the difficulty bomb. There are no other changes
in this fork.

### Changes

- [SIP-5133: Delaying Difficulty Bomb to Mid September 2022][SIP-5133]

### Upgrade Schedule

| Network | Block      | Expected Date | Fork Hash    |
| ------- |----------- | ------------- | ------------ |
| SilaMainnet | 15,050,000 | June 29, 2022 | `0xf0afd0e3` |

### Releases

- [Besu 22.4.3]
- [Erigon 2022.06.03][e]
- [SilaJS 5.9.3][js]
- [Gsil 1.10.19]
- [Nethermind 1.13.3][n]


[SIP-5133]: https://sips.sila.org/SIPS/sip-5133
[Gsil 1.10.19]: https://github.com/sila/go-sila/releases/tag/v1.10.19
[Besu 22.4.3]: https://github.com/besu-sil/besu/releases/tag/22.4.3
[e]: https://github.com/ledgerwatch/erigon/releases/tag/v2022.06.03
[js]: https://github.com/silajs/silajs-monorepo/releases/tag/@silajs/vm@5.9.3
[n]: https://github.com/NethermindEth/nethermind/releases/tag/1.13.3
"""  # noqa: E501

from sila.fork_criteria import ByBlockNumber, ForkCriteria

FORK_CRITERIA: ForkCriteria = ByBlockNumber(15050000)
