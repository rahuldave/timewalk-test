# Only the tests

A walk on one part of tally: the steps where tests matter.

## step-01 Before any test
The code counts words, and nothing checks it.

$ echo "a b a" | PYTHONPATH=src python3 -m tally

## step-02 Two tests
One test fails until counting ignores case.

$ PYTHONPATH=src python3 -m unittest discover -s tests -q

## step-05 Still green
The new function arrives, and the old tests still pass.
