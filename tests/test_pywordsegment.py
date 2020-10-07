import unittest

import pywordsegment


class WordSegmentTestCase(
    unittest.TestCase,
):
    def test_segment_1(
        self,
    ):
        word_segmenter = pywordsegment.WordSegmenter()
        self.assertEqual(
            first=word_segmenter.segment(
                text='theusashops',
            ),
            second=[
                'the',
                'usa',
                'shops',
            ],
        )

    def test_segment_2(
        self,
    ):
        word_segmenter = pywordsegment.WordSegmenter()
        self.assertEqual(
            first=word_segmenter.segment(
                text='choosespain',
            ),
            second=[
                'choose',
                'spain',
            ],
        )

    def test_segment_3(
        self,
    ):
        word_segmenter = pywordsegment.WordSegmenter()
        self.assertEqual(
            first=word_segmenter.segment(
                text='thisisatest',
            ),
            second=[
                'this',
                'is',
                'a',
                'test',
            ],
        )

    def test_segment_4(
        self,
    ):
        word_segmenter = pywordsegment.WordSegmenter()
        self.assertEqual(
            first=word_segmenter.segment(
                text='wheninthecourseofhumaneventsitbecomesnecessary',
            ),
            second=[
                'when',
                'in',
                'the',
                'course',
                'of',
                'human',
                'events',
                'it',
                'becomes',
                'necessary',
            ],
        )

    def test_segment_5(
        self,
    ):
        word_segmenter = pywordsegment.WordSegmenter()
        self.assertEqual(
            first=word_segmenter.segment(
                text='whorepresents',
            ),
            second=[
                'who',
                'represents',
            ],
        )

    def test_segment_6(
        self,
    ):
        word_segmenter = pywordsegment.WordSegmenter()
        self.assertEqual(
            first=word_segmenter.segment(
                text='expertsexchange',
            ),
            second=[
                'experts',
                'exchange',
            ],
        )

    def test_segment_7(
        self,
    ):
        word_segmenter = pywordsegment.WordSegmenter()
        self.assertEqual(
            first=word_segmenter.segment(
                text='speedofart',
            ),
            second=[
                'speed',
                'of',
                'art',
            ],
        )

    def test_segment_8(
        self,
    ):
        word_segmenter = pywordsegment.WordSegmenter()
        self.assertEqual(
            first=word_segmenter.segment(
                text='nowisthetimeforallgood',
            ),
            second=[
                'now',
                'is',
                'the',
                'time',
                'for',
                'all',
                'good',
            ],
        )

    def test_segment_9(
        self,
    ):
        word_segmenter = pywordsegment.WordSegmenter()
        self.assertEqual(
            first=word_segmenter.segment(
                text='itisatruthuniversallyacknowledged',
            ),
            second=[
                'it',
                'is',
                'a',
                'truth',
                'universally',
                'acknowledged',
            ],
        )

    def test_segment_10(
        self,
    ):
        word_segmenter = pywordsegment.WordSegmenter()
        self.assertEqual(
            first=word_segmenter.segment(
                text='itwasabrightcolddayinaprilandtheclockswerestrikingthirteen',
            ),
            second=[
                'it',
                'was',
                'a',
                'bright',
                'cold',
                'day',
                'in',
                'april',
                'and',
                'the',
                'clocks',
                'were',
                'striking',
                'thirteen',
            ],
        )

    def test_segment_11(
        self,
    ):
        word_segmenter = pywordsegment.WordSegmenter()
        self.assertEqual(
            first=word_segmenter.segment(
                text='CaseTest',
            ),
            second=[
                'case',
                'test',
            ],
        )
