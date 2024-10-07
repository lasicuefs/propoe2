import xml.etree.ElementTree as ET
from .sentence import Sentence
from .verse_structure import VerseStructure
from .utils import remove_end_ponctuation, remove_pontuation
from .rhyme import Rhyme


class Mives:
    def __init__(self, path):
        # List of Rhyme objects
        self.sentences = self.read(path)

    def read(self, path):
        """Read Mives' XML and return a list of Rhyme objects.

        Parameter:
          path: Location of MIVES' XML.

        Return:
          sentences: List of Rhyme
        """
        tree = ET.parse(path)
        root = tree.getroot()
        all_rhymes = []
        all_sentences = []
        for sentences in root:
            last_syllable, sentence_info = self.get_sentence(sentences)
            if sentence_info:
                if last_syllable not in all_rhymes:
                    all_sentences.append(Rhyme(last_syllable))
                    all_rhymes.append(last_syllable)
                self.find(all_sentences, last_syllable).add(sentence_info)

        return all_sentences

    def find(self, arr, rhyme):
        """Find Rhyme object given rhyme"""
        for x in arr:
            if x.rhyme == rhyme:
                return x

    def get_last_syllable(self, sentence):
        """Find rhyme from the scanned sentence.

        Example:
          Input:
            "A/lar/m#o/u/se/ o/ a/cam/pa/m#en/to."
          Output:
            "to"

        """
        sentence = remove_end_ponctuation(sentence)
        last_syllable = sentence.split("/")[-1].strip()
        last_syllable = remove_pontuation(last_syllable)
        return last_syllable

    def get_verse_info(self, verses, sentence):
        """Extract Verse_structure from XML."""
        syllable_number = verses[0].text
        stress_position = verses[1].text
        scanned_sentence = verses[2].text
        last_syllable = self.get_last_syllable(scanned_sentence)
        return last_syllable, VerseStructure(
            sentence, syllable_number, stress_position, scanned_sentence
        )

    def get_sentence(self, sentences):
        """Read XML, extract object Sentence and its Verse_Strucuture."""
        sentence_obj = None
        sentence = sentences[0].text
        link = sentences[1].text
        sentence_number = sentences[2].text
        verse_structures = []
        for verses in sentences[3]:
            last_syllable, verse_struct = self.get_verse_info(verses, sentence)
            verse_structures.append(verse_struct)
        # Remove error in Mives. Sentences with no stress syllable in the last word
        if (
            "#"
            in remove_end_ponctuation(verse_struct.scanned_sentence).split()[-1]
        ):
            sentence_obj = Sentence(
                sentence, link, sentence_number, verse_structures
            )
        return last_syllable, sentence_obj
