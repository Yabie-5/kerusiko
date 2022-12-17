import re
import spacy
import warnings

warnings.simplefilter('ignore')

class Analizer:

    nlp = spacy.load("ja_ginza")

    def analyzer(text):
        """ 形態素解析を行う """

        doc = Analizer.nlp(text)
        sequence = []
        for token in doc:
            sequence.append([token.text, token.pos_])

        return sequence


    def is_noun(part):
            return re.match('NOUN|PROPN',part)

