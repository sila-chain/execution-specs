---
name: assess-sip
description: Assess an SIP's implementation complexity and scope.
---

# Assess SIP

Structured assessment of SIP implementation complexity. When invoked with an SIP number or description, perform the following analysis.

## 1. Classify the Change Type(s)

- **New opcode** — requires: `vm/instructions/`, gas cost, `op_implementation` registration
- **New precompile** — requires: `vm/precompiled_contracts/`, address constant, mapping, gas cost
- **New transaction type** — requires: `transactions.py`, `fork.py` validation, exception types
- **System contract** — requires: contract deployment in genesis, state handling
- **Block header/body field** — requires: `blocks.py`, RLP encoding changes
- **Gas cost change** — requires: `vm/gas.py` constant updates, possibly interpreter changes
- **Execution layer request** — requires: request handling in `requests.py`
- **Constraint change** — requires: validation logic in `fork.py` or `blocks.py`

## 2. Estimate Scope

- **Small** (1-2 files in spec, 1 test file): gas repricing, simple constraint
- **Medium** (3-5 files in spec, 2-3 test files): new opcode, new precompile
- **Large** (5-10 files in spec, 5+ test files): new tx type, new system contract
- **XL** (10+ files, multi-SIP umbrella): VM overhaul (e.g., EOF)

## 3. Identify Required Test Categories

Map the change types to the relevant `SIPChecklist` categories (from `execution_testing.checklists.sip_checklist`). List the checklist items that need to be covered.

## 4. Identify Prior Art

Find similar completed SIPs in the repo to use as implementation reference:

- New opcode → check recent opcode additions in latest fork's `vm/instructions/`
- New precompile → `tests/osaka/sip7951_p256verify_precompiles/`
- New tx type → `tests/prague/sip7702_set_code_tx/`
- Gas changes → check `vm/gas.py` diffs between recent forks

## 5. Output Structured Assessment

Produce a summary with:

- Change types identified
- Estimated scope (Small / Medium / Large / XL)
- Spec files to modify (with paths)
- Test files to create
- SIPChecklist categories to cover
- Reference implementations to follow
