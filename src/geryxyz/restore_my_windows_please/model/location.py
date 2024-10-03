import re
from enum import StrEnum, IntEnum
from time import sleep

import structlog
from ahk import AHK
from pydantic import BaseModel


logger = structlog.stdlib.get_logger()


class WindowState(IntEnum):
    MINIMIZED = -1
    MAXIMIZED = 1
    RESTORED = 0


class LocationDeclaration(BaseModel):
    process_regex: str = ".*"
    window_title_regex: str = ".*"
    top: int = 0
    left: int = 0
    width: int = 100
    height: int = 100
    state: WindowState | None = None

    
    class Config:
        frozen = True
        arbitrary_types_allowed = False

    @property
    def unique_id(self) -> tuple[str, str]:
        return self.process_regex, self.window_title_regex

    def restore(self):
        ahk = AHK()
        windows = ahk.list_windows()
        for window in windows:
            title_match = re.search(self.window_title_regex, window.title)
            process_match = re.search(self.process_regex, window.process_name)
            if title_match and process_match:
                if self.state == WindowState.MAXIMIZED:
                    window.maximize()
                    logger.info("Maximized window", window=window.title, process=window.process_name)
                elif self.state == WindowState.MINIMIZED:
                    window.minimize()
                    logger.info("Minimized window", window=window.title, process=window.process_name)
                else:
                    window.move(self.left, self.top, width=self.width, height=self.height)
                    window.restore()
                    logger.info("Restored window", window=window.title, process=window.process_name)
