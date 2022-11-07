import unittest

from score import get_score


class TestGetScoreFunction(unittest.TestCase):
    def setUp(self):
        self.game_stamp = [
            {"offset": 0, "score": {"home": 0, "away": 0}},
            {"offset": 2, "score": {"home": 1, "away": 0}},
            {"offset": 3, "score": {"home": 2, "away": 0}},
            {"offset": 5, "score": {"home": 2, "away": 0}},
            {"offset": 7, "score": {"home": 2, "away": 1}},
        ]

    def test_get_exist_time_stamp(self):
        self.assertEqual(get_score(self.game_stamp, 2), (1, 0))
        self.assertEqual(get_score(self.game_stamp, 3), (2, 0))
        self.assertEqual(get_score(self.game_stamp, 5), (2, 0))

    def test_get_first_exist_time_stamp(self):
        self.assertEqual(get_score(self.game_stamp, 0), (0, 0))

    def test_get_last_exist_time_stamp(self):
        self.assertEqual(get_score(self.game_stamp, 7), (2, 1))

    def test_get_not_exist_time_stamp(self):
        self.assertEqual(get_score(self.game_stamp, 1), (0, 0))
        self.assertEqual(get_score(self.game_stamp, 4), (2, 0))
        self.assertEqual(get_score(self.game_stamp, 6), (2, 0))

    def test_get_time_stamp_later_than_last(self):
        self.assertEqual(get_score(self.game_stamp, 8), (2, 1))
        self.assertEqual(get_score(self.game_stamp, 10), (2, 1))
        self.assertEqual(get_score(self.game_stamp, 1000000), (2, 1))

    def test_get_time_stamp_earlier_than_first(self):
        with self.assertRaises(ValueError):
            get_score(self.game_stamp, -1)


if __name__ == "__main__":
    unittest.main()
