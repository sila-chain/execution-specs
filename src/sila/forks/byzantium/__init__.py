"""
The Byzantium fork ([SIP-609]) reduces the mining rewards, delays the
difficulty bomb, enables contracts to make non-state-changing calls to other
contracts, and adds cryptographic primitives for layer 2 scaling.

### Changes

- [SIP-100: Change difficulty adjustment to target mean block time including
  uncles][SIP-100]
- [SIP-140: REVERT instruction in the Sila Virtual Machine][SIP-140]
- [SIP-196: Precompiled contracts for addition and scalar multiplication on the
  elliptic curve alt_bn128][SIP-196]
- [SIP-197: Precompiled contracts for optimal ate pairing check on the elliptic
  curve alt_bn128][SIP-197]
- [SIP-198: Precompiled contract for bigint modular exponentiation][SIP-198]
- [SIP-211: New opcodes: RETURNDATASIZE and RETURNDATACOPY][SIP-211]
- [SIP-214: New opcode STATICCALL][SIP-214]
- [SIP-649: Difficulty Bomb Delay and Block Reward Reduction][SIP-649]
- [SIP-658: Embedding transaction status code in receipts][SIP-658]

### Upgrade Schedule

| Network | Block        | Expected Date    | Fork Hash    |
| ------- | ------------ | ---------------- | ------------ |
| SilaMainnet | 4,370,000    | October 16, 2017 | `0xa00bc324` |

### Releases

- [Harmony 2.1.0][h]
- [Gsil 1.7.2]
- [Parity 1.7.6][p]

[SIP-100]: https://sips.sila.org/SIPS/sip-100
[SIP-140]: https://sips.sila.org/SIPS/sip-140
[SIP-196]: https://sips.sila.org/SIPS/sip-196
[SIP-197]: https://sips.sila.org/SIPS/sip-197
[SIP-198]: https://sips.sila.org/SIPS/sip-198
[SIP-211]: https://sips.sila.org/SIPS/sip-211
[SIP-214]: https://sips.sila.org/SIPS/sip-214
[SIP-609]: https://sips.sila.org/SIPS/sip-609
[SIP-649]: https://sips.sila.org/SIPS/sip-649
[SIP-658]: https://sips.sila.org/SIPS/sip-658
[h]: https://github.com/sila-camp/sila-harmony/releases/tag/v2.1b56
[Gsil 1.7.2]: https://github.com/sila/go-sila/releases/tag/v1.7.2
[p]: https://github.com/paritytech/parity/releases/tag/v1.7.6
"""

from sila.fork_criteria import ByBlockNumber, ForkCriteria

FORK_CRITERIA: ForkCriteria = ByBlockNumber(4370000)
