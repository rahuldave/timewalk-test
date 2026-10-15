# A bigger tally, one move at a time

tally counts words, has tests, and writes a report. Now it grows as a real project does. It gets a dependency with
a range of versions, and a tool for its docs in a group of its own. It gets a page of docs with a picture, and a
library of its own in the same workspace. Then ruff passes its code. Last, it drops a dependency that it no longer
needs.

We make each change in moves. A move is one small change, made by one patch or by one command. You make each move,
and the page checks your files against it.

> Note: the walk is on the branch `extra`, with the tags extra-00 to extra-04 and a lettered extra-03b. The files
> that a command writes are what uv 0.12.13 and ruff 0.17.0 wrote. A learner with a newer uv or mdformat gets other
> versions in `pyproject.toml` and `uv.lock`. In the walk extra, `loose` lets them match. In the walk strict-extra,
> the learner takes the author's files in place of each uv command.

## extra-00 Where it starts

$ just setup

tally counts the words of a file, and `--top N` keeps the most common. Run it on the corpus, to see where we begin.

$ uv run tally --top 3 data/corpus.txt

It prints `127 line`, `126 class` and `125 word`, one to a line.

## extra-01 A table, and a tool for the docs

$ just setup

A list of counts is hard to read at a glance. A table lines up the words and the counts. A small package,
tabulate, draws tables, so tally depends on it. The docs come later, and their tool comes now, in a group of its own.

### extra-01.1 tabulate, in a range of versions

tally needs tabulate to draw a table. A new version 1.0 of tabulate could change how it draws one, so tally takes
any 0.9 version, and no later one. `uv add` with a range of versions puts the range in `pyproject.toml`, and the
exact version in `uv.lock`:

do$ uv add "tabulate>=0.9,<0.10"

::: watch
In `pyproject.toml`, the list `dependencies` now holds `tabulate>=0.9,<0.10`. In `uv.lock`, tabulate has the version
0.9.0, the one version in that range.
:::

$ uv run python -c "import tabulate; print(tabulate.__version__)"

It prints `0.9.0`.

files:
- diff `pyproject.toml`: tabulate, with the range of its versions.
  show: `"tabulate>=0.9,<0.10",`
- diff `uv.lock`: the exact version of tabulate.

### extra-01.2 tally --table

tally prints one line for each word, with the count first. A new option, `--table`, prints the same counts as a
table, with a header. `main` takes the option out of the arguments, and passes the rows to `tabulate`.

patch$ src/tally/__init__.py

::: do
The patch adds `from tabulate import tabulate` under `import sys`, after a blank line. In `main`, it adds the flag
`as_table`, and prints the rows with `tabulate` when the flag is set.
:::

::: watch
In `main` of `src/tally/__init__.py`, the flag `as_table` is true when the arguments hold `--table`. The rows then go
to `tabulate`, with the header `word` and `times`.
:::

$ uv run tally --top 3 --table data/corpus.txt

It prints a header, `word` and `times`, a line of dashes, and the three words with their counts in a column on the
right.

files:
- diff `src/tally/__init__.py`: the option `--table`, which prints the rows with tabulate.
  show: `print(tabulate(rows, headers=["word", "times"]))`

### extra-01.3 mdformat, in the group docs

The docs will be Markdown files. mdformat formats Markdown, and its option `--check` says whether a file is
formatted. Only the people who write the docs need it, so it goes in a group of its own, `docs`:

do$ uv add --group docs mdformat

`uv sync` installs the group `dev` and no other group, unless the project names more. One more line in the table
`[tool.uv]` of `pyproject.toml` names both groups, so that `just setup` installs mdformat too.

patch$ pyproject.toml

::: do
After `uv add`, the patch adds a table `[tool.uv]` at the end of `pyproject.toml`, with the line `default-groups`.
:::

::: watch
`pyproject.toml` has a group `docs` with mdformat, and at its end a table `[tool.uv]` whose `default-groups` names
`dev` and `docs`.
:::

$ uv sync -q && uv run --no-sync mdformat --version

`uv sync` installs mdformat. Then `uv run --no-sync` runs it without another sync, and it prints `mdformat 1.0.0`, or a
newer version.

files:
- diff `pyproject.toml`: the group `docs`, and the groups that `uv sync` installs.
  show: `default-groups = ["dev", "docs"]`
- diff `uv.lock`: the exact versions of mdformat and of the packages it needs.

## extra-02 The docs

$ just setup

The README says in a few lines how to run tally. A user who wants more needs a page of docs. We write it piece by
piece, with a picture. The README then shows how to count from Python, and a recipe checks that the docs are
formatted.

