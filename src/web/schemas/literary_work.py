from enum import Enum
from pydantic import BaseModel, Field, model_validator
from typing import Annotated, Self

__all__ = ["LiteraryWork"]


class LiteraryWorkEnum(str, Enum):
    OS_SERTOES = "xml/sentencas.xml"
    MACUNAIMA = "xml/sentencas.xml"


class LiteraryWork(BaseModel):
    name: Annotated[str,
        Field(
            examples=[
               "OS_SERTOES"
            ],
            min_length=1,
            max_length=50,
            pattern=r"^[A-Z_]+",
            strict=True,
        )]

    @model_validator(mode="after")
    def validate_status(self, value) -> Self:
        assert LiteraryWorkEnum[self.name.upper()].name
        return self


    def value(self)-> str:
        return LiteraryWorkEnum[self.name.upper()].value