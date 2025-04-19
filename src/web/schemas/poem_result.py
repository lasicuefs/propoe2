from typing import Protocol
from pydantic import BaseModel

from src.model.poem import Poem
from src.model.score import PoemScore as DomainEvaluation
from src.web.schemas._util import to_kebab

__all__ = ["Poem"]


class IsPoem(Protocol):
    """Protocol to avoid import from domain"""

    @property
    def poem(self) -> Poem: ...


class Evaluation(BaseModel):
    """Final evaluation returned by Propoe's algorithm."""

    vocal_harmony: float
    accentuation: float
    tonic_position: float
    internal_rhyme: float
    rhythmic_structure: float
    score: float

    @staticmethod
    def from_domain(model: DomainEvaluation) -> "Evaluation":
        return Evaluation(
            accentuation=model.score.accent_score,
            internal_rhyme=model.score.rhyme_intern_score,
            rhythmic_structure=model.score.rhyme_structure_score,
            tonic_position=model.score.stress_score,
            vocal_harmony=model.score.consonant_rhyme_score,
            score=model.score.score_result,
        )

    class Config:
        """Allows ``kebab-case`` instead of only ``snake_case``"""

        alias_generator = to_kebab
        populate_by_name = True


class Poem(BaseModel):
    """Result schema for ``/poem/`` endpoint"""

    content: list[str]
    evaluation: Evaluation
    id: str = ""

    @staticmethod
    def from_domain(poem: IsPoem) -> "Poem":
        return Poem(
            content=poem.content.splitlines(),
            evaluation=Evaluation.from_domain(poem.evaluation),
        )

    def with_id(self, id: str) -> "Poem":
        self.id = id
        return self
