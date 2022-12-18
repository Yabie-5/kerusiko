import spacy
import random
import re
import warnings
from itertools import chain
import analyzer
import similer

warnings.simplefilter('ignore')

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

        for word in wordList:
            if p1 and p2:
                if (p1, p2) not in markov:
                    markov[(p1, p2)] = []
                markov[(p1, p2)].append(word)
            p1, p2 = p2, word

        return markov
    
    def get_corpus():
        path = "data/corpus.txt"
        file = open(path, 'r', encoding="utf-8")

        text = file.read().replace("\n","")

        sequence_li = Markov.text_of_sequence_of_words(text)

        marcov_dict = Markov.get_marcov_dict(sequence_li)

        return sequence_li, marcov_dict

    def generate(sentence, markov, worldList):
        """ マルコフ辞書から文書を作り出す
        """
        p1, p2 = random.choice(list(markov.keys()))

        count = 0

        while count < len(worldList)*1.5:

            if ((p1, p2) in markov) == True:
                tmp = random.choice(list(markov[(p1, p2)]))
                sentence += tmp

            p1, p2 = p2,tmp
            count += 1

        # sentence = sentence.replace("^ 。", "") と同義
        sentence = re.sub("^.+ 。", "", sentence)

        # 最後の句点(。)から、
        if re.search(".+。", sentence):
            sentence = re.search(".+。", sentence).group()

        sentence = re.sub(" ", "", sentence)

        return sentence

    def make(self):
        sequence_li, marcov_dict = Markov.get_corpus()
        sentence = ""
        sentence = Markov.generate(sentence=sentence, markov=marcov_dict, worldList=sequence_li)

        return sentence
    



if __name__=="__main__":
    markov = Markov()
    print("++++++++++++++++++++++++")
    print("Starting PRTS system ...")
    print("++++++++++++++++++++++++")
    text = markov.make()
    sentences = text.split("。")
    if "" in sentences:
        sentences.remove("")
    print("私に何か用事でもあるのか？")
    
    
    while True:
        line = input(">")
        if line == "":
            print("\n...時間だ。仕事に戻るとしよう")
            break
        
        parts = analyzer.Analizer.analyzer(line)

        input_sentence = [] 
        for sen, pos in parts:
            input_sentence.append(sen)

        similer_words = []
        m = []
        for word, part in parts:

            if analyzer.Analizer.is_noun(part):
                # 入力値の類似単語の抽出
                # ここで、コーパスに入っているか確認する必要あり。
                try:
                    similer_words = similer.Similer.similer(word=word)
                except Exception as e:
                    error_text = f"すまない、{word}は後で覚えておこう。"
                    print(error_text)
                
                similer.Similer.train(input_sentence)


                simi_words = []
                for simi_word in similer_words:
                    simi_parts=analyzer.Analizer.analyzer(simi_word)
                    for simi_word, simi_part in simi_parts:
                        if analyzer.Analizer.is_noun(simi_part):
                            simi_words.append(simi_word)
                

                for element in sentences:
                    find = ".*?" + word + ".*"
                    tmp = re.findall(find, element)
                    if tmp:
                        m.append(tmp)
                    else:
                        for s_w in simi_words:
                            if not len(m)>0:
                                find = ".*?" + s_w + ".*"
                                tmp = re.findall(find, element)
                                if tmp:
                                    m.append(tmp)

                           
        
        m = list(chain.from_iterable(m))

        ans=[]
        for s_w in simi_words:
            if not len(ans)>0:
                for m_ in m:
                    find = ".*?" + s_w + ".*"
                    tmp = re.findall(find, m_)
                    if tmp:
                        ans.append(tmp)
                        sim = s_w

        ans = list(chain.from_iterable(ans))
        if ans:
            print("↓↓↓生成された文↓↓↓")
            print(random.choice(ans))
        else:
            print("↓↓↓生成された文↓↓↓")
            print(random.choice(sentences))

        print(f"====================================")
        print(f"類似している単語->{sim}")
        print(f"その他の類似単語->{simi_words}")
        print(f"====================================")

            

