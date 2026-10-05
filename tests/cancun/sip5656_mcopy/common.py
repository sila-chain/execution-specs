"""
Common procedures to test [SIP-5656: MCOPY - Memory copying
instruction](https://github.com/sila-chain/SIPs/blob/main/SIPS/sip-5656.md).
"""

from copy import copy

REFERENCE_SPEC_GIT_PATH = "SIPS/sip-5656.md"
REFERENCE_SPEC_VERSION = "8d98dc3c535067ece64b601bb4bc7c29291512bb"


def mcopy(*, src: int, dest: int, length: int, memory: bytes) -> bytes:
    """Perform the mcopy routine as the Sivm would do it."""
    if length == 0:
        return memory

    res = bytearray(copy(memory))

    # If the destination or source are larger than the memory, we need to
    # extend the memory
    max_byte_index = max(src, dest) + length
    if max_byte_index > len(memory):
        res.extend(b"\x00" * (max_byte_index - len(memory)))

    for i in range(length):
        if (src + i) >= len(memory):
            src_b = 0
        else:
            src_b = memory[src + i]

        res[dest + i] = src_b
    return bytes(res)
