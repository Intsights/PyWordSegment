import gzip
import importlib.resources
import typing

from . import pywordsegment


class WordSegmenter:
    word_segmenter: pywordsegment.WordSegmenter = None

    @staticmethod
    def load() -> None:
        if WordSegmenter.word_segmenter is None:
            unigrams_serialized = gzip.decompress(
                data=importlib.resources.read_binary(
                    package=__package__,
                    resource='unigrams.msgpack.gz',
                ),
            )
            bigrams_serialized = gzip.decompress(
                data=importlib.resources.read_binary(
                    package=__package__,
                    resource='bigrams.msgpack.gz',
                ),
            )

            WordSegmenter.word_segmenter = pywordsegment.WordSegmenter(
                unigrams_serialized=unigrams_serialized,
                bigrams_serialized=bigrams_serialized,
            )

    @staticmethod
    def segment(
        text: str,
    ) -> typing.List[str]:
        if WordSegmenter.word_segmenter is None:
            WordSegmenter.load()

        return WordSegmenter.word_segmenter.segment(text)

    @staticmethod
    def exist_as_segment(
        substring: str,
        text: str,
    ) -> bool:
        if WordSegmenter.word_segmenter is None:
            WordSegmenter.load()

        return WordSegmenter.word_segmenter.exist_as_segment(substring, text)
