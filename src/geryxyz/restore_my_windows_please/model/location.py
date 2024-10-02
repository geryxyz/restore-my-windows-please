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
    