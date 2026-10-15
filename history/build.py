"""Build repo/, the project that the walks in this folder step through, from the commits listed here.

    python3 history/build.py [DEST]        default DEST: repo/ beside this folder; an existing DEST is replaced

The project is `tally`, a small word counter. Its history has what every kind of walk needs:

- tagged steps on main, step-00 to step-06, each an annotated tag whose message is the step's note;
- small commits before step-01, step-02, step-03, step-04 and step-05, for a tutorial. Their subjects start with
  `step-02.1:` and so on, though timewalk names a move by its place: the chmod move of hooks-01 has no subject. The last commit of a step has the plain `step-NN:` subject and the tag. step-03.1 is what
  `uv add --dev ruff` made: its pyproject.toml, and its uv.lock, which is kept in step-03.1-uv.lock;
- two steps of one commit, with no moves: step-00, the first step, and step-06, a step after it that stands on its tag;
- a branch `parts` from step-00 with its own tags, `parts-01` and `parts-02`, for a walk on one part;
- a branch `hooks` from step-01 with its own tags, `hooks-00` to `hooks-02`, and small commits between them, for a
  tutorial on one part: a git hook that checks the code before each commit.
- a branch `release` from step-02 with its own tags, `release-00` to `release-02`, for a tutorial with `loose`. Its
  first move renames a file by a patch. Its second changes the version in pyproject.toml, so the commit's own uv.lock
  is out of date, and its third runs `uv lock` and adds a list of changes. release-02 renames and removes files by
  command, `mv` and `rm`, as a student who never commits must: `git rm` and `git mv` need git's index.
- a branch `extra` from step-06 with its own tags, `extra-00` to `extra-04` and a lettered `extra-03b`, for a tutorial
  with the cases a bigger project meets: `uv add` with a range, a dependency group, `uv remove`, a workspace made by
  `uv init --lib`, a picture changed by a patch, a path with a space, a README with a fenced block, a step of twelve
  moves, a command that writes its files and exits 1, and a `uv add` and a patch on one file in one move. Each file
  that a command writes is what that command wrote, with uv 0.12.13; the uv.lock files are kept in `history/extra/`.

Every author, committer and date is fixed, so the commits get the same hashes on every build.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

RUNNABLE = object()   # in place of a file's text: make the file that is there executable, as chmod +x does
GONE = object()   # in place of a file's text: delete the file, as a rename does to the old path


README = "# tally\n\nCount the words in a text.\n"
# The project starts as `uv init --package --name tally` starts one: a pyproject.toml with an entry point and a
# build system, .python-version, .gitignore and uv.lock. Every command runs through uv, in the project's own .venv.
PYPROJECT = '''[project]
name = "tally"
version = "0.1.0"
description = "Count the words in a text"
readme = "README.md"
requires-python = ">=3.12"
dependencies = []

[project.scripts]
tally = "tally:main"

[build-system]
requires = ["uv_build>=0.12.13,<0.13.0"]
build-backend = "uv_build"
'''
PYTHON_VERSION = "3.12\n"
GITIGNORE = "# Python-generated files\n__pycache__/\n*.py[oc]\nbuild/\ndist/\nwheels/\n*.egg-info\n\n# Virtual environments\n.venv\n"
# The lock of a project with no dependencies: the same on every build.
UV_LOCK = 'version = 1\nrevision = 3\nrequires-python = ">=3.12"\n\n[[package]]\nname = "tally"\nversion = "0.1.0"\nsource = { editable = "." }\n'
JUSTFILE = """# The recipes of tally. Each one runs through uv, in the project's own environment.
default:
    @just --list

# Make the environment of this step: the first command of every step
setup:
    uv sync

# Count the words of a file
run file:
    uv run tally {{ file }}

# Run the tests
test:
    uv run python -m unittest discover -s tests -q
