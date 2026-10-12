# tally, one move at a time

The walk is a tutorial through the tagged steps of tally, and the small commits between them. Each small commit is
a move, one small action. In do mode, the default, you make each move by hand from its notes, run the command at its end, and press
Done. In watch mode, Show checks out each move's commit instead. Either way, the command at the end of a move
shows what the move did. Every command runs through uv.

Each move first says what it does. In do mode, the notes then give the code to write and the commands to run. In
watch mode, they say what to look at. The files of the move, their changes and the commands that check the move
are the same in both modes.

## step-00 Where it starts

$ just setup

The project is a uv project with a command that has nothing to count. The step has no moves, because the tutorial
starts here. Run just setup, then the command below, and go to the next step.

$ uv run tally

## step-01 Counting

$ just setup

The step has two moves. The first adds a function that counts, and the second the command that uses it. Each move
ends with a command that shows what it did.

### step-01.1 A function that counts

Now we add `count`, a function that counts the words of a text. It goes in `src/tally/__init__.py`, above `main`.
`count` makes a dictionary from each word to how many times it appears. The command does not use it yet.

::: do
In `src/tally/__init__.py`, above `main`, add `count`:

```python
def count(text):
    counts = {}
    for word in text.split():
        counts[word] = counts.get(word, 0) + 1
    return counts
```
:::

::: watch
Read `count` in the change of `src/tally/__init__.py`.
:::

The move changes one file:

- `src/tally/__init__.py`: 7 lines added; adds `count`.

The line to read first is the one that adds 1 to the count of a word.

files:
- diff `src/tally/__init__.py`: a dictionary from each word to how many times it appears.
  show: `counts[word] = counts.get(word, 0) + 1`

$ uv run python -c "from tally import count; print(count('a b a'))"

The function works, and prints `{'a': 2, 'b': 1}`. The command still has nothing to count.

### step-01.2 The command counts

Now the command counts. `main` reads a file, or the standard input when no file is given. Then it prints each word
with its count, and it needs `import sys` under the docstring of the module. This move is the tagged commit of the step.

::: do
In `src/tally/__init__.py`, add `import sys` under the docstring of the module, with a blank line before it. Then
write `main` again:

```python
def main() -> None:
    text = open(sys.argv[1]).read() if len(sys.argv) > 1 else sys.stdin.read()
    for word, n in sorted(count(text).items()):
        print(n, word)
```
:::

::: watch
Read the new `main` in the change of `src/tally/__init__.py`.
:::

The move changes one file:

- `src/tally/__init__.py`: 5 lines added, 1 removed; changes `main`.

files:
- diff `src/tally/__init__.py`: `main` reads the text and prints the counts.
  show: `for word, n in sorted(count(text).items()):`

$ echo "a b a" | uv run tally

## step-02 Tests, one at a time

$ just setup

We add the tests one file at a time, and run them after each. The code starts as it was at step-01, so it does
not ignore case yet.

### step-02.1 A test of counting

Now we start the tests. They go in a new folder, `tests`. The first file, `tests/test_count.py`, has two tests. The
second test asks for something that the code cannot do yet. It expects `count` to ignore case.

::: do
Make the folder, and run the tests in it. The folder has no tests yet, so unittest prints `NO TESTS RAN`.

$ mkdir -p tests
$ uv run python -m unittest discover -s tests -q
:::

Each test calls `count` on a short text, and compares the result with the dictionary that it expects.

::: do
Make `tests/test_count.py`:

```python
import unittest

from tally import count


class Count(unittest.TestCase):
    def test_words(self):
        self.assertEqual(count("a b a"), {"a": 2, "b": 1})

    def test_case(self):
        self.assertEqual(count("A a"), {"a": 2})
```
:::

::: watch
Read the two tests in the change of `tests/test_count.py`.
:::

The move changes one file:

- `tests/test_count.py`: a new file of 11 lines; adds `class Count`, `test_words` and `test_case`.

