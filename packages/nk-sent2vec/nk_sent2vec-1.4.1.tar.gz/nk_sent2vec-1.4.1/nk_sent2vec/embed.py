""" wrapper functions for the sent2vec model object """

from typing import List

import sent2vec


class Sent2Vec:
    def __init__(self, path):
        model = sent2vec.Sent2vecModel()
        model.load_model(path)
        self.model = model

    def produce(self, sentences: List[str]):
        return self.model.embed_sentences(sentences)

    def embed_sentence(self, sentence: str):
        return self.model.embed_sentences([sentence])

    def embed_sentences(self, sentences: List[str]):
        return self.model.embed_sentences(sentences)

    def train_model(self, input_path, output_path):
        # TODO
        pass

    def nearest_neighbors(self, query_sentence, corpus_path):
        # ./fasttext nnSent model.bin corpora [k]
        # TODO
        pass

    def analogies(self, query_sentence, corpus_path):
        # ./fasttext analogiesSent model.bin corpora [k]
        # TODO
        pass
