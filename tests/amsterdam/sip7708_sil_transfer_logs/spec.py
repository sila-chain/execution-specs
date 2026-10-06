"""Defines SIP-7708 specification constants and functions."""

from dataclasses import dataclass

from execution_testing import Address, Bytes, Hash, TransactionLog, keccak256


@dataclass(frozen=True)
class ReferenceSpec:
    """Defines the reference spec version and git path."""

    git_path: str
    version: str


ref_spec_7708 = ReferenceSpec(
    "SIPS/sip-7708.md", "73f81186409d3f202d7946a6b24c9d7fad0e9232"
)


class Spec:
    """
    Parameters from the SIP-7708 specifications as defined at
    https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-7708.md.
    """

    SYSTEM_ADDRESS: Address = Address(
        0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFE
    )
    TRANSFER_TOPIC: Hash = Hash(
        keccak256(b"Transfer(address,address,uint256)")
    )


def transfer_log(
    sender: Address, recipient: Address, amount: int
) -> TransactionLog:
    """Create an expected Transfer log for SIP-7708."""
    return TransactionLog(
        address=Spec.SYSTEM_ADDRESS,
        topics=[
            Spec.TRANSFER_TOPIC,
            Hash(bytes(sender).rjust(32, b"\x00")),
            Hash(bytes(recipient).rjust(32, b"\x00")),
        ],
        data=Bytes(amount.to_bytes(32, "big")),
    )
