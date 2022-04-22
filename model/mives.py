import xml.etree.ElementTree as ET
from .sentence import Sentence
from .verse_structure import Verse_structure
import re
from .utils import *
import string


class Mives():

    def __init__(self, path):
        self.sentences = self.read(path)

    def read(self, path):
        tree = ET.parse(path)
        root = tree.getroot()
        all_sentences = {}
        for sentences in root:
            last_syllable, sentence_info = self.get_sentence(sentences)
            if sentence_info:
                if last_syllable not in all_sentences:
                    all_sentences[last_syllable] = []
                all_sentences[last_syllable].append(sentence_info)
        return all_sentences

    def get_last_syllable(self, sentence):
        sentence = remove_end_ponctuation(sentence)
        last_syllable = sentence.split("/")[-1]
        exclude = set(string.punctuation)
        last_syllable = ''.join(
            ch for ch in last_syllable if ch not in exclude)
        return last_syllable

    def get_verse_info(self, verses, sentence):
        syllable_number = verses[0].text
        stress_position = verses[1].text
        scanned_sentence = verses[2].text
        last_syllable = self.get_last_syllable(scanned_sentence)
        return last_syllable,  Verse_structure(sentence, syllable_number, stress_position, scanned_sentence)

    def get_sentence(self, sentences):
        sentence_obj = None
        sentence = sentences[0].text
        link = sentences[1].text
        sentence_number = sentences[2].text
        verse_structures = []
        for verses in sentences[3]:
            last_syllable, verse_struct = self.get_verse_info(verses, sentence)
            verse_structures.append(verse_struct)
        if "#" in remove_end_ponctuation(verse_struct.scanned_sentence).split()[-1]:
            sentence_obj = Sentence(
                sentence, link, sentence_number, verse_structures)
        return last_syllable, sentence_obj
