# timewalk-test

The integration test of [timewalk](https://github.com/rahuldave/timewalk). It is a small class kit made only for
testing: a class folder with notes and slides, a project history that `history/build.py` builds into `repo/`, and
tests that drive the page in two windows, the way a class uses it.

```
just test                                     # build repo/, then run every test
TIMEWALK_LOCAL=~/Projects/timewalk just test  # test a working copy of timewalk in place of the branch
just present                                  # open the default walk in a browser
```

`pyproject.toml` takes timewalk from its `walks` branch on GitHub, where the work in progress lives. Students use
`main`, which this repository does not touch.

## What is here

| Path | What it is |
|---|---|
| `history/build.py` | Builds `repo/`, the project `tally`: tagged steps `step-00` to `step-05`, small commits between some of them, and a branch `parts` with its own tags. The same hashes on every build |
| `notes.md`, `slides/` | The default walk: a narrative, one section and one or more slides for each step |
| `tests/` | pytest and Playwright: two windows through every step and slide, a command typed into a shell, the PDF |

The tests need Chrome, `git`, `uv` and `just`. Each test builds its own copy of the project in a temporary folder.
