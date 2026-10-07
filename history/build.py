"""Build repo/, the project that the walks in this folder step through, from the commits listed here.

    python3 history/build.py [DEST]        default DEST: repo/ beside this folder; an existing DEST is replaced

The project is `tally`, a small word counter. Its history has what every kind of walk needs:

- tagged steps on main, step-00 to step-05, each an annotated tag whose message is the step's note;
- small commits between step-01 and step-02, and between step-03 and step-04, for a tutorial. Their subjects
  start with `step-02.1:` and so on. The last commit of a step has the plain `step-NN:` subject and the tag;
- a branch `parts` from step-00 with its own tags, `parts-01` and `parts-02`, for a walk on one part.

Every author, committer and date is fixed, so the commits get the same hashes on every build.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

README = "# tally\n\nCount the words in a text.\n"
PYPROJECT = '[project]\nname = "tally"\nversion = "0.1.0"\nrequires-python = ">=3.11"\n'
JUSTFILE = "# The recipes of tally\ndefault:\n    @just --list\n\n# Count the words of a file\nrun file:\n    python3 -m tally {{ file }}\n\n# Run the tests\ntest:\n    python3 -m unittest discover -s tests -q\n"
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
TYPED = COUNT_2.replace("def count(text):", "def count(text: str) -> dict[str, int]:")
DOCS = TYPED.replace("def count(text: str) -> dict[str, int]:\n", 'def count(text: str) -> dict[str, int]:\n    "How many times each word appears, ignoring case."\n')
TOP = DOCS.replace("\n\ndef main", '''

def top(counts: dict[str, int], n: int) -> list[tuple[str, int]]:
    "The n most common words, most common first."
    return sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))[:n]


def main''')

# (subject, files written, the tag and its note or None)
MAIN = [
    ("step-00: the project, with a command that has nothing to count",
     {"README.md": README, "pyproject.toml": PYPROJECT, "justfile": JUSTFILE, "src/tally/__init__.py": MAIN_0, "src/tally/__main__.py": DUNDER},
     ("step-00", "Where it starts\n\nA project with a command that does nothing yet.")),
    ("step-01: count the words", {"src/tally/__init__.py": COUNT_1},
     ("step-01", "Counting\n\nThe command counts words, one line per word.")),
    ("step-02.1: a test of counting", {"tests/test_count.py": TEST_COUNT}, None),
    ("step-02.2: a test of an empty text", {"tests/test_empty.py": TEST_EMPTY}, None),
    ("step-02: case does not matter, and the tests pass", {"src/tally/__init__.py": COUNT_2},
     ("step-02", "Tests\n\nTwo tests, one failing, and the fix.")),
    ("step-03: a line length for ruff", {"pyproject.toml": PYPROJECT + RUFF},
     ("step-03", "Formatting\n\nruff gets a line length.")),
    ("step-04.1: types", {"src/tally/__init__.py": TYPED}, None),
    ("step-04: a docstring", {"src/tally/__init__.py": DOCS},
     ("step-04", "Types and docs\n\nThe function says what it takes, returns and does.")),
    ("step-05: the most common words", {"src/tally/__init__.py": TOP},
     ("step-05", "More\n\nA function for the most common words.")),
]
# Commits on the branch `parts`, from step-00: only the tests, for a walk on one part.
PARTS = [
    ("parts-01: the counting code, with its test", {"src/tally/__init__.py": COUNT_2, "tests/test_count.py": TEST_COUNT},
     ("parts-01", "Tests first\n\nThe code and its first test.")),
    ("parts-02: a test of an empty text", {"tests/test_empty.py": TEST_EMPTY},
     ("parts-02", "One more test\n\nAn empty text.")),
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
        git(dest, "add", "-A", when=clock)
        git(dest, "commit", "-q", "-m", subject, when=clock)
        if tag:
            git(dest, "tag", "-a", tag[0], "-m", tag[1], when=clock)
        clock += 1
    return clock


def build(dest: Path) -> None:
    "Make the repository at dest, replacing what is there."
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    git(dest, "init", "-q", "-b", "main")
    clock = commit_all(dest, MAIN, 0)
    git(dest, "switch", "-q", "-c", "parts", "step-00")
    commit_all(dest, PARTS, clock)
    git(dest, "switch", "-q", "main")


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE.parent / "repo"
    build(target.resolve())
    print(f"build: {target} has {len(MAIN)} commits on main and {len(PARTS)} on parts")