The test to watch is `test_case`.

files:
- diff `tests/test_count.py`: two tests. The second asks for something the code cannot do yet.
  show: `self.assertEqual(count("A a"), {"a": 2})`

$ uv run python -m unittest discover -s tests -q

One test fails. `test_case` expects `{"a": 2}`, and gets `{"A": 1, "a": 1}`.

> Say: look, a failure. It is a question that the code has not answered yet.

### step-02.2 A test of an empty text

Now we test an empty text, in a new file, `tests/test_empty.py`. An empty text has no words, so `count` must give
an empty dictionary.

::: do
Make `tests/test_empty.py`:

```python
import unittest

from tally import count


class Empty(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(count(""), {})
```
:::

::: watch
Read the test in the change of `tests/test_empty.py`.
:::

The move changes one file:

- `tests/test_empty.py`: a new file of 8 lines; adds `class Empty` and `test_empty`.

files:
- diff `tests/test_empty.py`: an empty text counts nothing.
  show: `self.assertEqual(count(""), {})`

$ uv run python -m unittest discover -s tests -q

The new test passes at once. `test_case` still fails.

### step-02.3 Case does not matter

Now we answer the failing test, `test_case`. In `count`, in `src/tally/__init__.py`, `text.split()` becomes
`text.lower().split()`. So `count` reads every word in lower case. This move is the tagged commit of the step.

::: do
Add `.lower()` after `text`, in the loop of `count`.
:::

::: watch
Find `lower()` in the change of `src/tally/__init__.py`.
:::

The move changes one file:

- `src/tally/__init__.py`: 1 line added, 1 removed; changes `count`.

One word, `lower()`, answers the failing test.

files:
- diff `src/tally/__init__.py`: one word, `lower()`, answers the failing test.
  show: `for word in text.lower().split():`

$ uv run python -m unittest discover -s tests -q
$ echo "The the" | uv run tally

All three tests pass, and "The the" is `2 the`.

## step-03 Formatting, and a corpus

$ just setup

The step has three moves. The first adds ruff, a formatter and linter, with `uv add`. The second gives ruff a line
length. The third makes `just setup` write `data/corpus.txt`, an artifact that git does not hold.

### step-03.1 ruff, a tool for development

Now we add ruff, the formatter and linter, to the group `dev` of the project. One command does it all. `uv add`
writes ruff into `pyproject.toml` and `uv.lock`, and installs it in `.venv`. The group `dev` is for the people who
work on tally. A user who installs tally does not get ruff.

do$ uv add --dev ruff

::: watch
Read the new group `dev` in the change of `pyproject.toml`, and then find ruff in the change of `uv.lock`.
:::

The move changes these files:

- `pyproject.toml`: 5 lines added; adds the group `dev`.
- `uv.lock`: 35 lines added; adds ruff, and the files of each of its versions for each system.

files:
- diff `pyproject.toml`: ruff, in a group of its own. The version is the newest on the day of the move.
  show: `"ruff>=0.17.0",`
- diff `uv.lock`: the exact version of ruff, which every learner gets with `just setup`.
  show: `name = "ruff"`

On a later day, `uv add` gets a newer ruff, so your files can name another version than the commit. timewalk
compares these two files by the names of their packages, and not their versions. So your files still match.

$ uv run ruff format --check

ruff reads every Python file of the project, and says that each one is already formatted.

### step-03.2 A line length for ruff

Now we give ruff a line length of 100, in a table `[tool.ruff]` of `pyproject.toml`. Every editor and every run of
ruff then agree on how long a line can be.

::: do
At the end of `pyproject.toml`, add the table:

```toml
[tool.ruff]
line-length = 100
```
:::

::: watch
Read the table at the end of the change of `pyproject.toml`.
:::

The move changes one file:

- `pyproject.toml`: 3 lines added; adds the table `[tool.ruff]`.

