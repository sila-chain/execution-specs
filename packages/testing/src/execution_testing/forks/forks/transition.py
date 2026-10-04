"""List of all transition fork definitions."""

from ..transition_base_fork import TransitionBaseClass, transition_fork
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
@transition_fork(to_fork=SilaLondon, from_fork=SilaBerlin, at_block=5)
class SilaBerlinToSilaLondonAt5(TransitionBaseClass):
    """SilaBerlin to SilaLondon transition at Block 5."""

    pass


@transition_fork(
    to_fork=SilaShanghai, from_fork=SilaParis, at_timestamp=15_000
)
class SilaParisToSilaShanghaiAtTime15k(TransitionBaseClass):
    """SilaParis to SilaShanghai transition at Timestamp 15k."""

    pass


@transition_fork(
    to_fork=SilaCancun, from_fork=SilaShanghai, at_timestamp=15_000
)
class SilaShanghaiToSilaCancunAtTime15k(TransitionBaseClass):
    """SilaShanghai to SilaCancun transition at Timestamp 15k."""

    pass


@transition_fork(to_fork=SilaPrague, from_fork=SilaCancun, at_timestamp=15_000)
class SilaCancunToSilaPragueAtTime15k(TransitionBaseClass):
    """SilaCancun to SilaPrague transition at Timestamp 15k."""

    pass


@transition_fork(to_fork=SilaOsaka, from_fork=SilaPrague, at_timestamp=15_000)
class SilaPragueToSilaOsakaAtTime15k(TransitionBaseClass):
    """SilaPrague to SilaOsaka transition at Timestamp 15k."""

    pass


@transition_fork(to_fork=BPO1, from_fork=SilaOsaka, at_timestamp=15_000)
class SilaOsakaToBPO1AtTime15k(TransitionBaseClass):
    """SilaOsaka to BPO1 transition at Timestamp 15k."""

    pass


@transition_fork(to_fork=BPO2, from_fork=BPO1, at_timestamp=15_000)
class BPO1ToBPO2AtTime15k(TransitionBaseClass):
    """BPO1 to BPO2 transition at Timestamp 15k."""

    pass


@transition_fork(to_fork=SilaAmsterdam, from_fork=BPO2, at_timestamp=15_000)
class BPO2ToSilaAmsterdamAtTime15k(TransitionBaseClass):
    """BPO2 to SilaAmsterdam transition at Timestamp 15k."""

    # TODO: We may need to adjust which BPO SilaAmsterdam inherits from as the
    # related SilaAmsterdam specs change over time, and before SilaAmsterdam is
    #  live on sila-mainnet.

    pass


@transition_fork(to_fork=BPO3, from_fork=BPO2, at_timestamp=15_000)
class BPO2ToBPO3AtTime15k(TransitionBaseClass):
    """BPO2 to BPO3 transition at Timestamp 15k."""

    pass


@transition_fork(to_fork=BPO4, from_fork=BPO3, at_timestamp=15_000)
class BPO3ToBPO4AtTime15k(TransitionBaseClass):
    """BPO3 to BPO4 transition at Timestamp 15k."""

    pass
