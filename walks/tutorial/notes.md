# tally, one move at a time

We build tally, a small word counter, one change at a time. It begins as a command with nothing to count. At the
end, it counts the words of a file, has tests and types, and writes a report of the most common words. Every
command runs through uv, in the project's own environment.

We make tally in moves. A move is one small change, made by one patch or by one command. A patch changes a file, and
a command such as `uv add` writes the files it needs.

::: do
You make each move, and the page checks your files against it. When they match, the move is made, and the next one
starts.
:::

Each move first says what problem it solves. Then it gives the change, piece by piece. Last, a command checks the
result, and a list names each file that changed, with what to look for in it.

## step-00 Where it starts

$ just setup

tally is a uv project with one command, `tally`, which has nothing to count yet. `just setup` makes the
environment of the project, `.venv`, with `uv sync`. Run the command, to see where we begin.

$ uv run tally

It prints `tally: nothing to count yet`.

files:
- file `pyproject.toml`: the project, and the table `[project.scripts]` that makes the command `tally`.
  show: `tally = "tally:main"`
- file `src/tally/__init__.py`: `main`, which has nothing to count yet.
- file `src/tally/__main__.py`: lets `python -m tally` run `main` too.
- file `justfile`: the recipes, with `setup` first.
- file `.python-version`: the version of Python that uv uses.
- file `uv.lock`: the exact packages, the same for every learner.
- file `.gitignore`: the files that git does not hold, such as `.venv`.
- file `README.md`: one line about tally.

## step-01 Counting

$ just setup

tally must count the words of a text. First we write a function that counts, and try it alone. Then the command
reads a text, and prints what the function counts.

### step-01.1 A function that counts

A word counter needs a way to count. A function, `count`, takes a text and gives a dictionary from each word to how
many times it appears. It goes in `src/tally/__init__.py`, above `main`. The command does not use it yet.

patch$ src/tally/__init__.py

::: do
The patch puts `count` above the line `def main() -> None:`, with two blank lines between them.
:::

::: watch
In `src/tally/__init__.py`, `count` now stands above `main`. It splits the text at every space, tab and end of line. For each word, it
adds 1 to the count so far, and `counts.get(word, 0)` gives 0 for a word it has not seen.
:::

$ uv run python -c "from tally import count; print(count('a b a'))"

It prints `{'a': 2, 'b': 1}`, two of `a` and one of `b`. So the function works, though the command still has
nothing to count.

files:
- diff `src/tally/__init__.py`: a dictionary from each word to how many times it appears.
  show: `counts[word] = counts.get(word, 0) + 1`

### step-01.2 The command counts

`count` works, but the command still prints that it has nothing to count. `main` must read a text and print the
counts. It reads the file that the command names, or the standard input when the command names no file. The module
`sys` gives both the arguments of the command and the standard input.

patch$ src/tally/__init__.py

::: do
The patch adds `import sys` under the docstring of the module, and writes `main` again, in place of the old one.
:::

::: watch
In `src/tally/__init__.py`, `import sys` now stands under the docstring of the module. The first line of `main`
reads the text, from the file named in `sys.argv[1]` or from the standard input. The loop prints each word with
its count. `sorted` puts the words in alphabetical order.
:::

$ echo "a b a" | uv run tally

It prints `2 a` and then `1 b`. The command now counts.

files:
- diff `src/tally/__init__.py`: `main` reads the text and prints the counts.
  show: `for word, n in sorted(count(text).items()):`

## step-02 Tests, one at a time

$ just setup

We cannot tell whether `count` still works after a change, unless we try it by hand each time. Tests try it for us.
Each test gives `count` a text, and compares what it gives back with what we expect.
We add the tests one file at a time, and run them after each. One test asks for something that `count` cannot do yet. It asks `count` to count
"The" and "the" as one word.

### step-02.1 A test of counting

Nothing checks yet that `count` gives the right counts. A test of `unittest`, the test library of Python, calls
`count` on a short text and compares the result with the dictionary that it expects. The tests go in a new folder,
`tests`.

::: do
Make the folder, and run the tests in it. The folder has no tests yet, so unittest prints `NO TESTS RAN`.

$ mkdir -p tests
$ uv run python -m unittest discover -s tests -q
:::

