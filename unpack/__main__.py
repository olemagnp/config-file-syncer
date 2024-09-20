from enum import Enum
import sys

from .unpacker import Unpacker

class Actions(Enum):
    POWERSHELL = 1
    SYMLINK = 2
    COPY_IN = 3
    COPY_OUT = 4

def main(action: Actions, appdir: str, dry_run: bool):
    unpacker = Unpacker(appdir)
    
    match action:
        case Actions.POWERSHELL:
            unpacker.powershell_script()
        case Actions.SYMLINK:
            unpacker.perform_unpack(dry_run)
        case Actions.COPY_IN:
            unpacker.fetch_from_targets(dry_run)
        case Actions.COPY_OUT:
            unpacker.copy_to_targets(dry_run)
        case _:
            raise ValueError(f"Illegal action {action}")

if __name__ == "__main__":
    args = {
    "action": Actions[sys.argv[1].upper()],
    "appdir": sys.argv[2],
    "dry_run": (sys.argv[3] if len(sys.argv) > 3 else "false") == "dry-run"
    }

    main(**args)
    