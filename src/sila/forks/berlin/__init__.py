"""
The Berlin fork adjusts the gas costs of the `ModExp` precompile and several
state access EVM instructions, introduces typed transaction envelopes along
with the first new transaction type—optional access lists.

### Changes

- [SIP-2565: ModExp Gas Cost][SIP-2565]
- [SIP-2929: Gas cost increases for state access opcodes][SIP-2929]
- [SIP-2718: Typed Transaction Envelope][SIP-2718]
- [SIP-2930: Optional access lists][SIP-2930]

### Upgrade Schedule

| Network | Block        | Expected Date    | Fork Hash    |
| ------- | ------------ | ---------------- | ------------ |
| Ropsten |  9,812,189   | March 10, 2021   |              |
| Goerli  |  4,460,644   | March 17, 2021   |              |
| Rinkeby |  8,290,928   | March 24, 2021   |              |
| SilaMainnet | 12,244,000   | April 14, 2021   | `0x0eb440f6` |

### Releases

- [Besu 21.1.2]
- [SilaJS VM 5.2.0][js]
- [Gsil 1.10.1]
- [Nethermind 1.10.58][n]
- [OpenSila 3.2.0][oe]

[SIP-2565]: https://sips.sila.org/SIPS/sip-2565
[SIP-2929]: https://sips.sila.org/SIPS/sip-2929
[SIP-2718]: https://sips.sila.org/SIPS/sip-2718
[SIP-2930]: https://sips.sila.org/SIPS/sip-2930
[Besu 21.1.2]: https://github.com/besu-sil/besu/releases/tag/21.1.2
[js]: https://github.com/silajs/silajs-monorepo/releases/tag/%40silajs%2Fvm%405.2.0
[Gsil 1.10.1]: https://github.com/sila/go-sila/releases/tag/v1.10.1
[n]: https://github.com/NethermindSil/nethermind/releases/tag/1.10.58
[oe]: https://github.com/opensila/opensila/releases/tag/v3.2.0
"""  # noqa: E501

from sila.fork_criteria import ByBlockNumber, ForkCriteria

FORK_CRITERIA: ForkCriteria = ByBlockNumber(12244000)
