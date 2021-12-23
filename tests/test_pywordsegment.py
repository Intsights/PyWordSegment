import unittest

import pywordsegment


class WordSegmentTestCase(
    unittest.TestCase,
):
    def test_segment_1(
        self,
    ):
        self.assertEqual(
            first=pywordsegment.WordSegmenter.segment(
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
        self.assertEqual(
            first=pywordsegment.WordSegmenter.segment(
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
        self.assertEqual(
            first=pywordsegment.WordSegmenter.segment(
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
        self.assertEqual(
            first=pywordsegment.WordSegmenter.segment(
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
        self.assertEqual(
            first=pywordsegment.WordSegmenter.segment(
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
        self.assertEqual(
            first=pywordsegment.WordSegmenter.segment(
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
        self.assertEqual(
            first=pywordsegment.WordSegmenter.segment(
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
        self.assertEqual(
            first=pywordsegment.WordSegmenter.segment(
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
        self.assertEqual(
            first=pywordsegment.WordSegmenter.segment(
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
        self.assertEqual(
            first=pywordsegment.WordSegmenter.segment(
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
        self.assertEqual(
            first=pywordsegment.WordSegmenter.segment(
                text='CaseTest',
            ),
            second=[
                'case',
                'test',
            ],
        )

    def test_segment_12(
        self,
    ):
        self.assertEqual(
            first=pywordsegment.WordSegmenter.segment(
                text='',
            ),
            second=[],
        )

    def test_segment_13(
        self,
    ):
        self.assertEqual(
            first=pywordsegment.WordSegmenter.segment(
                text='a',
            ),
            second=[
                'a',
            ],
        )

    def test_exist_as_segment_1(
        self,
    ):
        self.assertFalse(
            expr=pywordsegment.WordSegmenter.exist_as_segment(
                substring='man',
                text='manual',
            ),
        )
        self.assertTrue(
            expr=pywordsegment.WordSegmenter.exist_as_segment(
                substring='man',
                text='oneman',
            ),
        )
