"""Test opcode gas costs."""

import pytest

from execution_testing.vm import Bytecode, Op

from ..forks.forks import (
    SilaBerlin,
    SilaConstantinopleFix,
    SilaHomestead,
    SilaIstanbul,
    SilaOsaka,
    SpuriousDragon,
)
from ..helpers import Fork


@pytest.mark.parametrize(
    "fork,opcode,expected_cost",
    [
        pytest.param(
            SilaOsaka,
            Op.MSTORE(new_memory_size=1),
            SilaOsaka.memory_expansion_gas_calculator()(new_bytes=1)
            + SilaOsaka.gas_costs().VERY_LOW,
            id="mstore_memory_expansion",
        ),
        pytest.param(
            SilaOsaka,
            Op.SSTORE,
            SilaOsaka.gas_costs().STORAGE_SET
            + SilaOsaka.gas_costs().COLD_STORAGE_ACCESS,
            id="sstore_defaults",
        ),
        pytest.param(
            SilaOsaka,
            Op.SSTORE(key_warm=True),
            SilaOsaka.gas_costs().STORAGE_SET,
            id="sstore_warm_key",
        ),
        # EXP tests
        pytest.param(
            SilaOsaka,
            Op.EXP(exponent=0),
            SilaOsaka.gas_costs().OPCODE_EXP_BASE,
            id="exp_zero_exponent",
        ),
        pytest.param(
            SilaOsaka,
            Op.EXP(exponent=0xFFFFFF),  # 3 bytes
            SilaOsaka.gas_costs().OPCODE_EXP_BASE
            + SilaOsaka.gas_costs().OPCODE_EXP_PER_BYTE * 3,
            id="exp_three_bytes",
        ),
        pytest.param(
            SilaOsaka,
            Op.EXP(exponent=0x1FFFFFF),  # 3 bytes
            SilaOsaka.gas_costs().OPCODE_EXP_BASE
            + SilaOsaka.gas_costs().OPCODE_EXP_PER_BYTE * 4,
            id="exp_three_bytes_plus_one_bit",
        ),
        # SHA3 tests
        pytest.param(
            SilaOsaka,
            Op.SHA3(data_size=0),
            SilaOsaka.gas_costs().OPCODE_KECCAK256_BASE,
            id="sha3_zero_data",
        ),
        pytest.param(
            SilaOsaka,
            Op.SHA3(data_size=64, new_memory_size=96),
            SilaOsaka.gas_costs().OPCODE_KECCAK256_BASE
            + SilaOsaka.gas_costs().OPCODE_KECCAK256_PER_WORD * 2
            + SilaOsaka.memory_expansion_gas_calculator()(new_bytes=96),
            id="sha3_with_data_and_memory",
        ),
        # BALANCE tests
        pytest.param(
            SilaOsaka,
            Op.BALANCE(address_warm=False),
            SilaOsaka.gas_costs().COLD_ACCOUNT_ACCESS,
            id="balance_cold_address",
        ),
        pytest.param(
            SilaOsaka,
            Op.BALANCE(address_warm=True),
            SilaOsaka.gas_costs().WARM_ACCESS,
            id="balance_warm_address",
        ),
        # CALLDATACOPY tests
        pytest.param(
            SilaOsaka,
            Op.CALLDATACOPY(data_size=32, new_memory_size=32),
            SilaOsaka.gas_costs().VERY_LOW
            + SilaOsaka.gas_costs().OPCODE_COPY_PER_WORD * 1
            + SilaOsaka.memory_expansion_gas_calculator()(new_bytes=32),
            id="calldatacopy_one_word",
        ),
        pytest.param(
            SilaOsaka,
            Op.CALLDATACOPY(
                data_size=64, new_memory_size=64, old_memory_size=32
            ),
            SilaOsaka.gas_costs().VERY_LOW
            + SilaOsaka.gas_costs().OPCODE_COPY_PER_WORD * 2
            + SilaOsaka.memory_expansion_gas_calculator()(
                new_bytes=64, previous_bytes=32
            ),
            id="calldatacopy_expansion",
        ),
        # CODECOPY tests
        pytest.param(
            SilaOsaka,
            Op.CODECOPY(data_size=96, new_memory_size=96),
            SilaOsaka.gas_costs().VERY_LOW
            + SilaOsaka.gas_costs().OPCODE_COPY_PER_WORD * 3
            + SilaOsaka.memory_expansion_gas_calculator()(new_bytes=96),
            id="codecopy_three_words",
        ),
        # EXTCODESIZE tests
        pytest.param(
            SilaOsaka,
            Op.EXTCODESIZE(address_warm=False),
            SilaOsaka.gas_costs().COLD_ACCOUNT_ACCESS,
            id="extcodesize_cold",
        ),
        pytest.param(
            SilaOsaka,
            Op.EXTCODESIZE(address_warm=True),
            SilaOsaka.gas_costs().WARM_ACCESS,
            id="extcodesize_warm",
        ),
        # EXTCODECOPY tests
        pytest.param(
            SilaOsaka,
            Op.EXTCODECOPY(
                address_warm=True, data_size=32, new_memory_size=32
            ),
            SilaOsaka.gas_costs().WARM_ACCESS
            + SilaOsaka.gas_costs().OPCODE_COPY_PER_WORD * 1
            + SilaOsaka.memory_expansion_gas_calculator()(new_bytes=32),
            id="extcodecopy_warm",
        ),
        pytest.param(
            SilaOsaka,
            Op.EXTCODECOPY(
                address_warm=False, data_size=64, new_memory_size=64
            ),
            SilaOsaka.gas_costs().COLD_ACCOUNT_ACCESS
            + SilaOsaka.gas_costs().OPCODE_COPY_PER_WORD * 2
            + SilaOsaka.memory_expansion_gas_calculator()(new_bytes=64),
            id="extcodecopy_cold",
        ),
        # EXTCODEHASH tests
        pytest.param(
            SilaOsaka,
            Op.EXTCODEHASH(address_warm=False),
            SilaOsaka.gas_costs().COLD_ACCOUNT_ACCESS,
            id="extcodehash_cold",
        ),
        pytest.param(
            SilaOsaka,
            Op.EXTCODEHASH(address_warm=True),
            SilaOsaka.gas_costs().WARM_ACCESS,
            id="extcodehash_warm",
        ),
        # RETURNDATACOPY tests
        pytest.param(
            SilaOsaka,
            Op.RETURNDATACOPY(data_size=32, new_memory_size=32),
            SilaOsaka.gas_costs().VERY_LOW
            + SilaOsaka.gas_costs().OPCODE_COPY_PER_WORD * 1
            + SilaOsaka.memory_expansion_gas_calculator()(new_bytes=32),
            id="returndatacopy",
        ),
        # MLOAD tests
        pytest.param(
            SilaOsaka,
            Op.MLOAD(new_memory_size=32),
            SilaOsaka.gas_costs().VERY_LOW
            + SilaOsaka.memory_expansion_gas_calculator()(new_bytes=32),
            id="mload_memory_expansion",
        ),
        # MSTORE8 tests
        pytest.param(
            SilaOsaka,
            Op.MSTORE8(new_memory_size=1),
            SilaOsaka.gas_costs().VERY_LOW
            + SilaOsaka.memory_expansion_gas_calculator()(new_bytes=1),
            id="mstore8_memory_expansion",
        ),
        # SLOAD tests
        pytest.param(
            SilaOsaka,
            Op.SLOAD(key_warm=False),
            SilaOsaka.gas_costs().COLD_STORAGE_ACCESS,
            id="sload_cold",
        ),
        pytest.param(
            SilaOsaka,
            Op.SLOAD(key_warm=True),
            SilaOsaka.gas_costs().WARM_SLOAD,
            id="sload_warm",
        ),
        # MCOPY tests
        pytest.param(
            SilaOsaka,
            Op.MCOPY(data_size=32, new_memory_size=32),
            SilaOsaka.gas_costs().VERY_LOW
            + SilaOsaka.gas_costs().OPCODE_COPY_PER_WORD * 1
            + SilaOsaka.memory_expansion_gas_calculator()(new_bytes=32),
            id="mcopy_one_word",
        ),
        pytest.param(
            SilaOsaka,
            Op.MCOPY(data_size=96, new_memory_size=128, old_memory_size=64),
            SilaOsaka.gas_costs().VERY_LOW
            + SilaOsaka.gas_costs().OPCODE_COPY_PER_WORD * 3
            + SilaOsaka.memory_expansion_gas_calculator()(
                new_bytes=128, previous_bytes=64
            ),
            id="mcopy_expansion",
        ),
        # LOG0 tests
        pytest.param(
            SilaOsaka,
            Op.LOG0(data_size=32, new_memory_size=32),
            SilaOsaka.gas_costs().OPCODE_LOG_BASE
            + SilaOsaka.gas_costs().OPCODE_LOG_DATA_PER_BYTE * 32
            + SilaOsaka.memory_expansion_gas_calculator()(new_bytes=32),
            id="log0",
        ),
        # LOG1 tests
        pytest.param(
            SilaOsaka,
            Op.LOG1(data_size=64, new_memory_size=64),
            SilaOsaka.gas_costs().OPCODE_LOG_BASE
            + SilaOsaka.gas_costs().OPCODE_LOG_DATA_PER_BYTE * 64
            + SilaOsaka.gas_costs().OPCODE_LOG_TOPIC
            + SilaOsaka.memory_expansion_gas_calculator()(new_bytes=64),
            id="log1",
        ),
        # LOG2 tests
        pytest.param(
            SilaOsaka,
            Op.LOG2(data_size=128, new_memory_size=128),
            SilaOsaka.gas_costs().OPCODE_LOG_BASE
            + SilaOsaka.gas_costs().OPCODE_LOG_DATA_PER_BYTE * 128
            + SilaOsaka.gas_costs().OPCODE_LOG_TOPIC * 2
            + SilaOsaka.memory_expansion_gas_calculator()(new_bytes=128),
            id="log2",
        ),
        # LOG3 tests
        pytest.param(
            SilaOsaka,
            Op.LOG3(data_size=256, new_memory_size=256),
            SilaOsaka.gas_costs().OPCODE_LOG_BASE
            + SilaOsaka.gas_costs().OPCODE_LOG_DATA_PER_BYTE * 256
            + SilaOsaka.gas_costs().OPCODE_LOG_TOPIC * 3
            + SilaOsaka.memory_expansion_gas_calculator()(new_bytes=256),
            id="log3",
        ),
        # LOG4 tests
        pytest.param(
            SilaOsaka,
            Op.LOG4(data_size=512, new_memory_size=512),
            SilaOsaka.gas_costs().OPCODE_LOG_BASE
            + SilaOsaka.gas_costs().OPCODE_LOG_DATA_PER_BYTE * 512
            + SilaOsaka.gas_costs().OPCODE_LOG_TOPIC * 4
            + SilaOsaka.memory_expansion_gas_calculator()(new_bytes=512),
            id="log4",
        ),
        # CREATE tests
        pytest.param(
            SilaOsaka,
            Op.CREATE(init_code_size=100, new_memory_size=100),
            SilaOsaka.gas_costs().OPCODE_CREATE_BASE
            # (100 + 31) // 32 = 4
            + SilaOsaka.gas_costs().CODE_INIT_PER_WORD * 4
            + SilaOsaka.memory_expansion_gas_calculator()(new_bytes=100),
            id="create_with_initcode",
        ),
        # CREATE2 tests
        pytest.param(
            SilaOsaka,
            Op.CREATE2(init_code_size=64, new_memory_size=64),
            SilaOsaka.gas_costs().OPCODE_CREATE_BASE
            + SilaOsaka.gas_costs().CODE_INIT_PER_WORD * 2
            + SilaOsaka.gas_costs().OPCODE_KECCAK256_PER_WORD * 2
            + SilaOsaka.memory_expansion_gas_calculator()(new_bytes=64),
            id="create2_with_initcode_and_hash",
        ),
        # CALL tests
        pytest.param(
            SilaOsaka,
            Op.CALL(
                address_warm=True, value_transfer=False, new_memory_size=64
            ),
            SilaOsaka.gas_costs().WARM_ACCESS
            + SilaOsaka.memory_expansion_gas_calculator()(new_bytes=64),
            id="call_warm_no_value",
        ),
        pytest.param(
            SilaOsaka,
            Op.CALL(address_warm=False, delegated_address=True),
            SilaOsaka.gas_costs().COLD_ACCOUNT_ACCESS
            + SilaOsaka.gas_costs().COLD_ACCOUNT_ACCESS,
            id="call_cold_delegated_address",
        ),
        pytest.param(
            SilaOsaka,
            Op.CALL(
                address_warm=False,
                delegated_address=True,
                delegated_address_warm=True,
            ),
            SilaOsaka.gas_costs().COLD_ACCOUNT_ACCESS
            + SilaOsaka.gas_costs().WARM_ACCESS,
            id="call_warm_delegated_address",
        ),
        pytest.param(
            SilaOsaka,
            Op.CALL(address_warm=False, value_transfer=True, account_new=True),
            SilaOsaka.gas_costs().COLD_ACCOUNT_ACCESS
            + SilaOsaka.gas_costs().CALL_VALUE
            + SilaOsaka.gas_costs().NEW_ACCOUNT,
            id="call_cold_account_new",
        ),
        pytest.param(
            SilaHomestead,
            Op.CALL(address_warm=False, value_transfer=True, account_new=True),
            40 + 9_000 + 25_000,
            id="call_cold_account_new_homestead",
        ),
        pytest.param(
            SilaOsaka,
            Op.CALL(
                address_warm=False,
                value_transfer=True,
                account_new=False,
                new_memory_size=32,
            ),
            SilaOsaka.gas_costs().COLD_ACCOUNT_ACCESS
            + SilaOsaka.gas_costs().CALL_VALUE
            + SilaOsaka.memory_expansion_gas_calculator()(new_bytes=32),
            id="call_cold_with_value",
        ),
        pytest.param(
            SilaOsaka,
            Op.CALL(
                address_warm=False,
                value_transfer=True,
                account_new=True,
                new_memory_size=32,
            ),
            SilaOsaka.gas_costs().COLD_ACCOUNT_ACCESS
            + SilaOsaka.gas_costs().CALL_VALUE
            + SilaOsaka.gas_costs().NEW_ACCOUNT
            + SilaOsaka.memory_expansion_gas_calculator()(new_bytes=32),
            id="call_cold_new_account",
        ),
        # CALLCODE tests
        pytest.param(
            SilaOsaka,
            Op.CALLCODE(
                address_warm=True, value_transfer=False, new_memory_size=32
            ),
            SilaOsaka.gas_costs().WARM_ACCESS
            + SilaOsaka.memory_expansion_gas_calculator()(new_bytes=32),
            id="callcode_warm",
        ),
        # DELEGATECALL tests
        pytest.param(
            SilaOsaka,
            Op.DELEGATECALL(address_warm=True, new_memory_size=32),
            SilaOsaka.gas_costs().WARM_ACCESS
            + SilaOsaka.memory_expansion_gas_calculator()(new_bytes=32),
            id="delegatecall_warm",
        ),
        pytest.param(
            SilaOsaka,
            Op.DELEGATECALL(address_warm=False, new_memory_size=64),
            SilaOsaka.gas_costs().COLD_ACCOUNT_ACCESS
            + SilaOsaka.memory_expansion_gas_calculator()(new_bytes=64),
            id="delegatecall_cold",
        ),
        # STATICCALL tests
        pytest.param(
            SilaOsaka,
            Op.STATICCALL(address_warm=True, new_memory_size=32),
            SilaOsaka.gas_costs().WARM_ACCESS
            + SilaOsaka.memory_expansion_gas_calculator()(new_bytes=32),
            id="staticcall_warm",
        ),
        pytest.param(
            SilaOsaka,
            Op.STATICCALL(address_warm=False, new_memory_size=0),
            SilaOsaka.gas_costs().COLD_ACCOUNT_ACCESS,
            id="staticcall_cold_no_memory",
        ),
        # RETURN tests
        pytest.param(
            SilaOsaka,
            Op.RETURN(new_memory_size=32),
            SilaOsaka.memory_expansion_gas_calculator()(new_bytes=32),
            id="return_no_deposit",
        ),
        pytest.param(
            SilaOsaka,
            Op.RETURN(code_deposit_size=100, new_memory_size=32),
            SilaOsaka.gas_costs().CODE_DEPOSIT_PER_BYTE * 100
            + SilaOsaka.memory_expansion_gas_calculator()(new_bytes=32),
            id="return_with_code_deposit",
        ),
        # REVERT tests
        pytest.param(
            SilaOsaka,
            Op.REVERT(new_memory_size=64),
            SilaOsaka.memory_expansion_gas_calculator()(new_bytes=64),
            id="revert_memory_expansion",
        ),
        # CLZ test (SilaOsaka-specific)
        pytest.param(
            SilaOsaka,
            Op.CLZ,
            SilaOsaka.gas_costs().LOW,
            id="clz_osaka",
        ),
        # Pre-SilaBerlin flat access costs. Literal values are the point:
        # they pin the historical schedule from the EELS vm/gas.py
        # constants of each fork.
        pytest.param(SilaHomestead, Op.CALL, 40, id="call_homestead"),
        pytest.param(SpuriousDragon, Op.CALL, 700, id="call_spurious_dragon"),
        pytest.param(
            SpuriousDragon,
            Op.CALL(address_warm=True),
            700,
            id="call_warmth_inert_spurious_dragon",
        ),
        pytest.param(
            SpuriousDragon,
            Op.CALL(address_warm=True, value_transfer=True, account_new=True),
            700 + 9_000 + 25_000,
            id="call_value_new_account_spurious_dragon",
        ),
        pytest.param(SilaHomestead, Op.BALANCE, 20, id="balance_homestead"),
        pytest.param(
            SpuriousDragon, Op.BALANCE, 400, id="balance_spurious_dragon"
        ),
        pytest.param(SilaIstanbul, Op.BALANCE, 700, id="balance_istanbul"),
        pytest.param(SilaHomestead, Op.SLOAD, 50, id="sload_homestead"),
        pytest.param(
            SpuriousDragon, Op.SLOAD, 200, id="sload_spurious_dragon"
        ),
        pytest.param(SilaIstanbul, Op.SLOAD, 800, id="sload_istanbul"),
        pytest.param(
            SilaHomestead, Op.EXTCODESIZE, 20, id="extcodesize_homestead"
        ),
        pytest.param(
            SpuriousDragon,
            Op.EXTCODESIZE,
            700,
            id="extcodesize_spurious_dragon",
        ),
        pytest.param(
            SilaConstantinopleFix,
            Op.EXTCODEHASH,
            400,
            id="extcodehash_constantinople_fix",
        ),
        pytest.param(
            SilaIstanbul, Op.EXTCODEHASH, 700, id="extcodehash_istanbul"
        ),
        pytest.param(
            SilaHomestead, Op.SELFDESTRUCT, 0, id="selfdestruct_homestead"
        ),
        pytest.param(
            SpuriousDragon,
            Op.SELFDESTRUCT,
            5_000,
            id="selfdestruct_spurious_dragon",
        ),
        pytest.param(
            SpuriousDragon,
            Op.SELFDESTRUCT(account_new=True),
            5_000 + 25_000,
            id="selfdestruct_new_account_spurious_dragon",
        ),
        # The new account charge is independent of a value transfer
        # until SIP-161, and SELFDESTRUCT charges nothing before
        # SIP-150.
        pytest.param(
            SilaHomestead,
            Op.CALL(account_new=True),
            40 + 25_000,
            id="call_new_account_without_value_homestead",
        ),
        pytest.param(
            SilaHomestead,
            Op.SELFDESTRUCT(account_new=True),
            0,
            id="selfdestruct_new_account_homestead",
        ),
    ],
)
def test_opcode_gas_costs(fork: Fork, opcode: Op, expected_cost: int) -> None:  # noqa: D103
    op_gas_cost_calc = fork.opcode_gas_calculator()
    assert expected_cost == op_gas_cost_calc(opcode)


