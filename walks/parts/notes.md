# Tests first, on the parts branch

We build the same counting code as the main history of tally, in another order. Here each test comes with the code
that it tests, and not after it. This history is on a branch of its own, `parts`, which leaves `main` where the
project begins.

> Note: the walk is a narrative on tags of its own, `parts-01` and `parts-02`. The replay copy moves to the branch
> `parts` when you choose this walk.

## parts-01 The code, with its test

$ just setup

Code and its test arrive together, so the test checks the code from the first day. Read `tests/test_count.py`,
then `count`.

$ uv run python -m unittest discover -s tests -v
$ git log --oneline --graph --all | head -12

Both tests pass. The graph shows the branch `parts`, which leaves `main` where the project begins.

> Ask: is it easier to read a test before the code, or after?

files:
- diff `tests/test_count.py`: a test of counting, and a test of case.
  show: `self.assertEqual(count("A a"), {"a": 2})`
- diff `src/tally/__init__.py`: `count`, which ignores case from the first day, and the command.
  show: `for word in text.lower().split():`

## parts-02 One more test

$ just setup

An empty text has no words, and `count` must give an empty dictionary for it. A test of an empty text says so. It
passes at once, because `count` already handles it.

$ uv run python -m unittest discover -s tests -v
$ echo "" | uv run tally && echo "(nothing, as the test says)"

The three tests pass, and tally prints nothing for an empty text.

files:
- diff `tests/test_empty.py`: an empty text counts nothing.
  show: `self.assertEqual(count(""), {})`
