from typing import Dict, Any
from pathlib import Path
from ..loader import Loader

import yaml

__all__ = ["YAMLLoader"]


class YAMLLoader(Loader):
    def load(self, path: Path, **kwargs) -> Dict[str, Any]:
        with open(path) as fin:
            return yaml.load(fin, Loader=yaml.Loader)
