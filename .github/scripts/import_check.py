"""
Import every module shipped in the spec wheel.

Run with an interpreter that has only the `sila-execution` wheel
installed: importing every module catches undeclared dependencies and
modules missing from the packages list, which only fail outside the
uv workspace.
"""

import importlib
import pkgutil

import sila
import sila_spec_tools

# `docc` plugins only load once the `doc` group installs docc, and
# importing a `__main__` would run it.
SKIP = {"sila_spec_tools.docc"}

for pkg in (sila, sila_spec_tools):
    for mod in pkgutil.walk_packages(pkg.__path__, f"{pkg.__name__}."):
        if mod.name in SKIP or mod.name.endswith(".__main__"):
            continue
        importlib.import_module(mod.name)
