__all__ = ["Prosody"]

from typing import Any, Self, Union
from pydantic import BaseModel, Field, model_validator

from src import api as domain

type Rhythm = list[Union[int, str, None]]


class Prosody(BaseModel):
    pattern: str = Field(
        examples=["ABAB CDCD", "AABB CC DD"]
    )
    rhythm: Rhythm = Field(
        examples=[
            [10, 10, 5, 5, 5],
            [10, 10, None, None, 5],
        ]
    )

    @model_validator(mode="after")
    def rhythm_and_pattern_matches(self, value: Any) -> Self:
        assert len(self.rhythm) == len(self.pattern.replace(" ", ""))
        return self
    
    def as_domain(self) -> domain.Prosody:
        return domain.Prosody(
            self.pattern,
            self.rhythm
        )