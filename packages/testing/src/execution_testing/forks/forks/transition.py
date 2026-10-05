"""List of all transition fork definitions."""

from ..transition_base_fork import transition_fork
from .forks import (
    BPO1,
    BPO2,
    BPO3,
    BPO4,
    SilaAmsterdam,
    SilaBerlin,
    SilaCancun,
    SilaLondon,
    SilaOsaka,
    SilaParis,
    SilaPrague,
    SilaShanghai,
)


# Transition Forks
@transition_fork(to_fork=SilaLondon, at_block=5)
class SilaBerlinToSilaLondonAt5(SilaBerlin):
    """SilaBerlin to SilaLondon transition at Block 5."""

    pass


@transition_fork(to_fork=SilaShanghai, at_timestamp=15_000)
class SilaParisToSilaShanghaiAtTime15k(SilaParis):
    """SilaParis to SilaShanghai transition at Timestamp 15k."""

    pass


@transition_fork(to_fork=SilaCancun, at_timestamp=15_000)
class SilaShanghaiToSilaCancunAtTime15k(SilaShanghai):
    """SilaShanghai to SilaCancun transition at Timestamp 15k."""

    pass


@transition_fork(to_fork=SilaPrague, at_timestamp=15_000)
class SilaCancunToSilaPragueAtTime15k(SilaCancun):
    """SilaCancun to SilaPrague transition at Timestamp 15k."""

    pass


@transition_fork(to_fork=SilaOsaka, at_timestamp=15_000)
class SilaPragueToSilaOsakaAtTime15k(SilaPrague):
    """SilaPrague to SilaOsaka transition at Timestamp 15k."""

    pass


@transition_fork(to_fork=BPO1, at_timestamp=15_000)
class SilaOsakaToBPO1AtTime15k(SilaOsaka):
    """SilaOsaka to BPO1 transition at Timestamp 15k."""

    pass


@transition_fork(to_fork=BPO2, at_timestamp=15_000)
class BPO1ToBPO2AtTime15k(BPO1):
    """BPO1 to BPO2 transition at Timestamp 15k."""

    pass


@transition_fork(to_fork=SilaAmsterdam, at_timestamp=15_000)
class BPO2ToSilaAmsterdamAtTime15k(BPO2):
    """BPO2 to SilaAmsterdam transition at Timestamp 15k."""

    # TODO: We may need to adjust which BPO SilaAmsterdam inherits from as the
    #  related SilaAmsterdam specs change over time, and before SilaAmsterdam is
    #  live on mainnet.

    pass


@transition_fork(to_fork=BPO3, at_timestamp=15_000)
class BPO2ToBPO3AtTime15k(BPO2):
    """BPO2 to BPO3 transition at Timestamp 15k."""

    pass


@transition_fork(to_fork=BPO4, at_timestamp=15_000)
class BPO3ToBPO4AtTime15k(BPO3):
    """BPO3 to BPO4 transition at Timestamp 15k."""

    pass
