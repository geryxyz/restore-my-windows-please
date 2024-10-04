import argparse
import json
import re
from pathlib import Path

import structlog
from ahk import AHK

from geryxyz.restore_my_windows_please.model.location import LocationDeclaration, WindowState

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
        minmax_state = window.get_minmax()
        state = WindowState(int(minmax_state))
        if window.process_name == "explorer.exe" and window.title == "Program Manager":
            logger.warn("Skipping desktop window", window=window.title, process=window.process_name)
            continue
        if window.process_name == "explorer.exe" and window.title == "":
            logger.warn("Skipping desktop environment", window=window.title, process=window.process_name)
            continue
        declaration = LocationDeclaration(
            process_regex="^" + re.escape(window.process_name) + "$",
            window_title_regex="^" + re.escape(window.title) + "$",
            top=position.y,
            left=position.x,
            width=position.width,
            height=position.height,
            state=state
        )
        entries[declaration.unique_id] = declaration
        logger.info("Saved window", window=window.title, process=window.process_name)
    with open(args.preset, "w") as preset_file:
        preset_file.write(json.dumps([value.model_dump() for value in entries.values()], indent=4))


if __name__ == "__main__":
    main()