files:
- diff `pyproject.toml`: one setting, for the linter and the formatter both.
  show: `line-length = 100`

$ uv run ruff check --show-settings src | grep line_length
$ uv run ruff format --check

The first command prints `linter.line_length = 100`, so ruff reads the setting. The code still fits, and every file
is already formatted.

### step-03.3 A corpus, which just setup makes

Now `just setup` makes an artifact, `data/corpus.txt`, a text of 2000 words to count. A new script,
`scripts/corpus.py`, writes it. git ignores the folder `data/`, so the corpus stays through every move. This move is
the tagged commit of the step.

::: do
Make `scripts/corpus.py`: open its change with its item below, and press **Apply this file**. Then add `data/` to
`.gitignore`, and add a line to the recipe `setup` of the `justfile`, after `uv sync`:

```just
    uv run python scripts/corpus.py data/corpus.txt
```
:::

::: watch
Read the new line of `setup` in the change of the `justfile`, and then open `scripts/corpus.py`.
:::

The move changes these files:

- `scripts/corpus.py`: a new file of 25 lines; adds `main`.
- `.gitignore`: 3 lines added; ignores `data/`.
- `justfile`: 1 line added; changes `setup`.

files:
- diff `justfile`: `just setup` now makes the corpus too.
  show: `uv run python scripts/corpus.py data/corpus.txt`
- diff `scripts/corpus.py`: the script writes the same 2000 words each time, and leaves a corpus that is there alone.
- diff `.gitignore`: git does not hold the corpus.
  show: `data/`

$ just setup
$ uv run tally data/corpus.txt | sort -rn | head -3

`just setup` writes the corpus once. tally prints the three most common words of it.

## step-04 Types, then a docstring

$ just setup

### step-04.1 Types

Now `count` gets types. Its signature says that it takes a `str`, and gives a `dict[str, int]`. The body stays
the same.

::: do
In `src/tally/__init__.py`, change the signature of `count` to this line:

```python
def count(text: str) -> dict[str, int]:
```
:::

::: watch
Compare the old signature with the new one in the change of `src/tally/__init__.py`.
:::

The move changes one file:

- `src/tally/__init__.py`: 1 line added, 1 removed; changes `count`, in its signature only.

files:
- diff `src/tally/__init__.py`: the signature says what goes in and what comes out.
  show: `def count(text: str) -> dict[str, int]:`

$ uv run python -m unittest discover -s tests -q

The tests pass as before, because types change what the code says, not what it does.

### step-04.2 A docstring

Now `count` gets a docstring, one line under its signature that says what the function does. Python keeps the line
in `count.__doc__`.

::: do
Under the signature of `count`, add one line:

```python
    "How many times each word of `text` appears, ignoring case."
```
:::

::: watch
Read the new line under the signature in the change of `src/tally/__init__.py`.
:::

The move changes one file:

- `src/tally/__init__.py`: 1 line added; changes `count`.

files:
- diff `src/tally/__init__.py`: one line under the signature says what the function does.
  show: ``"How many times each word of `text` appears, ignoring case."``

$ uv run python -c "import tally; print(tally.count.__doc__)"

## step-05 The most common words, and a report

$ just setup

The step has three moves. They add a function with its test, an option on the command, and a recipe that makes an
artifact.

### step-05.1 A function for the most common words

Now we add `top`, a function that gives the n most common words, and its test. `top` goes in
`src/tally/__init__.py`, after `count`. It sorts the counts by count, most common first, and then by the word. Then
it keeps the first n. The test, in a new file `tests/test_top.py`, gives `top` three words.

::: do
Add `top` to `src/tally/__init__.py`, after `count`:

```python
def top(counts: dict[str, int], n: int) -> list[tuple[str, int]]:
    "The n most common words, most common first."
    return sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))[:n]
```

Then make `tests/test_top.py`:

```python
import unittest

from tally import top


class Top(unittest.TestCase):
    def test_most_common_first(self):
        self.assertEqual(top({"a": 1, "b": 3, "c": 2}, 2), [("b", 3), ("c", 2)])
```
:::

