import gzip
import importlib.resources
import sys
import typing

from . import pywordsegment

PY_VERSION_MAJOR = sys.version_info.major
PY_VERSION_MINOR = sys.version_info.minor

class WordSegmenter:
    word_segmenter: pywordsegment.WordSegmenter = None

    @staticmethod
    def load() -> None:
        if WordSegmenter.word_segmenter is None:
            if PY_VERSION_MAJOR > 3 and PY_VERSION_MINOR >= 11:
                with importlib.resources.files(
                    __package__,
                ).joinpath(
                    'unigrams.msgpack.gz',
                ).open(
                    'rb',
                ) as binary_file:
                    unigrams_serialized = gzip.decompress(
                        data=binary_file,
                    )
            else:
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