"""
MAIN_0 = '"""tally: count the words in a text."""\n\n\ndef main() -> None:\n    print("tally: nothing to count yet")\n'
DUNDER = "from tally import main\n\nmain()\n"
COUNT_1 = '''"""tally: count the words in a text."""

import sys


def count(text):
    counts = {}
    for word in text.split():
        counts[word] = counts.get(word, 0) + 1
    return counts


def main() -> None:
    text = open(sys.argv[1]).read() if len(sys.argv) > 1 else sys.stdin.read()
    for word, n in sorted(count(text).items()):
        print(n, word)
'''
# step-01.1: the function first, which the command does not use yet
COUNT_0 = COUNT_1.replace("import sys\n\n\n", "\n").replace('''    text = open(sys.argv[1]).read() if len(sys.argv) > 1 else sys.stdin.read()
    for word, n in sorted(count(text).items()):
        print(n, word)
''', '''    print("tally: nothing to count yet")
''')
assert "sys" not in COUNT_0 and "def count" in COUNT_0
COUNT_2 = COUNT_1.replace("for word in text.split():", "for word in text.lower().split():")
TEST_COUNT = '''import unittest

from tally import count


class Count(unittest.TestCase):
    def test_words(self):
        self.assertEqual(count("a b a"), {"a": 2, "b": 1})

    def test_case(self):
        self.assertEqual(count("A a"), {"a": 2})
'''
TEST_EMPTY = '''import unittest

from tally import count


class Empty(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(count(""), {})
'''
# step-03.1: what `uv add --dev ruff` wrote, run with uv 0.12.13 on the project at step-02. uv put ruff in the group dev of
# pyproject.toml, and ruff and its wheels in uv.lock. The lock is kept beside this file, so every build gives the same hashes.
DEV_RUFF = PYPROJECT + '\n[dependency-groups]\ndev = [\n    "ruff>=0.17.0",\n]\n'
UV_LOCK_RUFF = (HERE / "step-03.1-uv.lock").read_text()
assert '\nname = "ruff"\nversion = "0.17.0"\n' in UV_LOCK_RUFF
RUFF = "\n[tool.ruff]\nline-length = 100\n"
# step-03 stages an artifact: data/corpus.txt, a text to count, made by a script and ignored by git. just setup makes it
# when it is missing, so a fresh clone, or a jump to a later step, has it too.
CORPUS = '''"""Write data/corpus.txt, a text of 2000 words to count, the same every time. Leave it alone if it is there."""

import sys
from pathlib import Path

WORDS = "the a word count text tally test step move commit tag note slide class shell file line code".split()


def main() -> None:
    target = Path(sys.argv[1] if len(sys.argv) > 1 else "data/corpus.txt")
    if target.exists():
        print(f"{target} is there")
        return
    seed, words = 7, []
    for _ in range(2000):
        seed = (seed * 1103515245 + 12345) % 2**31
        words.append(WORDS[seed % len(WORDS)])
    target.parent.mkdir(parents=True, exist_ok=True)
    lines = (" ".join(words[i : i + 12]) for i in range(0, len(words), 12))
    target.write_text("\\n".join(lines) + "\\n")
    print(f"wrote {target}: {len(words)} words")


if __name__ == "__main__":
    main()
'''
GITIGNORE_DATA = GITIGNORE + "\n# Artifacts that just setup makes: they are not in git\ndata/\n"
JUSTFILE_DATA = JUSTFILE.replace("setup:\n    uv sync\n", "setup:\n    uv sync\n    uv run python scripts/corpus.py data/corpus.txt\n")
TYPED = COUNT_2.replace("def count(text):", "def count(text: str) -> dict[str, int]:")
# step-04.2: a docstring with a word in backticks, which the notes quote with a show: line in two backticks
DOCS = TYPED.replace("def count(text: str) -> dict[str, int]:\n", 'def count(text: str) -> dict[str, int]:\n    "How many times each word of `text` appears, ignoring case."\n')
TOP = DOCS.replace("\n\ndef main", '''

def top(counts: dict[str, int], n: int) -> list[tuple[str, int]]:
    "The n most common words, most common first."
    return sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))[:n]


def main''')
TOP_CLI = TOP.replace('''def main() -> None:
    text = open(sys.argv[1]).read() if len(sys.argv) > 1 else sys.stdin.read()
    for word, n in sorted(count(text).items()):
        print(n, word)
''', '''def main() -> None:
    "Count the words of a file, or of the standard input. With --top N, only the N most common."
    args, n = sys.argv[1:], None
    if args[:1] == ["--top"]:
        n, args = int(args[1]), args[2:]
    text = open(args[0]).read() if args else sys.stdin.read()
    counts = count(text)
    for word, times in top(counts, n) if n else sorted(counts.items()):
        print(times, word)
''')
TEST_TOP = '''import unittest

from tally import top


class Top(unittest.TestCase):
    def test_most_common_first(self):
        self.assertEqual(top({"a": 1, "b": 3, "c": 2}, 2), [("b", 3), ("c", 2)])
'''
# step-05 makes an artifact of its own, build/top.txt; just setup makes it again when it is missing.
JUSTFILE_REPORT = JUSTFILE_DATA.replace("    uv run python scripts/corpus.py data/corpus.txt\n",
                                        "    uv run python scripts/corpus.py data/corpus.txt\n    test -f build/top.txt || just report\n") + \
    "\n# Write the ten most common words of the corpus to build/top.txt\nreport:\n    mkdir -p build\n    uv run tally --top 10 data/corpus.txt > build/top.txt\n"

# step-06: one commit, with no moves. The README says how to run tally, its tests and its report.
README_RUN = README + """
## Run it

