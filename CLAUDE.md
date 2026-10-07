# timewalk-test

The integration test of timewalk. Read README.md. Keep it generic: it tests timewalk, and names no class.

- Each test builds its own project from `history/build.py` in a temporary folder. Never test against `repo/` in
  place, and never against a class of Rahul's.
- A new feature of timewalk gets its case here: a history, notes or slides that use it, and a test that drives it in
  two windows. Add a broken copy for each new check of the linter.
- `pyproject.toml` points at the branch under work. Move it back to `main` when that branch is merged.
- End every commit message with the line `Coded using Claude`. Ask before every commit.
