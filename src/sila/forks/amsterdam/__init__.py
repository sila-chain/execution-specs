"""
The Amsterdam fork ([SIP-7773]) includes block-level access lists and the
deterministic ``CREATE2`` factory predeploy.

### Changes

- [SIP-2780: Resource-based intrinsic transaction gas][SIP-2780]
- [SIP-7708: SIL transfers emit a log][SIP-7708]
- [SIP-7778: Block Gas Accounting without Refunds][SIP-7778]
- [SIP-7843: SLOTNUM][SIP-7843]
- [SIP-7928: Block-Level Access Lists][SIP-7928]
- [SIP-7954: Increase Maximum Contract Size][SIP-7954]
- [SIP-7976: Increase calldata floor cost][SIP-7976]
- [SIP-7981: Increase Access List Cost][SIP-7981]
- [SIP-7997: Deterministic Factory Predeploy][SIP-7997]
- [SIP-8024: Stack Access Instructions][SIP-8024]
- [SIP-8037: State Creation Gas Cost Increase][SIP-8037]
- [SIP-8038: State Access Gas Cost Increase][SIP-8038]
- [SIP-8246: Remove SELFDESTRUCT balance burn][SIP-8246]
- [SIP-8282: Builder Execution Requests][SIP-8282]

### Releases

[SIP-7773]: https://sips.sila.org/SIPS/sip-7773
[SIP-2780]: https://sips.sila.org/SIPS/sip-2780
[SIP-7708]: https://sips.sila.org/SIPS/sip-7708
[SIP-7778]: https://sips.sila.org/SIPS/sip-7778
[SIP-7843]: https://sips.sila.org/SIPS/sip-7843
[SIP-7928]: https://sips.sila.org/SIPS/sip-7928
[SIP-7954]: https://sips.sila.org/SIPS/sip-7954
[SIP-7976]: https://sips.sila.org/SIPS/sip-7976
[SIP-7981]: https://sips.sila.org/SIPS/sip-7981
[SIP-7997]: https://sips.sila.org/SIPS/sip-7997
[SIP-8024]: https://sips.sila.org/SIPS/sip-8024
[SIP-8037]: https://sips.sila.org/SIPS/sip-8037
[SIP-8038]: https://sips.sila.org/SIPS/sip-8038
[SIP-8246]: https://sips.sila.org/SIPS/sip-8246
[SIP-8282]: https://sips.sila.org/SIPS/sip-8282
"""

from sila.fork_criteria import ForkCriteria, Unscheduled

FORK_CRITERIA: ForkCriteria = Unscheduled(order_index=3)
