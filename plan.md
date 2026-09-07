# Local CLI Book Tracker — Plan

**Reference:** MT948-PLAN-A

## Goal

A single-user command-line tool to track personal reading: add books, list them, and update status. No accounts, sync, or multi-user features.

## Storage (confirmed)

Data lives in a **local SQLite database** file `books.db` (default path: `~/.booktracker/books.db`). Create the parent directory and initialize the schema on first use. Override path via env `BOOKTRACKER_PATH`. Persistence uses Python’s standard **`sqlite3`** module only — no third-party DB drivers.

## Proposed data model

Schema version tracked in a small `meta` table (`key`/`value`); books in a `books` table:

```sql
CREATE TABLE IF NOT EXISTS meta (
  key   TEXT PRIMARY KEY,
  value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS books (
  id         TEXT PRIMARY KEY,  -- 8-char hex
  title      TEXT NOT NULL,
  author     TEXT NOT NULL,
  status     TEXT NOT NULL CHECK (status IN ('to-read', 'in-progress', 'finished')),
  added_at   TEXT NOT NULL,     -- ISO-8601 UTC
  updated_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_books_updated_at ON books (updated_at DESC);
CREATE INDEX IF NOT EXISTS idx_books_status ON books (status);
```

| Field | Notes |
|--------|--------|
| `id` | Short unique hex id (8 chars), assigned on add |
| `title`, `author` | Non-empty strings; trim whitespace |
| `status` | Exactly one of: `to-read`, `in-progress`, `finished` |
| `added_at` / `updated_at` | ISO-8601 UTC strings |

Default status on add: `to-read`.

### Persistence operations

- **Open:** connect to `BOOKTRACKER_PATH` (or default); `PRAGMA foreign_keys=ON`; ensure schema via `CREATE TABLE IF NOT EXISTS`.
- **Add:** `INSERT` one row; commit.
- **List:** `SELECT … ORDER BY updated_at DESC`; optional `WHERE status = ?`.
- **Update:** `UPDATE` matched by `id`; set `updated_at` to now; fail if zero rows.
- **Integrity:** wrap mutating commands in a transaction; reject invalid status / empty title/author before write.

## CLI (unchanged surface)

- **Runtime:** Python 3.11+ stdlib only (`argparse`, `sqlite3`, `pathlib`, `uuid`, `datetime`) — no third-party deps.
- **Entry point:** `booktracker` (or `python -m booktracker`).
- **Config override:** env `BOOKTRACKER_PATH` for the SQLite file location.

### Command examples

```bash
# Add
booktracker add --title "Dune" --author "Frank Herbert"
booktracker add -t "Dune" -a "Frank Herbert" --status in-progress

# List (all; optional filter)
booktracker list
booktracker list --status to-read
booktracker list --status finished

# Update (by id; change status and/or metadata)
booktracker update a1b2c3d4 --status finished
booktracker update a1b2c3d4 --title "Dune (rev)" --author "F. Herbert"
```

List output: one line per book — `id  status  title — author` — sorted by `updated_at` descending.

Errors: clear messages and non-zero exit for missing id, invalid status, empty title/author, or unreadable/corrupt database.

## Implementation steps

1. Scaffold package: `booktracker/` with `__main__.py`, `cli.py`, `store.py`, `models.py`.
2. Implement SQLite store: connect, migrate/create schema, CRUD helpers (`add`, `list`, `update`).
3. Implement `add`, `list`, `update` with argparse subcommands.
4. Validate status enum and required fields at the CLI boundary.
5. Smoke-test manually against a temp DB via `BOOKTRACKER_PATH`.
6. (Optional follow-up, out of scope unless requested) shell completion or export.

## Acceptance checks

- [ ] Can add a book with title + author; appears in list with status `to-read` and a stable id.
- [ ] Can add with explicit `--status` any of the three allowed values.
- [ ] `list` shows all books; `--status` filters correctly.
- [ ] `update <id> --status …` changes status and bumps `updated_at`.
- [ ] `update` with unknown id fails non-zero with a readable error.
- [ ] Invalid status is rejected without writing partial data.
- [ ] Data persists across process exits in the configured `books.db` SQLite file.
- [ ] Schema is created automatically on first run; subsequent runs reuse the same DB.
- [ ] Mutating ops use transactions; no partial row on validation failure.
- [ ] Plan reference **MT948-PLAN-A** retained in docs/revisions.

## Out of scope (this plan)

Web UI, ratings, notes, ISBN lookup, import/export formats other than the store file, multi-user or remote sync.

## Completed work (contribution turn 1)

- Added standalone `bookstats.py` with `count_statuses(books)` and `render_summary(books)` (stdlib only); full CLI/storage not implemented.
- `count_statuses` returns `{to-read, in-progress, finished}` including zeros; each book dict has a valid status.
- `render_summary` temporarily emits plain text lines `to-read: N` / `in-progress: N` / `finished: N` (no trailing newline); format pending Q6.
- Added `test_bookstats.py` (unittest: empty input, mixed statuses, plain output) and ran it.
- Deleted `obsolete.txt`; preserved `KEEP.txt` byte-for-byte; left Q1–Q5 and prior plan content intact.

## Completed work (contribution turn 2)

- Applied Q6: `render_summary` now returns `json.dumps(count_statuses(books), sort_keys=True)`; `count_statuses` unchanged.
- Updated output tests to assert the JSON string and decoded counts; ran the tests.
- Preserved prior plan content; `KEEP.txt` byte-for-byte; Q1–Q6 attributions; did not recreate `obsolete.txt`.