@pytest.mark.parametrize(
    "fork,bytecode,expected_cost",
    [
        pytest.param(
            SilaOsaka,
            Op.ADD + Op.SUB,
            SilaOsaka.gas_costs().VERY_LOW * 2,
            id="sum_of_opcodes",
        ),
        pytest.param(
            SilaOsaka,
            Op.ADD(1, 1),
            SilaOsaka.gas_costs().VERY_LOW * 3,
            id="opcode_with_args",
        ),
        pytest.param(
            SilaOsaka,
            Op.SSTORE(1, 2, key_warm=True),
            SilaOsaka.gas_costs().STORAGE_SET
            + SilaOsaka.gas_costs().VERY_LOW * 2,
            id="opcode_with_metadata",
        ),
    ],
)
def test_bytecode_gas_costs(  # noqa: D103
    fork: Fork, bytecode: Bytecode, expected_cost: int
) -> None:
    assert expected_cost == bytecode.gas_cost(fork)


@pytest.mark.parametrize(
    "fork,opcode,expected_refund",
    [
        pytest.param(
            SilaOsaka,
            Op.SSTORE(original_value=0, new_value=0),
            0,
            id="sstore_no_refund_zero_to_zero",
        ),
        pytest.param(
            SilaOsaka,
            Op.SSTORE(original_value=1, new_value=1),
            0,
            id="sstore_no_refund_nonzero_to_nonzero",
        ),
        pytest.param(
            SilaOsaka,
            Op.SSTORE(original_value=1, new_value=0),
            SilaOsaka.gas_costs().REFUND_STORAGE_CLEAR,
            id="sstore_refund_clear_storage",
        ),
        pytest.param(
            SilaOsaka,
            Op.ADD,
            0,
            id="add_no_refund",
        ),
        pytest.param(
            SilaOsaka,
            Op.MSTORE,
            0,
            id="mstore_no_refund",
        ),
        # Legacy storage refunds, every clearing write refunds.
        pytest.param(
            SilaHomestead,
            Op.SSTORE(original_value=5, new_value=0),
            15_000,
            id="sstore_clear_homestead",
        ),
        pytest.param(
            SilaHomestead,
            Op.SSTORE(original_value=0, current_value=5, new_value=0),
            15_000,
            id="sstore_re_clear_homestead",
        ),
        # SIP-2200 net metering refunds at SilaIstanbul.
        pytest.param(
            SilaIstanbul,
            Op.SSTORE(original_value=5, current_value=6, new_value=5),
            5_000 - 800,
            id="sstore_restore_reset_istanbul",
        ),
        pytest.param(
            SilaIstanbul,
            Op.SSTORE(original_value=0, current_value=5, new_value=0),
            20_000 - 800,
            id="sstore_restore_set_istanbul",
        ),
        # SIP-2929 warm and cold refund terms.
        pytest.param(
            SilaOsaka,
            Op.SSTORE(original_value=5, current_value=6, new_value=5),
            SilaOsaka.gas_costs().COLD_STORAGE_WRITE
            - SilaOsaka.gas_costs().COLD_STORAGE_ACCESS
            - SilaOsaka.gas_costs().WARM_SLOAD,
            id="sstore_restore_reset_osaka",
        ),
        # SIP-3529 boundary for the storage clear refund.
        pytest.param(
            SilaBerlin,
            Op.SSTORE(original_value=5, new_value=0),
            15_000,
            id="sstore_clear_berlin",
        ),
        # SELFDESTRUCT refund until SIP-3529 removes it.
        pytest.param(
            SilaHomestead,
            Op.SELFDESTRUCT(self_destructed_account=True),
            24_000,
            id="selfdestruct_refund_homestead",
        ),
        pytest.param(
            SilaBerlin,
            Op.SELFDESTRUCT(self_destructed_account=True),
            24_000,
            id="selfdestruct_refund_berlin",
        ),
        pytest.param(
            SilaOsaka,
            Op.SELFDESTRUCT(self_destructed_account=True),
            0,
            id="selfdestruct_refund_osaka",
        ),
    ],
)
def test_opcode_refunds(fork: Fork, opcode: Op, expected_refund: int) -> None:  # noqa: D103
    op_refund_calc = fork.opcode_refund_calculator()
    assert expected_refund == op_refund_calc(opcode)


