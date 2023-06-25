from abc import ABCMeta, abstractmethod
from pathlib import Path
from typing import Dict, Any


class Loader(metaclass=ABCMeta):
    @abstractmethod
    def load(self, path: Path, **kwargs) -> Dict[str, Any]:
        pass
