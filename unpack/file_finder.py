import pathlib
from typing import List

import yaml

from .filespec import FileSpec


class FileFinder:
    def __init__(self):
        self.replacements = {}
    
    def _get_system_path(self, sys_path_str: str) -> pathlib.Path:
        path = sys_path_str
        for old, new in self.replacements.items():
            path = path.replace(old, new)
        return pathlib.Path(path).expanduser().absolute()

    def get_files(self, dir: pathlib.Path) -> List[FileSpec]:
        yaml_path = dir.joinpath("_paths.yaml").expanduser()
        if not yaml_path.exists():
            raise ValueError("Directory does not contain any '_paths.yaml' files")
        
        with open(yaml_path, "r") as f:
            data = yaml.safe_load(f)
            
            paths_spec = data["paths"]
            files = []
            
            for file_desc, file_spec in paths_spec.items():
                src = dir.joinpath(file_spec["src"])
                dst = self._get_system_path(file_spec["dst"])
                is_dir = file_spec["is_dir"] if "is_dir" in file_spec else False
                
                files.append(FileSpec(file_desc, src, dst, is_dir))
        return files