import argparse
import json
from pathlib import Path

import structlog

from geryxyz.restore_my_windows_please.model.location import LocationDeclaration

logger = structlog.stdlib.get_logger()


def main():
    parser = argparse.ArgumentParser(description="Restore your windows")
    parser.add_argument("preset", type=Path, help="Preset to use")
    args = parser.parse_args()

    logger.info("Restoring windows", preset=args.preset)
    with open(args.preset, "r") as preset_file:
        entries = json.load(preset_file)
        entries = [LocationDeclaration(**entry) for entry in entries]

    for entry in entries:
        entry.restore()


if __name__ == "__main__":
    main()
