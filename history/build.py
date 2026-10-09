"""Build repo/, the project that the walks in this folder step through, from the commits listed here.

    python3 history/build.py [DEST]        default DEST: repo/ beside this folder; an existing DEST is replaced

The project is `tally`, a small word counter. Its history has what every kind of walk needs:

- tagged steps on main, step-00 to step-05, each an annotated tag whose message is the step's note;
- small commits before step-01, step-02, step-04 and step-05, for a tutorial; step-00 and step-03 have none. Their subjects
  start with `step-02.1:` and so on. The last commit of a step has the plain `step-NN:` subject and the tag;
- a branch `parts` from step-00 with its own tags, `parts-01` and `parts-02`, for a walk on one part;
- a branch `hooks` from step-01 with its own tags, `hooks-00` to `hooks-02`, and small commits between them, for a
  tutorial on one part: a git hook that checks the code before each commit.

Every author, committer and date is fixed, so the commits get the same hashes on every build.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

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
    target.write_text("\\n".join(" ".join(words[i:i + 12]) for i in range(0, len(words), 12)) + "\\n")
    print(f"wrote {target}: {len(words)} words")


if __name__ == "__main__":
    main()
'''
GITIGNORE_DATA = GITIGNORE + "\n# Artifacts that just setup makes: they are not in git\ndata/\n"
JUSTFILE_DATA = JUSTFILE.replace("setup:\n    uv sync\n", "setup:\n    uv sync\n    uv run python scripts/corpus.py data/corpus.txt\n")
TYPED = COUNT_2.replace("def count(text):", "def count(text: str) -> dict[str, int]:")
DOCS = TYPED.replace("def count(text: str) -> dict[str, int]:\n", 'def count(text: str) -> dict[str, int]:\n    "How many times each word appears, ignoring case."\n')
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
    ("step-03: a line length for ruff, and a corpus to count", {"pyproject.toml": PYPROJECT + RUFF, "scripts/corpus.py": CORPUS,
                                                             ".gitignore": GITIGNORE_DATA, "justfile": JUSTFILE_DATA},
     ("step-03", "Formatting, and a corpus\n\nruff gets a line length, and just setup makes data/corpus.txt.")),
    ("step-04.1: types", {"src/tally/__init__.py": TYPED}, None),
    ("step-04: a docstring", {"src/tally/__init__.py": DOCS},
     ("step-04", "Types and docs\n\nThe function says what it takes, returns and does.")),
    ("step-05.1: a function for the most common words, with its test", {"src/tally/__init__.py": TOP, "tests/test_top.py": TEST_TOP}, None),
    ("step-05.2: tally --top N", {"src/tally/__init__.py": TOP_CLI}, None),
    ("step-05: a report of the corpus, which just setup makes", {"justfile": JUSTFILE_REPORT},
     ("step-05", "The most common words\n\nA function, an option, and a report that just setup makes.")),
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
    ("hooks-01: a recipe that installs the hook", {"justfile": SETUP},
     ("hooks-01", "The hook\n\nA check before each commit, installed with just install-hook.")),
    ("hooks-02.1: a first test", {"tests/test_count.py": TEST_COUNT.replace("    def test_case(self):\n        self.assertEqual(count(\"A a\"), {\"a\": 2})\n", "")}, None),
    ("hooks-02: the hook runs the tests too", {"hooks/pre-commit": HOOK_TESTS},
     ("hooks-02", "Tests in the hook\n\nA commit with a failing test is refused.")),
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
            path.write_text(text)
            if name.startswith("hooks/"):
                path.chmod(0o755)  # git runs a hook only if it can execute it
        git(dest, "add", "-A", when=clock)
        git(dest, "commit", "-q", "-m", subject, when=clock)
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
    commit_all(dest, HOOKS, clock + 1)
    git(dest, "switch", "-q", "main")


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE.parent / "repo"
    build(target.resolve())
    print(f"build: {target} has {len(MAIN)} commits on main, {len(PARTS)} on parts and {len(HOOKS)} on hooks")
