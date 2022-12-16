import re
import spacy

class Analizer:

    nlp = spacy.load("ja_ginza")

    def text_of_sequence_of_words(text):
        """ 形態素解析を行う """

        doc = Analizer.nlp(text)
        sequence = []
        for token in doc:
            sequence.append(token.text, token.pos_)

        return sequence


    def is_noun(part):
            return re.match('NOUN|PROPN',part)

