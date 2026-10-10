# A git hook, one move at a time

A tutorial on one part of tally, on a branch of its own: a hook that checks the code before each commit. Its tags
are hooks-00 to hooks-02, and the small commits between them are the moves. This walk starts in watch mode: Show
checks out each move's commit, and the command at the end of the move shows what it did. Switch to Do to make the
moves by hand. The slides do not follow the moves here: sync is off for this walk in toc.toml.

## hooks-00 Where the hooks start

$ just setup

tally counts words, and nothing checks the code before a commit. This step is step-01 of main, with another name.

$ just --list

## hooks-01 The hook

$ just setup

We build the hook in three moves: a recipe, a script that runs it, and a recipe that installs it.

### hooks-01.1 A recipe that checks the code

Add a `check` recipe to the justfile. It compiles every Python file, which catches a syntax error before a commit
does.

```just
# Check that every Python file compiles
check:
    uv run python -m py_compile src/tally/*.py
```

This is the file changed:

- `justfile`: 4 lines added; adds `recipe check`.

files:
- diff `justfile`: the recipe compiles every Python file.
  show: `uv run python -m py_compile src/tally/*.py`

$ just check && echo "the code compiles"

### hooks-01.2 A hook script

Make `hooks/pre-commit`, and make it executable with `chmod +x hooks/pre-commit`. git runs it before each commit,
and refuses the commit when it fails.

```sh
#!/bin/sh
# Run before each commit: refuse it if the code does not compile.
just check
```

This is the file changed:

- `hooks/pre-commit`: a new file of 3 lines.

files:
- file `hooks/pre-commit`: three lines; git runs it before a commit.
- diff `hooks/pre-commit`: the hook only runs the check.
  show: `just check`

Run it by hand on a broken file, and see it refuse. Then remove the file:

$ printf 'def (\n' > src/tally/broken.py; sh hooks/pre-commit; echo "the hook said $?"
$ rm src/tally/broken.py

The hook says 1: a commit would be refused.

### hooks-01.3 Install it

Hooks are not cloned with a repository: each copy installs its own. Add an `install-hook` recipe that tells git to
use the `hooks` folder. It changes git's config, so it is a recipe of its own, and not part of `just setup`, which
only makes the environment and the artifacts. This move is the tagged commit of the step.

```just
# Make git run the hooks in hooks/, before each commit
install-hook:
    git config core.hooksPath hooks
```

This is the file changed:

- `justfile`: 4 lines added; adds `recipe install-hook`.

files:
- diff `justfile`: one line of git config, in a recipe of its own.
  show: `git config core.hooksPath hooks`

$ just install-hook && git config core.hooksPath

It prints `hooks`: git now runs the hook before each commit.

> Note: the replay copy is a git worktree, and a worktree shares the repository's config. So this setting reaches
> the repository you started from too. That is harmless here: where `hooks/` does not exist, git runs nothing.

## hooks-02 Tests in the hook

$ just setup

Two moves: a first test, and a hook that runs the tests too.

### hooks-02.1 A first test

Make `tests/test_count.py` with one test of counting:

```python
import unittest

from tally import count


class Count(unittest.TestCase):
    def test_words(self):
        self.assertEqual(count("a b a"), {"a": 2, "b": 1})
```

This is the file changed:

- `tests/test_count.py`: a new file of 9 lines; adds `class Count` and `test_words`.

files:
- diff `tests/test_count.py`: one test of counting.
  show: `self.assertEqual(count("a b a"), {"a": 2, "b": 1})`

$ uv run python -m unittest discover -s tests -q

### hooks-02.2 The hook runs the tests too

Add one line to `hooks/pre-commit`, so that a failing test refuses a commit as well:

```sh
uv run python -m unittest discover -s tests -q
```

This is the file changed:

- `hooks/pre-commit`: 1 line added.

files:
- diff `hooks/pre-commit`: the tests run after the check.
  show: `uv run python -m unittest discover -s tests -q`

$ sh hooks/pre-commit && echo "the hook passed"

The hook compiles the code, runs the tests, and passes.
