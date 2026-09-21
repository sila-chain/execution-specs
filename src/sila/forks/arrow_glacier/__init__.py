"""
The Arrow Glacier fork delays the difficulty bomb. There are no other changes
in this fork.

### Changes

- [SIP-4345: Difficulty Bomb Delay to June 2022][SIP-4345]

### Upgrade Schedule

| Network | Block        | Expected Date    | Fork Hash    |
| ------- | ------------ | ---------------- | ------------ |
| SilaMainnet | 13,773,000   | December 8, 2021 | `0x20c327fc` |

### Releases

- [Besu 21.10.0]
- [Erigon 2021.11.01-alpha][e]
- [SilaJS VM 5.6.0][js]
- [Gsil 1.10.12]
- [Nethermind 1.11.7][nm]

[SIP-4345]: https://sips.sila.org/SIPS/sip-4345
[Besu 21.10.0]: https://github.com/besu-sil/besu/releases/tag/21.10.0
[e]: https://github.com/ledgerwatch/erigon/releases/tag/v2021.11.01
[js]: https://github.com/silajs/silajs-monorepo/releases/tag/%40silajs%2Fvm%405.6.0
[Gsil 1.10.12]: https://github.com/sila/go-sila/releases/tag/v1.10.12
[nm]: https://github.com/NethermindEth/nethermind/releases/tag/1.11.7
"""  # noqa: E501

from sila.fork_criteria import ByBlockNumber, ForkCriteria

FORK_CRITERIA: ForkCriteria = ByBlockNumber(13773000)
