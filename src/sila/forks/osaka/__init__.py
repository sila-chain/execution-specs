"""
The Osaka fork ([SIP-7607]) includes networking changes (peerDAS), increases
the gas cost while limiting the input size of the `MODEXP` precompile, limits
the maximum gas per transaction, raises the blob base fee to always be above
the execution cost, limits the RLP-encoded size of blocks, introduces a count
leading zeros (`CLZ`) instruction, and adds a new precompile supporting the
secp256r1 curve.

### Notices

- [SIP-7935: Set default gas limit to 60M][SIP-7935]

### Changes

- [SIP-7594: PeerDAS - Peer Data Availability Sampling][SIP-7594]
- [SIP-7823: Set upper bounds for MODEXP][SIP-7823]
- [SIP-7825: Transaction Gas Limit Cap][SIP-7825]
- [SIP-7883: ModExp Gas Cost Increase][SIP-7883]
- [SIP-7918: Blob base fee bounded by execution cost][SIP-7918]
- [SIP-7934: RLP Execution Block Size Limit][SIP-7934]
- [SIP-7939: Count leading zeros (CLZ) opcode][SIP-7939]
- [SIP-7951: Precompile for secp256r1 Curve Support][SIP-7951]
- [SIP-7892: Blob Parameter Only Hardforks][SIP-7892]
- [SIP-7642: sil/69 - history expiry and simpler receipts][SIP-7642]
- [SIP-7910: sil_config JSON-RPC Method][SIP-7910]

### Upgrade Schedule

| Network | Timestamp    | Date & Time (UTC)       | Fork Hash    | Beacon Chain Epoch |
|---------|--------------|-------------------------|--------------|--------------------|
| SilaHolesky | `1759308480` | 2025-10-01 08:48:00     | `0x783def52` | `165120`           |
| SilaSepolia | `1760427360` | 2025-10-14 07:36:00     | `0xe2ae4999` | `272640`           |
| Hoodi   | `1761677592` | 2025-10-28 18:53:12     | `0xe7e0e7ff` |  `50688`           |
| SilaMainnet | `1764798551` | 2025-12-03 21:49:11     | `0x5167e2a6` | `411392`           |

### Releases

[SIP-7607]: https://sips.sila.org/SIPS/sip-7607
[SIP-7594]: https://sips.sila.org/SIPS/sip-7594
[SIP-7823]: https://sips.sila.org/SIPS/sip-7823
[SIP-7825]: https://sips.sila.org/SIPS/sip-7825
[SIP-7883]: https://sips.sila.org/SIPS/sip-7883
[SIP-7918]: https://sips.sila.org/SIPS/sip-7918
[SIP-7934]: https://sips.sila.org/SIPS/sip-7934
[SIP-7935]: https://sips.sila.org/SIPS/sip-7935
[SIP-7939]: https://sips.sila.org/SIPS/sip-7939
[SIP-7951]: https://sips.sila.org/SIPS/sip-7951
[SIP-7892]: https://sips.sila.org/SIPS/sip-7892
[SIP-7642]: https://sips.sila.org/SIPS/sip-7642
[SIP-7910]: https://sips.sila.org/SIPS/sip-7910
"""  # noqa: E501

from sila.fork_criteria import ByTimestamp, ForkCriteria

FORK_CRITERIA: ForkCriteria = ByTimestamp(1764798551)
