# tally, step by step

The notes of the default walk, a narrative: one section for each tagged step, from a project that does nothing to
a word counter with tests, types, and a report. tally is a uv project from its first commit: every command runs
through `uv run`, in the project's own `.venv`, never the system Python. Each step starts with `just setup`, which
brings the environment, and any artifact the step needs, up to date. It never touches git: no commit, branch or
config.

Lines that start with "> " are cues for you. Hide them in the Room window.

## step-00 Where it starts
time: 0:00

$ just setup

> Say: we build a word counter in six steps. Ask the class what it should do before we write any of it.

The project is a uv project, as `uv init --package` makes one. Open `pyproject.toml`: the `[project.scripts]`
table makes a command called `tally`, and the `[build-system]` table lets uv install the project into its own
`.venv`. Open `.python-version` and `uv.lock` too. Both are in git, so every learner gets the same Python and the
same packages.

`just setup` ran `uv sync`. It made `.venv`, which git ignores and timewalk never touches, whatever step you move to.

$ uv run tally
$ ls -a

The command prints that it has nothing to count yet. The project has a command, and the command has no work.

main$ git log --oneline --decorate --all | head -20

> Ask: what should "the" and "The" count as?

## step-01 Counting
time: 0:05

$ just setup

`count` splits a text into words and counts each one. `main` reads a file, or the standard input when you give
none. Open `src/tally/__init__.py` in "Changes in this step".

$ echo "a b a" | uv run tally
$ echo "The the THE" | uv run tally

The first command prints `2 a` and `1 b`. The second prints three words of one each: tally does not know yet that
they are one word. The second slide is a picture of what `count` does.

> Ask: is that a bug? Who decides?

## step-02 Tests
time: 0:10

$ just setup

Two test files arrive, and one of the three tests fails until counting ignores case. The fix is one line in
`count`: `text.lower()`. Read `tests/test_count.py` first, then the fix in "Changes in this step".

$ uv run python -m unittest discover -s tests -q
$ echo "The the THE" | uv run tally

The tests pass, and the second command now prints `3 the`.

A code block in the notes is code to read, not a command to run:

```
$ this line is not a button
```

> Say: the tutorial walk shows this step one commit at a time, with the failing test in the middle.

## step-03 Formatting, and a corpus
time: 0:15

$ just setup

Two things arrive. ruff gets a line length in `pyproject.toml`. And `just setup` now makes an artifact:
`data/corpus.txt`, a text of 2000 words, from `scripts/corpus.py`. An artifact is a file that a step needs and git
does not hold. `.gitignore` lists `data/`, so the corpus is untracked, and it stays through every move.

$ head -3 data/corpus.txt
$ uv run tally data/corpus.txt | sort -rn | head -5
$ just setup

The second `just setup` says that the corpus is there, and leaves it alone. The slide pane shows a whole document
for this step: it scrolls.

Now make an edit from the shell, then open `src/tally/__init__.py` and choose "Edits since the step":

$ printf '\n# an edit made in class\n' >> src/tally/__init__.py

With `--discard-edits`, the step bar warns, and the next move throws the edit away. The corpus stays: it is
untracked, not an edit.

## step-04 Types and docs
time: 0:20

$ just setup

`count` says what it takes and what it returns, and has a docstring. The behaviour is the same. Open
`src/tally/__init__.py` in "Changes in this step".

$ uv run python -c "import tally; help(tally.count)" | head -6
$ uv run python -m unittest discover -s tests -q

> Ask: who reads a type hint? The person, the editor, or Python?

## step-05 The most common words
time: 0:25

$ just setup

`top` returns the most common words, `tally --top N` prints them, and `just report` writes them to
`build/top.txt`. That report is an artifact that this step makes. `just setup` makes it when it is missing, so a
learner who jumps straight here still has it.

$ cat build/top.txt
$ uv run tally --top 3 data/corpus.txt
$ just test

A long command goes to the Runs tab, so the first shell stays free, and a second one to Runs 2:

runs$ for i in 1 2 3 4 5; do echo "epoch $i"; sleep 1; done
runs2$ for i in 1 2 3; do echo "sweep $i"; sleep 2; done

> Say: delete the report, run just setup, and it comes back.

$ rm build/top.txt; just setup; ls build
