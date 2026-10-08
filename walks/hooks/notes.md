# A git hook, one move at a time

A tutorial on one part of tally, on its own branch: a hook that checks the code before each commit. Its tags
are hooks-00 to hooks-02, and the small commits between them are the moves. The slides do not follow the
moves here: sync is off for this walk in toc.toml.

## hooks-00 Where the hooks start

tally counts words, and nothing checks the code before a commit.

$ just --list

## hooks-01 The hook

We build the hook in three moves.

### hooks-01.1 A recipe that checks the code
A `check` recipe compiles every Python file. The recipe buttons above the terminal show it.

files:

$ just check

### hooks-01.2 A hook script
`hooks/pre-commit` runs the check. Run it by hand with a broken file, and see it refuse.

files:

$ printf 'def (\n' > src/tally/broken.py; sh hooks/pre-commit; echo "the hook said $?"
$ rm src/tally/broken.py

### hooks-01.3 Install it with just setup
`just setup` tells git to use the hooks folder. A step's last move is the tagged commit.

files:

$ just setup && git config core.hooksPath

## hooks-02 Tests in the hook

### hooks-02.1 A first test
One test file arrives, and it passes.

files:

$ PYTHONPATH=src python3 -m unittest discover -s tests -q

### hooks-02.2 The hook runs the tests too
Now a failing test stops a commit, as well as a file that does not compile.

files:

$ PYTHONPATH=src sh hooks/pre-commit && echo "the hook passed"
