import pathlib
import pickle
import gzip

from . import pywordsegment


segment = pywordsegment.segment
exist_as_segment = pywordsegment.exist_as_segment


def create_dictionary_file() -> None:
    current_file_dir = pathlib.Path(__file__).parent.absolute()

    unigrams_file = current_file_dir.joinpath('unigrams.pkl.gz')
    unigrams = pickle.load(
        file=gzip.GzipFile(
            filename=str(unigrams_file),
        ),
    )

    bigrams_file = current_file_dir.joinpath('bigrams.pkl.gz')
    bigrams = pickle.load(
        file=gzip.GzipFile(
            filename=str(bigrams_file),
        ),
    )

    pywordsegment.create_dictionary_file(
        unigrams=unigrams,
        bigrams=bigrams,
        total_words_frequency=1024908267229.0,
    )
