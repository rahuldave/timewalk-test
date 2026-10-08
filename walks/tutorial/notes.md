# tally, one move at a time

A tutorial: the tagged steps of tally, and the small commits between them. Each small commit is a move, one atomic
action. In do mode, the default, you make each move by hand from its notes, run the command at its end, and press
Done. In watch mode, Show checks out each move's commit instead. Either way, the command at the end of a move
shows what the move did. Every command runs through uv.

## step-00 Where it starts

$ just setup

A uv project with a command that has nothing to count. This step has no moves: it is where the tutorial starts.

$ uv run tally

## step-01 Counting

$ just setup

`count` arrives in one commit, so this step has no moves either.

$ echo "a b a" | uv run tally

## step-02 Tests, one at a time

$ just setup

We add the tests one file at a time, and run them after each. The code starts as it was at step-01: it does not
ignore case yet.

### step-02.1 A test of counting

Make `tests/test_count.py` with two tests. The second one asks for something the code cannot do yet:

```python
import unittest

from tally import count


class Count(unittest.TestCase):
    def test_words(self):
        self.assertEqual(count("a b a"), {"a": 2, "b": 1})

    def test_case(self):
        self.assertEqual(count("A a"), {"a": 2})
```

What changed:

- `tests/test_count.py`: new file, 11 lines; adds `class Count`, `test_words` and `test_case`. The test that
  matters is `test_case`.

files:
- diff `tests/test_count.py`: two tests. The second asks for something the code cannot do yet.
  show: `self.assertEqual(count("A a"), {"a": 2})`

$ uv run python -m unittest discover -s tests -q

One test fails: `test_case` expects `{"a": 2}`, and gets `{"A": 1, "a": 1}`.

> Say: look, a failure. It is a question that the code has not answered yet.

### step-02.2 A test of an empty text

Make `tests/test_empty.py`:

```python
import unittest

from tally import count


class Empty(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(count(""), {})
```

What changed:

- `tests/test_empty.py`: new file, 8 lines; adds `class Empty` and `test_empty`.

files:
- diff `tests/test_empty.py`: an empty text counts nothing.
  show: `self.assertEqual(count(""), {})`

$ uv run python -m unittest discover -s tests -q

The new test passes at once. `test_case` still fails.

### step-02.3 Case does not matter

In `count`, in `src/tally/__init__.py`, change `text.split()` to `text.lower().split()`. This move is the tagged
commit of the step.

What changed:

- `src/tally/__init__.py`: +1 -1; changes `count`. One word, `lower()`, answers the failing test.

files:
- diff `src/tally/__init__.py`: one word, `lower()`, answers the failing test.
  show: `for word in text.lower().split():`

$ uv run python -m unittest discover -s tests -q
$ echo "The the" | uv run tally

All three tests pass, and "The the" is `2 the`.

## step-03 Formatting, and a corpus

$ just setup

One commit: ruff gets a line length, and `just setup` makes `data/corpus.txt`, an artifact that git does not hold.

$ uv run tally data/corpus.txt | sort -rn | head -3

## step-04 Types, then a docstring

$ just setup

### step-04.1 Types

In `src/tally/__init__.py`, give `count` its types:

```python
def count(text: str) -> dict[str, int]:
```

What changed:

- `src/tally/__init__.py`: +1 -1; changes `count`, in its signature only.

files:
- diff `src/tally/__init__.py`: the signature says what goes in and what comes out.
  show: `def count(text: str) -> dict[str, int]:`

$ uv run python -m unittest discover -s tests -q

The tests pass as before: types change what the code says, not what it does.

### step-04.2 A docstring

Under the signature of `count`, add one line:

```python
    "How many times each word appears, ignoring case."
```

What changed:

- `src/tally/__init__.py`: +1 -0; changes `count`.

files:
- diff `src/tally/__init__.py`: one line under the signature says what the function does.
  show: `"How many times each word appears, ignoring case."`

$ uv run python -c "import tally; print(tally.count.__doc__)"

## step-05 The most common words, and a report

$ just setup

Three moves: a function with its test, an option on the command, and a recipe that makes an artifact.

### step-05.1 A function for the most common words

Add `top` to `src/tally/__init__.py`, after `count`, and its test in `tests/test_top.py`:

```python
def top(counts: dict[str, int], n: int) -> list[tuple[str, int]]:
    "The n most common words, most common first."
    return sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))[:n]
```

```python
import unittest

from tally import top


class Top(unittest.TestCase):
    def test_most_common_first(self):
        self.assertEqual(top({"a": 1, "b": 3, "c": 2}, 2), [("b", 3), ("c", 2)])
```

What changed:

- `src/tally/__init__.py`: +5 -0; adds `top`.
- `tests/test_top.py`: new file, 8 lines; adds `class Top` and `test_most_common_first`.

files:
- diff `src/tally/__init__.py`: sort by count, most common first, then by the word.
  show: `return sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))[:n]`
- file `tests/test_top.py`: its test, with three words.

$ uv run python -m unittest discover -s tests -q

### step-05.2 tally --top N

Teach `main` an option: with `--top N`, print only the N most common words, with `top`. Open the move's change to
see one way to write it.

What changed:

- `src/tally/__init__.py`: +8 -3; changes `main`.

files:
- diff `src/tally/__init__.py`: `main` reads the option before the file name.
  show: `if args[:1] == ["--top"]:`

$ uv run tally --top 3 data/corpus.txt

Three lines, the most common word first.

### step-05.3 A report, which just setup makes

Add a `report` recipe to the justfile that writes `build/top.txt`, and make `just setup` run it when the file is
missing. This move is the tagged commit of the step.

```just
# Write the ten most common words of the corpus to build/top.txt
report:
    mkdir -p build
    uv run tally --top 10 data/corpus.txt > build/top.txt
```

What changed:

- `justfile`: +6 -0; adds `recipe report`, and a line in `setup`.

files:
- diff `justfile`: the report, and the line in `setup` that makes it when it is missing.
  show: `uv run tally --top 10 data/corpus.txt > build/top.txt`
  show: `test -f build/top.txt || just report`

$ just setup
$ cat build/top.txt

`build/top.txt` is an artifact: made by this step, ignored by git, and made again by `just setup` when it is missing.
