# timewalk-test

The integration test of [timewalk](https://github.com/rahuldave/timewalk), and a class kit that shows every
feature of it. A class folder with eleven walks steps through `tally`, a small word counter, whose history
`history/build.py` builds into `repo/`. The tests drive the page in two windows, the way a class uses it.

```
just present            # open the walks in a browser, starting on the default walk
just present tutorial   # start on another walk: narrative, tests, parts, story, tutorial, hooks, small, testing, finish, release or extra
just check              # check the notes and slides of every walk against the steps, then the pages that students read
just pdf hooks          # the PDF of one walk's slides, in build/
just build              # build repo/ again, and start again from the first step
just pages              # render the pages that students read, for every walk, into pages/
just site               # build the website of pages/ into _site/, and serve it at http://127.0.0.1:8000
just style              # check the README, notes and slides by walk-kit's writing guide; --all reviews each file whole
just follow             # follow every Build it yourself page and part page in a scratch clone, as a student would
just test               # build a fresh copy, then run every test
just publish            # push repo/ to github.com/rahuldave/tally, every branch and tag
just walk-init          # make ../tally-walk, the repository that students fork, with walk-kit
just walk-update        # write the notes, slides and pages of every walk into ../tally-walk
```

timewalk-test is a whole class, as a class made with walk-kit is. Its project, tally, is on GitHub at
rahuldave/tally, and its walk repository is tally-walk, beside this folder and at rahuldave/tally-walk. Each change to
walk-kit is tried here first. `just walk-update` writes tally-walk again, and walk-kit's follow.py follows each of its
pages. Then a push of tally-walk runs its Pages workflow, which publishes its site.

timewalk-test also tests the pages that students read. The `walk` skill, in walk-kit, makes these pages from the facts
of each walk. `just pages` writes them into `pages/`, one folder for each walk, and you can commit them. A tutorial also
gets a Build it yourself page, with every command to run.

The recipes `check`, `style` and `follow` are the recipes of a class made with walk-kit. So when timewalk-test runs
them, it tests the recipes that classes use. `just check` runs `timewalk-check`, and then walk-kit's
`render.py --class`, which checks the pages of every walk. `just style` runs walk-kit's `style.py` on the README, the
notes and the slides. `just follow` renders the pages into `build/pages`, and follows each Build it yourself page and
each part page of the websites.

`just test -k pages` makes the pages again in a temporary folder. Then it runs each Build it yourself page in a fresh
copy of the project, and every check on the page must pass. It also follows each part page of the websites, checks
each page to read with walk-kit's `read_check.py`, and runs `render.py --class`. With `TIMEWALK_TEST_GITHUB=1`, it also
runs walk-kit's `just test-github`, which follows the pages of tally-walk on GitHub.

The website of the pages is at https://rahuldave.com/timewalk-test/, with one site for each walk. GitHub publishes
it on each push to `main` that changes `pages/`. `just site` builds the same website on your computer.

To check the pages of every walk without writing them, run this in the class folder:

```
TIMEWALK=~/Projects/timewalk python3 ~/Projects/walk-kit/scripts/render.py --class . --repo repo --github https://github.com/o/tally
```

It must report 0 problems and 0 warnings for every walk. It reports a file that the do mode does not give in full.
It also reports the words of timewalk, such as "step", "move" and "commit", in the text that a reader reads.

`pyproject.toml` takes timewalk from its `main` branch on GitHub. To use a working copy of timewalk instead,
put `TIMEWALK_LOCAL=~/Projects/timewalk` before any recipe.

## A tour

Run `just present`. Open two windows, yours and the **Room** window that its button opens. Change the
walk with the menu at the left of the step bar.

| Walk | Kind | Try this |
|---|---|---|
| **tally, step by step** (`narrative`) | narrative, every step | Right and Left through the seven steps. The notes use every kind of line: `time:` for the clock band, `>` cues, and commands for **At this step**, **Runs**, **Runs 2** and **Main**. step-01 has a picture slide. step-03 shows a whole document, and its command makes an edit: open `src/tally/__init__.py` and choose **Your edits**. The recipe buttons above the terminal come from the project's justfile |
| **Only the tests** (`tests`) | narrative, some steps | Three of the seven steps, with slides borrowed from the default walk's folder |
| **Tests first, on the parts branch** (`parts`) | narrative, its own tags | Steps `parts-01` and `parts-02`, on another branch. The replay copy moves to that branch |
| **tally, one move at a time** (`tutorial`) | tutorial | The band under the step bar says what to do. At step-01, make the first move by hand and press Done, or press Shift+Right. Each move is one small commit: the notes gray the moves still to come, `files:` opens what the move changed, and a move with slides of its own shows them. When every move is made, **Next step** ends the notes. At step-02.1, run the tests and see one fail. At step-03.1, run `uv add --dev ruff`: your files match even with a newer ruff. Switch to **Watch** to see "The move ran:" in its place |
| **How tally counts, in three stops** (`story`) | narrative, some moves and a step | A small walk taken out of the tutorial with `select`. Its first stop says what the walk leaves out, under "About this walk" |
| **Two parts of tally, one move at a time** (`small`) | tutorial, some moves | A small tutorial taken out of the big one. Its first part is a range of moves with a title. "About this walk" names the moves that it leaves out between its parts |
| **The tests of tally, with notes of its own** (`testing`) | tutorial, some moves, notes of its own | A small tutorial with its own notes, `walks/testing/notes.md`. Its `{{include ...}}` lines take the move sections from the tutorial's notes. Each stop runs `$ just setup`, and has its own words between and after the moves: what the walk leaves out, and what the moves did |
| **Types, then the report, with notes of its own** (`finish`) | tutorial, a step and a move, notes of its own | A stop with a whole step, `{{include step-04}}`, which brings the step's `$ just setup` with it, then a stop of one move after a gap, `{{include step-05.3}}`. Its own text has a block for each mode |
| **A git hook, one move at a time** (`hooks`) | tutorial, its own tags, sync off | A tutorial on one part, on the branch `hooks`. At move hooks-01.3, the hook refuses a broken file. Up and Down page through the slides without making moves |
| **A release of tally, one move at a time** (`release`) | tutorial, its own tags, `loose` | A tutorial on the branch `release`. Move release-01.1 renames a file by a patch. Move release-01.2 changes the version in `pyproject.toml`, so its own `uv.lock` is out of date until release-01.3 runs `uv lock`. Its Build it yourself page sets the version with a command, and `git check` compares `uv.lock` by the names of its packages, so release-01.2 passes. In release-02, `mv` and `rm` rename and remove files, as a student who never commits must |
| **A bigger tally, one move at a time** (`extra`) | tutorial, its own tags, `loose` | A tutorial on the branch `extra`, with the cases of a bigger project. extra-01.1 runs `uv add` with a range of versions, and extra-01.3 adds a group `docs`, then a patch on the same `pyproject.toml`. extra-02 has twelve moves, so 02.10 to 02.12 come after 02.9: a page `docs/how to run.md`, with a space in its path, a picture `docs/tally.png` changed by a patch, and a README with a fenced block. extra-03 makes a library in the workspace with `uv init --lib`. In the lettered extra-03b, `uv run ruff check --fix` writes its fix and exits 1. extra-04 ends with `uv remove` |

### An example of each feature

| Feature | Where |
|---|---|
| A block for one mode, `::: do` and `::: watch` | Every move of the tutorial. step-05.2 has one block for each mode, then one important command that both modes run |
| Several minor commands in one `do` block, then a shared check | step-02.1: `mkdir -p tests` and a first test run, then the tests |
| Shared commands, the same in both modes | step-05.3 |
| A `do$` line, a command that makes the move | step-03.1, `do$ uv add --dev ruff`, and hooks-01.3, `do$ chmod +x hooks/pre-commit`, a move with no subject |
| `loose`, files that match by the names of their packages | The tutorial in `toc.toml`, for the `pyproject.toml` and `uv.lock` of step-03.1 |
| A rename by a patch, with `patch$` lines for the old path and the new | release-01.1, in `walks/release/notes.md` |
| A move whose commit has a `uv.lock` that is out of date | release-01.2. The next move, release-01.3, runs `do$ uv lock` |
| `uv add` with a range of versions, a dependency group, and `uv remove` | extra-01.1 `do$ uv add "tabulate>=0.9,<0.10"`, extra-01.3 `do$ uv add --group docs mdformat`, extra-04.2 `do$ uv remove tabulate`, in `walks/extra/notes.md` |
| A `do$` line and a `patch$` line on one file in one move | extra-01.3: `uv add`, then a line by hand in `pyproject.toml` |
| A workspace, made by `uv init --lib`, with `loose` on the library's `pyproject.toml` | extra-03.1 to extra-03.3. The patch of extra-03.3 changes both packages |
| A binary file, made and changed by a patch | extra-02.4 and extra-02.8, `docs/tally.png`. Build it yourself takes it with `git restore` |
| A path with a space, in a `patch$` line in backticks | extra-02.1, ``patch$ `docs/how to run.md` `` |
| A README with a fenced block, changed by a patch and by a command | extra-02.6 and extra-02.9, then extra-02.11 `do$ uv run mdformat README.md` |
| A step of more than nine moves | extra-02, with twelve |
| A `do$` line that writes its files and exits 1 | extra-03b.1, `do$ uv run ruff check --fix`. `timewalk-check` warns of it |
| A lettered step, between two numbered ones | extra-03b, with two moves |
| A cue right before a fenced block with two blank lines in it, and notes that end with a blank line | extra-03.3, in `walks/extra/notes.md` |
| A rename and a removal by command, `do$ mv` and `do$ rm`, and never `git mv` or `git rm`, which fail for a student who never commits | release-02.1 renames a file that the walk never changed. release-02.3 renames a file that release-01.1 made, and release-02.4 patches it. release-02.5 removes a file that release-02.2 changed |
| A `show:` line in two backticks, for a line with a backtick in it | step-04.2, which quotes the docstring of `count` |
| `select`, with a range of moves and a title | The walk `small` in `toc.toml` |
| `intro`, the text under "About this walk" | `walks/small/intro.md`, with a cue that the Room hides, and `walks/story/intro.md` |
| Notes of its own, with `shared` and `{{include ...}}` lines | The walks `testing` and `finish` in `toc.toml`, and `walks/testing/notes.md` and `walks/finish/notes.md`. The text before the first `##` is the intro, with a cue in `testing` that the Room hides |
| An include of moves, of a range of moves, and of a whole step | `testing`: `step-02.1`, then `step-02.2..step-02.3`. `finish`: `step-04` |
| Blocks for one mode in a walk's own text | The second stop of `finish` |
| A step of one commit, without moves, after the first step | step-06. It stands on its tag, and step-05 ends with **Next step: step-06** |
| A document in place of slides | step-03 of the default walk, `slides/formatting.md` |
| A `patch$` line for each file that a move changes by hand, in the shared text: **Apply patch** in do mode, a pointer to the diff in watch mode | Every move of the tutorials, for example step-03.3, with three |
| A move of one command on a file of a patch, with no subject | hooks-01.3, `do$ chmod +x hooks/pre-commit` after hooks-01.2 brings the file in |
| The checks of a move, under "Check it" | The last shared commands of every move, for example `$ uv run python -m unittest discover -s tests -q` |
| The text of a step before its first move, under the step's title | The text of each step of the tutorial, after `$ just setup` |
| `files:` last, with an item and words for every file | Every move of every tutorial, `uv.lock` too at step-03.1 |

Also try **Shell** (Alt+Enter), the layouts (Alt+1, Alt+2, Alt+3), the notes (Alt+\\), and **Edit** in the
notes column.

## How the class is made

| Path | What it is |
|---|---|
| `history/build.py` | Builds `repo/`: tagged steps `step-00` to `step-06` on `main`, with small commits for the tutorial before step-01, step-02, step-03, step-04 and step-05, and none before step-06; a branch `parts` with tags `parts-01` and `parts-02`; a branch `hooks` with tags `hooks-00` to `hooks-02` and small commits between them; a branch `release` with tags `release-00` to `release-02`; and a branch `extra` from step-06 with tags `extra-00` to `extra-04` and a lettered `extra-03b`. The same hashes on every build |
| `history/step-03.1-uv.lock` | The `uv.lock` that `uv add --dev ruff` wrote at step-03.1, with uv 0.12.13 on the project at step-02. `build.py` reads it, so every build gives the same hashes |
| `history/extra/` | The `uv.lock` that each `uv add` or `uv remove` of the walk `extra` wrote, with uv 0.12.13 at the commit before its move. `build.py` reads them |
| `toc.toml` | The table of contents: the eleven walks, the default first. Each has a `description`, which the band shows at the walk's first step |
| `notes.md`, `slides/` | The default walk: its notes, and its manifest with the slide files |
| `walks/NAME/` | Each other walk: `notes.md`, and `slides/slides.toml` with its own slide files. The small walks `small` and `story` have only an `intro.md`, and read the notes and slides of the tutorial. The small walks `testing` and `finish` have only a `notes.md` of their own, and read the move sections and the slides of the tutorial |
| `pages/ID/` | The pages of each walk, from `just pages`: `read.md`, `build.md` for a tutorial, and the website in `site/` |
| `justfile` | The recipes above |
| `tests/` | pytest and Playwright: two windows through every walk, step, move and slide, commands typed into a shell, the checks on broken copies of the class, and the PDF. `tests/test_facts.py` checks the facts that `timewalk-export --json` writes, for a tutorial, a narrative, the small walks with `select` and with notes of their own, and a narrative that stops at moves, against timewalk's `facts.schema.json`. `tests/test_pages.py` renders the pages of every walk, follows each Build it yourself page and part page, checks each page to read, and runs `render.py --class` |

**`just setup` starts every step, and it never touches git.** It makes the environment (`uv sync`) and the
artifacts that the step needs. The artifacts are `data/corpus.txt` from step-03, and `build/top.txt` from step-05.
git ignores both, so they stay through every move. `just setup` makes them again when they are missing.

Anything that changes git, such as installing a hook in the hooks walk, is a recipe of its own. The notes ask the
learner to run it.

## How the notes are written

Real classes copy these notes, so they keep the rules of timewalk's "What a narrative and a tutorial need":

- **The reader never meets timewalk's words.** The text says no "step", "move", "commit" or "Start". The heading
  `### step-02.1 Title` keeps its name for timewalk, and only its title is for the reader. A cue, `> Say:` or
  `> Note:`, is for the presenter alone, and can say anything.
- **A step opens with what we build, and why.** A move opens with the problem, and the change that solves it.
- **Then the change, piece by piece.** Each file of a move comes from a `do$` line, the command that writes it, or a
  `patch$` line, the diff of the move's commit. The notes copy no code. A `do` block says where the patch goes, and a
  `watch` block says what the change does, and where to see it.
- **A move does one thing,** a patch or a command. A command on a file that a patch brings in gets a move of its own.
- **Then the check,** with what it prints. The page shows it under "Check it".
- **Last, `files:`,** with an item and words for every file of the change. No list of the files in the text.

timewalk's site explains each part, in "Several walks" and "Build a class with several walks".

The tests need Chrome, `git`, `uv` and `just`. Each test builds its own copy of the project in a temporary folder.