The first file of tests, `tests/test_count.py`, has two tests. `test_words` counts `a b a`. `test_case` counts
`A a`, and expects the one word `a`, twice. The code cannot do this yet.

patch$ tests/test_count.py

::: do
The patch makes the file `tests/test_count.py`, with the class `Count` and its two tests.
:::

::: watch
In the change of `tests/test_count.py`, look at `test_case`. It is the test that fails below.
:::

$ uv run python -m unittest discover -s tests -q

One test fails. `test_case` expects `{'a': 2}`, and gets `{'A': 1, 'a': 1}`. The failure is a question that the
code has not answered yet.

> Say: look, a failure. Ask the class what the smallest change is that makes it pass.

files:
- diff `tests/test_count.py`: two tests. The second asks for something the code cannot do yet.
  show: `self.assertEqual(count("A a"), {"a": 2})`

### step-02.2 A test of an empty text

An empty file is a text with no words. `count` must give an empty dictionary for it, and not fail. A test in a
file of its own, `tests/test_empty.py`, says so, and keeps it true after later changes.

patch$ tests/test_empty.py

::: do
The patch makes the file `tests/test_empty.py`, with the class `Empty` and its test.
:::

::: watch
The new file `tests/test_empty.py` holds one test, `test_empty`. It gives `count` the empty text `""`, and
expects the empty dictionary `{}`.
:::

$ uv run python -m unittest discover -s tests -q

The new test passes at once, because `split()` finds no words in an empty text. `test_case` still fails.

files:
- diff `tests/test_empty.py`: an empty text counts nothing.
  show: `self.assertEqual(count(""), {})`

### step-02.3 Case does not matter

`test_case` fails, because `count` counts `A` and `a` as two words. When `count` puts the text in lower case before
it splits it, every word is counted in lower case. One word in the loop of `count`, `lower()`, does it.

patch$ src/tally/__init__.py

::: do
In `count`, the patch puts `text.lower().split()` in place of `text.split()`.
:::

::: watch
In `count`, in `src/tally/__init__.py`, the loop now splits `text.lower()`, and not `text`. So `A` and `a` are
the same word.
:::

$ uv run python -m unittest discover -s tests -q
$ echo "The the" | uv run tally

All three tests pass, and the command prints `2 the` for "The the".

files:
- diff `src/tally/__init__.py`: one word, `lower()`, answers the failing test.
  show: `for word in text.lower().split():`

## step-03 Formatting, and a corpus

$ just setup

tally works, and it has tests. Two things help the work ahead. Code in one style is easier to read and to change,
so we install ruff, a formatter and linter. And a count of three words shows little, so `just setup` makes a
corpus, a text of 2000 words to count.

### step-03.1 ruff, a tool for development

Each person writes code in a style of their own, with other quotes, blank lines and lengths of line. A formatter
writes every file in one style. A linter reads the code, and reports mistakes that the tests do not find. ruff is
both. It goes in the group `dev` of the project. The group `dev` is for the people who work on tally, so a user
who installs tally does not get ruff.

One command does it all. `uv add` writes ruff into `pyproject.toml` and `uv.lock`, and installs it in `.venv`.

do$ uv add --dev ruff

::: do
On a later day, `uv add` gets a newer ruff, and your two files name another version than the ones here. The
version is then the only difference, and that is correct.
:::

::: watch
In `pyproject.toml`, a new table `[dependency-groups]` has the group `dev`, with the line `"ruff>=0.17.0",`. In
`uv.lock`, the entry `name = "ruff"` gives the exact version, and the files of ruff for each system.
:::

$ uv run ruff format --check

ruff reads every Python file of the project, and prints `5 files already formatted`.

files:
- diff `pyproject.toml`: ruff, in a group of its own. The version is the newest on the day that ruff was added.
  show: `"ruff>=0.17.0",`
- diff `uv.lock`: the exact version of ruff, which every learner gets with `just setup`.
  show: `name = "ruff"`

### step-03.2 A line length for ruff

ruff and each editor have their own idea of how long a line can be. A setting in `pyproject.toml` makes them agree.
It is a table `[tool.ruff]`, with a line length of 100.

patch$ pyproject.toml

::: do
The patch adds the table `[tool.ruff]` at the end of `pyproject.toml`, after the group `dev`.
:::

