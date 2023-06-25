import json
from typing import Dict, Any
from pathlib import Path
from ..loader import Loader

__all__ = ["JSONLoader"]


class JSONLoader(Loader):
    def load(self, path: Path, **kwargs) -> Dict[str, Any]:
        with open(path) as fin:
            return json.load(fin)
