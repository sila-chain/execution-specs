# SIP Checklist Generation

The SIP checklist feature helps track test coverage for SIP implementations by automatically generating filled checklists based on test markers.

## Overview

When implementing tests for an SIP, you can mark specific tests as covering checklist items from the [SIP testing checklist template](../writing_tests/checklist_templates/sip_testing_checklist_template.md). The framework will then generate a filled checklist showing which items have been implemented.

## Marking Tests as implementing SIP Checklist Items

To mark a test as implementing a specific checklist item, use the structured `SIPChecklist` class:

### The `SIPChecklist` Class

```python
import pytest
from execution_testing.tools import StateTestFiller
from execution_testing.checklists import SIPChecklist

@SIPChecklist.TransactionType.Test.IntrinsicValidity.GasLimit.Exact()
def test_exact_intrinsic_gas(state_test: StateTestFiller):
    """Test transaction with exact intrinsic gas limit."""
    # Test implementation
    pass

# You can also use the marker without parentheses
@SIPChecklist.TransactionType.Test.IntrinsicValidity.GasLimit.Insufficient
def test_insufficient_intrinsic_gas(state_test: StateTestFiller):
    """Test transaction with insufficient intrinsic gas limit."""
    # Test implementation
    pass
```

The `SIPChecklist` class provides type safety and IDE autocompletion, making it easier to find and reference checklist items correctly.

### Marker Parameters

- **First positional parameter** (required): The checklist item ID (`SIPChecklist` reference)
- **`sip` keyword parameter** (optional): List of additional SIPs covered by the test

Example with multiple SIPs covered by the same test:

```python
@SIPChecklist.TransactionType.Test.Signature.Invalid.V.Two(
    sip=[7702, 2930]
)
def test_invalid_signature(state_test: StateTestFiller):
    """Test invalid signature that affects multiple SIPs."""
    pass
```

### Partial ID Matching

You can use partial IDs that will match all checklist items starting with that prefix:

```python
@SIPChecklist.TransactionType.Test.Signature.Invalid()
def test_all_invalid_signatures(state_test: StateTestFiller):
    """Test covering all invalid signature scenarios."""
    pass
```

## Generating Checklists

### Using the Dedicated `checklist` Command

To generate only checklists without filling fixtures:

```bash
# Generate checklists for all SIPs
uv run checklist

# Generate checklist for specific SIP
uv run checklist --sip 7702

# Specify output directory
uv run checklist --output ./my-checklists

# Multiple SIPs
uv run checklist --sip 7702 --sip 2930
```

### Automatic Generation in Documentation

When building the documentation with `mkdocs`, checklists are automatically generated for all SIPs that have tests with checklist markers. The checklists appear in the test documentation alongside the test modules.

## External Coverage and Not Applicable Items

### External Coverage

For checklist items that are covered by external tests, procedures, or tools (e.g., EELS coverage), create a file named `sip_checklist_external_coverage.txt` in the SIP test directory:

```text
# tests/prague/sip7702_set_code_tx/sip_checklist_external_coverage.txt
general/code_coverage/eels = Covered by EELS test suite
general/code_coverage/second_client = Covered by Nethermind tests
```

Format: `checklist_item_id = reason`

### Not Applicable Items

For checklist items that are not applicable to a specific SIP, create a file named `sip_checklist_not_applicable.txt` in the SIP test directory:

```text
# tests/prague/sip7702_set_code_tx/sip_checklist_not_applicable.txt
system_contract = SIP-7702 does not introduce a system contract
precompile = SIP-7702 does not introduce a precompile
```

Format: `checklist_item_id = reason`

Both files support partial ID matching, so you can mark entire sections as not applicable:

## MyPy Type Checking Support

The `SIPChecklist` classes are made callable through a companion `.pyi` stub file that provides proper type hints for mypy. This allows you to use both decorator patterns without type checking errors:

```python
# Both of these work with proper mypy support
@SIPChecklist.Opcode.Test.StackComplexOperations()  # With parentheses
@SIPChecklist.Opcode.Test.StackComplexOperations   # Without parentheses
```

### Regenerating Type Stubs

If you modify the `SIPChecklist` class structure in `packages/testing/src/execution_testing/checklists/sip_checklist.py`, you need to regenerate the type stub file:

```bash
# Generate the stub file (for maintainers):
uv run generate_checklist_stubs

# Preview what would be generated without writing the file
uv run generate_checklist_stubs --dry-run

# Generate to a custom location
uv run generate_checklist_stubs --output path/to/custom/stubs.pyi
```

