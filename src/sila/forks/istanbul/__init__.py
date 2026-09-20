"""
The Istanbul fork ([SIP-1679]) makes changes to the gas costs of EVM
instructions and data, adds a cryptographic primitive, and introduces an
instruction to fetch the current chain identifier.

### Changes

- [SIP-152: Add BLAKE2 compression function `F` precompile][SIP-152]
- [SIP-1108: Reduce alt_bn128 precompile gas costs][SIP-1108]
- [SIP-1344: ChainID opcode][SIP-1344]
- [SIP-1884: Repricing for trie-size-dependent opcodes][SIP-1884]
- [SIP-2028: Transaction data gas cost reduction][SIP-2028]
- [SIP-2200: Structured Definitions for Net Gas Metering][SIP-2200]

### Upgrade Schedule

| Network | Block        | Expected Date    | Fork Hash    |
| ------- | ------------ | ---------------- | ------------ |
| Ropsten |  6,485,846   |                  |              |
| Goerli  |  1,561,651   |                  |              |
| Rinkeby |  5,435,345   |                  |              |
| Kovan   | 14,111,141   |                  |              |
| SilaMainnet |  9,069,000   | December 8, 2019 | `0x879d6e30` |

### Releases

- [Aleth 1.7.1][a]
- [Besu 1.3.6]
- [SilaJS 4.0.2][js]
- [Gsil 1.9.9]
- [Nethermind 1.2.3][n]
- [Parity 2.5.11-stable][p]
- [Trinity 0.1.0-alpha.31][t]

[SIP-1679]: https://sips.sila.org/SIPS/sip-1679
[SIP-152]: https://sips.sila.org/SIPS/sip-152
[SIP-1108]: https://sips.sila.org/SIPS/sip-1108
[SIP-1344]: https://sips.sila.org/SIPS/sip-1344
[SIP-1884]: https://sips.sila.org/SIPS/sip-1884
[SIP-2028]: https://sips.sila.org/SIPS/sip-2028
[SIP-2200]: https://sips.sila.org/SIPS/sip-2200
[a]: https://github.com/sila/aleth/releases/tag/v1.7.1
[Besu 1.3.6]: https://github.com/besu-sil/besu/releases/tag/1.3.6
[js]: https://github.com/silajs/silajs-blockchain/releases/tag/v4.0.2
[Gsil 1.9.9]: https://github.com/sila/go-sila/releases/tag/v1.9.9
[n]: https://github.com/NethermindEth/nethermind/releases/tag/1.2.3
[p]: https://github.com/paritytech/parity-sila/releases/tag/v2.5.11
[t]: https://github.com/sila/trinity/releases/tag/v0.1.0-alpha.31
"""

from sila.fork_criteria import ByBlockNumber, ForkCriteria

FORK_CRITERIA: ForkCriteria = ByBlockNumber(9069000)
