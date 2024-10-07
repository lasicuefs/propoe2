from typing import Literal
from .utils import (
    scanned_sentence_preprocess,
    sentence_preprocess,
    remove_end_ponctuation,
)
# TODO: resolve importing missing file
from .utils import left_consonant_removal

# TODO: Should it be an ``StrEnum``?
type AccentationKind = (
    Literal["Esdrúxula"] | Literal["Grave"] | Literal["Aguda"]
)

class VerseStructure:
    # TODO: define what each attribute here is
    # TODO: define what each method does

    def __init__(
        self, sentence, syllable_number, stress_position, scanned_sentence
    ) -> None:
        self.metric: int = int(syllable_number)
        self.stress_position = stress_position.split()
        self.scanned_sentence = scanned_sentence
        self.accent: AccentationKind | None = self.accentuation()
        self.syllables = self.get_syllables()
        self.sentence = sentence

        self.stress_syllables, self.pos_stress_dict = self.stress_syllable()

    def __repr__(self) -> str:
        return (
            "\n Syllable number: "
            + str(self.metric)
            + "\n Stress position: "
            + " ".join(self.stress_position)
            + "\n Scanned sentence: "
            + self.scanned_sentence
            + "\n Stress syllables: "
            + str(self.stress_syllables)
            + "\n Accentuation: "
            + str(self.accent)
        )

    def get_syllables(self) -> list[str]:
        sentence = scanned_sentence_preprocess(self.scanned_sentence)
        return [s.strip() for s in sentence.split("/")]

    def get_last_word(self) -> str:
        sentence = sentence_preprocess(self.sentence)
        word = sentence.split(" ")[-1].strip()
        return word

    def get_last_stress(self):
        return self.stress_syllables[-1].strip()

    def get_last_syllables(self) -> str:
        after = self.syllables[int(self.stress_position[-1]) :]
        stress = self.scanned_sentence.split("/")[
            int(self.stress_position[-1]) - 1
        ]
        stress = stress.split("#")[-1]
        after.insert(0, stress)
        return remove_end_ponctuation("".join(after))

    def stress_syllable(self):
        # TODO: define what is the return type of this method
        """
        Return:
          syllables: List of stressed syllables.
          pos_syllables: Dict that maps stress position to the syllable.
        """
        syllables = []
        pos_syllables = {}
        splited_sentence = self.scanned_sentence.split("/")
        for pos in self.stress_position:
            s = splited_sentence[int(pos) - 1]
            syllables.append(s.strip())
            pos_syllables[pos] = s.strip()
        return syllables, pos_syllables

    def accentuation(self) -> AccentationKind | None:
        """Return accentutation of the sentence."""
        s = remove_end_ponctuation(self.scanned_sentence)
        last_word = s.split()[-1]
        syllables = last_word.split("/")
        for i in range(1, len(syllables) + 1):
            if "#" in syllables[-i]:
                if i == 3:
                    return "Esdrúxula"
                elif i == 2:
                    return "Grave"
                elif i == 1:
                    return "Aguda"
