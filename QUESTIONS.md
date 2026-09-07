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

## Q6 — Summary output format
- **Status:** answered
- **Asked by:** agent (contribution turn 1 / turn 3 of plan)
- **Answered by:** simulated human (test fixture authorized by Petar)
- **Question:** Should `render_summary` return plain text or a JSON string?
- **Context:** Implementing a small standalone summary module (`bookstats.py`). Temporary assumption while OPEN: plain text, one line per status exactly `to-read: N`, `in-progress: N`, `finished: N`, separated by newlines, with no trailing newline. Code proceeds under that assumption until you confirm.
- **Answer:** Return a JSON string with all three status counts. Use json.dumps with sort_keys=True. Keep count_statuses unchanged.


---

Q1–Q6 are answered. Apply the simulated Q6 answer in the next contribution turn.
