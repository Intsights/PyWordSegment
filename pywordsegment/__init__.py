import gzip
import pathlib
import pickle
import typing

from . import pywordsegment


class WordSegmenter:
    word_segmenter: pywordsegment.WordSegmenter = None

    @staticmethod
    def load() -> None:
        if WordSegmenter.word_segmenter is None:
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

            WordSegmenter.word_segmenter = pywordsegment.WordSegmenter(
                unigrams=unigrams,
                bigrams=bigrams,
                total_words_frequency=1024908267229.0,
            )

    @staticmethod
    def segment(
        text: str,
    ) -> typing.List[str]:
        if WordSegmenter.word_segmenter is None:
            WordSegmenter.load()

        return WordSegmenter.word_segmenter.segment(
            text=text,
        )

    @staticmethod
    def exist_as_segment(
        substring: str,
        text: str,
    ) -> bool:
        if WordSegmenter.word_segmenter is None:
            WordSegmenter.load()

        return WordSegmenter.word_segmenter.exist_as_segment(
            substring=substring,
            text=text,
        )