Make the environment, the corpus and the report first. Then count the words of a file:

    just setup
    uv run tally data/corpus.txt

`uv run tally --top 10 data/corpus.txt` prints only the ten most common words. `just test` runs the tests, and
`just report` writes the ten most common words of the corpus to `build/top.txt`.
"""

# (subject, files written, the tag and its note or None)
MAIN = [
    ("step-00: the project, with a command that has nothing to count",
     {"README.md": README, "pyproject.toml": PYPROJECT, ".python-version": PYTHON_VERSION, ".gitignore": GITIGNORE, "uv.lock": UV_LOCK,
      "justfile": JUSTFILE, "src/tally/__init__.py": MAIN_0, "src/tally/__main__.py": DUNDER},
     ("step-00", "Where it starts\n\nA project with a command that does nothing yet.")),
    ("step-01.1: a function that counts", {"src/tally/__init__.py": COUNT_0}, None),
    ("step-01: the command counts the words", {"src/tally/__init__.py": COUNT_1},
     ("step-01", "Counting\n\nThe command counts words, one line per word.")),
    ("step-02.1: a test of counting", {"tests/test_count.py": TEST_COUNT}, None),
    ("step-02.2: a test of an empty text", {"tests/test_empty.py": TEST_EMPTY}, None),
    ("step-02: case does not matter, and the tests pass", {"src/tally/__init__.py": COUNT_2},
     ("step-02", "Tests\n\nTwo tests, one failing, and the fix.")),
    ("step-03.1: ruff, a tool for development, added with uv add --dev ruff", {"pyproject.toml": DEV_RUFF, "uv.lock": UV_LOCK_RUFF}, None),
    ("step-03.2: a line length for ruff", {"pyproject.toml": DEV_RUFF + RUFF}, None),
    ("step-03: a corpus to count, which just setup makes", {"scripts/corpus.py": CORPUS, ".gitignore": GITIGNORE_DATA, "justfile": JUSTFILE_DATA},
     ("step-03", "Formatting, and a corpus\n\nuv adds ruff as a tool for development, ruff gets a line length, and just setup makes data/corpus.txt.")),
    ("step-04.1: types", {"src/tally/__init__.py": TYPED}, None),
    ("step-04: a docstring", {"src/tally/__init__.py": DOCS},
     ("step-04", "Types and docs\n\nThe function says what it takes, returns and does.")),
    ("step-05.1: a function for the most common words, with its test", {"src/tally/__init__.py": TOP, "tests/test_top.py": TEST_TOP}, None),
    ("step-05.2: tally --top N", {"src/tally/__init__.py": TOP_CLI}, None),
    ("step-05: a report of the corpus, which just setup makes", {"justfile": JUSTFILE_REPORT},
     ("step-05", "The most common words\n\nA function, an option, and a report that just setup makes.")),
    ("step-06: the README says how to run tally", {"README.md": README_RUN},
     ("step-06", "How to run it\n\nThe README says how to run tally, its tests and its report.")),
]
# Commits on the branch `parts`, from step-00: only the tests, for a walk on one part.
PARTS = [
    ("parts-01: the counting code, with its test", {"src/tally/__init__.py": COUNT_2, "tests/test_count.py": TEST_COUNT},
     ("parts-01", "Tests first\n\nThe code and its first test.")),
    ("parts-02: a test of an empty text", {"tests/test_empty.py": TEST_EMPTY},
     ("parts-02", "One more test\n\nAn empty text.")),
]

# The branch `hooks`, from step-01: a tutorial on one part, with tags of its own and small commits between them.
CHECK = JUSTFILE + "\n# Check that every Python file compiles\ncheck:\n    uv run python -m py_compile src/tally/*.py\n"
HOOK = "#!/bin/sh\n# Run before each commit: refuse it if the code does not compile.\njust check\n"
# just setup only makes the environment and the artifacts; it never touches git. Installing the hook changes git's
# config, so it is a recipe of its own, run on purpose.
SETUP = CHECK + "\n# Make git run the hooks in hooks/, before each commit. This changes git's config, so it is not part of setup\ninstall-hook:\n    git config core.hooksPath hooks\n"
HOOK_TESTS = HOOK + "uv run python -m unittest discover -s tests -q\n"
HOOKS = [
    ("hooks-01.1: a recipe that checks the code", {"justfile": CHECK}, None),
    ("hooks-01.2: a hook script that runs the check", {"hooks/pre-commit": HOOK}, None),
    ("", {"hooks/pre-commit": RUNNABLE}, None),   # a move of one command, chmod +x, with no subject, as jj new leaves it
    ("hooks-01: a recipe that installs the hook", {"justfile": SETUP},
     ("hooks-01", "The hook\n\nA check before each commit, installed with just install-hook.")),
    ("hooks-02.1: a first test", {"tests/test_count.py": TEST_COUNT.replace("    def test_case(self):\n        self.assertEqual(count(\"A a\"), {\"a\": 2})\n", "")}, None),
    ("hooks-02: the hook runs the tests too", {"hooks/pre-commit": HOOK_TESTS},
     ("hooks-02", "Tests in the hook\n\nA commit with a failing test is refused.")),
]

# The branch `release`, from step-02: a tutorial whose files are compared loosely, as in a class with uv.
# release-01.1 renames tests/test_empty.py by a patch, and adds a test: git finds the rename, as the two files are alike.
TEST_EDGE = TEST_EMPTY.replace("class Empty(", "class Edge(") + '''
    def test_spaces(self):
        self.assertEqual(count("  \\n\\t "), {})
'''
# release-01.2 changes the version, and not uv.lock, which still names 0.1.0: `uv lock --check` fails at that commit.
# release-01 is what `uv lock` then writes, with a list of the changes of the release.
CHANGES = "# Changes\n\n## 0.2.0\n\nThe tests of an empty text are now the tests of edge cases, with a test of a text of spaces.\n"
VERSION_2 = PYPROJECT.replace('version = "0.1.0"', 'version = "0.2.0"')
UV_LOCK_2 = UV_LOCK.replace('version = "0.1.0"', 'version = "0.2.0"')
# release-02.2 adds a test to tests/test_count.py. release-02.3 renames tests/test_edge.py to tests/test_tally.py with `mv`,
# release-02.4 copies the class of tests/test_count.py into it, and release-02 removes tests/test_count.py.
TEST_LINES = TEST_COUNT + '''
    def test_lines(self):
        self.assertEqual(count("a b\\na"), {"a": 2, "b": 1})
'''
TEST_TALLY = TEST_EDGE + "\n\n" + TEST_LINES.split("\n\n\n", 1)[1]
RELEASE = [
    ("release-01.1: the tests of an empty text become the tests of edge cases", {"tests/test_empty.py": GONE, "tests/test_edge.py": TEST_EDGE}, None),
    ("release-01.2: version 0.2.0", {"pyproject.toml": VERSION_2}, None),
    ("release-01: the lock of version 0.2.0, written by uv lock, and the list of changes", {"uv.lock": UV_LOCK_2, "CHANGES.md": CHANGES},
     ("release-01", "Release 0.2.0\n\nThe tests of edge cases get their name, and tally gets a new version and its lock.")),
    # release-02: each file moves or goes by a command, as `mv` and `rm` leave it. The student never commits, so git's index
    # still has the files of release-00: `git rm tests/test_count.py` would fail on the change of release-02.2, and
    # `git mv tests/test_edge.py` on a file that the index does not have.
    ("release-02.1: the justfile gets a hidden name, by mv justfile .justfile", {"justfile": GONE, ".justfile": JUSTFILE}, None),
    ("release-02.2: a test of a text of several lines", {"tests/test_count.py": TEST_LINES}, None),
    ("release-02.3: the tests of edge cases get the name tests/test_tally.py, by mv tests/test_edge.py tests/test_tally.py",
     {"tests/test_edge.py": GONE, "tests/test_tally.py": TEST_EDGE}, None),
    ("release-02.4: the tests of counting go into tests/test_tally.py", {"tests/test_tally.py": TEST_TALLY}, None),
    ("release-02: the old file of tests goes, by rm tests/test_count.py", {"tests/test_count.py": GONE},
     ("release-02", "Tidy the project\n\nThe recipes get a hidden file, and every test goes in one file.")),
]


# The branch `extra`, from step-06: a tutorial with the cases of a bigger project. Each file that a command writes is
# what that command wrote, with uv 0.12.13 and ruff 0.17.0, run at the commit before its move. The uv.lock files are
# kept in history/extra/: to make one again, run the move's command on a clone of repo/ at the commit before the move.
EXTRA_LOCK = {name: (HERE / "extra" / f"{name}-uv.lock").read_text() for name in ("extra-01.1", "extra-01.3", "extra-03.2", "extra-04.2")}
PY_STEP_06 = DEV_RUFF + RUFF
# extra-01.1: uv add "tabulate>=0.9,<0.10". Only 0.9.0 is in that range, so the lock is the same on any day.
PY_TABLE = PY_STEP_06.replace("dependencies = []", 'dependencies = [\n    "tabulate>=0.9,<0.10",\n]')
# extra-01.3: uv add --group docs mdformat, then a line by hand: uv sync installs the group docs too
PY_DOCS = PY_TABLE.replace('dev = [\n    "ruff>=0.17.0",\n]\n', 'dev = [\n    "ruff>=0.17.0",\n]\ndocs = [\n    "mdformat>=1.0.0",\n]\n')
PY_GROUPS = PY_DOCS + '\n[tool.uv]\ndefault-groups = ["dev", "docs"]\n'
# extra-03.1: uv init --lib --author-from none packages/talib adds the member, and leaves uv.lock out of date
PY_WORKSPACE = PY_GROUPS + '\n[tool.uv.workspace]\nmembers = [\n    "packages/talib",\n]\n'
TALIB_PY = '''[project]
name = "talib"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.12"
dependencies = []

[build-system]
requires = ["uv_build>=0.12.13,<0.13.0"]
build-backend = "uv_build"
'''
TALIB_HELLO = 'def hello() -> str:\n    return "Hello from talib!"\n'
# extra-03.2: uv add talib finds the member of the workspace, and gives it a source
PY_TALIB = PY_WORKSPACE.replace('    "tabulate>=0.9,<0.10",\n]', '    "tabulate>=0.9,<0.10",\n    "talib",\n]') + \
    "\n[tool.uv.sources]\ntalib = { workspace = true }\n"
# extra-04.2: uv remove tabulate
PY_NO_TABULATE = PY_TALIB.replace('    "tabulate>=0.9,<0.10",\n', "")

# extra-01.2: tally --table prints the counts as a table, with tabulate
TABLE = TOP_CLI.replace("import sys\n", "import sys\n\nfrom tabulate import tabulate\n").replace('''def main() -> None:
    "Count the words of a file, or of the standard input. With --top N, only the N most common."
    args, n = sys.argv[1:], None
    if args[:1] == ["--top"]:
        n, args = int(args[1]), args[2:]
    text = open(args[0]).read() if args else sys.stdin.read()
    counts = count(text)
    for word, times in top(counts, n) if n else sorted(counts.items()):
        print(times, word)
''', '''def main() -> None:
    "Count the words of a file, or of the standard input. Options: --top N, and --table."
    args = sys.argv[1:]
    as_table = "--table" in args
    args, n = [arg for arg in args if arg != "--table"], None
    if args[:1] == ["--top"]:
        n, args = int(args[1]), args[2:]
    text = open(args[0]).read() if args else sys.stdin.read()
    counts = count(text)
    rows = top(counts, n) if n else sorted(counts.items())
    if as_table:
        print(tabulate(rows, headers=["word", "times"]))
        return
    for word, times in rows:
        print(times, word)
''')
assert "tabulate(rows" in TABLE
# extra-03.3: top goes into the library talib, and tally imports it from there
TALIB_TOP = '''"""talib: small helpers for the counts of words."""


def top(counts: dict[str, int], n: int) -> list[tuple[str, int]]:
    "The n most common words, most common first."
    return sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))[:n]
'''
TOP_FUNCTION = '''def top(counts: dict[str, int], n: int) -> list[tuple[str, int]]:
    "The n most common words, most common first."
    return sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))[:n]


'''
assert TOP_FUNCTION in TABLE
TABLE_TALIB = TABLE.replace(TOP_FUNCTION, "").replace("from tabulate import tabulate\n", "from tabulate import tabulate\nfrom talib import top\n")
# extra-03b.1: uv run ruff check --fix rewrites the list of words of scripts/corpus.py (SIM905), and exits 1 on
# the open() of main, which it cannot fix (SIM115)
CORPUS_FIXED = CORPUS.replace(
    'WORDS = "the a word count text tally test step move commit tag note slide class shell file line code".split()',
    'WORDS = ["the", "a", "word", "count", "text", "tally", "test", "step", "move", "commit", "tag", "note", "slide", '
    '"class", "shell", "file", "line", "code"]')
assert CORPUS_FIXED != CORPUS
# extra-03b.2: main closes the file it opens
OPEN = "    text = open(args[0]).read() if args else sys.stdin.read()\n"
WITH = "    if args:\n        with open(args[0]) as file:\n            text = file.read()\n    else:\n        text = sys.stdin.read()\n"
assert OPEN in TABLE_TALIB
TABLE_WITH = TABLE_TALIB.replace(OPEN, WITH)
# extra-04.1: tally draws the table itself, the same as tabulate drew it
OWN_TABLE = TABLE_WITH.replace("from tabulate import tabulate\n", "").replace("\n\ndef main", '''

def table(rows: list[tuple[str, int]]) -> str:
    "The rows under a header and a rule: the words on the left, the counts on the right."
    left = max([len("word") + 2, *(len(word) for word, _ in rows)])
    right = max([len("times") + 2, *(len(str(times)) for _, times in rows)])
    lines = [f"{'word':<{left}}  {'times':>{right}}", f"{'-' * left}  {'-' * right}"]
    lines += [f"{word:<{left}}  {times:>{right}}" for word, times in rows]
    return "\\n".join(lines)


def main''').replace('print(tabulate(rows, headers=["word", "times"]))', "print(table(rows))")
assert "tabulate" not in OWN_TABLE


def png(width: int, height: int, bars: list[int], colour: tuple[int, int, int]) -> bytes:
    "A picture of bars, as a PNG with stored deflate blocks: the same bytes on every machine, whatever its zlib."
    import struct
    import zlib

    rows = b""
    for y in range(height):
        row = bytearray([0])   # filter: none
        for x in range(width):
            bar, gap = divmod(x, 6)
            up = bar < len(bars) and gap < 5 and height - y <= bars[bar]
            row += bytes(colour if up else (255, 255, 255))
        rows += bytes(row)
    raw = b"\x78\x01"
    for start in range(0, len(rows), 65535):
        block = rows[start : start + 65535]
        last = 1 if start + 65535 >= len(rows) else 0
        raw += bytes([last]) + struct.pack("<HH", len(block), len(block) ^ 0xFFFF) + block
    raw += struct.pack(">I", zlib.adler32(rows))

    def chunk(kind: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))

    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)) + chunk(b"IDAT", raw) + chunk(b"IEND", b"")


# extra-02: the docs, in twelve moves, so that 02.10 to 02.12 come after 02.9
CHART = png(60, 30, [27, 26, 26, 25, 24, 24, 23, 22, 22, 21], (9, 105, 218))
CHART_SORTED = png(60, 30, [27, 26, 26, 25, 24, 24, 23, 22, 22, 21], (26, 127, 55))
HOW = """# How to run tally

