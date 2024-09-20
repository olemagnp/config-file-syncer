
from collections.abc import Callable
import os
import pathlib
import shutil
from typing import Iterable

from .filespec import FileSpec
from .file_finder import FileFinder


class Unpacker:
    def __init__(self, appdir: str):
        self.dir = pathlib.Path(appdir)
        self.filespecs = FileFinder().get_files(self.dir)
        
    def _check_exists(self, filespec: FileSpec, filefinder: Callable[[FileSpec], Iterable[pathlib.Path]] = lambda f: (f.src,)):
        files = filefinder(filespec)
        for file in files:
            if not file.exists():
                raise ValueError(f"File does not exists: {file.exists}")

    def powershell_script(self,):
        for filespec in self.filespecs:
            self._check_exists(filespec)
            print(f"New-Item -Path {filespec.dst} -Value {filespec.src} -ItemType SymbolicLink -Force")

    def perform_unpack(self, dry_run: bool):
        for filespec in self.filespecs:
            self._check_exists(filespec)
            print(f"Creating symlink for {"dir" if filespec.is_dir else "file"} {filespec.name}")
            print(f"\tsrc: {filespec.src}")
            print(f"\tdst: {filespec.dst}")
            if not dry_run:
                os.symlink(filespec.src, filespec.dst, target_is_directory=filespec.is_dir)

    def copy_to_targets(self, dry_run: bool):
        for filespec in self.filespecs:
            print()
            print(f"{filespec.name}:")
            print(f"\tCopying from {filespec.src} to {filespec.dst}")
            self._check_exists(filespec)
            if filespec.dst.exists():
                cont = input(f"\tTarget file {filespec.dst} already exists, and will be {"merged with" if filespec.is_dir else "overidden by"} the new content. Continue? [Y/n]")
                if cont.lower() == "n":
                    print("\tSkipping")
                    continue
            if not dry_run:
                if filespec.is_dir:
                    shutil.copytree(filespec.src, filespec.dst, dirs_exist_ok=True)
                else:
                    shutil.copy2(filespec.src, filespec.dst)

    def fetch_from_targets(self, dry_run: bool):
        for filespec in self.filespecs:
            print()
            print(f"{filespec.name}:")
            print(f"\tCopying from {filespec.dst} to {filespec.src}")
            if not filespec.dst.exists():
                print(f"\tTarget file {filespec.dst} not found.\nSkipping.")
                continue
            if filespec.src.exists():
                cont = input(f"\tSource file {filespec.src} already exists, and will be overidden. Continue? [Y/n]")
                if cont.lower() == "n":
                    print("\tSkipping")
                    continue
            if not dry_run:
                if filespec.is_dir:
                    shutil.copytree(filespec.dst, filespec.src, dirs_exist_ok=True)
                else:
                    shutil.copy2(filespec.dst, filespec.src)
