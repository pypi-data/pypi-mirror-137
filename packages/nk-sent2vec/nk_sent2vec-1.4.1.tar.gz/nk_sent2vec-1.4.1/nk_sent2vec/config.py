import os
from pathlib import Path


def get_model_path():
    ''' get the default model path, which is ../models/<model-name>.bin '''
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = Path(current_dir).parent
    return str(parent_dir / 'models' / 'torontobooks_unigrams.bin')


MODEL_PATH = os.getenv('MODEL_PATH', get_model_path())

# TODO add switch / env var for different pretrained models:
# sent2vec_wiki_unigrams 5GB (600dim, trained on english wikipedia)
# sent2vec_wiki_bigrams 16GB (700dim, trained on english wikipedia)
# sent2vec_twitter_unigrams 13GB (700dim, trained on english tweets)
# sent2vec_twitter_bigrams 23GB (700dim, trained on english tweets)
# sent2vec_toronto books_unigrams 2GB (700dim, trained on the BookCorpus dataset)
# sent2vec_toronto books_bigrams 7GB (700dim, trained on the BookCorpus dataset)
