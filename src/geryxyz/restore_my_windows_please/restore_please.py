import argparse
import json
from pathlib import Path

import structlog

logger = structlog.stdlib.get_logger()


def main():
    parser = argparse.ArgumentParser(description="Restore your windows")
    parser.add_argument("--preset", type=Path, help="Preset to use")
    args = parser.parse_args()

    logger.info("Restoring windows", preset=args.preset)
    preset_file: Path = args.preset
    entries = json.loads(preset_file.read_text())


if __name__ == "__main__":
    main()