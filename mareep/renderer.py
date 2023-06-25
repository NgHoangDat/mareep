import os
from pathlib import Path
from typing import *

from jinja2 import Template
from mousse import Dataclass
from typer import progressbar

from .loaders import loaders

__all__ = ["Renderer"]


class Renderer(Dataclass):
    template_path: Path
    output_path: Path
    data_path: Path = None
    case_sensitive: bool = True

    def render(self, **kwargs):
        assert self.template_path.exists(), f"Invalid path: {self.template_path}"

        template_files = []
        if self.template_path.is_dir():
            template_files = [file for file in self.template_path.rglob("*.j2")]
        else:
            template_files = [self.template_path]

        env = os.environ.copy()
        if not self.case_sensitive:
            env = {key.lower(): val for key, val in env.items()}

        if self.data_path is not None:
            assert self.data_path.exists(), f"Invalid path: {self.data_path}"
            data_type = self.data_path.suffix[1:]
            assert data_type in loaders, f"Invalid data file: {self.data_path}"

            data = loaders[data_type].load(self.data_path)
            if not self.case_sensitive:
                data = {key.lower(): val for key, val in data.items()}

            env.update(data)

        if not self.case_sensitive:
            kwargs = {key.lower(): val for key, val in kwargs.items()}

        env.update(kwargs)

        with progressbar(template_files) as progress:
            for template_file in progress:
                with open(template_file) as fin:
                    template: Template = Template(fin.read())

                if template_file.suffix == ".j2":
                    output_file: Path = self.output_path / template_file.stem
                else:
                    output_file: Path = self.output_path / template_file.name

                output_file.parent.mkdir(parents=True, exist_ok=True)

                with open(output_file, "w") as fout:
                    fout.write(template.render(env))
