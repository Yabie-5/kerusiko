from gensim.test.utils import common_texts
from gensim.models import Word2Vec

class Similer:
  def similer(word):
    model = Word2Vec.load("./model/word2vec.model")

    sim_word=[]
    for li in model.wv.most_similar(word, topn=30)[7:]:
      sim_word.append(li[0])
    

    return sim_word

  def train(sentence):
    batch_size = 100 # 一度に処理するサンプル数
    max_epoch = 1000 # 重み更新回数（学習回数）


    model = Word2Vec.load("./model/word2vec.model")
    model.build_vocab([sentence], update=True)
    model.train([sentence], total_examples=batch_size, epochs=max_epoch)
    print("*****学習中*****")
    model.save("./model/word2vec.model")

