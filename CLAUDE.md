# timewalk-test

The integration test of timewalk. Read README.md. Keep it generic. It tests timewalk, and names no class.

- Each test builds its own project from `history/build.py` in a temporary folder. Never test against `repo/` in
  place, and never against a class of Rahul's.
- Give each new feature of timewalk its case here. A case is a history, notes or slides that use the feature, and a
  test that drives it in two windows. Add a broken copy for each new check of the linter.
- `history/build.py` writes every commit from the texts in it, and from `history/step-03.1-uv.lock`, the lock that
  `uv add --dev ruff` wrote. To make that lock again, run `uv add --dev ruff` on a clone of `repo/` at step-02, and copy
  its `uv.lock` there. Then put the version of ruff in `DEV_RUFF` and in the notes of step-03.1.
- Write the notes by "How the notes are written" in the README. Each change says what it solves, then the change
  piece by piece, then the check, and last `files:` with every file. Keep timewalk's words out of the text that a
  reader reads. Check the pages with the `render.py` line of the README, and `tests/test_facts.py` checks the facts.
- Keep step-06 one commit, with no moves. timewalk's guide asks for a step without moves after the first step, and the
  tests drive it.
- The README has a table of the example of each feature. Keep it true when a walk or the history changes.
- `pyproject.toml` points at the branch under work. Move it back to `main` when that branch is merged.
- End every commit message with the line `Coded using Claude`. Ask before every commit.
