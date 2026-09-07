"""Summary helpers for book tracker status counts."""

import json

STATUSES = ("to-read", "in-progress", "finished")


def count_statuses(books):
    """Return counts for to-read, in-progress, and finished (including zeros).

    Each book is a dict with a valid ``status`` key.
    """
    counts = {status: 0 for status in STATUSES}
    for book in books:
        counts[book["status"]] += 1
    return counts


def render_summary(books):
    """Return a JSON string of status counts (sort_keys=True)."""
    return json.dumps(count_statuses(books), sort_keys=True)
