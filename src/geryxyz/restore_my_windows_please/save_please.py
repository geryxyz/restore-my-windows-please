import argparse
import json
from pathlib import Path

import structlog
from ahk import AHK

from geryxyz.restore_my_windows_please.model.location import LocationDeclaration

logger = structlog.stdlib.get_logger()


def main():
    parser = argparse.ArgumentParser(description="Save your windows")
    parser.add_argument("preset", type=Path, help="Preset to use")
    args = parser.parse_args()

    logger.info("Saving windows", preset=args.preset)
    ahk = AHK()
    windows = ahk.list_windows()
    entries = dict()
    for window in windows:
        position = window.get_position()
        declaratoin = LocationDeclaration(
            process_regex=window.process_name,
            window_title_regex=window.title,
            top=position.y,
            left=position.x,
            width=position.width,
            height=position.height,
        )
        entries[declaratoin.unique_id] = declaratoin
    with open(args.preset, "w") as preset_file:
        preset_file.write(json.dumps([value.model_dump() for value in entries.values()], indent=4))


if __name__ == "__main__":
    main()