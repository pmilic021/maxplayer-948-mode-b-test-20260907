"""unittest coverage for bookstats summary helpers."""

import unittest

from bookstats import count_statuses, render_summary


class TestCountStatuses(unittest.TestCase):
    def test_empty_input(self):
        self.assertEqual(
            count_statuses([]),
            {"to-read": 0, "in-progress": 0, "finished": 0},
        )

    def test_mixed_statuses(self):
        books = [
            {"status": "to-read"},
            {"status": "finished"},
            {"status": "in-progress"},
            {"status": "to-read"},
            {"status": "finished"},
            {"status": "finished"},
        ]
        self.assertEqual(
            count_statuses(books),
            {"to-read": 2, "in-progress": 1, "finished": 3},
        )


class TestRenderSummary(unittest.TestCase):
    def test_plain_output_empty(self):
        self.assertEqual(
            render_summary([]),
            "to-read: 0\nin-progress: 0\nfinished: 0",
        )

    def test_plain_output_mixed(self):
        books = [
            {"status": "finished"},
            {"status": "to-read"},
            {"status": "in-progress"},
            {"status": "to-read"},
        ]
        self.assertEqual(
            render_summary(books),
            "to-read: 2\nin-progress: 1\nfinished: 1",
        )
        self.assertFalse(render_summary(books).endswith("\n"))


if __name__ == "__main__":
    unittest.main()
