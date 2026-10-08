# Only the tests

A narrative on one part of tally: the three steps where the tests matter. It uses some of the steps of main, and
borrows slides from the default walk. Every command runs through uv.

## step-01 Before any test

$ just setup

The code counts words, and nothing checks it. Read `count` in `src/tally/__init__.py`, and ask what could go wrong.

$ echo "a b a" | uv run tally
$ echo "The the" | uv run tally

The second command counts "The" and "the" as two words. Nothing says whether that is right.

> Ask: write down one test you would add, before we look at ours.

## step-02 Two tests

$ just setup

Two test files arrive: `tests/test_count.py` with two tests, and `tests/test_empty.py` with one. The case test
failed until counting learned to ignore case, in the same step.

$ uv run python -m unittest discover -s tests -v
$ echo "The the" | uv run tally

All three tests pass, and "The the" is now `2 the`.

> Say: a test is a question the code must answer. The case test asked one that the code could not answer yet.

## step-05 Still green

$ just setup

Two steps later, `top` arrives with a test of its own, and the old tests still pass. The tests did not change
when the types and the docstring arrived at step-04: they check what the code does, not how it says it.

$ uv run python -m unittest discover -s tests -v
$ uv run tally --top 3 data/corpus.txt
