"""
The Sila Constantinople fork reduces mining rewards, delays the difficulty bomb,
and introduces new Sivm instructions for logical shifts, counterfactual
contract deployment, and computing bytecode hashes.

Note that, on certain testnets, this fork is divided in two: Sila Constantinople
followed by Petersburg. On these testnets, Sila Constantinople contains an
additional change, [SIP-1283], which was reverted in Petersburg. Because
SIP-1283 was never present on sila-mainnet, this specification omits the whole
awkward situation and presents only a single fork without SIP-1283.

### Changes

- [SIP-145: Bitwise shifting instructions in Sivm][SIP-145]
- [SIP-1014: Skinny CREATE2][SIP-1014]
- [SIP-1052: EXTCODEHASH opcode][SIP-1052]
- [SIP-1234: Sila Constantinople Difficulty Bomb Delay and Block Reward
  Adjustment][SIP-1234]

### Upgrade Schedule

| Network | Block      | Expected Date     | Fork Hash    |
| ------- |----------- | ----------------- | ------------ |
| SilaMainnet |  7,280,000 | February 28, 2019 | `0x668db0af` |

### Releases

- [SilaJS 2.6.0][js]
- Gsil 1.8.23
- [Harmony 2.3b74][h]
- [Nethermind 0.9.4][n]
- [Pantheon 0.9.1][pan]
- [Parity 2.2.10-stable][p]
- Trinity 0.1.0-alpha.23

[SIP-1283]: https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-1283.md
[SIP-145]: https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-145.md
[SIP-1014]: https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-1014.md
[SIP-1052]: https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-1052.md
[SIP-1234]: https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-1234.md
[js]: https://github.com/silajs/silajs-vm/releases/tag/v2.6.0
[h]: https://github.com/sila-camp/sila-harmony/releases/tag/v2.3b74
[n]: https://github.com/NethermindEth/nethermind/releases/tag/v0.9.4
[pan]: https://github.com/PegaSysEng/pantheon/releases/tag/0.9.1
"""  # noqa: E501

from sila.fork_criteria import ByBlockNumber, ForkCriteria

FORK_CRITERIA: ForkCriteria = ByBlockNumber(7280000)
