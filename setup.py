from pathlib import Path
from typing import *

import setuptools

__PACKAGE__ = "mareep"
__VERSION__ = "0.0.3"

base_dir = Path(__file__).resolve().parent

with open(base_dir / "README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


def read_requirements(path: Union[str, Path]):
    with open(path, "r") as fh:
        return {line.strip() for line in fh.readlines() if not line.startswith("#")}


requirements = list(read_requirements(base_dir / "requirements.txt"))

extras_require = {}
for path in Path("extras").rglob("*.txt"):
    extras_require[path.stem] = read_requirements(path)

packages = setuptools.find_packages()
entry_points = {"console_scripts": (f"{__PACKAGE__} = {__PACKAGE__}.__main__:main",)}


setuptools.setup(
    name=__PACKAGE__,
    packages=packages,
    version=__VERSION__,
    author="nghoangdat",
    author_email="18.hoang.dat.12@gmail.com",
    description=__PACKAGE__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/NgHoangDat/{__PACKAGE__}.git",
    download_url=f"https://github.com/NgHoangDat/{__PACKAGE__}/archive/v{__VERSION__}.tar.gz",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points=entry_points,
    install_requires=requirements,
    extras_require=extras_require,
)
