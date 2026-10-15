<!-- Made by the walk skill's render.py from the facts of the walk. Do not edit it by hand: run just walk-update again. -->

# A release of tally, one move at a time

**Build it yourself.** Every command to run and every change to make by hand, to make the project yourself. [Read the tutorial](read.md) is the other way to read it.

Each part ends with a section called **What changed**. It lists every file that the part changes, with a link to the file, and then the whole diff of each file, folded. A lockfile and a binary file have a link alone. The text above it explains the change. What changed is what you check your files against.

In Build it yourself, a file that a command makes says which command. A diff that is open is a patch. Apply it with the command in the text, or make the same change in your editor.

tally counts words, and has two files of tests. We make a release, version 0.2.0. First the tests of an empty text
get a name that fits more cases. Then tally gets its new version, and last the lockfile records it.

We make the release in moves. A move is one small change, made by one patch or by one command. You make each move,
and the page checks your files against it.

## Get the project

You build the project in a clone of your own, on a branch `mine` that starts where this walk starts. Run the commands of these pages in its top folder.

```bash
git clone https://github.com/rahuldave/tally
cd tally
git switch -c mine bfcbe07463b5
```

Then add the command `git check`, which compares your files with the project's after each move, and leaves what `git add` has staged as it was. It compares `pyproject.toml` by the names of its packages, so another version of a package does not count as a difference. It does not compare the lines of `uv.lock`. It checks that you and the project both have a `uv.lock`, or both have none. It also checks that your `uv.lock` is up to date with your `pyproject.toml`. Where the project's own `uv.lock` is not, the page gives `git check` the option `--stale-lock`, which leaves out that check.

```bash
echo '/pyproject.toml diff=names' >> .git/info/attributes
git config diff.names.textconv "sed -E 's/^([[:space:]]*\"[A-Za-z0-9_.-]+(\\[[^]]*\\])?)[^\";]*/\\1/'"
git config alias.check '!f() { i="$(git rev-parse --git-path check-index)" && { cp "$(git rev-parse --git-path index)" "$i" 2>/dev/null || rm -f "$i"; } && export GIT_INDEX_FILE="$i" && git add -A && git diff --cached "$1" -- ":/" ":(top,exclude,glob)uv.lock" && git diff --cached --name-status --diff-filter=AD "$1" -- ":(top,glob)uv.lock" && { [ "$2" = --stale-lock ] || [ ! -f uv.lock ] || uv lock --check -q; }; }; f'
```

<a id="release-00"></a>

## 0 Where the release starts

```bash
just setup
```

tally counts the words of a text, and two files of tests check it. Run the tests, to see where we begin.

```bash
uv run python -m unittest discover -s tests -q
```

All three tests pass.

Check your files against this part. The command prints nothing when they match, and otherwise shows what differs:

```bash
git check bfcbe07463b5
```

If you are stuck, this command puts the files of this part in place of yours. A file that you made yourself stays:

```bash
git rm -rq --cached --ignore-unmatch -- :/ && git restore --source bfcbe07463b5 --staged --worktree -- :/
```

### What changed

