# A release of tally, one move at a time

tally counts words, and has two files of tests. We make a release, version 0.2.0. First the tests of an empty text
get a name that fits more cases. Then tally gets its new version, and last the lockfile records it. After the release, we tidy the project. The
recipes get a hidden file, and every test goes in one file.

We make the release in moves. A move is one small change, made by one patch or by one command. You make each move,
and the page checks your files against it.

> Note: the walk is on the branch `release`, with the tags release-00 to release-02. Its second move leaves
> `uv.lock` out of date on purpose, as a project does between an edit of `pyproject.toml` and `uv lock`.

> Note: release-02 renames and removes files with `mv` and `rm`, not `git mv` and `git rm`. A learner never commits,
> so git's index still has the files of release-00. `git rm` and `git mv` fail on the files that the walk changed.

## release-00 Where the release starts

$ just setup

tally counts the words of a text, and two files of tests check it. Run the tests, to see where we begin.

$ uv run python -m unittest discover -s tests -q

All three tests pass.

## release-01 Release 0.2.0

$ just setup

A release gives users a new version. Before it, we tidy the tests, and after it, the lockfile must name the new
version too.

### release-01.1 Tests of edge cases

The file `tests/test_empty.py` tests one edge case, an empty text. A text of spaces alone is another edge case. One
file can test both, so it gets a name that fits both, `tests/test_edge.py`, and a second test.

patch$ tests/test_empty.py
patch$ tests/test_edge.py

::: do
The patch renames `tests/test_empty.py` to `tests/test_edge.py`. It also renames the class to `Edge`, and adds the
test `test_spaces`.
:::

::: watch
The file `tests/test_empty.py` is now `tests/test_edge.py`. Its class is `Edge`, and its new test `test_spaces`
expects no words in a text of spaces, tabs and a newline.
:::

$ uv run python -m unittest discover -s tests -q

All four tests pass.

files:
- diff `tests/test_edge.py`: a new name, and a second test.
  show: `def test_spaces(self):`

### release-01.2 Version 0.2.0

Users tell one release from another by its version. The version is a line of `pyproject.toml`.

patch$ pyproject.toml

::: do
The patch changes one line of `pyproject.toml`, `version`, from `0.1.0` to `0.2.0`.
:::

::: watch
In `pyproject.toml`, the line `version` now says `0.2.0`.
:::

$ grep -n '^version' pyproject.toml

It prints `3:version = "0.2.0"`. The lockfile, `uv.lock`, still names version 0.1.0 of tally, so it is out of date.
The next move brings it up to date.

files:
- diff `pyproject.toml`: the new version.
  show: `version = "0.2.0"`

### release-01.3 The lock, and the list of changes

`uv.lock` records the exact version of each package of the project, tally too. `uv lock` writes it again from
`pyproject.toml`:

do$ uv lock

A user of a release wants to know what changed. A new file, `CHANGES.md`, says it for 0.2.0.

patch$ CHANGES.md

::: do
The patch makes the file `CHANGES.md`, with a heading for 0.2.0 and one sentence.
:::

::: watch
The new file `CHANGES.md` has a heading for 0.2.0, and says what changed in the tests.
:::

$ uv lock --check && grep -A1 '^name = "tally"' uv.lock

`uv lock --check` prints nothing, because the lockfile is up to date. Then `grep` prints the entry of tally, with
`version = "0.2.0"`.

files:
- diff `uv.lock`: the version of tally.
  show: `version = "0.2.0"`
- diff `CHANGES.md`: the changes of 0.2.0.

## release-02 Tidy the project

$ just setup

The release is out. Now we tidy the project, so that it is easier to find your way in it. The top folder keeps
the files that a user reads first. The tests, in two files, go into one file, named after the project.

Each file that moves or goes here moves by a command, `mv`, or goes by a command, `rm`.

### release-02.1 A hidden file for the recipes

A user of tally reads `README.md` first, and has no use for the recipes of the `justfile`. They are for the people
who work on tally. `just` also finds its recipes in a file named `.justfile`, a hidden file that `ls` does not list.
`mv` gives the `justfile` that name:

do$ mv justfile .justfile

::: watch
The file `justfile` is now `.justfile`, with the same recipes.
:::

$ just --list

It prints the same four recipes as before, `default`, `run`, `setup` and `test`.

files:
- diff `.justfile`: the recipes, in a hidden file.

### release-02.2 A test of lines

A text often has more than one line. No test yet gives `count` a text with a newline in it. A new test,
`test_lines`, counts `a b`, a newline, and `a`.

patch$ tests/test_count.py

::: do
The patch adds the test `test_lines` at the end of the class `Count`.
:::

::: watch
At the end of `tests/test_count.py`, the new test `test_lines` expects two of `a` and one of `b`, across two lines.
:::

$ uv run python -m unittest discover -s tests -q

All five tests pass.

files:
- diff `tests/test_count.py`: a test of a text of two lines.
  show: `def test_lines(self):`

### release-02.3 One name for the tests

The tests are in two files, `tests/test_count.py` and `tests/test_edge.py`. One file is one place to look. It
gets the name of the project, `tests/test_tally.py`. `mv` gives the file of edge cases that name:

do$ mv tests/test_edge.py tests/test_tally.py

::: watch
The file `tests/test_edge.py` is now `tests/test_tally.py`, with the same two tests.
:::

$ uv run python -m unittest discover -s tests -q

All five tests pass, as before. unittest finds each file whose name starts with `test`.

files:
- diff `tests/test_tally.py`: the tests of edge cases, under the new name.

### release-02.4 Every test in one file

The class `Count`, with its three tests, goes into `tests/test_tally.py` too.

patch$ tests/test_tally.py

::: do
The patch adds the class `Count`, with its three tests, at the end of `tests/test_tally.py`.
:::

::: watch
At the end of `tests/test_tally.py`, the class `Count` has the three tests of `tests/test_count.py`.
:::

$ uv run python -m unittest discover -s tests -q

All eight tests pass. The three tests of `Count` run twice, once from each file. The next change removes the old
file.

files:
- diff `tests/test_tally.py`: every test of tally, in one file.
  show: `class Count(unittest.TestCase):`

### release-02.5 The old file of tests goes

Every test of `tests/test_count.py` is now in `tests/test_tally.py` too. `rm` removes the old file:

do$ rm tests/test_count.py

::: watch
The file `tests/test_count.py` is gone, and its tests stay in `tests/test_tally.py`.
:::

$ uv run python -m unittest discover -s tests -q

Each test runs once again, and all five tests pass.

files:
- diff `tests/test_count.py`: its tests are in `tests/test_tally.py`.