::: watch
At the end of `pyproject.toml`, the table `[tool.ruff]` sets `line-length = 100`. The linter and the formatter
both read it.
:::

$ uv run ruff check --show-settings src | grep line_length
$ uv run ruff format --check

The first command prints `linter.line_length = 100`, so ruff reads the setting. The code still fits, and every file
is already formatted.

files:
- diff `pyproject.toml`: one setting, for the linter and the formatter both.
  show: `line-length = 100`

### step-03.3 A corpus, which just setup makes

A count of `a b a` shows little. tally needs a long text to count, the same for every learner. A script,
`scripts/corpus.py`, writes `data/corpus.txt`, 2000 words from a short list, in the same order each time. The
script comes whole, as a patch.

patch$ scripts/corpus.py

The corpus is an artifact, a file that the project makes and git does not hold. So `.gitignore` names the folder
`data/`. git leaves an ignored file alone, so the corpus stays when the code changes.

patch$ .gitignore

::: do
The patch adds the folder `data/` at the end of `.gitignore`, under a comment.
:::

`just setup` makes the environment, and now it runs the script too. So every learner has the corpus. The script
does not touch a corpus that is already there, so a second `just setup` writes nothing.

patch$ justfile

::: do
In the recipe `setup`, the patch adds the line that runs the script, after the line `uv sync`.
:::

::: watch
The new file `scripts/corpus.py` picks each word from the list `WORDS`, with a number that it works out from the
number before it. The first number is always 7, so the words are the same each time. `.gitignore` now ends with
`data/`, and the recipe `setup` of the `justfile` runs the script after `uv sync`.
:::

$ just setup
$ uv run tally data/corpus.txt | sort -rn | head -3

`just setup` prints `wrote data/corpus.txt: 2000 words`. `sort -rn` puts the lines of tally in order of count, highest
first, and `head -3` keeps the first three. They are `127 line`, `126 class` and `125 word`.

files:
- diff `justfile`: `just setup` now makes the corpus too.
  show: `uv run python scripts/corpus.py data/corpus.txt`
- diff `scripts/corpus.py`: the script writes the same 2000 words each time, and does not touch a corpus that is already there.
  show: `if target.exists():`
- diff `.gitignore`: git does not hold the corpus.
  show: `data/`

## step-04 Types, then a docstring

$ just setup

To learn what `count` takes and what it gives, a reader must now read its body. Its signature can say it at a
glance, and an editor can check it. One line under the signature can say what the function does. Neither changes
what `count` does, so the tests pass as before.

### step-04.1 Types

The signature `def count(text):` does not say what `text` is, or what `count` gives back. Types say it. `count`
takes a `str`, and gives a `dict[str, int]`, a dictionary from words to counts. The body stays the same.

patch$ src/tally/__init__.py

::: do
The patch writes the signature of `count` again, with its types.
:::

::: watch
In `src/tally/__init__.py`, the signature of `count` now says `text: str`, and `-> dict[str, int]` for what it
gives back. The body is the same.
:::

$ uv run python -m unittest discover -s tests -q

The three tests pass as before, because types change what the code says, not what it does.

files:
- diff `src/tally/__init__.py`: the signature says what goes in and what comes out.
  show: `def count(text: str) -> dict[str, int]:`

### step-04.2 A docstring

The types say what `count` takes and gives, but not what it does with the text. A docstring says it. It is a string on
the first line of a function. Python keeps it in `count.__doc__`, and `help(count)` prints it.

patch$ src/tally/__init__.py

::: do
The patch adds the docstring under the signature of `count`, before the line `counts = {}`.
:::

::: watch
In `src/tally/__init__.py`, the first line of `count` is now its docstring. It says that `count` ignores case.
:::

$ uv run python -c "import tally; print(tally.count.__doc__)"

It prints the docstring, ``How many times each word of `text` appears, ignoring case.``

files:
- diff `src/tally/__init__.py`: one line under the signature says what the function does.
  show: ``"How many times each word of `text` appears, ignoring case."``

## step-05 The most common words, and a report

$ just setup

tally prints a line for every word, in alphabetical order. A reader of a long text wants the most common words
first, and only a few of them. A function finds them, and an option of the command prints them. A recipe writes a
report of the ten most common words of the corpus.

### step-05.1 A function for the most common words

