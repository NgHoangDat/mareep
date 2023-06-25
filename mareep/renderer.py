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
    extensions: List[str] = ["j2", "jinja2", "jinja"]

    case_sensitive: bool = True

    use_env: bool = False
    env_prefix: str = ""
    
    vars_path: Path = None
    section: str = None

    output_path: Path

    def render(self, **kwargs):
        assert self.template_path.exists(), f"Invalid path: {self.template_path}"

        template_files = []
        if self.template_path.is_dir():
            template_files = []
            for extension in self.extensions:
                template_files += [
                    file for file in self.template_path.rglob(f"*.{extension}")
                ]
        else:
            template_files = [self.template_path]

        env = {}
        if self.use_env:
            for key, val in os.environ.items():
                if not self.case_sensitive:
                    key = key.lower()
                
                if key.startswith(self.env_prefix):
                    key = key[len(self.env_prefix):]
                    env[key] = val

        if self.vars_path is not None:
            assert self.vars_path.exists(), f"Invalid path: {self.vars_path}"
            data_type = self.vars_path.suffix[1:]
            assert data_type in loaders, f"Invalid data file: {self.vars_path}"

            data = loaders[data_type].load(self.vars_path)
            if self.section is not None:
                data = data[self.section]
            
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

                if template_file.suffix[1:] in self.extensions:
                    output_file: Path = self.output_path / template_file.stem
                else:
                    output_file: Path = self.output_path / template_file.name

                output_file.parent.mkdir(parents=True, exist_ok=True)

                with open(output_file, "w") as fout:
                    fout.write(template.render(env))