### extra-02.1 A page on how to run tally

A user who opens the folder `docs` wants one page on how to run tally. Its name has spaces in it, `how to run.md`,
as the names of pages often do.

patch$ `docs/how to run.md`

::: do
The patch makes the file `docs/how to run.md`, with a heading and two sections, "Set up" and "Count the words of a
file".
:::

::: watch
The new page `docs/how to run.md` has two sections, each with a command in a fenced block of `sh`.
:::

$ uv run mdformat --check docs

It prints nothing, because the page is formatted as mdformat formats it.

files:
- file `docs/how to run.md`: the page, with how to set up and how to count.
  show: `# How to run tally`

### extra-02.2 The most common words

The page does not say how to keep only the most common words. A section says it, with the option `--top`.

patch$ `docs/how to run.md`

::: do
The patch adds the section "Only the most common words" at the end of `docs/how to run.md`.
:::

::: watch
At the end of `docs/how to run.md`, the section "Only the most common words" runs `uv run tally --top 10`.
:::

$ uv run tally --top 10 data/corpus.txt

It prints the ten lines that the section promises, from `127 line` down to `110 code`.

files:
- diff `docs/how to run.md`: the option `--top`.
  show: `## Only the most common words`

### extra-02.3 The table

The option `--table` is new, and the page does not name it. A section names it.

patch$ `docs/how to run.md`

::: do
The patch adds the section "A table" at the end of `docs/how to run.md`.
:::

::: watch
At the end of `docs/how to run.md`, the section "A table" runs tally with `--top 10 --table`.
:::

$ uv run mdformat --check docs

It prints nothing, so the page is still formatted.

files:
- diff `docs/how to run.md`: the option `--table`.
  show: `## A table`

### extra-02.4 A picture of the most common words

A picture tells at a glance that the ten most common words have about the same count. A file `docs/tally.png`
draws them as ten blue bars. The file is binary, so its patch has no lines to read.

patch$ docs/tally.png

::: do
The patch makes the file `docs/tally.png`, a picture of 60 by 30 pixels.
:::

::: watch
The new file `docs/tally.png` is a picture of ten blue bars, one for each of the most common words.
:::

$ file docs/tally.png

It prints `docs/tally.png: PNG image data, 60 x 30, 8-bit/color RGB, non-interlaced`.

files:
- diff `docs/tally.png`: ten bars, one for each of the most common words.

### extra-02.5 The page shows the picture

The picture is in the folder `docs`, but no page shows it. The section on the most common words shows it, under
its command.

patch$ `docs/how to run.md`

::: do
The patch adds a line with the picture under the sentence "It prints the ten most common words, the most common
first."
:::

::: watch
In `docs/how to run.md`, the section "Only the most common words" shows `tally.png`, with words that say what it
draws.
:::

$ grep -n 'tally.png' "docs/how to run.md"

It prints the line of the picture, with its number.

files:
- diff `docs/how to run.md`: the picture, in its section.
  show: `![The ten most common words of the corpus, as bars](tally.png)`

### extra-02.6 Count from Python

tally is a library as well as a command. A user who writes Python wants to call `count` and `top`. A new section of
the README shows how, in a fenced block of Python.

patch$ README.md

::: do
The patch adds the section "Count from Python" at the end of `README.md`, with a block that counts a short text.
:::

::: watch
At the end of `README.md`, the section "Count from Python" counts the words of `"the cat and the hat"`, and keeps
the two most common.
:::

$ uv run python -c "from tally import count, top; print(top(count('the cat and the hat'), 2))"

It prints `[('the', 2), ('and', 1)]`, as the README says.

files:
- diff `README.md`: the section "Count from Python", with its block of code.
  show: `print(top(counts, 2))`

### extra-02.7 The README links to the page

A reader of the README does not know that the page exists. A link at the end of the README names it. The path has
spaces, so the link writes each one as `%20`.

patch$ README.md

::: do
The patch adds one sentence at the end of `README.md`, with a link to `docs/how%20to%20run.md`.
:::

::: watch
The last sentence of `README.md` links to the page `docs/how to run.md`, with `%20` for each space.
:::

$ grep -o 'docs/how%20to%20run.md' README.md

It prints the path of the link, `docs/how%20to%20run.md`.

files:
- diff `README.md`: a link to the page.
  show: `The page [How to run tally](docs/how%20to%20run.md) says more, with a picture of the most common words.`

### extra-02.8 The picture in green

The blue bars look like links on a page of blue links. Green bars stand apart. The patch replaces the picture.

