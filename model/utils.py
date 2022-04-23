import re


def sentence_preprocess(sentence):
    sentence = sentence.lower()
    # Remove all pontuation
    sentence = re.sub(
        r'[^\w\sZáàâãéèêíïóôõöúçñ]', '', sentence)
    return sentence


def consonant_removal(sentence):
    sentence = sentence.lower()
    # Remove all pontuation
    sentence = re.sub(
        r'[^aeiouáàâãéèêíïóôõöú]', '', sentence)
    return sentence


def scanned_sentence_preprocess(sentence):
    sentence = sentence.lower()
    # Remove all pontuation
    sentence = re.sub(
        r'[^\w\sZáàâãéèêíïóôõöúçñ/]', '', sentence)
    return sentence


def remove_end_ponctuation(sentence):
    return re.sub('^[^a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ]*|[^a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ]*$', '', sentence)
