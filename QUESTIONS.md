# QUESTIONS

## Q1 — Persistent storage format
- **Status:** answered
- **Asked by:** agent (turn 1)
- **Answered by:** simulated human (test fixture authorized by Petar)
- **Question:** Confirm that a single local JSON file (`~/.booktracker/books.json`, overridable via `BOOKTRACKER_PATH`) is acceptable for v1 storage. Plan MT948-PLAN-A assumes yes until you decide otherwise.
- **Context:** The first plan assumed JSON pending confirmation.
- **Answer:** Use SQLite instead of a JSON file. Store the data in a local books.db file. Use Python’s standard sqlite3 module. Keep the application local and single-user.

## Q2 — Runtime / language
- **Status:** answered
- **Asked by:** agent (turn 1)
- **Answered by:** agent (assumption)
- **Decision:** Python 3.11+ with stdlib only (`argparse`, `json`, `pathlib`). No third-party dependencies.

## Q3 — Default status on add
- **Status:** answered
- **Asked by:** agent (turn 1)
- **Answered by:** agent (assumption)
- **Decision:** New books default to `to-read` unless `--status` is passed.

## Q4 — Book identity for updates
- **Status:** answered
- **Asked by:** agent (turn 1)
- **Answered by:** agent (assumption)
- **Decision:** Assign an 8-character hex `id` on add; `update` addresses books by that id (not by title).

## Q5 — List sort order
- **Status:** answered
- **Asked by:** agent (turn 1)
- **Answered by:** agent (assumption)
- **Decision:** Sort by `updated_at` descending.

---

No unanswered questions remain. Storage is confirmed as SQLite (`books.db` via stdlib `sqlite3`); Q2–Q5 assumptions still hold. Ready for implementation when requested.
