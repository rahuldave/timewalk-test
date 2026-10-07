# tally, one move at a time

The notes of the tutorial. A step with small commits before it has one ### section for each, in order.

## step-00 Where it starts

$ python3 -m tally

## step-01 Counting

$ echo "a b a" | PYTHONPATH=src python3 -m tally

## step-02 Tests, one at a time

We add the tests one by one, and run them after each.

### step-02.1 A test of counting
One test file arrives.

files:

$ PYTHONPATH=src python3 -m unittest discover -s tests -q

### step-02.2 A test of an empty text
A second test file.

files:

$ echo move-two

### step-02.3 Case does not matter
Counting ignores case, and the tests pass.

files:

$ echo move-three

## step-03 Formatting

ruff gets a line length.

## step-04 Types, then a docstring

### step-04.1 Types
files:

### step-04.2 A docstring
files:

## step-05 More

A function for the most common words.
