
from dataclasses import dataclass
import pathlib


@dataclass
class FileSpec:
    name: str
    src: pathlib.Path
    dst: pathlib.Path
    is_dir: bool