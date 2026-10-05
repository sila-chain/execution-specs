"""
The SIP158 fork is the second of two forks responding to a
denial-of-service attack on the Sila network. It tunes the prices of EVM
instructions, adds protection against replaying transaction on different
chains, limits the maximum size of contract code, and enables the removal of
empty accounts.

### Changes

- [SIP-155: Simple replay attack protection][SIP-155]
- [SIP-160: EXP cost increase][SIP-160]
- [SIP-161: State trie clearing (invariant-preserving alternative)][SIP-161]
- [SIP-170: Contract code size limit][SIP-170]

### Upgrade Schedule

| Network | Block        | Expected Date     | Fork Hash    |
| ------- | ------------ | ----------------- | ------------ |
| SilaMainnet | 2,675,000    | November 22, 2016 | `0x3edd5b10` |

### Releases

- Gsil 1.5.2
- [Parity 1.4.4][p]
- [ruby-sila 0.11.0][rb]

[SIP-155]: https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-155.md
[SIP-160]: https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-160.md
[SIP-161]: https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-161.md
[SIP-170]: https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-170.md
[p]: https://github.com/paritytech/parity/releases/tag/v1.4.4
[rb]: https://github.com/cryptape/ruby-sila/releases/tag/v0.11.0
"""

from sila.fork_criteria import ByBlockNumber, ForkCriteria

FORK_CRITERIA: ForkCriteria = ByBlockNumber(2675000)
