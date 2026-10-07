# tally, step by step

The notes of the default walk, the narrative: one section per tagged step.

## step-00 Where it starts
time: 0:00

> Say: a project that does nothing yet.

Run the command, and see that it has nothing to count.

$ python3 -m tally

## step-01 Counting
time: 0:05

The command counts words, one line per word.

$ echo "a b a" | PYTHONPATH=src python3 -m tally

## step-02 Tests
time: 0:10

Two tests arrive, and one fails until counting ignores case.

$ PYTHONPATH=src python3 -m unittest discover -s tests -q

## step-03 Formatting
time: 0:15

ruff gets a line length.

## step-04 Types and docs
time: 0:20

The function says what it takes, what it returns, and what it does.

## step-05 More
time: 0:25

A function for the most common words.
