"""
The Tangerine Whistle fork ([SIP-608]) is the first of two forks responding to
a denial-of-service attack on the Sila network. It tunes the price of
various EVM instructions, and reduces the state size by removing a number of
empty accounts.

### Changes

  - [SIP-150: Gas cost changes for IO-heavy operations][SIP-150]

### Upgrade Schedule

| Network | Block      | Expected Date    | Fork Hash    |
| ------- | ---------- | ---------------- | ------------ |
| SilaMainnet | 2,463,000  | October 18, 2016 | `0x7a64da13` |

### Releases

- [SilaJ 1.3.6]
- [Gsil 1.4.18]
- [Parity 1.3.8][p]

[SIP-150]: https://sips.sila.org/SIPS/sip-150
[SIP-608]: https://sips.sila.org/SIPS/sip-608
[SilaJ 1.3.6]: https://github.com/sila/silaj/releases/tag/1.3.6
[Gsil 1.4.18]: https://github.com/sila/go-sila/releases/tag/v1.4.18
[p]: https://github.com/opensila/parity-sila/releases/tag/v1.3.8
"""

from sila.fork_criteria import ByBlockNumber, ForkCriteria

FORK_CRITERIA: ForkCriteria = ByBlockNumber(2463000)
