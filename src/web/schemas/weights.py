from pydantic import BaseModel, Field

from src import api as domain

__all__ = ["Weights"]


class Weights(BaseModel):
    vocal_harmony: float = Field(default=1, ge=0, le=1)
    accentuation: float = Field(default=1, ge=0, le=1)
    tonic_position: float = Field(default=1, ge=0, le=1)
    internal_rhyme: float = Field(default=1, ge=0, le=1)
    rhythmic_structure: float = Field(default=1, ge=0, le=1)

    def as_domain(self) -> domain.Weights:
        return domain.Weights(
            accentuation=self.accentuation,
            internal_rhyme=self.internal_rhyme,
            rhythmic_structure=self.rhythmic_structure,
            tonic_position=self.tonic_position,
            vocal_harmony=self.vocal_harmony,
        )

    class Config:
        @staticmethod
        def to_kebab(x: str) -> str:
            return x.replace("_", "-")

        alias_generator = to_kebab
        populate_by_name = True
