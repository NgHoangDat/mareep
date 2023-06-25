import re
from importlib import import_module
from pathlib import Path

from mousse import export_subclass

from .loader import Loader


CURRENT_PATH = Path(__file__).resolve()
CURRENT_DIR = CURRENT_PATH.parent

modules = []
loaders = {}

for child in CURRENT_DIR.glob("*"):
    if child.is_dir() and not child.name.startswith("_"):
        module = import_module(f".{child.name}", package=__name__)
        modules.append(child.name)
        for key, val in export_subclass(Loader, module=module).items():
            match = re.match(".+(?=Loader)", key)
            if match:
                start, end = match.span()
                loaders[key[start:end].lower()] = val()


__all__ = ["loaders"] + modules
