<!-- Made by the walk skill's render.py from the facts of the walk. Do not edit it by hand: run just walk-update again. -->

# A release of tally, one move at a time

**Build it yourself.** Every command to run and every change to make by hand, to make the project yourself. [Read the tutorial](read.md) is the other way to read it.

Each part ends with a section called **What changed**. It lists every file that the part changes, with a link to the file, and then the whole diff of each file, folded. A lockfile and a binary file have a link alone. The text above it explains the change. What changed is what you check your files against.

In Build it yourself, a file that a command makes says which command. A diff that is open is a patch. Apply it with the command in the text, or make the same change in your editor.

tally counts words, and has two files of tests. We make a release, version 0.2.0. First the tests of an empty text
get a name that fits more cases. Then tally gets its new version, and last the lockfile records it. After the release, we tidy the project. The
recipes get a hidden file, and every test goes in one file.

We make the release in moves. A move is one small change, made by one patch or by one command.

You make each move, and the page checks your files against it.

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
`pyproject.toml`.

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

`uv lock --check` prints `Resolved 1 package` and the time it took, and stops with no error, because the lockfile is
up to date. Then `grep` prints the entry of tally, with
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

<a id="release-02"></a>

## 2 Tidy the project

```bash
just setup
```

The release is out. Now we tidy the project, so that it is easier to find your way in it. The top folder keeps
the files that a user reads first. The tests, in two files, go into one file, named after the project.

Each file that moves or goes here moves by a command, `mv`, or goes by a command, `rm`.