patch$ docs/tally.png

::: do
The patch replaces `docs/tally.png` with the same bars in green.
:::

::: watch
`docs/tally.png` has the same ten bars, now green.
:::

$ file docs/tally.png

It prints `docs/tally.png: PNG image data, 60 x 30, 8-bit/color RGB, non-interlaced`, as before. Only the colour
changed.

files:
- diff `docs/tally.png`: the bars, in green.

### extra-02.9 Count a file from Python

A short text in the README shows little. The block of Python now counts the corpus, and keeps the three most common
words.

patch$ README.md

::: do
In the block of Python of `README.md`, the patch adds `from pathlib import Path`, and counts the text of
`data/corpus.txt`. The sentence under the block gives the new output.
:::

::: watch
The block of Python in `README.md` reads `data/corpus.txt` with `Path`, and prints the three most common words.
:::

This command takes the block of Python out of the README, and runs it:

$ sed -n '/^```python$/,/^```$/p' README.md | sed '1d;$d' | uv run python -

It prints `[('line', 127), ('class', 126), ('word', 125)]`, as the README says.

files:
- diff `README.md`: the block of Python counts the corpus.
  show: `counts = count(Path("data/corpus.txt").read_text())`

### extra-02.10 A recipe that checks the docs

Nobody remembers to run mdformat on each page. A recipe, `just docs`, checks the README and the folder `docs` in one
command.

patch$ justfile

::: do
The patch adds the recipe `docs` at the end of the `justfile`.
:::

::: watch
At the end of the `justfile`, the recipe `docs` runs `mdformat --check` on `README.md` and on `docs`.
:::

$ just docs

It fails, with exit code 1. mdformat says that `README.md` is not formatted. The section "Run it" has a block of
code indented by four spaces, and mdformat writes a fenced block.

files:
- diff `justfile`: the recipe `docs`.
  show: `uv run mdformat --check README.md docs`

### extra-02.11 The README as mdformat writes it

The check fails on the README. mdformat without `--check` formats the file in place:

do$ uv run mdformat README.md

::: watch
In the section "Run it" of `README.md`, the two indented lines are now a fenced block.
:::

$ just docs

It prints the command of the recipe, and mdformat prints nothing. The README and the page are formatted.

files:
- diff `README.md`: a fenced block in place of the indented lines.

### extra-02.12 The page says how to check the docs

A writer of the docs needs to know that the recipe exists. A last section of the page names it.

patch$ `docs/how to run.md`

::: do
The patch adds the section "Check the docs" at the end of `docs/how to run.md`.
:::

::: watch
At the end of `docs/how to run.md`, the section "Check the docs" runs `just docs`, and says what it prints.
:::

$ just docs

mdformat prints nothing, so the new section is formatted too.

files:
- diff `docs/how to run.md`: how to check the docs.
  show: `## Check the docs`

## extra-03 A library

$ just setup

`top` keeps the most common words of any counts. Another program that counts words could use it too. So it goes
into a library of its own, `talib`, in the same workspace. A workspace is a set of packages that share one
`uv.lock`.

### extra-03.1 A library, with uv init

`uv init --lib` makes a library. In a folder of a project, it also makes the library a member of the project's
workspace. `--author-from none` leaves out the name of the author, which uv would take from your git settings.

do$ uv init --lib --author-from none packages/talib

::: watch
The folder `packages/talib` holds a new project, with its own `pyproject.toml` and a function `hello`. The
`pyproject.toml` of tally names it under `[tool.uv.workspace]`.
:::

`uv.lock` does not name talib yet, so it is out of date until the next move. A `uv run` would lock it again, so the
check reads the file:

$ grep -A2 'tool.uv.workspace' pyproject.toml

It prints the table `[tool.uv.workspace]`, with `members = [` and `"packages/talib",` under it.

files:
- diff `pyproject.toml`: the workspace, with talib as its member.
  show: `"packages/talib",`
- file `packages/talib/pyproject.toml`: the project of the library.
- file `packages/talib/src/talib/__init__.py`: a first function, `hello`.
- file `packages/talib/README.md`: empty, for the words about the library.
- file `packages/talib/src/talib/py.typed`: empty, to say that the library has types.

### extra-03.2 tally depends on talib

tally cannot import talib until it depends on it. `uv add` finds talib in the workspace, and takes it from there:

do$ uv add talib

::: watch
`pyproject.toml` lists `talib` under `dependencies`, and a table `[tool.uv.sources]` says that it comes from the
workspace. `uv.lock` names both packages.
:::

$ uv run python -c "import talib; print(talib.hello())"

