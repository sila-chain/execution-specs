"""
The second blob parameter only (BPO) fork, BPO2 ([SIP-8135]), includes only
changes to the blob fee schedule.

### Changes

- [SIP-7892: Blob Parameter Only Hardforks][SIP-7892]

### Upgrade Schedule

| Network | Timestamp    | Date & Time (UTC)       | Fork Hash    | Beacon Chain Epoch |
|---------|--------------|-------------------------|--------------|--------------------|
| SilaHolesky | `1760389824` | 2025-10-13 21:10:24     | `0x9bc6cb31` | `167936`           |
| SilaSepolia | `1761607008` | 2025-10-27 23:16:48     | `0x268956b6` | `275712`           |
| Hoodi   | `1762955544` | 2025-11-12 13:52:24     | `0x23aa1351` |  `54016`           |
| SilaMainnet | `1767747671` | 2026-01-07 01:01:11     | `0x07c9462e` | `419072`           |

[SIP-8135]: https://sips.sila.org/SIPS/sip-8135
[SIP-7892]: https://sips.sila.org/SIPS/sip-7892
"""  # noqa: E501

from sila.fork_criteria import ByTimestamp, ForkCriteria

FORK_CRITERIA: ForkCriteria = ByTimestamp(1767747671)
