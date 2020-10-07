import pathlib
import typing

from . import pywordsegment


class WordSegmenter:
    word_segmenter: pywordsegment.WordSegmenter = None

    def __init__(
        self,
    ) -> None:
        if WordSegmenter.word_segmenter is None:
            WordSegmenter.word_segmenter = pywordsegment.WordSegmenter(
                unigrams_file_path=str(pathlib.Path(__file__).parent.absolute().joinpath('unigrams.txt')),
                bigrams_file_path=str(pathlib.Path(__file__).parent.absolute().joinpath('bigrams.txt')),
                total_words_frequency=1024908267229.0,
            )

    def segment(
        self,
        text: str,
    ) -> typing.List[str]:
        return self.word_segmenter.segment(
            text=text,
        )

    def exist_as_segment(
        self,
        substring: str,
        text: str,
    ) -> bool:
        return self.word_segmenter.exist_as_segment(
            substring=substring,
            text=text,
        )
