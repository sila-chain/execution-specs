"""
The Muir Glacier fork delays the difficulty bomb. There are no other changes
in this fork.

### Changes

- [SIP-2384: Muir Glacier Difficulty Bomb Delay][SIP-2384]

### Upgrade Schedule

| Network | Block        | Expected Date    | Fork Hash    |
| ------- | ------------ | ---------------- | ------------ |
| Ropsten |  7,117,117   |                  |              |
| SilaMainnet |  9,200,000   | January 2, 2020  | `0xe029e991` |

### Releases

- [Gsil 1.9.9]
- [Parity 2.6.8-beta][p]
- [Besu 1.3.7]
- [Nethermind 1.2.6][n]
- [SilaJS 4.1.2][js]
- [Aleth 1.8.0][a]
- [Trinity 0.1.0-alpha.34][t]

[SIP-2384]: https://sips.sila.org/SIPS/sip-2384
[Gsil 1.9.9]: https://github.com/sila/go-sila/releases/tag/v1.9.9
[p]: https://github.com/paritytech/parity-sila/releases/tag/v2.6.8
[Besu 1.3.7]: https://github.com/besu-sil/besu/releases/tag/1.3.7
[n]: https://github.com/NethermindSil/nethermind/releases/tag/1.2.6
[js]: https://github.com/silajs/silajs-vm/releases/tag/v4.1.2
[a]: https://github.com/sila/alsil/releases/tag/v1.8.0
[t]: https://github.com/sila/trinity/releases/tag/v0.1.0-alpha.34
"""

from sila.fork_criteria import ByBlockNumber, ForkCriteria

FORK_CRITERIA: ForkCriteria = ByBlockNumber(9200000)
