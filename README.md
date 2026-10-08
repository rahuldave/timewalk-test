# timewalk-test

The integration test of [timewalk](https://github.com/rahuldave/timewalk), and a class kit that shows every
feature of it. A class folder with five walks steps through `tally`, a small word counter, whose history
`history/build.py` builds into `repo/`. The tests drive the page in two windows, the way a class uses it.

```
just present            # open the walks in a browser, starting on the default walk
just present tutorial   # start on another walk: narrative, tests, parts, tutorial or hooks
just check              # check the notes and slides of every walk against the steps
just pdf hooks          # the PDF of one walk's slides, in build/
just build              # build repo/ again, and start again from the first step
just test               # build a fresh copy, then run every test
```

`pyproject.toml` takes timewalk from its `walks` branch on GitHub. To use a working copy of timewalk instead,
put `TIMEWALK_LOCAL=~/Projects/timewalk` before any recipe. Students use timewalk's `main`, which this
repository does not touch.

## A tour

Run `just present`. Two windows are useful: yours, and the **Room** window that its button opens. Change the
walk with the menu at the left of the step bar.

| Walk | Kind | Try this |
|---|---|---|
| **tally, step by step** (`narrative`) | narrative, every step | Right and Left through the six steps. The notes use every kind of line: `time:` for the clock band, `>` cues, and commands for **At this step**, **Runs**, **Runs 2** and **Main**. step-01 has a picture slide. step-03 shows a whole document, and its command makes an edit: open `src/tally/__init__.py` and choose "Edits since the step". The recipe buttons above the terminal come from the project's justfile |
| **Only the tests** (`tests`) | narrative, some steps | Three of the six steps, with slides borrowed from the default walk's folder |
| **Tests first, on the parts branch** (`parts`) | narrative, its own tags | Steps `parts-01` and `parts-02`, on another branch. The replay copy moves to that branch |
| **tally, one move at a time** (`tutorial`) | tutorial | Go to step-02 and press Shift+Right. Each move is one small commit: the notes gray the moves still to come, `files:` opens what the move changed, and a move with slides of its own shows them. At move 1, run the tests and see one fail |
| **A git hook, one move at a time** (`hooks`) | tutorial, its own tags, sync off | A tutorial on one part, on the branch `hooks`. At move hooks-01.2, the hook refuses a broken file. Up and Down page through the slides without making moves |

Also try **Shell** (Alt+Enter), the layouts (Alt+1, Alt+2, Alt+3), the notes (Alt+\\), and **Edit** in the
notes column.

## How the class is made

| Path | What it is |
|---|---|
| `history/build.py` | Builds `repo/`: tagged steps `step-00` to `step-05` on `main`, with small commits for the tutorial before step-02, step-04 and step-05; a branch `parts` with tags `parts-01` and `parts-02`; and a branch `hooks` with tags `hooks-00` to `hooks-02` and small commits between them. The same hashes on every build |
| `toc.toml` | The table of contents: the five walks, the default first |
| `notes.md`, `slides/` | The default walk: its notes, and its manifest with the slide files |
| `walks/NAME/` | Each other walk: `notes.md`, and `slides/slides.toml` with its own slide files |
| `justfile` | The recipes above |
| `tests/` | pytest and Playwright: two windows through every walk, step, move and slide, commands typed into a shell, the checks on broken copies of the class, and the PDF |

**`just setup` starts every step, and it never touches git.** It makes the environment (`uv sync`) and the
artifacts that the step needs: `data/corpus.txt` from step-03, and `build/top.txt` from step-05. Both are ignored by
git, so they stay through every move, and `just setup` makes them again when they are missing. Anything that changes
git, such as installing a hook in the hooks walk, is a recipe of its own, which the notes ask the learner to run.

timewalk's site explains each part, in "Several walks" and "Build a class with several walks".

The tests need Chrome, `git`, `uv` and `just`. Each test builds its own copy of the project in a temporary folder.
