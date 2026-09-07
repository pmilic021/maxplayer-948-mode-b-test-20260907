"""unittest coverage for bookstats summary helpers."""

import json
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
    def test_json_output_empty(self):
        raw = render_summary([])
        self.assertEqual(
            raw,
            json.dumps(
                {"finished": 0, "in-progress": 0, "to-read": 0},
                sort_keys=True,
            ),
        )
        self.assertEqual(
            json.loads(raw),
            {"to-read": 0, "in-progress": 0, "finished": 0},
        )

    def test_json_output_mixed(self):
        books = [
            {"status": "finished"},
            {"status": "to-read"},
            {"status": "in-progress"},
            {"status": "to-read"},
        ]
        raw = render_summary(books)
        expected_counts = {"to-read": 2, "in-progress": 1, "finished": 1}
        self.assertEqual(raw, json.dumps(expected_counts, sort_keys=True))
        self.assertEqual(json.loads(raw), expected_counts)


if __name__ == "__main__":
    unittest.main()
