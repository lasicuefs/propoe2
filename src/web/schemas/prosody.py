__all__ = ["Prosody"]

from typing import Annotated, Any, Self, Union
from pydantic import BaseModel, Field, model_validator

from src import api as domain

type Rhythm = list[Union[int, str, None]]


class Prosody(BaseModel):
    pattern: Annotated[
        str,
        Field(
            examples=["ABAB CDCD", "AABB CC DD"],
            min_length=1,
            max_length=100,
            pattern=r"([A-Z]:whitespace:)*",
        ),
    ]
    rhythm: Annotated[
        Rhythm,
        Field(
            examples=[
                [10] * 8,
                [10, 10, None, None, 5],
            ]
        ),
    ]

    @model_validator(mode="after")
    def rhythm_and_pattern_matches(self, values) -> Self:
        assert len(self.rhythm) == len(self.pattern.replace(" ", ""))
        return self

    def as_domain(self) -> domain.Prosody:
        return domain.Prosody(self.pattern, self.rhythm)
