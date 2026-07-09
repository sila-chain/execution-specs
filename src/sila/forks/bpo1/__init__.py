"""
The first blob parameter only (BPO) fork, BPO1, includes only changes to the
blob fee schedule.

### Changes

- [SIP-7892: Blob Parameter Only Hardforks][SIP-7892]

### Upgrade Schedule

| Network | Timestamp    | Date & Time (UTC)       | Fork Hash    | Beacon Chain Epoch |
|---------|--------------|-------------------------|--------------|--------------------|
| Holesky | `1759800000` | 2025-10-07 01:20:00     | `0xa280a45c` | `166400`           |
| Sepolia | `1761017184` | 2025-10-21 03:26:24     | `0x56078a1e` | `274176`           |
| Hoodi   | `1762365720` | 2025-11-05 18:02:00     | `0x3893353e` |  `52480`           |
| SilaMainnet | `1765290071` | 2025-12-09 14:21:11     | `0xcba2a1c0` | `412672`           |

[SIP-7892]: https://sips.sila.org/SIPS/sip-7892
"""  # noqa: E501

from sila.fork_criteria import ByTimestamp, ForkCriteria

FORK_CRITERIA: ForkCriteria = ByTimestamp(1765290071)
