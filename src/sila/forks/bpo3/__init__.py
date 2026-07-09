"""
The third blob parameter only (BPO) fork, BPO3, includes only changes to the
blob fee schedule.

### Changes

- [SIP-7892: Blob Parameter Only Hardforks][SIP-7892]

### Upgrade Schedule

| Network | Timestamp    | Date & Time (UTC)       | Fork Hash    | Beacon Chain Epoch |
|---------|--------------|-------------------------|--------------|--------------------|
| Holesky | `          ` |                         | `          ` | `      `           |
| Sepolia | `          ` |                         | `          ` | `      `           |
| Hoodi   | `          ` |                         | `          ` |  `     `           |
| SilaMainnet | `          ` |                         | `          ` | `      `           |

[SIP-7892]: https://sips.sila.org/SIPS/sip-7892
"""  # noqa: E501

from sila.fork_criteria import ForkCriteria, Unscheduled

FORK_CRITERIA: ForkCriteria = Unscheduled(order_index=0)
