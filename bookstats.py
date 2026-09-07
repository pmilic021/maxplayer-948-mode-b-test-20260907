"""Summary helpers for book tracker status counts."""

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
    """Return a plain-text summary, one line per status, no trailing newline.

    Temporary assumption (Q6 OPEN): plain text rather than JSON.
    """
    counts = count_statuses(books)
    return "\n".join(f"{status}: {counts[status]}" for status in STATUSES)
