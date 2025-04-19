from typing import Protocol
from pydantic import BaseModel
from src.model.score import Score as DomainScore


from src.web.schemas._util import to_kebab

__all__ = ["Poem"]


class IsPoem(Protocol):
    """Protocol to avoid import from domain"""
    @property
    def verses(self) -> list[str]:...

    @property
    def scanned_verses(self) -> list[str]: ...

    @property
    def poem_structure(self) -> str: ...

    @property
    def poem_score(self) -> DomainScore: ...

    @property
    def verses_score(self) -> list[DomainScore]: ...

class Score(BaseModel):
    """Final evaluation returned by Propoe's algorithm."""
    vocal_harmony: float
    accentuation: float
    tonic_position: float
    internal_rhyme: float
    rhythmic_structure: float
    score: float

    @staticmethod
    def from_domain(model: DomainScore) -> "Score":
        return Score(
            accentuation=model.accent_score,
            internal_rhyme=model.rhyme_intern_score,
            rhythmic_structure=model.rhyme_structure_score,
            tonic_position=model.stress_score,
            vocal_harmony=model.consonant_rhyme_score,
            score=model.score_result,
        )

    class Config:
        """Allows ``kebab-case`` instead of only ``snake_case``"""
        alias_generator = to_kebab
        populate_by_name = True

class Poem(BaseModel):
    """Result schema for ``/poem/`` endpoint"""

    verses:list[str]
    scanned_verses: list[str]
    poem_structure: str
    poem_score: Score
    verses_score: list[Score]
    id: str = ""

    @staticmethod
    def from_domain(poem: IsPoem) -> "Poem":
        verses_score = []
        for score in poem.verses_score:
            verses_score.append(Score.from_domain(score))

        return Poem(verses=poem.verses,
                    scanned_verses=poem.scanned_verses,
                    poem_structure=poem.poem_structure,
                    poem_score=Score.from_domain(poem.poem_score),
                    verses_score=verses_score
                    )

    def with_id(self, id: str) -> "Poem":
        self.id = id
        return self


