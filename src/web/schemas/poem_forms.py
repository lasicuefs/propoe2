from enum import StrEnum
from typing import Annotated, Self, Union

from pydantic import BaseModel, Field, model_validator

from src import api as domain
from src.web.schemas._util import to_kebab

__all__ = ["PoemForms"]

type Rhythm = list[Union[int, str, None]]


class AvailableLiteraryWorks(StrEnum):
    """All available literary works for poem generation."""

    OS_SERTOES = "xml/sentencas.xml"
    MACUNAIMA = "xml/sentencas.xml"


class LiteraryWork(BaseModel):
    """Literary work schema."""

    name: Annotated[
        str,
        Field(
            examples=["OS_SERTOES"],
            min_length=1,
            max_length=50,
            pattern=r"^[A-Z_]+",
            strict=True,
        ),
    ]

    @model_validator(mode="after")
    def validate_status(self, value) -> Self:
        assert AvailableLiteraryWorks[self.name.upper()].name
        return self

    def value(self) -> str:
        return AvailableLiteraryWorks[self.name.upper()].value


class Prosody(BaseModel):
    """The Prosody's entry Schema."""

    pattern: Annotated[
        str,
        Field(
            examples=["ABAB CDCD", "AABB CC DD"],
            min_length=1,
            max_length=100,
            pattern=r"^[A-Z]+"  # First stanza
            + r"( [A-Z]+)*$",  # Left optional stanzas
            strict=True,
        ),
    ]
    rhythm: Annotated[
        Rhythm,
        Field(
            examples=[
                [10] * 8,
                [10, 10, None, None, 5],
            ],
            min_length=1,
            max_length=100,
            strict=True,
        ),
    ]

    @model_validator(mode="after")
    def rhythm_and_pattern_matches(self) -> Self:
        """Checks if Rhythm and Pattern has the same length"""

        assert len(self.rhythm) == len(
            self.pattern.replace(" ", "")
        ), "Pattern's and Rythm's lenghts don't match"

        return self

    def as_domain(self) -> domain.Prosody:
        """Converts the Schema to Domain's model"""

        return domain.Prosody(self.pattern, self.rhythm)


class Weights(BaseModel):
    """Weights' schema"""

    vocal_harmony: float = Field(default=1, ge=0)
    accentuation: float = Field(default=1, ge=0)
    tonic_position: float = Field(default=1, ge=0)
    internal_rhyme: float = Field(default=1, ge=0)
    rhythmic_structure: float = Field(default=1, ge=0)
    semantic_similarity: float = Field(default=1, ge=0)
    metaphor: float = Field(default=1, ge=0)

    def as_domain(self) -> domain.Weights:
        """Converts the Schema to Domain's model"""

        return domain.Weights(
            accentuation=self.accentuation,
            internal_rhyme=self.internal_rhyme,
            rhythmic_structure=self.rhythmic_structure,
            tonic_position=self.tonic_position,
            vocal_harmony=self.vocal_harmony,
            semantic_similarity = self.semantic_similarity,
            metaphor = self.metaphor
        )

    class Config:
        """Allows ``kebab-case`` instead of ``snake_case``."""

        alias_generator = to_kebab
        populate_by_name = True


class PoemForms(BaseModel):
    """Entry Scheme for the /poem/ endpoint"""

    prosody: Prosody
    weights: Weights