::: watch
Read `top` in the change of `src/tally/__init__.py`, and then open its test, `tests/test_top.py`.
:::

The move changes these files:

- `src/tally/__init__.py`: 5 lines added; adds `top`.
- `tests/test_top.py`: a new file of 8 lines; adds `class Top` and `test_most_common_first`.

files:
- diff `src/tally/__init__.py`: sort by count, most common first, then by the word.
  show: `return sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))[:n]`
- file `tests/test_top.py`: its test, with three words.

$ uv run python -m unittest discover -s tests -q

### step-05.2 tally --top N

Now we teach `main` an option, `--top N`. With the option, `main` prints only the N most common words, with `top`.
Without it, `main` prints every count, as before. `main` reads the option before the file name.

::: do
In `src/tally/__init__.py`, write `main` again:

```python
def main() -> None:
    "Count the words of a file, or of the standard input. With --top N, only the N most common."
    args, n = sys.argv[1:], None
    if args[:1] == ["--top"]:
        n, args = int(args[1]), args[2:]
    text = open(args[0]).read() if args else sys.stdin.read()
    counts = count(text)
    for word, times in top(counts, n) if n else sorted(counts.items()):
        print(times, word)
```
:::

::: watch
In the change of `src/tally/__init__.py`, the three lines under the docstring read the option.
:::

The move changes one file:

- `src/tally/__init__.py`: 8 lines added, 3 removed; changes `main`.

files:
- diff `src/tally/__init__.py`: `main` reads the option before the file name.
  show: `if args[:1] == ["--top"]:`

$ uv run tally --top 3 data/corpus.txt

The command prints three lines, the most common word first.

### step-05.3 A report, which just setup makes

Now we add a report of the corpus. A new recipe in the `justfile`, `report`, writes the ten most common words to
`build/top.txt`. Also, `just setup` runs `report` when that file is missing. This move is the tagged commit of the
step.

::: do
At the end of the `justfile`, add the recipe:

```just
# Write the ten most common words of the corpus to build/top.txt
report:
    mkdir -p build
    uv run tally --top 10 data/corpus.txt > build/top.txt
```

Then, in the recipe `setup`, add a line after the line that makes the corpus:

```just
    test -f build/top.txt || just report
```
:::

::: watch
Read the recipe and the new line of `setup` in the change of the `justfile`.
:::

The move changes one file:

- `justfile`: 6 lines added; adds `recipe report`, and a line in `setup`.

files:
- diff `justfile`: the report, and the line in `setup` that makes it when it is missing.
  show: `uv run tally --top 10 data/corpus.txt > build/top.txt`
  show: `test -f build/top.txt || just report`

The recipe has two lines, and `just` prints each line before it runs it.

- **`mkdir -p build`** makes the folder `build`, and does nothing when the folder is there.
- **`uv run tally --top 10 data/corpus.txt`** counts the corpus, and keeps the ten most common words.
- **`> build/top.txt`** sends what tally prints to the file, in place of the terminal.

git ignores `build/`, so the report is an artifact. The commit holds the recipe, and not the report. A report from an
earlier pass stays through every move. So remove the report first, and then `just setup` makes it again:

$ rm -f build/top.txt
$ just setup
$ cat build/top.txt

The file has ten lines, the most common word first.

## step-06 How to run it

$ just setup

The step is one commit, with no moves. The step bar stands on its tag, so the code is already there in both modes.
The README gets a section, "Run it", that says how to run tally, its tests and its report.

The step changes one file:

- `README.md`: 10 lines added; adds the section "Run it".

files:
- diff `README.md`: the commands that a new user needs first, in the order to run them.
  show: `## Run it`

$ uv run tally --top 3 data/corpus.txt
$ just test

The command prints the three most common words of the corpus, and the tests pass. step-06 is the last step.