- <a id="release-00-.gitignore-a5cc29"></a>`.gitignore`: New, 10 lines. [The file](https://github.com/rahuldave/tally/blob/bfcbe07463b5c6f3c0764e4ac19a054cb0acee20/.gitignore).
- <a id="release-00-.python-version-7696e9"></a>`.python-version`: New, 1 line. [The file](https://github.com/rahuldave/tally/blob/bfcbe07463b5c6f3c0764e4ac19a054cb0acee20/.python-version).
- <a id="release-00-README.md-8ec9a0"></a>`README.md`: New, 3 lines. [The file](https://github.com/rahuldave/tally/blob/bfcbe07463b5c6f3c0764e4ac19a054cb0acee20/README.md).
- <a id="release-00-justfile-424f0b"></a>`justfile`: adds `recipe default`, `recipe run`, `recipe setup`, `recipe test`. New, 15 lines. [The file](https://github.com/rahuldave/tally/blob/bfcbe07463b5c6f3c0764e4ac19a054cb0acee20/justfile).
- <a id="release-00-pyproject.toml-5d07e7"></a>`pyproject.toml`: New, 14 lines. [The file](https://github.com/rahuldave/tally/blob/bfcbe07463b5c6f3c0764e4ac19a054cb0acee20/pyproject.toml).
- <a id="release-00-src-tally-__init__.py-b5485b"></a>`src/tally/__init__.py`: adds `count`, `main`. New, 16 lines. [The file](https://github.com/rahuldave/tally/blob/bfcbe07463b5c6f3c0764e4ac19a054cb0acee20/src/tally/__init__.py).
- <a id="release-00-src-tally-__main__.py-534c24"></a>`src/tally/__main__.py`: New, 3 lines. [The file](https://github.com/rahuldave/tally/blob/bfcbe07463b5c6f3c0764e4ac19a054cb0acee20/src/tally/__main__.py).
- <a id="release-00-tests-test_count.py-e674f6"></a>`tests/test_count.py`: adds `class Count`, `test_case`, `test_words`. New, 11 lines. [The file](https://github.com/rahuldave/tally/blob/bfcbe07463b5c6f3c0764e4ac19a054cb0acee20/tests/test_count.py).
- <a id="release-00-tests-test_empty.py-ffb51e"></a>`tests/test_empty.py`: adds `class Empty`, `test_empty`. New, 8 lines. [The file](https://github.com/rahuldave/tally/blob/bfcbe07463b5c6f3c0764e4ac19a054cb0acee20/tests/test_empty.py).
- <a id="release-00-uv.lock-8356d8"></a>`uv.lock`: New, 8 lines. [The file](https://github.com/rahuldave/tally/blob/bfcbe07463b5c6f3c0764e4ac19a054cb0acee20/uv.lock).

<details><summary>The diff of <code>.gitignore</code></summary>

```diff
@@ -0,0 +1,10 @@
+# Python-generated files
+__pycache__/
+*.py[oc]
+build/
+dist/
+wheels/
+*.egg-info
+
+# Virtual environments
+.venv
```

</details>

<details><summary>The diff of <code>.python-version</code></summary>

```diff
@@ -0,0 +1 @@
+3.12
```

</details>

<details><summary>The diff of <code>README.md</code></summary>

```diff
@@ -0,0 +1,3 @@
+# tally
+
+Count the words in a text.
```

</details>

<details><summary>The diff of <code>justfile</code></summary>

```diff
@@ -0,0 +1,15 @@
+# The recipes of tally. Each one runs through uv, in the project's own environment.
+default:
+    @just --list
+
+# Make the environment of this step: the first command of every step
+setup:
+    uv sync
+
+# Count the words of a file
+run file:
+    uv run tally {{ file }}
+
+# Run the tests
+test:
+    uv run python -m unittest discover -s tests -q
```

</details>

<details><summary>The diff of <code>pyproject.toml</code></summary>

```diff
@@ -0,0 +1,14 @@
+[project]
+name = "tally"
+version = "0.1.0"
+description = "Count the words in a text"
+readme = "README.md"
+requires-python = ">=3.12"
+dependencies = []
+
+[project.scripts]
+tally = "tally:main"
+
+[build-system]
+requires = ["uv_build>=0.12.13,<0.13.0"]
+build-backend = "uv_build"
```

</details>

<details><summary>The diff of <code>src/tally/__init__.py</code></summary>

```diff
@@ -0,0 +1,16 @@
+"""tally: count the words in a text."""
+
+import sys
+
+
+def count(text):
+    counts = {}
+    for word in text.lower().split():
+        counts[word] = counts.get(word, 0) + 1
+    return counts
+
+
+def main() -> None:
+    text = open(sys.argv[1]).read() if len(sys.argv) > 1 else sys.stdin.read()
+    for word, n in sorted(count(text).items()):
+        print(n, word)
```

</details>

<details><summary>The diff of <code>src/tally/__main__.py</code></summary>

```diff
@@ -0,0 +1,3 @@
+from tally import main
+
+main()
```

</details>

<details><summary>The diff of <code>tests/test_count.py</code></summary>

```diff
@@ -0,0 +1,11 @@
+import unittest
+
+from tally import count
+
+
+class Count(unittest.TestCase):
+    def test_words(self):
+        self.assertEqual(count("a b a"), {"a": 2, "b": 1})
+
+    def test_case(self):
+        self.assertEqual(count("A a"), {"a": 2})
```

</details>

<details><summary>The diff of <code>tests/test_empty.py</code></summary>

```diff
@@ -0,0 +1,8 @@
+import unittest
+
+from tally import count
+
+
+class Empty(unittest.TestCase):
+    def test_empty(self):
+        self.assertEqual(count(""), {})
```

</details>

[The code](https://github.com/rahuldave/tally/tree/bfcbe07463b5c6f3c0764e4ac19a054cb0acee20).

<a id="release-01"></a>

## 1 Release 0.2.0

```bash
just setup
```

A release gives users a new version. Before it, we tidy the tests, and after it, the lockfile must name the new
version too.

[The code before this part](https://github.com/rahuldave/tally/tree/bfcbe07463b5c6f3c0764e4ac19a054cb0acee20). [The code after it](https://github.com/rahuldave/tally/tree/96d6bbd94a65f08776215543e0d3c49575422541).

<a id="release-01.1"></a>

### 1.1 Tests of edge cases

The file `tests/test_empty.py` tests one edge case, an empty text. A text of spaces alone is another edge case. One
file can test both, so it gets a name that fits both, `tests/test_edge.py`, and a second test.

Apply the patch that renames `tests/test_empty.py` to [`tests/test_edge.py`](#release-01.1-tests-test_edge.py-24a601), from the top of the project:

```bash
curl -fsSL https://github.com/rahuldave/tally/commit/a54eadb267e9052af3b1f4f5b2fe3e8f2a4184f7.diff | git apply --include=tests/test_edge.py
```

The patch renames `tests/test_empty.py` to `tests/test_edge.py`. It also renames the class to `Edge`, and adds the
test `test_spaces`.

```bash
uv run python -m unittest discover -s tests -q
```

All four tests pass.

Check your files against this move. The command prints nothing when they match, and otherwise shows what differs:

```bash
git check a54eadb267e9
```

If you are stuck, this command puts the files of this move in place of yours. A file that you made yourself stays:

```bash
git restore --source bfcbe07463b5 --staged -- :/ && git restore --source a54eadb267e9 --staged --worktree -- :/
```

#### What changed

- <a id="release-01.1-tests-test_edge.py-24a601"></a>`tests/test_edge.py`: a new name, and a second test. Renamed from `tests/test_empty.py`, 4 lines added, 1 removed. [The file](https://github.com/rahuldave/tally/blob/a54eadb267e9052af3b1f4f5b2fe3e8f2a4184f7/tests/test_edge.py).
  - look at `def test_spaces(self):`

<details open><summary>The patch to <code>tests/test_edge.py</code></summary>

```diff
@@ -3,6 +3,9 @@ import unittest
 from tally import count
 
 
-class Empty(unittest.TestCase):
+class Edge(unittest.TestCase):
     def test_empty(self):
         self.assertEqual(count(""), {})
+
+    def test_spaces(self):
+        self.assertEqual(count("  \n\t "), {})
```

</details>

[This change on GitHub](https://github.com/rahuldave/tally/commit/a54eadb267e9052af3b1f4f5b2fe3e8f2a4184f7). [The code after it](https://github.com/rahuldave/tally/tree/a54eadb267e9052af3b1f4f5b2fe3e8f2a4184f7).

<a id="release-01.2"></a>

### 1.2 Version 0.2.0

Users tell one release from another by its version. The version is a line of `pyproject.toml`.

Apply the patch to [`pyproject.toml`](#release-01.2-pyproject.toml-5d07e7), from the top of the project:

```bash
curl -fsSL https://github.com/rahuldave/tally/commit/aea02344f2e362ad133d77ae05653994a652aab3.diff | git apply --include=pyproject.toml
```

The patch changes one line of `pyproject.toml`, `version`, from `0.1.0` to `0.2.0`.

```bash
grep -n '^version' pyproject.toml
```

It prints `3:version = "0.2.0"`. The lockfile, `uv.lock`, still names version 0.1.0 of tally, so it is out of date.
The next move brings it up to date.

At this move, the project's own `uv.lock` does not match its `pyproject.toml`. So the command has `--stale-lock`, which leaves out the check that your `uv.lock` matches your `pyproject.toml`.

Check your files against this move. The command prints nothing when they match, and otherwise shows what differs:

```bash
git check aea02344f2e3 --stale-lock
```

If you are stuck, this command puts the files of this move in place of yours. A file that you made yourself stays:

```bash
git restore --source a54eadb267e9 --staged -- :/ && git restore --source aea02344f2e3 --staged --worktree -- :/
```

#### What changed

- <a id="release-01.2-pyproject.toml-5d07e7"></a>`pyproject.toml`: the new version. 1 line added, 1 removed. [The file](https://github.com/rahuldave/tally/blob/aea02344f2e362ad133d77ae05653994a652aab3/pyproject.toml).
  - look at `version = "0.2.0"`

<details open><summary>The patch to <code>pyproject.toml</code></summary>

```diff
@@ -1,6 +1,6 @@
 [project]
 name = "tally"
-version = "0.1.0"
+version = "0.2.0"
 description = "Count the words in a text"
 readme = "README.md"
 requires-python = ">=3.12"
```

</details>

[This change on GitHub](https://github.com/rahuldave/tally/commit/aea02344f2e362ad133d77ae05653994a652aab3). [The code after it](https://github.com/rahuldave/tally/tree/aea02344f2e362ad133d77ae05653994a652aab3).

<a id="release-01.3"></a>

### 1.3 The lock, and the list of changes

`uv.lock` records the exact version of each package of the project, tally too. `uv lock` writes it again from
`pyproject.toml`:

```bash
uv lock
```

A user of a release wants to know what changed. A new file, `CHANGES.md`, says it for 0.2.0.

Apply the patch to [`CHANGES.md`](#release-01.3-CHANGES.md-7facec), from the top of the project:

```bash
curl -fsSL https://github.com/rahuldave/tally/commit/96d6bbd94a65f08776215543e0d3c49575422541.diff | git apply --include=CHANGES.md
```

The patch makes the file `CHANGES.md`, with a heading for 0.2.0 and one sentence.

```bash
uv lock --check && grep -A1 '^name = "tally"' uv.lock
```

`uv lock --check` prints nothing, because the lockfile is up to date. Then `grep` prints the entry of tally, with
`version = "0.2.0"`.

Check your files against this move. The command prints nothing when they match, and otherwise shows what differs:

```bash
git check 96d6bbd94a65
```

If you are stuck, this command puts the files of this move in place of yours. A file that you made yourself stays:

```bash
git restore --source aea02344f2e3 --staged -- :/ && git restore --source 96d6bbd94a65 --staged --worktree -- :/
```

#### What changed

- <a id="release-01.3-CHANGES.md-7facec"></a>`CHANGES.md`: the changes of 0.2.0. New, 5 lines. [The file](https://github.com/rahuldave/tally/blob/96d6bbd94a65f08776215543e0d3c49575422541/CHANGES.md).
- <a id="release-01.3-uv.lock-8356d8"></a>`uv.lock`: the version of tally. 1 line added, 1 removed. It comes from `uv lock`. [The file](https://github.com/rahuldave/tally/blob/96d6bbd94a65f08776215543e0d3c49575422541/uv.lock).
  - look at `version = "0.2.0"`

<details open><summary>The patch to <code>CHANGES.md</code></summary>

```diff
@@ -0,0 +1,5 @@
+# Changes
+
+## 0.2.0
+
+The tests of an empty text are now the tests of edge cases, with a test of a text of spaces.
```

</details>

[This change on GitHub](https://github.com/rahuldave/tally/commit/96d6bbd94a65f08776215543e0d3c49575422541). [The code after it](https://github.com/rahuldave/tally/tree/96d6bbd94a65f08776215543e0d3c49575422541).
