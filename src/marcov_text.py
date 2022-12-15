import spacy
import random
import re

nlp = spacy.load("ja_ginza")

def text_of_sequence_of_words(text):
    """ 形態素解析を行う """

    doc = nlp(text)
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

def generate(sentence,markov, worldList):
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

def overlap(sentence):
    """ 重複した文章の除去 """

    sentence = sentence.split('。')
    if "" in sentence:
        sentence.remove('')

    new = []
    for str in sentence:
        str += "。"
        if str == "。":
            break
        new.append(str)
    new = set(new)

    sentence = "".join(new)

    return sentence


def get_copath():
    path = "../data/copath.txt"
    file = open(path, 'r', encoding="utf-8")

    text = file.read().replace("\n","")

    sequence_li = text_of_sequence_of_words(text)

    marcov_dict = get_marcov_dict(sequence_li)

    return sequence_li, marcov_dict

if __name__=="__main__":
    sequence_li, marcov_dict = get_copath()
    sentence = ""
    while(not sentence):
        sentence = generate(sentence=sentence, markov=marcov_dict, worldList=sequence_li)
        sentence = overlap(sentence=sentence)

    print(sentence)
    input("[Enter]キーで終了")

