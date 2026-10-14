# Only the tests

We follow tally, a word counter, through the three places where its tests matter. We see it before any test, then
when the tests come, and last when new code comes with a test of its own. Every command runs through uv.

> Note: the walk is a narrative of three of the seven steps of main, and it borrows slides from the default walk.

## step-01 Before any test

$ just setup

tally counts words, and nothing checks it. Read `count` in `src/tally/__init__.py`, and ask what could go wrong.

$ echo "a b a" | uv run tally
$ echo "The the" | uv run tally

The second command counts "The" and "the" as two words. Nothing says whether that is right.

> Ask: write down one test you would add, before we look at ours.

files:
- file `src/tally/__init__.py`: `count`, and the command that uses it.
  show: `for word in text.split():`

## step-02 Two tests

$ just setup

A test gives `count` a text, and compares what it gives back with what we expect. `tests/test_count.py` holds two
tests, and `tests/test_empty.py` one. The test of case failed until `count` ignored case, with one word, `lower()`.

$ uv run python -m unittest discover -s tests -v
$ echo "The the" | uv run tally

All three tests pass, and the command now prints `2 the` for "The the".

> Say: a test is a question the code must answer. The case test asked one that the code could not answer yet.

files:
- diff `tests/test_count.py`: a test of counting, and a test of case.
  show: `self.assertEqual(count("A a"), {"a": 2})`
- diff `tests/test_empty.py`: an empty text counts nothing.
- diff `src/tally/__init__.py`: the word that answers the test of case.
  show: `for word in text.lower().split():`

## step-05 Still green

$ just setup

Much later, `top` comes with a test of its own, and the old tests still pass. The types and the docstring that came
in between did not change a test. The tests check what the code does, and not how it says it.

$ uv run python -m unittest discover -s tests -v
$ uv run tally --top 3 data/corpus.txt

The four tests pass, and the command prints the three most common words of the corpus.

files:
- file `tests/test_top.py`: the new test, of `top`.
- diff `src/tally/__init__.py`: types, a docstring, `top` and the option `--top`.
- diff `pyproject.toml`: ruff, and its line length.
- diff `uv.lock`: the exact version of ruff.
- diff `justfile`: `just setup` makes the corpus and the report.
- diff `scripts/corpus.py`: the script that writes the corpus.
- diff `.gitignore`: git does not hold the corpus.
