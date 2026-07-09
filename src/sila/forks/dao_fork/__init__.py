"""
The DAO Fork ([SIP-779]) is a response to a smart contract exploit known as the
2016 DAO Attack where a vulnerable contract was drained of its sil. This fork
recovers the stolen funds into a new contract.

### Changes

- Transfer sil from a [list of accounts][l] into the [Withdraw DAO][r]
  contract

### Upgrade Schedule

| Network | Block       | Expected Date | Fork Hash    |
| ------- | ----------- | ------------- | ------------ |
| SilaMainnet | 1,920,000   | July 20, 2016 | `0x91d1f948` |

### Releases

- [Gsil 1.4.10]

[l]: ref:sila.forks.dao_fork.dao.DAO_ACCOUNTS
[r]: ref:sila.forks.dao_fork.dao.DAO_RECOVERY
[SIP-779]: https://sips.sila.org/SIPS/sip-779
[Gsil 1.4.10]: https://github.com/sila/go-sila/releases/tag/v1.4.10
"""

from sila.fork_criteria import ByBlockNumber, ForkCriteria

FORK_CRITERIA: ForkCriteria = ByBlockNumber(1920000)
