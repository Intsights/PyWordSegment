import typing


class WordSegmenter:
    def __init__(
        self,
    ) -> None: ...

    def segment(
        self,
        text: str,
    ) -> typing.List[str, str]: ...

    def exist_as_segment(
        self,
        substring: str,
        text: str,
    ) -> bool: ...
