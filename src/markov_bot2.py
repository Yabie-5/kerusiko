import spacy
import random
import re
import warnings
from itertools import chain

import analyzer


class Markov:
    nlp = spacy.load("ja_ginza")

    def text_of_sequence_of_words(text):
        """ 形態素解析を行う """

        doc = Markov.nlp(text)
        sequence = []
        for token in doc:
            sequence.append(token.text)

        return sequence

    def get_marcov_dict(wordList):
        markov = {}
        p1 = ''
        p2 = ''
        p3 = ''

        for word in wordList:
            if p1 and p2 and p3:
                if (p1, p2, p3) not in markov:
                    markov[(p1, p2, p3)] = []
                markov[(p1, p2, p3)].append(word)
            p1, p2, p3 = p2, p3, word

        return markov
    
    def get_copath():
        path = "data/copath.txt"
        file = open(path, 'r', encoding="utf-8")

        text = file.read().replace("\n","")

        sequence_li = Markov.text_of_sequence_of_words(text)

        marcov_dict = Markov.get_marcov_dict(sequence_li)

        return sequence_li, marcov_dict

    def generate(sentence, markov, worldList):
        """ マルコフ辞書から文書を作り出す
        """
        p1, p2, p3 = random.choice(list(markov.keys()))

        count = 0

        while count < len(worldList):

            if ((p1, p2, p3) in markov) == True:
                tmp = random.choice(list(markov[(p1, p2, p3)]))
                sentence += tmp

            p1, p2, p3 = p2, p3, tmp
            count += 1

        # sentence = sentence.replace("^ 。", "") と同義
        sentence = re.sub("^.+ 。", "", sentence)

        # 最後の句点(。)から、
        if re.search(".+。", sentence):
            sentence = re.search(".+。", sentence).group()

        sentence = re.sub(" ", "", sentence)

        return sentence

    def make(self):
        sequence_li, marcov_dict = Markov.get_copath()
        sentence = ""
        sentence = Markov.generate(sentence=sentence, markov=marcov_dict, worldList=sequence_li)

        return sentence
    



if __name__=="__main__":
    markov = Markov()
    print("++++++++++++++++++++++++")
    print("++++++++++++++++++++++++")
    print("Starting PRTS system ...")
    text = markov.make()
    sentences = text.split("。")
    if "" in sentences:
        sentences.remove("")
    print("議論しようではないか。")
    

    while True:
        line = input(">")

        parts = analyzer.analyzer(line)

        m = []
        for word, part in parts:

            if analyzer.keyword_check(part):
                
                for element in sentences:
                    find = ".*?" + word + ".*"
                    tmp = re.findall(find, element)

        m = list(chain.from_iterable(m))
        if m:
            print(random.choice(m))
        else:
            print(random.choice(sentences))

