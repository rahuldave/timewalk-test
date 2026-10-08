# Tests first, on the parts branch

A narrative on tags of its own: `parts-01` and `parts-02`, on the branch `parts`, which starts at step-00. The same
code as main reaches, in another order: here the tests come with the code, not after it. The replay copy moves to
that branch when you choose this walk.

## parts-01 The code, with its test

$ just setup

The counting code and its first test arrive in one commit. Read `tests/test_count.py`, then `count`.

$ uv run python -m unittest discover -s tests -v
$ git log --oneline --graph --all | head -12

The graph shows the branch `parts` leaving main at step-00.

> Ask: is it easier to read a test before the code, or after?

## parts-02 One more test

$ just setup

A test of an empty text arrives. It passes at once: `count` already handles it.

$ uv run python -m unittest discover -s tests -v
$ echo "" | uv run tally && echo "(nothing, as the test says)"
