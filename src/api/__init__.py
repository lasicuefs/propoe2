from dataclasses import dataclass
from functools import lru_cache
import random

from src.model.filter import Filter
from src.model.mives import Mives
from src.model.poem_builder import PoemBuilder
from src.model.rhyme import Rhyme


@dataclass(frozen=True, kw_only=True)
class Weights:
    """Propoe's Evaluation Weights.

    This will define how Propoe should evaluate and take decisions
    for the poem making.

    Attributes
    ----------
    vocal_harmony: int
        Toante & consonant rhymes' weight

    accentuation: int
        Accentuation's weight

    tonic_position: int
        Tonical Position's weight

    internal_rhyme: int
        Internal rhymes's weight

    rhythmic_structure: int
        Rhythmic structure's weight

    Note
    ----
    All values are set-up to 1 by default.
    """

    vocal_harmony: int = 1
    accentuation: int = 1
    tonic_position: int = 1
    internal_rhyme: int = 1
    rhythmic_structure: int = 1

    @property
    @lru_cache
    def as_dict(self) -> dict[str, int]:
        """Returns itself as a dict[str, int]

        Note
        ----
        The returned keys does not matches with the real attribute's name,
        but with the internal API that is written in Portuguese.
        """
        return {
            "Rima toante & consoante": self.vocal_harmony,
            "Acentuacao": self.accentuation,
            "Posicao tonica": self.tonic_position,
            "Rima interna": self.internal_rhyme,
            "Estrutura ritmica": self.rhythmic_structure,
        }


@dataclass(frozen=True)
class Prosody:
    """Poem's Rythm and Rythm

    Attributes
    ----------
    rhythm: list[int]
        The Rhythm's Pattern

    rhyme: str
        The Rhyme's Pattern

    pattern: str
        The Rhyme's Pattern. Alternative to ``rhyme``

    Example
    -------
    >>> Prosody("ABAB CD", [10, 12, 10, 12, 7, 7])
    >>> Prosody("ABAB CD", [10, 12, 10, 12, None, None])

    Raises
    ------
    AssertionError:
        If the Rhyme and Rhythm's lenght are different.
        They should be one to one.

    Deprecates
    ----------
    This substitutes the variables `metrificacao` and `padrao_ritmico`, used before.
    """

    _rhyme_pattern: str
    _raw_rhythm_pattern: list[int | str | None]

    def __post_init__(self):
        assert len(self._stanzaless_rhyme) == len(self._raw_rhythm_pattern)

    @property
    def _final_rhythm(self) -> list[int]:
        """Final Rhythm

        Replaces all unknown values by a random number between 3 and 12.
        """
        return [
            value
            if isinstance(value, int) and value > 0
            else random.randrange(3, 13)
            for value in self._raw_rhythm_pattern
        ]

    @property
    def _stanzaless_rhyme(self) -> str:
        return self._rhyme_pattern.replace(" ", "")

    @property
    def rhythm(self) -> list[int]:
        """The Rhythm's Pattern"""
        return self._final_rhythm

    @property
    def rhyme(self) -> str:
        """The Rhyme's Pattern"""
        return self._rhyme_pattern

    @property
    def pattern(self) -> str:
        """The Rhyme's Pattern

        Alternative to ``rhyme``.
        """
        return self.rhyme


@dataclass(frozen=True, kw_only=True)
class Propoe:
    filename: str
    mives_file: str
    prosody: Prosody
    evaluation_weights: Weights
    seed: int | None = None

    @property
    def builder(self) -> PoemBuilder:
        return PoemBuilder(
            self.sentences,
            self.prosody.rhythm,
            self.prosody.pattern,
            self.evaluation_weights.as_dict,
            self.filename,
            self.seed,
        )

    @property
    def filter(self) -> Filter:
        return Filter(
            sentences=Mives(self.mives_file).sentences,
            metric=self.prosody.rhythm,
            rhyme_pattern=self.prosody.pattern,
            seed=self.seed,
        )

    @property
    def sentences(self) -> dict[str, Rhyme]:
        return self.filter.get_rhymes()

    def build(self) -> None:
        builder = self.builder
        builder.build()
        builder.result()
