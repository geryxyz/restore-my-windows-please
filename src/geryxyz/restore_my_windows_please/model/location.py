import re

from ahk import AHK
from pydantic import BaseModel


class LocationDeclaration(BaseModel):
    process_regex: str = ".*"
    window_title_regex: str = ".*"
    top: int = 0
    left: int = 0
    width: int = 100
    height: int = 100
    
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
                window.move(self.left, self.top, width=self.width, height=self.height)
                window.activate()