tally counts the words of a text file.

## Set up

Run this once, and again after each change of the project:

```sh
just setup
```

## Count the words of a file

```sh
uv run tally data/corpus.txt
```

It prints each word with its count, one word to a line, in the order of the alphabet.
"""
HOW_TOP = HOW + """
## Only the most common words

```sh
uv run tally --top 10 data/corpus.txt
```

It prints the ten most common words, the most common first.
"""
HOW_TABLE = HOW_TOP + """
## A table

```sh
uv run tally --top 10 --table data/corpus.txt
```

It prints the same words as a table, with a header.
"""
HOW_PICTURE = HOW_TABLE.replace("It prints the ten most common words, the most common first.\n",
                                "It prints the ten most common words, the most common first.\n\n"
                                "![The ten most common words of the corpus, as bars](tally.png)\n")
HOW_CHECK = HOW_PICTURE + """
## Check the docs

```sh
just docs
```

It prints nothing when every page of the docs is formatted as mdformat formats it.
"""
README_PYTHON = README_RUN + """
## Count from Python

tally is a library too. `count` counts the words of a text, and `top` keeps the most common:

```python
from tally import count, top

counts = count("the cat and the hat")
print(top(counts, 2))
```

It prints `[('the', 2), ('and', 1)]`.
"""
README_LINK = README_PYTHON + "\nThe page [How to run tally](docs/how%20to%20run.md) says more, with a picture of the most common words.\n"
README_FILE = README_LINK.replace('''```python
from tally import count, top

counts = count("the cat and the hat")
print(top(counts, 2))
```

It prints `[('the', 2), ('and', 1)]`.
''', '''```python
from pathlib import Path

from tally import count, top

counts = count(Path("data/corpus.txt").read_text())
print(top(counts, 3))
```

It prints `[('line', 127), ('class', 126), ('word', 125)]`, the three most common words of the corpus.
''')
assert README_FILE != README_LINK
# extra-02.11: uv run mdformat README.md writes the two indented lines of "Run it" as a fenced block
README_FORMATTED = README_FILE.replace("\n    just setup\n    uv run tally data/corpus.txt\n", "\n```\njust setup\nuv run tally data/corpus.txt\n```\n")
assert README_FORMATTED != README_FILE
JUSTFILE_DOCS = JUSTFILE_REPORT + "\n# Check that the README and the docs are formatted as mdformat formats them\ndocs:\n    uv run mdformat --check README.md docs\n"

EXTRA = [
    ("extra-01.1: tabulate, added with uv add", {"pyproject.toml": PY_TABLE, "uv.lock": EXTRA_LOCK["extra-01.1"]}, None),
    ("extra-01.2: tally --table", {"src/tally/__init__.py": TABLE}, None),
    ("extra-01: mdformat in the group docs, which uv sync installs", {"pyproject.toml": PY_GROUPS, "uv.lock": EXTRA_LOCK["extra-01.3"]},
     ("extra-01", "A table, and a tool for the docs\n\ntally prints a table with tabulate, and mdformat comes in a group of its own.")),
    ("extra-02.1: a page on how to run tally", {"docs/how to run.md": HOW}, None),
    ("extra-02.2: the most common words", {"docs/how to run.md": HOW_TOP}, None),
    ("extra-02.3: the table", {"docs/how to run.md": HOW_TABLE}, None),
    ("extra-02.4: a picture of the most common words", {"docs/tally.png": CHART}, None),
    ("extra-02.5: the page shows the picture", {"docs/how to run.md": HOW_PICTURE}, None),
    ("extra-02.6: the README counts from Python", {"README.md": README_PYTHON}, None),
    ("extra-02.7: the README links to the page", {"README.md": README_LINK}, None),
    ("extra-02.8: the picture in green", {"docs/tally.png": CHART_SORTED}, None),
    ("extra-02.9: the README counts a file", {"README.md": README_FILE}, None),
    ("extra-02.10: a recipe that checks the docs", {"justfile": JUSTFILE_DOCS}, None),
    ("extra-02.11: the README as mdformat formats it, by uv run mdformat README.md", {"README.md": README_FORMATTED}, None),
    ("extra-02: the page says how to check the docs", {"docs/how to run.md": HOW_CHECK},
     ("extra-02", "The docs\n\nA page on how to run tally, with a picture, and a README that counts from Python.")),
    ("extra-03.1: a library talib, made with uv init --lib",
     {"pyproject.toml": PY_WORKSPACE, "packages/talib/pyproject.toml": TALIB_PY, "packages/talib/README.md": "",
      "packages/talib/src/talib/__init__.py": TALIB_HELLO, "packages/talib/src/talib/py.typed": ""}, None),
    ("extra-03.2: tally depends on talib, added with uv add", {"pyproject.toml": PY_TALIB, "uv.lock": EXTRA_LOCK["extra-03.2"]}, None),
    ("extra-03: top goes into talib", {"packages/talib/src/talib/__init__.py": TALIB_TOP, "src/tally/__init__.py": TABLE_TALIB},
     ("extra-03", "A library\n\nA second package in the workspace, talib, holds top, and tally depends on it.")),
    ("extra-03b.1: what ruff check --fix fixes", {"scripts/corpus.py": CORPUS_FIXED}, None),
    ("extra-03b: main closes its file", {"src/tally/__init__.py": TABLE_WITH},
     ("extra-03b", "Lint\n\nruff fixes what it can, and we fix the rest by hand.")),
    ("extra-04.1: tally draws its own table", {"src/tally/__init__.py": OWN_TABLE}, None),
    ("extra-04: tabulate goes, with uv remove", {"pyproject.toml": PY_NO_TABULATE, "uv.lock": EXTRA_LOCK["extra-04.2"]},
     ("extra-04", "One dependency less\n\ntally draws its table itself, and uv remove takes tabulate out.")),
]


def git(dest: Path, *args: str, when: int = 0) -> str:
    "Run git in dest with a fixed author, committer and date."
    stamp = f"2026-01-01T{10 + when // 60:02d}:{when % 60:02d}:00+00:00"
    env = {**os.environ, "GIT_AUTHOR_NAME": "timewalk-test", "GIT_AUTHOR_EMAIL": "test@example.com", "GIT_COMMITTER_NAME": "timewalk-test",
           "GIT_COMMITTER_EMAIL": "test@example.com", "GIT_AUTHOR_DATE": stamp, "GIT_COMMITTER_DATE": stamp, "GIT_CONFIG_GLOBAL": "/dev/null"}
    return subprocess.run(["git", "-C", str(dest), *args], check=True, capture_output=True, text=True, env=env).stdout


def commit_all(dest: Path, commits: list, clock: int) -> int:
    "Write and commit each entry, tagging where asked. Returns the clock after the last commit."
    for subject, files, tag in commits:
        for name, text in files.items():
            path = dest / name
            path.parent.mkdir(parents=True, exist_ok=True)
            if text is RUNNABLE:
                path.chmod(0o755)  # git runs a hook only if it can execute it
                continue
            if text is GONE:
                path.unlink()
                continue
            if isinstance(text, bytes):
                path.write_bytes(text)   # a binary file, such as a picture
                continue
            path.write_text(text)   # a file that exists keeps its mode
        git(dest, "add", "-A", when=clock)
        git(dest, "commit", "-q", "--allow-empty-message", "-m", subject, when=clock)
        if tag:
            git(dest, "tag", "-a", tag[0], "-m", tag[1], when=clock)
        clock += 1
    return clock


def build(dest: Path) -> None:
    "Make the repository at dest, replacing what is there, and the replay copy that timewalk made of the old one."
    replay = dest.parent / f"{dest.name}-replay"
    link = replay / ".git"
    # The replay copy is a worktree of the repository replaced here: without it, timewalk would refuse the folder.
    # Only a worktree of dest is removed, never another folder of that name.
    if link.is_file() and link.read_text().strip() == f"gitdir: {dest / '.git' / 'worktrees' / replay.name}":
        shutil.rmtree(replay)
    # Since timewalk 1.1, the replay copy is a clone whose remote "home" is dest. It too belongs to the old history.
    config = replay / ".git" / "config"
    if config.is_file() and f"url = {dest}\n" in config.read_text():
        shutil.rmtree(replay)
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    git(dest, "init", "-q", "-b", "main")
    clock = commit_all(dest, MAIN, 0)
    git(dest, "switch", "-q", "-c", "parts", "step-00")
    clock = commit_all(dest, PARTS, clock)
    git(dest, "switch", "-q", "-c", "hooks", "step-01")
    git(dest, "tag", "-a", "hooks-00", "-m", "Where the hooks start\n\ntally counts words, and nothing checks it.", when=clock)
    clock = commit_all(dest, HOOKS, clock + 1)
    git(dest, "switch", "-q", "-c", "release", "step-02")
    git(dest, "tag", "-a", "release-00", "-m", "Where the release starts\n\ntally counts words, and has two files of tests.", when=clock)
    clock = commit_all(dest, RELEASE, clock + 1)
    git(dest, "switch", "-q", "-c", "extra", "step-06")
    git(dest, "tag", "-a", "extra-00", "-m", "Where it starts\n\ntally counts words, has tests, and writes a report.", when=clock)
    commit_all(dest, EXTRA, clock + 1)
    git(dest, "switch", "-q", "main")


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE.parent / "repo"
    build(target.resolve())
    print(f"build: {target} has {len(MAIN)} commits on main, {len(PARTS)} on parts, {len(HOOKS)} on hooks, {len(RELEASE)} on release"
          f" and {len(EXTRA)} on extra")