[The code before this part](https://github.com/rahuldave/tally/tree/96d6bbd94a65f08776215543e0d3c49575422541). [The code after it](https://github.com/rahuldave/tally/tree/eb82f801c8df99c497da0e5940a6a97593808319).

<a id="release-02.1"></a>

### 2.1 A hidden file for the recipes

A user of tally reads `README.md` first, and has no use for the recipes of the `justfile`. They are for the people
who work on tally. `just` also finds its recipes in a file named `.justfile`, a hidden file that `ls` does not list.
`mv` gives the `justfile` that name.

```bash
mv justfile .justfile
```

```bash
just --list
```

It prints the same four recipes as before, `default`, `run`, `setup` and `test`.

Check your files against this move. The command prints nothing when they match, and otherwise shows what differs:

```bash
git check f338b5b0824c
```

If you are stuck, this command puts the files of this move in place of yours. A file that you made yourself stays:

```bash
git restore --source 96d6bbd94a65 --staged -- :/ && git restore --source f338b5b0824c --staged --worktree -- :/
```

#### What changed

- <a id="release-02.1-.justfile-a21be3"></a>`.justfile`: the recipes, in a hidden file. Renamed from `justfile`. It comes from `mv justfile .justfile`. [The file](https://github.com/rahuldave/tally/blob/f338b5b0824cd8dbb2bbc27c04d7bf2de0032cd7/.justfile).

[This change on GitHub](https://github.com/rahuldave/tally/commit/f338b5b0824cd8dbb2bbc27c04d7bf2de0032cd7). [The code after it](https://github.com/rahuldave/tally/tree/f338b5b0824cd8dbb2bbc27c04d7bf2de0032cd7).

<a id="release-02.2"></a>

### 2.2 A test of lines

A text often has more than one line. No test yet gives `count` a text with a newline in it. A new test,
`test_lines`, counts `a b`, a newline, and `a`.

Apply the patch to [`tests/test_count.py`](#release-02.2-tests-test_count.py-e674f6), from the top of the project:

```bash
curl -fsSL https://github.com/rahuldave/tally/commit/3a4ad8d9af5153b7eb458030e59169de6d7fef95.diff | git apply --include=tests/test_count.py
```

The patch adds the test `test_lines` at the end of the class `Count`.

```bash
uv run python -m unittest discover -s tests -q
```

All five tests pass.

Check your files against this move. The command prints nothing when they match, and otherwise shows what differs:

```bash
git check 3a4ad8d9af51
```

If you are stuck, this command puts the files of this move in place of yours. A file that you made yourself stays:

```bash
git restore --source f338b5b0824c --staged -- :/ && git restore --source 3a4ad8d9af51 --staged --worktree -- :/
```

#### What changed

- <a id="release-02.2-tests-test_count.py-e674f6"></a>`tests/test_count.py`: a test of a text of two lines. 3 lines added. [The file](https://github.com/rahuldave/tally/blob/3a4ad8d9af5153b7eb458030e59169de6d7fef95/tests/test_count.py).
  - look at `def test_lines(self):`

<details open><summary>The patch to <code>tests/test_count.py</code></summary>

```diff
@@ -9,3 +9,6 @@ class Count(unittest.TestCase):
 
     def test_case(self):
         self.assertEqual(count("A a"), {"a": 2})
+
+    def test_lines(self):
+        self.assertEqual(count("a b\na"), {"a": 2, "b": 1})
```

</details>

[This change on GitHub](https://github.com/rahuldave/tally/commit/3a4ad8d9af5153b7eb458030e59169de6d7fef95). [The code after it](https://github.com/rahuldave/tally/tree/3a4ad8d9af5153b7eb458030e59169de6d7fef95).

<a id="release-02.3"></a>

### 2.3 One name for the tests

The tests are in two files, `tests/test_count.py` and `tests/test_edge.py`. One file is one place to look. It
gets the name of the project, `tests/test_tally.py`. `mv` gives the file of edge cases that name.

```bash
mv tests/test_edge.py tests/test_tally.py
```

```bash
uv run python -m unittest discover -s tests -q
```

All five tests pass, as before. unittest finds each file whose name starts with `test`.

Check your files against this move. The command prints nothing when they match, and otherwise shows what differs:

```bash
git check fa608c2a2aa3
```

If you are stuck, this command puts the files of this move in place of yours. A file that you made yourself stays:

```bash
git restore --source 3a4ad8d9af51 --staged -- :/ && git restore --source fa608c2a2aa3 --staged --worktree -- :/
```

#### What changed

- <a id="release-02.3-tests-test_tally.py-b402c1"></a>`tests/test_tally.py`: the tests of edge cases, under the new name. Renamed from `tests/test_edge.py`. It comes from `mv tests/test_edge.py tests/test_tally.py`. [The file](https://github.com/rahuldave/tally/blob/fa608c2a2aa34ad657eaea6348198955863191e2/tests/test_tally.py).

[This change on GitHub](https://github.com/rahuldave/tally/commit/fa608c2a2aa34ad657eaea6348198955863191e2). [The code after it](https://github.com/rahuldave/tally/tree/fa608c2a2aa34ad657eaea6348198955863191e2).

<a id="release-02.4"></a>

### 2.4 Every test in one file

The class `Count`, with its three tests, goes into `tests/test_tally.py` too.

Apply the patch to [`tests/test_tally.py`](#release-02.4-tests-test_tally.py-b402c1), from the top of the project:

```bash
curl -fsSL https://github.com/rahuldave/tally/commit/3d2bf4fc97f4b3711f3f8378b4db3311ce795a24.diff | git apply --include=tests/test_tally.py
```

The patch adds the class `Count`, with its three tests, at the end of `tests/test_tally.py`.

```bash
uv run python -m unittest discover -s tests -q
```

All eight tests pass. The three tests of `Count` run twice, once from each file. The next change removes the old
file.

Check your files against this move. The command prints nothing when they match, and otherwise shows what differs:

```bash
git check 3d2bf4fc97f4
```

If you are stuck, this command puts the files of this move in place of yours. A file that you made yourself stays:

```bash
git restore --source fa608c2a2aa3 --staged -- :/ && git restore --source 3d2bf4fc97f4 --staged --worktree -- :/
```

#### What changed

- <a id="release-02.4-tests-test_tally.py-b402c1"></a>`tests/test_tally.py`: every test of tally, in one file. 11 lines added. [The file](https://github.com/rahuldave/tally/blob/3d2bf4fc97f4b3711f3f8378b4db3311ce795a24/tests/test_tally.py).
  - look at `class Count(unittest.TestCase):`

<details open><summary>The patch to <code>tests/test_tally.py</code></summary>

```diff
@@ -9,3 +9,14 @@ class Edge(unittest.TestCase):
 
     def test_spaces(self):
         self.assertEqual(count("  \n\t "), {})
+
+
+class Count(unittest.TestCase):
+    def test_words(self):
+        self.assertEqual(count("a b a"), {"a": 2, "b": 1})
+
+    def test_case(self):
+        self.assertEqual(count("A a"), {"a": 2})
+
+    def test_lines(self):
+        self.assertEqual(count("a b\na"), {"a": 2, "b": 1})
```

</details>

[This change on GitHub](https://github.com/rahuldave/tally/commit/3d2bf4fc97f4b3711f3f8378b4db3311ce795a24). [The code after it](https://github.com/rahuldave/tally/tree/3d2bf4fc97f4b3711f3f8378b4db3311ce795a24).

<a id="release-02.5"></a>

### 2.5 The old file of tests goes

Every test of `tests/test_count.py` is now in `tests/test_tally.py` too. `rm` removes the old file.

```bash
rm tests/test_count.py
```

```bash
uv run python -m unittest discover -s tests -q
```

Each test now runs one time only, and all five tests pass.

Check your files against this move. The command prints nothing when they match, and otherwise shows what differs:

```bash
git check eb82f801c8df
```

If you are stuck, this command puts the files of this move in place of yours. A file that you made yourself stays:

```bash
git restore --source 3d2bf4fc97f4 --staged -- :/ && git restore --source eb82f801c8df --staged --worktree -- :/
```

#### What changed

- <a id="release-02.5-tests-test_count.py-e674f6"></a>`tests/test_count.py`: its tests are in `tests/test_tally.py`. Deleted. It comes from `rm tests/test_count.py`.

<details><summary>The diff that <code>rm tests/test_count.py</code> makes in <code>tests/test_count.py</code></summary>

```diff
@@ -1,14 +0,0 @@
-import unittest
-
-from tally import count
-
-
-class Count(unittest.TestCase):
-    def test_words(self):
-        self.assertEqual(count("a b a"), {"a": 2, "b": 1})
-
-    def test_case(self):
-        self.assertEqual(count("A a"), {"a": 2})
-
-    def test_lines(self):
-        self.assertEqual(count("a b\na"), {"a": 2, "b": 1})
```

</details>

[This change on GitHub](https://github.com/rahuldave/tally/commit/eb82f801c8df99c497da0e5940a6a97593808319). [The code after it](https://github.com/rahuldave/tally/tree/eb82f801c8df99c497da0e5940a6a97593808319).
