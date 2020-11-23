import typing


class WordSegmenter:
    @staticmethod
    def load() -> None: ...

    @staticmethod
    def segment(
        text: str,
    ) -> typing.List[str]: ...

    @staticmethod
    def exist_as_segment(
        substring: str,
        text: str,
    ) -> bool: ...
