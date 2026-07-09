"""
The Constantinople fork reduces mining rewards, delays the difficulty bomb,
and introduces new EVM instructions for logical shifts, counterfactual
contract deployment, and computing bytecode hashes.

Note that, on certain testnets, this fork is divided in two: Constantinople
followed by Petersburg. On these testnets, Constantinople contains an
additional change, [SIP-1283], which was reverted in Petersburg. Because
SIP-1283 was never present on sila-mainnet, this specification omits the whole
awkward situation and presents only a single fork without SIP-1283.

### Changes

- [SIP-145: Bitwise shifting instructions in EVM][SIP-145]
- [SIP-1014: Skinny CREATE2][SIP-1014]
- [SIP-1052: EXTCODEHASH opcode][SIP-1052]
- [SIP-1234: Constantinople Difficulty Bomb Delay and Block Reward
  Adjustment][SIP-1234]

### Upgrade Schedule

| Network | Block      | Expected Date     | Fork Hash    |
| ------- |----------- | ----------------- | ------------ |
| SilaMainnet |  7,280,000 | February 28, 2019 | `0x668db0af` |

### Releases

- [SilaJS 2.6.0][js]
- [Gsil 1.8.23]
- [Harmony 2.3b74][h]
- [Nethermind 0.9.4][n]
- [Pantheon 0.9.1][pan]
- [Parity 2.2.10-stable][p]
- [Trinity 0.1.0-alpha.23][t]

[SIP-1283]: https://sips.sila.org/SIPS/sip-1283
[SIP-145]: https://sips.sila.org/SIPS/sip-145
[SIP-1014]: https://sips.sila.org/SIPS/sip-1014
[SIP-1052]: https://sips.sila.org/SIPS/sip-1052
[SIP-1234]: https://sips.sila.org/SIPS/sip-1234
[js]: https://github.com/silajs/silajs-vm/releases/tag/v2.6.0
[Gsil 1.8.23]: https://github.com/sila/go-sila/releases/tag/v1.8.23
[h]: https://github.com/sila-camp/sila-harmony/releases/tag/v2.3b74
[n]: https://github.com/NethermindSil/nethermind/releases/tag/v0.9.4
[pan]: https://github.com/PegaSysEng/pantheon/releases/tag/0.9.1
[t]: https://github.com/sila/trinity/releases/tag/v0.1.0-alpha.23
"""  # noqa: E501

from sila.fork_criteria import ByBlockNumber, ForkCriteria

FORK_CRITERIA: ForkCriteria = ByBlockNumber(7280000)
