''' Tests for nk_sent2vec '''
import numpy as np

from . import embed_sentences, model, train_model, nearest_neighbors, analogies, produce

test_docs = ['this is a test', 'this is a trap']


def test_produce():
    embeddings = produce(test_docs)
    assert isinstance(embeddings, np.ndarray)
    assert embeddings.shape == (len(test_docs), model.get_emb_size())


def test_embed_sentences():

    embeddings = embed_sentences(test_docs)
    print(embeddings)
    print(embeddings.shape)
    assert isinstance(embeddings, np.ndarray)
    assert embeddings.shape == (len(test_docs), model.get_emb_size())


def test_train_model():
    train_model('input_path', 'output_path')


def test_nearest_neighbors():
    nearest_neighbors('query_sentence', 'corpus_path')


def test_analogies():
    analogies('query_sentence', 'corpus_path')
