"""Reference spec for [SIP-7997: Deterministic Factory Predeploy](https://sips.sila.org/SIPS/sip-7997)."""

from dataclasses import dataclass

from execution_testing import Bytes


@dataclass(frozen=True)
class ReferenceSpec:
    """Reference specification."""

    git_path: str
    version: str


ref_spec_7997 = ReferenceSpec(
    git_path="SIPS/sip-7997.md",
    version="a0a7f5adb491fc6ad4b008f307899c30f348db22",
)


@dataclass(frozen=True)
class Spec:
    """Constants from SIP-7997."""

    FACTORY_ADDRESS: int = 0x4E59B44847B379578588920CA78FBF26C0B4956C
    FACTORY_BYTECODE: Bytes = Bytes(
        "7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe0"
        "3601600081602082378035828234f58015156039578182fd"
        "5b8082525050506014600cf3"
    )