It prints `Hello from talib!`.

files:
- diff `pyproject.toml`: talib, from the workspace.
  show: `talib = { workspace = true }`
- diff `uv.lock`: talib, as a member of the workspace.

### extra-03.3 top goes into talib

`top` is still in tally, and talib has only `hello`. One patch moves `top` across, in both packages.

patch$ packages/talib/src/talib/__init__.py
patch$ src/tally/__init__.py

::: do
In `packages/talib/src/talib/__init__.py`, the patch puts a docstring and `top` in place of `hello`. In
`src/tally/__init__.py`, it removes `top`, and adds `from talib import top` under `from tabulate import tabulate`.
:::

::: watch
`top` is now in `packages/talib/src/talib/__init__.py`. `src/tally/__init__.py` imports it from talib, so the tests
that import `top` from tally still find it.
:::

$ uv run python -m unittest discover -s tests -q

All four tests pass.

$ head -4 packages/talib/src/talib/__init__.py

> Say: two blank lines stand between the docstring and `top`, as PEP 8 asks. The output below shows them.
```text
"""talib: small helpers for the counts of words."""


def top(counts: dict[str, int], n: int) -> list[tuple[str, int]]:
```

It prints the docstring of the library, two blank lines, and the first line of `top`.

files:
- diff `packages/talib/src/talib/__init__.py`: `top`, in place of `hello`.
  show: `def top(counts: dict[str, int], n: int) -> list[tuple[str, int]]:`
- diff `src/tally/__init__.py`: `top` comes from talib.
  show: `from talib import top`

## extra-03b Lint

$ just setup

ruff finds code that works but could be better, such as a file that nobody closes. It fixes some of what it finds
by itself, and leaves the rest to us.

### extra-03b.1 What ruff fixes

`ruff check --fix` fixes what it can, and lists the rest. It writes its fixes, and then exits with code 1, because
one problem is left.

do$ uv run ruff check --fix

::: watch
In `scripts/corpus.py`, ruff wrote the list `WORDS` as a list of strings, in place of a string that the code split.
:::

$ uv run ruff check --statistics

It fails, with exit code 1. It prints one line for the rule `SIM115`, open-file-with-context-handler, and then
`Found 1 error.` `main` opens a file and never closes it, and ruff cannot fix that.

files:
- diff `scripts/corpus.py`: a list of words, as ruff writes it.
  show: `WORDS = ["the", "a", "word", "count", "text", "tally", "test", "step", "move", "commit", "tag", "note", "slide", "class", "shell", "file", "line", "code"]`

### extra-03b.2 main closes its file

ruff cannot fix SIM115. A `with` block closes the file when the block ends.

patch$ src/tally/__init__.py

::: do
In `main` of `src/tally/__init__.py`, the patch puts an `if` and a `with` block in place of the line
`text = open(args[0]).read() if args else sys.stdin.read()`.
:::

::: watch
`main` in `src/tally/__init__.py` reads the file in a `with` block, and reads the standard input when there is no
file.
:::

$ uv run ruff check

It prints `All checks passed!`.

files:
- diff `src/tally/__init__.py`: a `with` block, which closes the file.
  show: `with open(args[0]) as file:`

## extra-04 One dependency less

$ just setup

tally uses tabulate for one table, of two columns. A few lines of its own draw the same table, and the project
needs one package less.

### extra-04.1 tally draws its own table

A function `table` draws the header, the rule of dashes, and the rows, with the same widths as tabulate.

patch$ src/tally/__init__.py

::: do
The patch removes `from tabulate import tabulate`, adds the function `table` above `main`, and calls it in place of
`tabulate`.
:::

::: watch
`src/tally/__init__.py` has a function `table`, and `main` prints `table(rows)`. Nothing imports tabulate now.
:::

$ uv run tally --top 3 --table data/corpus.txt

It prints the same table as tabulate printed. It has the header `word` and `times`, a rule of dashes, and three
rows.

files:
- diff `src/tally/__init__.py`: the function `table`, in place of tabulate.
  show: `def table(rows: list[tuple[str, int]]) -> str:`

### extra-04.2 tabulate goes

Nothing imports tabulate now, but the project still depends on it. `uv remove` takes it out of `pyproject.toml`
and `uv.lock`:

do$ uv remove tabulate

::: watch
`pyproject.toml` no longer lists tabulate, and `uv.lock` no longer has it.
:::

$ uv run python -m unittest discover -s tests -q

All four tests pass, without tabulate.

files:
- diff `pyproject.toml`: tabulate is gone.
- diff `uv.lock`: tabulate is gone.