@pytest.mark.parametrize(
    "fork,bytecode,expected_refund",
    [
        pytest.param(
            SilaOsaka,
            Op.SSTORE(original_value=1, new_value=0),
            SilaOsaka.gas_costs().REFUND_STORAGE_CLEAR,
            id="single_sstore_clear",
        ),
        pytest.param(
            SilaOsaka,
            Op.SSTORE(original_value=2, new_value=0)
            + Op.SSTORE(original_value=1, new_value=0),
            SilaOsaka.gas_costs().REFUND_STORAGE_CLEAR * 2,
            id="double_sstore_clear",
        ),
        pytest.param(
            SilaOsaka,
            Op.SSTORE(original_value=1, new_value=2)
            + Op.SSTORE(original_value=1, new_value=0),
            SilaOsaka.gas_costs().REFUND_STORAGE_CLEAR,
            id="mixed_sstore_one_clear",
        ),
        pytest.param(
            SilaOsaka,
            Op.ADD + Op.SUB,
            0,
            id="no_refund_opcodes",
        ),
    ],
)
def test_bytecode_refunds(  # noqa: D103
    fork: Fork, bytecode: Bytecode, expected_refund: int
) -> None:
    assert expected_refund == bytecode.refund(fork)


@pytest.mark.parametrize(
    "fork,opcode,expected_cost",
    [
        # No-op: new == current (value_reset=True on clean slot)
        pytest.param(
            SilaOsaka,
            Op.SSTORE(key_warm=True, original_value=0, new_value=0),
            SilaOsaka.gas_costs().WARM_SLOAD,
            id="sstore_noop_zero_warm",  # 0 → 0
        ),
        pytest.param(
            SilaOsaka,
            Op.SSTORE(key_warm=False, original_value=0, new_value=0),
            SilaOsaka.gas_costs().COLD_STORAGE_ACCESS
            + SilaOsaka.gas_costs().WARM_SLOAD,
            id="sstore_noop_zero_cold",  # 0 → 0
        ),
        pytest.param(
            SilaOsaka,
            Op.SSTORE(key_warm=True, original_value=5, new_value=5),
            SilaOsaka.gas_costs().WARM_SLOAD,
            id="sstore_noop_nonzero_warm",  # 5 → 5
        ),
        pytest.param(
            SilaOsaka,
            Op.SSTORE(key_warm=False, original_value=5, new_value=5),
            SilaOsaka.gas_costs().COLD_STORAGE_ACCESS
            + SilaOsaka.gas_costs().WARM_SLOAD,
            id="sstore_noop_nonzero_cold",  # 5 → 5
        ),
        # Create storage: 0 → X (original == 0)
        pytest.param(
            SilaOsaka,
            Op.SSTORE(key_warm=True, new_value=5),
            SilaOsaka.gas_costs().STORAGE_SET,
            id="sstore_create_warm",  # 0 → 5
        ),
        pytest.param(
            SilaOsaka,
            Op.SSTORE(key_warm=False, new_value=5),
            SilaOsaka.gas_costs().COLD_STORAGE_ACCESS
            + SilaOsaka.gas_costs().STORAGE_SET,
            id="sstore_create_cold",  # 0 → 5
        ),
        # Modify storage: X → Y (original != 0, new != 0, new != original)
        pytest.param(
            SilaOsaka,
            Op.SSTORE(key_warm=True, original_value=5, new_value=7),
            SilaOsaka.gas_costs().STORAGE_RESET,
            id="sstore_modify_warm",  # 5 → 7
        ),
        pytest.param(
            SilaOsaka,
            Op.SSTORE(key_warm=False, original_value=5, new_value=7),
            SilaOsaka.gas_costs().COLD_STORAGE_ACCESS
            + SilaOsaka.gas_costs().STORAGE_RESET,
            id="sstore_modify_cold",  # 5 → 7
        ),
        # Clear storage: X → 0 (original != 0, new == 0)
        pytest.param(
            SilaOsaka,
            Op.SSTORE(key_warm=True, original_value=5, new_value=0),
            SilaOsaka.gas_costs().STORAGE_RESET,
            id="sstore_clear_warm",  # 5 → 0
        ),
        pytest.param(
            SilaOsaka,
            Op.SSTORE(key_warm=False, original_value=5, new_value=0),
            SilaOsaka.gas_costs().COLD_STORAGE_ACCESS
            + SilaOsaka.gas_costs().STORAGE_RESET,
            id="sstore_clear_cold",  # 5 → 0
        ),
        # Legacy SSTORE, charged by the current value only. Literal
        # values pin the historical schedule from the EELS vm/gas.py
        # constants of each fork.
        pytest.param(
            SilaHomestead,
            Op.SSTORE(new_value=5),
            20_000,
            id="sstore_set_homestead",  # 0 → 5
        ),
        pytest.param(
            SilaHomestead,
            Op.SSTORE(original_value=5, new_value=0),
            5_000,
            id="sstore_clear_homestead",  # 5 → 0
        ),
        pytest.param(
            SilaHomestead,
            Op.SSTORE(original_value=5, current_value=0, new_value=7),
            20_000,
            id="sstore_dirty_set_homestead",  # 5 → 0 → 7
        ),
        pytest.param(
            SilaHomestead,
            Op.SSTORE(key_warm=True, new_value=5),
            20_000,
            id="sstore_warmth_inert_homestead",  # 0 → 5
        ),
        # SIP-2200 net metering at SilaIstanbul.
        pytest.param(
            SilaIstanbul,
            Op.SSTORE(original_value=5, new_value=5),
            800,
            id="sstore_noop_istanbul",  # 5 → 5
        ),
        pytest.param(
            SilaIstanbul,
            Op.SSTORE(original_value=5, current_value=6, new_value=7),
            800,
            id="sstore_dirty_istanbul",  # 5 → 6 → 7
        ),
        pytest.param(
            SilaIstanbul,
            Op.SSTORE(new_value=5),
            20_000,
            id="sstore_set_istanbul",  # 0 → 5
        ),
        pytest.param(
            SilaIstanbul,
            Op.SSTORE(original_value=5, new_value=0),
            5_000,
            id="sstore_clear_istanbul",  # 5 → 0
        ),
    ],
)
def test_sstore_gas_costs(fork: Fork, opcode: Op, expected_cost: int) -> None:
    """Test SSTORE gas costs for all single-SSTORE scenarios."""
    assert opcode.gas_cost(fork) == expected_cost
