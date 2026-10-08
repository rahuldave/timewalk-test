# tally, step by step

The notes of the default walk, a narrative: one section for each tagged step. This walk shows every kind of
line that a notes file can hold. Lines that start with "> " are cues for you; hide them in the Room window.

## step-00 Where it starts
time: 0:00

> Say: a project that does nothing yet. Ask what it should count.

The project has a command, and the command has nothing to count. Run it.

$ python3 -m tally
main$ git log --oneline --decorate --all | head -20

## step-01 Counting
time: 0:05

The command counts words, one line per word. The second slide is a picture.

$ echo "a b a" | PYTHONPATH=src python3 -m tally

> Ask: what should "A" and "a" count as?

## step-02 Tests
time: 0:10

Two tests arrive, and one fails until counting ignores case. Read `tests/test_count.py`, then run them.

$ PYTHONPATH=src python3 -m unittest discover -s tests -q

A code block in the notes is code to read, not a command to run:

```
$ this line is not a button
```

## step-03 Formatting
time: 0:15

ruff gets a line length. The slide pane shows a whole document instead of slides: it scrolls.

Make an edit from the shell, then open `src/tally/__init__.py` and choose "Edits since the step". With
`--discard-edits`, the step bar warns, and the next move throws the edit away.

$ printf '\n# an edit made in class\n' >> src/tally/__init__.py

## step-04 Types and docs
time: 0:20

The function says what it takes, what it returns, and what it does. Open `src/tally/__init__.py` in
"Changes in this step".

## step-05 More
time: 0:25

A function for the most common words. A long command goes to the Runs tab, so the first shell stays free,
and a second one to Runs 2.

runs$ for i in 1 2 3 4 5; do echo "epoch $i"; sleep 1; done
runs2$ for i in 1 2 3; do echo "sweep $i"; sleep 2; done
$ just --list
