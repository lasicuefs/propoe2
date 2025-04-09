from src.model.score import Score
from dataclasses import dataclass

@dataclass
class Poem:
    poem_structure: str
    verses: list[str]
    verses_score: list[Score]
    verse_structure: list
    poem_score: object

    def __repr__(self):
        index = 0
        poem = ""
        for letter in self.poem_structure:
            if letter == " ":
                poem += "\n"
            else:
                poem += self.verses[index] + "\n"
                index += 1
        return poem

