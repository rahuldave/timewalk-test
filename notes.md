# tally, step by step

We follow tally, a word counter, from a project that does nothing to a command with tests, types and a report.
tally is a uv project from the beginning. Every command runs through `uv run`, in the project's own `.venv`, and
never in the Python of the system. Each part begins with `just setup`, which brings the environment and the files
that the code needs up to date. `just setup` never changes git.

> Note: these notes are for the default walk, a narrative, with one section for each tagged step. Lines that start
> with "> " are cues for you. The Room window hides them.

## step-00 Where it starts
time: 0:00

$ just setup

> Say: we build a word counter in seven steps. Ask the class what it should do before we write any of it.

A project needs a place for its code, a command to run, and the same packages for everyone. tally is a uv project,
as `uv init --package` makes one. In `pyproject.toml`, the table `[project.scripts]` makes a command called
`tally`, and the table `[build-system]` lets uv install the project into its own `.venv`. `.python-version` and
`uv.lock` are in git, so every learner gets the same Python and the same packages.

`just setup` ran `uv sync`, which made `.venv`. git ignores `.venv`, so it stays as it is when the code changes.

$ uv run tally
$ ls -a

The command prints `tally: nothing to count yet`. The project has a command, and the command has no work.

main$ git log --oneline --decorate --all | head -20

> Ask: what should "the" and "The" count as?

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
time: 0:05

$ just setup

A word counter must count. A function, `count`, splits a text into words and counts each one. `main` reads a
file, or the standard input when you give no file, and prints each word with its count.

$ echo "a b a" | uv run tally
$ echo "The the THE" | uv run tally

The first command prints `2 a` and `1 b`. The second prints three lines, `1 THE`, `1 The` and `1 the`. tally counts
each as a different word, because it does not know yet that case does not matter. The second slide is a picture of what `count` does.

> Ask: is that a bug, and who decides?

files:
- diff `src/tally/__init__.py`: `count`, and a `main` that reads the text and prints the counts.
  show: `counts[word] = counts.get(word, 0) + 1`

## step-02 Tests
time: 0:10

$ just setup

We cannot tell whether `count` still works after a change, unless we try it by hand each time. Tests try it for
us. Two files of tests hold three tests, and one of them fails until counting ignores case. The fix is one word in
`count`, `lower()`. Read `tests/test_count.py` first, then the fix.

$ uv run python -m unittest discover -s tests -q
$ echo "The the THE" | uv run tally

The tests pass, and the second command now prints `3 the`.

A code block in the notes is code to read, not a command to run:

```
$ this line is not a button
```

> Say: the tutorial walk shows this step one commit at a time, with the failing test in the middle.

files:
- file `tests/test_count.py`: two tests, and `test_case` is the one that failed.
- diff `tests/test_empty.py`: an empty text counts nothing.
  show: `self.assertEqual(count(""), {})`
- diff `src/tally/__init__.py`: the fix, one word.
  show: `for word in text.lower().split():`

## step-03 Formatting, and a corpus
time: 0:15

$ just setup

Code in one style is easier to read and to change, and a count of three words shows little. So ruff, a formatter
and linter, comes in as a tool for development. `uv add --dev ruff` wrote it into the group `dev` of
`pyproject.toml`, and into `uv.lock`, and `just setup` installs it. ruff also gets a line length in
`pyproject.toml`.

And `just setup` now makes an artifact, `data/corpus.txt`, a text of 2000 words, with `scripts/corpus.py`. An
artifact is a file that the project makes and git does not hold. `.gitignore` names `data/`, so git leaves the
corpus alone, and it stays when the code changes.

$ uv run ruff format --check
$ head -3 data/corpus.txt
$ uv run tally data/corpus.txt | sort -rn | head -5
$ just setup

The second `just setup` prints `data/corpus.txt is there`, and leaves the corpus alone.

> Note: the slide pane shows a whole document for this step, and the document scrolls.

Edit the code, as a learner would. This command adds a comment at the end of `src/tally/__init__.py`:

$ printf '\n# an edit made in class\n' >> src/tally/__init__.py

> Note: open `src/tally/__init__.py` and choose "Your edits". The next move keeps the edit on a branch such as
> `timewalk/saved/step-03`, and your window says where. The corpus stays, because it is untracked and no step has a
> file in its place.

files:
- diff `pyproject.toml`: the group `dev`, with ruff, and the line length.
  show: `line-length = 100`
- diff `uv.lock`: the exact version of ruff.
  show: `name = "ruff"`
- diff `scripts/corpus.py`: writes the same 2000 words each time, and leaves a corpus that is there alone.
- diff `justfile`: `just setup` runs the script.
  show: `uv run python scripts/corpus.py data/corpus.txt`
- diff `.gitignore`: git does not hold the corpus.
  show: `data/`

## step-04 Types and docs
time: 0:20

$ just setup

To learn what `count` takes and gives, a reader had to read its body. Now its signature says so, with types, and a
docstring says in one line what it does. What `count` does is the same.

$ uv run python -c "import tally; help(tally.count)" | head -6
$ uv run python -m unittest discover -s tests -q

`help` prints the signature and the docstring, and the tests pass as before.

> Ask: who reads a type hint, the person, the editor, or Python?

files:
- diff `src/tally/__init__.py`: the types in the signature of `count`, and its docstring.
  show: `def count(text: str) -> dict[str, int]:`

## step-05 The most common words
time: 0:25

$ just setup

A reader of a long text wants the most common words first, and only a few. `top` returns the most common words,
`tally --top N` prints them, and `just report` writes them to `build/top.txt`. That report is an artifact too.
`just setup` makes it when it is missing, so a learner who comes straight here still has it.

$ cat build/top.txt
$ uv run tally --top 3 data/corpus.txt
$ just test

A long command runs in a terminal of its own, so the first terminal stays free. A second long command runs in a
third terminal:

runs$ for i in 1 2 3 4 5; do echo "epoch $i"; sleep 1; done

runs2$ for i in 1 2 3; do echo "sweep $i"; sleep 2; done

> Say: delete the report, run just setup, and it comes back.

$ rm build/top.txt; just setup; ls build

files:
- diff `src/tally/__init__.py`: `top`, and the option `--top` of `main`.
  show: `if args[:1] == ["--top"]:`
- file `tests/test_top.py`: the test of `top`.
- diff `justfile`: the recipe `report`, and the line of `setup` that runs it.
  show: `test -f build/top.txt || just report`

## step-06 How to run it
time: 0:30

$ just setup

A new user does not know which commands to run first. The README now says how to run tally, its tests and its
report. Only `README.md` changes, so the code is as it was.

$ uv run tally --top 3 data/corpus.txt

> Ask: what else would a new user ask before they run it?

files:
- diff `README.md`: a section, "Run it", with the commands that a new user needs first.
  show: `## Run it`
