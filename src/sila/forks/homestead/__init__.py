"""
The Homestead fork increases the gas cost of creating contracts, restricts the
range of valid ECDSA signatures for transactions (but not precompiles), tweaks
the behavior of contract creation with insufficient gas, delays the
difficulty bomb, and adds an improved delegate call EVM instruction.

### Changes

- [SIP-2: Homestead Hard-fork Changes][SIP-2]
- [SIP-7: DELEGATECALL][SIP-7]
- [SIP-8: devp2p Forward Compatibility Requirements for Homestead][SIP-8]

### Upgrade Schedule

| Network | Block        | Expected Date    | Fork Hash    |
| ------- | ------------ | ---------------- | ------------ |
| Morden  |    494,000   |                  |              |
| SilaMainnet |  1,150,000   |  March 14, 2016  | `0x97c2c34c` |

### Releases

- [CPP Sila 1.2.0][cpp]
- [Gsil 1.3.5]

[SIP-2]: https://sips.sila.org/SIPS/sip-2
[SIP-7]: https://sips.sila.org/SIPS/sip-7
[SIP-8]: https://sips.sila.org/SIPS/sip-8
[cpp]: https://github.com/sila/webthree-umbrella/releases/tag/v1.2.0
[Gsil 1.3.5]: https://github.com/sila/go-sila/releases/tag/v1.3.5
"""

from sila.fork_criteria import ByBlockNumber, ForkCriteria

FORK_CRITERIA: ForkCriteria = ByBlockNumber(1150000)
