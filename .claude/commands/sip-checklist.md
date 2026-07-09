# SIP Checklist

Guide for using the SIP testing checklist system to track test coverage. Run this skill when working on SIP test coverage or checklists.

## What It Is

The `SIPChecklist` class (in `execution_testing.checklists.sip_checklist`) provides a hierarchical marker system for tagging tests with what aspect of an SIP they cover. Categories include:

- `General`, `Opcode`, `Precompile`, `SystemContract`, `TransactionType`
- `BlockHeaderField`, `BlockBodyField`, `GasCostChanges`, `GasRefundsChanges`
- `ExecutionLayerRequest`, `BlobCountChanges`

Each category has deep sub-items (e.g., `SIPChecklist.Opcode.Test.GasUsage.Normal`).

## Usage in Tests

```python
@SIPChecklist.TransactionType.Test.IntrinsicValidity.GasLimit.Exact()
def test_exact_intrinsic_gas(state_test: StateTestFiller):
    ...

# Multi-SIP coverage:
@SIPChecklist.TransactionType.Test.Signature.Invalid.V.Two(sip=[2930])
def test_invalid_v(state_test: StateTestFiller):
    ...
```

## Generating Checklists

Run `uv run checklist` to generate coverage reports. Template at `docs/writing_tests/checklist_templates/sip_testing_checklist_template.md`.

## Marking Items as Externally Covered or N/A

Create `sip_checklist_external_coverage.txt` in the SIP test directory:

```
general/code_coverage/eels = Covered by EELS test suite
```

Create `sip_checklist_not_applicable.txt` for inapplicable items:

```
system_contract = SIP-7702 does not introduce a system contract
precompile/ = SIP-7702 does not introduce a precompile
```

(trailing `/` marks entire category as N/A)

## Completed Examples

Reference these for patterns:

- `tests/prague/sip7702_set_code_tx/` — comprehensive checklist for a transaction type SIP
- `tests/osaka/sip7951_p256verify_precompiles/` — precompile checklist example

## References

See `docs/writing_tests/checklist_templates/` for templates and detailed documentation.
