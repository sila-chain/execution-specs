"""
The fourth blob parameter only (BPO) fork, BPO4, includes only changes to the
blob fee schedule.

### Changes

- [SIP-7892: Blob Parameter Only Hardforks][SIP-7892]

### Upgrade Schedule

| Network | Timestamp    | Date & Time (UTC)       | Fork Hash    | Beacon Chain Epoch |
|---------|--------------|-------------------------|--------------|--------------------|
| SilaHolesky | `          ` |                         | `          ` | `      `           |
| SilaSepolia | `          ` |                         | `          ` | `      `           |
| Hoodi   | `          ` |                         | `          ` |  `     `           |
| SilaMainnet | `          ` |                         | `          ` | `      `           |

[SIP-7892]: https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-7892.md
"""  # noqa: E501

from sila.fork_criteria import ForkCriteria, Unscheduled

FORK_CRITERIA: ForkCriteria = Unscheduled(order_index=1)
