from pydantic import BaseModel


class ExtraescolarResponse(BaseModel):
    culturales: list[str]
    deportivas: list[str]
