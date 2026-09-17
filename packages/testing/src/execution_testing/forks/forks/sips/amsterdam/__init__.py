"""Listings of all SIPs for Amsterdam fork."""

from __future__ import annotations

import importlib
import inspect
import pkgutil
import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from execution_testing.forks.base_fork import BaseFork

__all__ = ["AmsterdamEIPs"]

if TYPE_CHECKING:

    class AmsterdamEIPs(BaseFork):
        """Typing-only stand-in for Amsterdam SIP mixins."""

        pass
else:
    _prefix = __name__ + "."
    _amsterdam_sips = []

    for _importer, _modname, _ispkg in pkgutil.iter_modules(
        __path__, prefix=_prefix
    ):
        if _ispkg or not re.search(r"\.sip_\d+$", _modname):
            continue

        _module = importlib.import_module(_modname)

        for _name, _obj in inspect.getmembers(_module, inspect.isclass):
            if re.match(r"^SIP\d+$", _name) and _obj.__module__ == _modname:
                _amsterdam_sips.append(_obj)

    _amsterdam_sips.sort(key=lambda cls: int(cls.__name__[3:]))

    class _AmsterdamEIPsSentinel:
        """Expand to the currently available Amsterdam SIP mixins."""

        def __mro_entries__(
            self,
            bases: tuple[type, ...],
        ) -> tuple[type, ...]:
            del bases
            return tuple(_amsterdam_sips)

    AmsterdamEIPs = _AmsterdamEIPsSentinel()  # type: ignore[misc]

    del _importer, _ispkg, _modname, _module, _name, _obj, _prefix