`count` gives the counts in no useful order. To find the most common words, tally must sort the counts, most common
first, and keep the first few. A function, `top`, does it. It sorts by count, highest first, and then by the
word, so that two words with the same count keep one order. Then it keeps the first `n`.

patch$ src/tally/__init__.py

::: do
The patch puts `top` after `count` and before `main`, with two blank lines around it.
:::

A test says what `top` must give. It gives `top` three words with their counts, and asks for the two most common.

patch$ tests/test_top.py

::: do
The patch makes the file `tests/test_top.py`, with its one test.
:::

::: watch
In `src/tally/__init__.py`, `top` stands between `count` and `main`. It sorts with the key `(-pair[1], pair[0])`.
The key is the count with a minus sign, so that the highest count comes first, and then the word. The new file
`tests/test_top.py` has one test, `test_most_common_first`.
:::

$ uv run python -m unittest discover -s tests -q

The four tests pass.

files:
- diff `src/tally/__init__.py`: sort by count, most common first, then by the word.
  show: `return sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))[:n]`
- file `tests/test_top.py`: its test, with three words.

### step-05.2 tally --top N

tally prints every word of a text, and the corpus fills the screen. An option, `--top N`, makes `main` print only the
`N` most common words, with `top`. Without the option, `main` prints every count, as before. `main` reads the
option before the name of the file, so the command is `tally --top 3 data/corpus.txt`.

patch$ src/tally/__init__.py

::: do
The patch writes `main` again, in place of the old one.
:::

::: watch
In `src/tally/__init__.py`, `main` now has a docstring, and the three lines under the docstring read the option.
When the first argument is `--top`, the second is the number `N`, and the name of the file comes after them. The
loop prints `top(counts, n)` when there is an `N`, and every count when there is not.
:::

$ uv run tally --top 3 data/corpus.txt

The command prints three lines, the most common word first. They are `127 line`, `126 class` and `125 word`.

files:
- diff `src/tally/__init__.py`: `main` reads the option before the name of the file.
  show: `if args[:1] == ["--top"]:`

### step-05.3 A report, which just setup makes

The most common words of the corpus make a report, which others want to read without running tally. A recipe of
the `justfile`, `report`, writes the ten most common words to `build/top.txt`. The recipe has two lines, and `just`
prints each line before it runs it. The second line has two parts.

- **`mkdir -p build`** makes the folder `build`, and does nothing when the folder is there.
- **`uv run tally --top 10 data/corpus.txt`** counts the corpus, and keeps the ten most common words.
- **`> build/top.txt`** sends what tally prints to the file, in place of the terminal.

patch$ justfile

::: do
The patch adds the recipe `report` at the end of the `justfile`.
:::

The report is an artifact, as the corpus is. git ignores the folder `build/`, so git holds the recipe, and not the
report. `just setup` makes the report when the file is missing. `test -f build/top.txt` is true when the file is
there, and `||` runs `just report` only when it is not.

::: do
The same patch adds a line to the recipe `setup`, after the line that makes the corpus.
:::

::: watch
At the end of the `justfile`, the new recipe `report` makes the folder `build`, and writes the report into it. In
the recipe `setup`, the new last line runs `just report` when `build/top.txt` is missing.
:::

A report from an earlier run stays, because git ignores it. So remove the report first, and then `just setup` makes
it again:

$ rm -f build/top.txt
$ just setup
$ cat build/top.txt

The file has ten lines, the most common word first.

files:
- diff `justfile`: the report, and the line in `setup` that makes it when it is missing.
  show: `uv run tally --top 10 data/corpus.txt > build/top.txt`
  show: `test -f build/top.txt || just report`

## step-06 How to run it

$ just setup

A new user of tally does not know which commands to run, or in which order. The README gets a section, "Run it",
that says how to run tally, its tests and its report. The code does not change.

patch$ README.md

::: do
The patch adds the section "Run it" to `README.md`, after the line `Count the words in a text.`
:::

::: watch
At the end of `README.md`, the new section "Run it" gives the two commands to run first, `just setup` and then
tally on the corpus. Under them, it names the option `--top`, the tests and the report.
:::

$ uv run tally --top 3 data/corpus.txt
$ just test

The command prints the three most common words of the corpus, and the tests pass. tally is finished.

files:
- diff `README.md`: the commands that a new user needs first, in the order to run them.
  show: `## Run it`