The generated stub file (`sip_checklist.pyi`) should be committed to the repository to ensure proper type checking for all developers.

```text
# Mark all system contract items as not applicable
system_contract/ = SIP does not introduce system contracts
```

## Output Format

The generated checklist will show:

- ✅ for completed items (either by tests or external coverage)
- N/A for not applicable items
- Test names that implement each item
- External coverage reasons where applicable
- A percentage of covered checklist items (excluding N/A items)
- Color-coded completion status: 🟢 (100%), 🟡 (>50%), 🔴 (≤50%)

Example output snippet:

```markdown
# SIP-7702 Test Checklist

## Checklist Progress Tracker

| Total Checklist Items | Covered Checklist Items | Percentage |
| --------------------- | ----------------------- | ---------- |
| 45 | 32 | 🟡 71.11% |

## General

#### Code coverage

| ID | Description | Status | Tests |
| -- | ----------- | ------ | ----- |
| `general/code_coverage/eels` | Run produced tests against EELS... | ✅ | Covered by EELS test suite |
| `general/code_coverage/test_coverage` | Run coverage on the test code itself... | ✅ | `tests/prague/sip7702_set_code_tx/test_set_code_txs.py::test_set_code_txs` |

## Transaction Type

| ID | Description | Status | Tests |
| -- | ----------- | ------ | ----- |
| `transaction_type/test/intrinsic_validity/gas_limit/exact` | Provide the exact intrinsic gas... | ✅ | `tests/prague/sip7702_set_code_tx/test_checklist_example.py::test_exact_intrinsic_gas` |
| `transaction_type/test/intrinsic_validity/gas_limit/insufficient` | Provide the exact intrinsic gas minus one... |  |  |

## System Contract

| ID | Description | Status | Tests |
| -- | ----------- | ------ | ----- |
| `system_contract/test/deployment/missing` | Verify block execution behavior... | N/A | SIP-7702 does not introduce a system contract |
```

## Best Practices

1. **Start with the checklist**: Review the checklist template before writing tests to ensure comprehensive coverage
2. **Use the `SIPChecklist` class**: Use `SIPChecklist.Opcode.Test.GasUsage.Normal` for type safety and IDE autocompletion
3. **Use descriptive test names**: The test name will appear in the checklist, so make it clear what the test covers
4. **Mark items as you go**: Add `sip_checklist` markers while writing tests, not as an afterthought
5. **Document external coverage**: If items are covered by external tools/tests, document this in `sip_checklist_external_coverage.txt`
6. **Be explicit about N/A items**: Document why items are not applicable in `sip_checklist_not_applicable.txt`
7. **Use partial IDs wisely**: When a test covers multiple related items, use partial IDs to mark them all
8. **Verify IDs before using**: Use `str(SIPChecklist.Section.Subsection)` to verify the exact string ID when needed

## Workflow Example

1. **Create test directory structure**:

      ```bash
      tests/prague/sip9999_new_feature/
      ├── __init__.py
      ├── spec.py
      ├── test_basic.py
      ├── sip_checklist_external_coverage.txt
      └── sip_checklist_not_applicable.txt
      ```

2. **Mark tests as you implement them**:

      ```python
      from execution_testing.checklists import SIPChecklist

      @SIPChecklist.Opcode.Test.GasUsage.Normal()
      def test_opcode_gas_consumption(state_test: StateTestFiller):
         """Test normal gas consumption of the new opcode."""
         pass
      ```

3. **Document external coverage**:

      ```text
      # sip_checklist_external_coverage.txt
      general/code_coverage/eels = Covered by sila/execution-specs PR #1234
      ```

      You can verify the correct ID using:

      ```python
      # str(SIPChecklist.General.CodeCoverage.Eels) = "general/code_coverage/eels"
      ```

4. **Mark non-applicable items**:

      ```text
      # sip_checklist_not_applicable.txt
      precompile/ = SIP-9999 introduces an opcode, not a precompile
      ```

      You can verify the correct ID using:

      ```python
      # str(SIPChecklist.Precompile) = "precompile"
      ```

5. **Generate and review checklist**:

      ```bash
      checklist --sip 9999
      # Review the generated checklist for completeness
      ```

## See Also

- [SIP Testing Checklist Template](./checklist_templates/sip_testing_checklist_template.md) - The full checklist template
