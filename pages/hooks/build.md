<!-- Made by the walk skill's render.py from the facts of the walk. Do not edit it by hand: run just walk-update again. -->

# A git hook, one move at a time

**Build it yourself.** Every command to run and every change to make by hand, to make the project yourself. [Read the tutorial](read.md) is the other way to read it.

Each part ends with a section called **What changed**. It lists every file that the part changes, with a link to the file, and then the whole diff of each file, folded. A lockfile and a binary file have a link alone. The text above it explains the change. What changed is what you check your files against.

In Build it yourself, a file that a command makes says which command. A diff that is open is a patch. Apply it with the command in the text, or make the same change in your editor.

tally counts words, and nothing stops a broken file from going into git. We build a hook, a script that git runs
before each `git commit`. The hook checks that the code compiles, and later that the tests pass. When the check
fails, git does not record the change.

We build the hook in moves. A move is one small change, made by one patch or by one command.

You make each move, and the page checks your files against it.

## Get the project

You build the project in a clone of your own, on a branch `mine` that starts where this walk starts. Run the commands of these pages in its top folder.

```bash
git clone https://github.com/rahuldave/tally
cd tally
git switch -c mine eb951f747563
```

Then add the command `git check`, which compares your files with the project's after each move, and leaves what `git add` has staged as it was.

```bash
git config alias.check '!f() { i="$(git rev-parse --git-path check-index)" && { cp "$(git rev-parse --git-path index)" "$i" 2>/dev/null || rm -f "$i"; } && export GIT_INDEX_FILE="$i" && git add -A && git diff --cached --stat "$1"; }; f'
```

<a id="hooks-00"></a>

## 0 Where the hooks start

```bash
just setup
```

tally counts the words of a text. Nothing checks the code before a `git commit`, so a file with a syntax error can
go into git. The recipes of the `justfile` show what the project can do now.

```bash
just --list
```

It lists the recipes of tally, and none of them checks the code.

Check your files against this part. The command prints nothing when they match, and otherwise shows what differs:

```bash
git check eb951f747563
```

If you are stuck, this command puts the files of this part in place of yours. A file that you made yourself stays:

```bash
git rm -rq --cached --ignore-unmatch -- :/ && git restore --source eb951f747563 --staged --worktree -- :/
```

### What changed

- <a id="hooks-00-.gitignore-a5cc29"></a>`.gitignore`: New, 10 lines. [The file](https://github.com/rahuldave/tally/blob/eb951f74756383392f528427a0cf44e135d5c64f/.gitignore).
- <a id="hooks-00-.python-version-7696e9"></a>`.python-version`: New, 1 line. [The file](https://github.com/rahuldave/tally/blob/eb951f74756383392f528427a0cf44e135d5c64f/.python-version).
- <a id="hooks-00-README.md-8ec9a0"></a>`README.md`: New, 3 lines. [The file](https://github.com/rahuldave/tally/blob/eb951f74756383392f528427a0cf44e135d5c64f/README.md).
- <a id="hooks-00-justfile-424f0b"></a>`justfile`: adds `recipe default`, `recipe run`, `recipe setup`, `recipe test`. New, 15 lines. [The file](https://github.com/rahuldave/tally/blob/eb951f74756383392f528427a0cf44e135d5c64f/justfile).
- <a id="hooks-00-pyproject.toml-5d07e7"></a>`pyproject.toml`: New, 14 lines. [The file](https://github.com/rahuldave/tally/blob/eb951f74756383392f528427a0cf44e135d5c64f/pyproject.toml).
- <a id="hooks-00-src-tally-__init__.py-b5485b"></a>`src/tally/__init__.py`: adds `count`, `main`. New, 16 lines. [The file](https://github.com/rahuldave/tally/blob/eb951f74756383392f528427a0cf44e135d5c64f/src/tally/__init__.py).
- <a id="hooks-00-src-tally-__main__.py-534c24"></a>`src/tally/__main__.py`: New, 3 lines. [The file](https://github.com/rahuldave/tally/blob/eb951f74756383392f528427a0cf44e135d5c64f/src/tally/__main__.py).
- <a id="hooks-00-uv.lock-8356d8"></a>`uv.lock`: New, 8 lines. [The file](https://github.com/rahuldave/tally/blob/eb951f74756383392f528427a0cf44e135d5c64f/uv.lock).

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
+    for word in text.split():
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

[The code](https://github.com/rahuldave/tally/tree/eb951f74756383392f528427a0cf44e135d5c64f).

<a id="hooks-01"></a>

## 1 The hook

```bash
just setup
```

A check that each person must remember to run is a check that someone forgets. We write the check as a recipe.
Then a hook runs the recipe before each `git commit`, and a last recipe tells git to use the hook.

[The code before this part](https://github.com/rahuldave/tally/tree/eb951f74756383392f528427a0cf44e135d5c64f). [The code after it](https://github.com/rahuldave/tally/tree/531ba4ddcb71619b788518683004a96f9574a461).

<a id="hooks-01.1"></a>

### 1.1 A recipe that checks the code

A file with a syntax error breaks tally, and nothing finds it before it goes into git. A recipe `check` compiles
every Python file of tally. Python then reports a syntax error at once, without running the code.

Apply the patch to [`justfile`](#hooks-01.1-justfile-424f0b), from the top of the project:

```bash
curl -fsSL https://github.com/rahuldave/tally/commit/e1ef40fe88bbf92165b8da067169897e163a59af.diff | git apply --include=justfile
```

The patch adds the recipe `check` at the end of the `justfile`.

```bash
just check && echo "the code compiles"
```

It prints `the code compiles`, because every file compiles.

Check your files against this move. The command prints nothing when they match, and otherwise shows what differs:

```bash
git check e1ef40fe88bb
```

If you are stuck, this command puts the files of this move in place of yours. A file that you made yourself stays:

```bash
git restore --source eb951f747563 --staged -- :/ && git restore --source e1ef40fe88bb --staged --worktree -- :/
```

#### What changed

- <a id="hooks-01.1-justfile-424f0b"></a>`justfile`: the recipe compiles every Python file. 4 lines added. [The file](https://github.com/rahuldave/tally/blob/e1ef40fe88bbf92165b8da067169897e163a59af/justfile).
  - look at `uv run python -m py_compile src/tally/*.py`

<details open><summary>The patch to <code>justfile</code></summary>

```diff
@@ -13,3 +13,7 @@ run file:
 # Run the tests
 test:
     uv run python -m unittest discover -s tests -q
+
+# Check that every Python file compiles
+check:
+    uv run python -m py_compile src/tally/*.py
```

</details>

[This change on GitHub](https://github.com/rahuldave/tally/commit/e1ef40fe88bbf92165b8da067169897e163a59af). [The code after it](https://github.com/rahuldave/tally/tree/e1ef40fe88bbf92165b8da067169897e163a59af).

<a id="hooks-01.2"></a>

### 1.2 A hook script

`just check` works only when someone runs it. A hook runs it every time. git runs the file `pre-commit` of its
folder of hooks before each `git commit`, and stops the `git commit` when the file fails. The hook,
`hooks/pre-commit`, has three lines. They name the shell that runs it, say what it does, and run the check. The
file comes whole, as a patch.

Apply the patch to [`hooks/pre-commit`](#hooks-01.2-hooks-pre-commit-470a57), from the top of the project:

```bash
curl -fsSL https://github.com/rahuldave/tally/commit/5bd8d5bb524c565e0cfa0cdfb184ca9895203ef1.diff | git apply --include=hooks/pre-commit
```

Read its last line, `just check`. It is the whole of what the hook does.

```bash
sh hooks/pre-commit; echo "the hook said $?"
```

The code compiles, so the hook says 0.

Check your files against this move. The command prints nothing when they match, and otherwise shows what differs:

```bash
git check 5bd8d5bb524c
```

If you are stuck, this command puts the files of this move in place of yours. A file that you made yourself stays:

```bash
git restore --source e1ef40fe88bb --staged -- :/ && git restore --source 5bd8d5bb524c --staged --worktree -- :/
```

#### What changed

- <a id="hooks-01.2-hooks-pre-commit-470a57"></a>`hooks/pre-commit`: three lines that git runs before a `git commit`. the hook only runs the check. New, 3 lines. [The file](https://github.com/rahuldave/tally/blob/5bd8d5bb524c565e0cfa0cdfb184ca9895203ef1/hooks/pre-commit).
  - look at `just check`

<details open><summary>The patch to <code>hooks/pre-commit</code></summary>

```diff
@@ -0,0 +1,3 @@
+#!/bin/sh
+# Run before each commit: refuse it if the code does not compile.
+just check
```

</details>

[This change on GitHub](https://github.com/rahuldave/tally/commit/5bd8d5bb524c565e0cfa0cdfb184ca9895203ef1). [The code after it](https://github.com/rahuldave/tally/tree/5bd8d5bb524c565e0cfa0cdfb184ca9895203ef1).

<a id="hooks-01.3"></a>

### 1.3 Make it runnable

git runs a hook only if the hook is executable, so we make it executable.

```bash
chmod +x hooks/pre-commit
```

Run the hook by hand on a broken file, and see it fail. Then remove the file:

```bash
printf 'def (\n' > src/tally/broken.py; ./hooks/pre-commit; echo "the hook said $?"
rm src/tally/broken.py
```

The hook says 1, so git would stop the `git commit`.

Check your files against this move. The command prints nothing when they match, and otherwise shows what differs:

```bash
git check 8d19bc56776a
```

If you are stuck, this command puts the files of this move in place of yours. A file that you made yourself stays:

```bash
git restore --source 5bd8d5bb524c --staged -- :/ && git restore --source 8d19bc56776a --staged --worktree -- :/
```

#### What changed

- <a id="hooks-01.3-hooks-pre-commit-470a57"></a>`hooks/pre-commit`: Its lines stay as they were. It comes from `chmod +x hooks/pre-commit`. [The file](https://github.com/rahuldave/tally/blob/8d19bc56776ab8ebc942b5465d8dd270e33e7485/hooks/pre-commit).

[This change on GitHub](https://github.com/rahuldave/tally/commit/8d19bc56776ab8ebc942b5465d8dd270e33e7485). [The code after it](https://github.com/rahuldave/tally/tree/8d19bc56776ab8ebc942b5465d8dd270e33e7485).

<a id="hooks-01.4"></a>

### 1.4 Install it

git does not copy hooks with a repository, and does not look in the folder `hooks` unless it is told to. So each
copy of the project installs the hook. A recipe `install-hook` sets `core.hooksPath`, the setting of git that names
the folder of hooks. The recipe changes the settings of git, so it is a recipe of its own, and not a part of
`just setup`. `just setup` only runs `uv sync`, which makes the environment.

Apply the patch to [`justfile`](#hooks-01.4-justfile-424f0b), from the top of the project:

```bash
curl -fsSL https://github.com/rahuldave/tally/commit/531ba4ddcb71619b788518683004a96f9574a461.diff | git apply --include=justfile
```

The patch adds the recipe `install-hook`, with its comment, at the end of the `justfile`.

```bash
just install-hook && git config core.hooksPath
```

It prints `hooks`, so git now runs the hook before each `git commit`.

Check your files against this move. The command prints nothing when they match, and otherwise shows what differs:

```bash
git check 531ba4ddcb71
```

If you are stuck, this command puts the files of this move in place of yours. A file that you made yourself stays:

```bash
git restore --source 8d19bc56776a --staged -- :/ && git restore --source 531ba4ddcb71 --staged --worktree -- :/
```

#### What changed

- <a id="hooks-01.4-justfile-424f0b"></a>`justfile`: one line of git config, in a recipe of its own. 4 lines added. [The file](https://github.com/rahuldave/tally/blob/531ba4ddcb71619b788518683004a96f9574a461/justfile).
  - look at `git config core.hooksPath hooks`

<details open><summary>The patch to <code>justfile</code></summary>

```diff
@@ -17,3 +17,7 @@ test:
 # Check that every Python file compiles
 check:
     uv run python -m py_compile src/tally/*.py
+
+# Make git run the hooks in hooks/, before each commit. This changes git's config, so it is not part of setup
+install-hook:
+    git config core.hooksPath hooks
```

</details>

[This change on GitHub](https://github.com/rahuldave/tally/commit/531ba4ddcb71619b788518683004a96f9574a461). [The code after it](https://github.com/rahuldave/tally/tree/531ba4ddcb71619b788518683004a96f9574a461).

<a id="hooks-02"></a>

## 2 Tests in the hook

```bash
just setup
```

Code that compiles can still count wrong. The tests find that, so the hook must run them too. First we write a
test, then the hook runs the tests after the check.

[The code before this part](https://github.com/rahuldave/tally/tree/531ba4ddcb71619b788518683004a96f9574a461). [The code after it](https://github.com/rahuldave/tally/tree/df640e57553c144400b44e92cf33341aafd445f2).

<a id="hooks-02.1"></a>

### 2.1 A first test

The hook can run tests only if there are tests. A first test, in `tests/test_count.py`, checks that `count` counts
the words of `a b a`.

Apply the patch to [`tests/test_count.py`](#hooks-02.1-tests-test_count.py-e674f6), from the top of the project:

```bash
curl -fsSL https://github.com/rahuldave/tally/commit/03c1416124f56e13bcd39af675927dcbd399de44.diff | git apply --include=tests/test_count.py
```

The patch makes the file `tests/test_count.py`, with the class `Count` and its test.

```bash
uv run python -m unittest discover -s tests -q
```

The test passes.

Check your files against this move. The command prints nothing when they match, and otherwise shows what differs:

```bash
git check 03c1416124f5
```

If you are stuck, this command puts the files of this move in place of yours. A file that you made yourself stays:

```bash
git restore --source 531ba4ddcb71 --staged -- :/ && git restore --source 03c1416124f5 --staged --worktree -- :/
```

#### What changed

- <a id="hooks-02.1-tests-test_count.py-e674f6"></a>`tests/test_count.py`: one test of counting. New, 9 lines. [The file](https://github.com/rahuldave/tally/blob/03c1416124f56e13bcd39af675927dcbd399de44/tests/test_count.py).
  - look at `self.assertEqual(count("a b a"), {"a": 2, "b": 1})`

<details open><summary>The patch to <code>tests/test_count.py</code></summary>

```diff
@@ -0,0 +1,9 @@
+import unittest
+
+from tally import count
+
+
+class Count(unittest.TestCase):
+    def test_words(self):
+        self.assertEqual(count("a b a"), {"a": 2, "b": 1})
+
```

</details>

[This change on GitHub](https://github.com/rahuldave/tally/commit/03c1416124f56e13bcd39af675927dcbd399de44). [The code after it](https://github.com/rahuldave/tally/tree/03c1416124f56e13bcd39af675927dcbd399de44).

<a id="hooks-02.2"></a>

### 2.2 The hook runs the tests too

The hook compiles the code, but a failing test does not stop a `git commit`. One more line in the hook runs the
tests after the check.

Apply the patch to [`hooks/pre-commit`](#hooks-02.2-hooks-pre-commit-470a57), from the top of the project:

```bash
curl -fsSL https://github.com/rahuldave/tally/commit/df640e57553c144400b44e92cf33341aafd445f2.diff | git apply --include=hooks/pre-commit
```

The patch adds one line at the end of `hooks/pre-commit`, after the line `just check`.

```bash
sh hooks/pre-commit && echo "the hook passed"
```

The hook compiles the code, runs the tests, and prints `the hook passed`.

Check your files against this move. The command prints nothing when they match, and otherwise shows what differs:

```bash
git check df640e57553c
```

If you are stuck, this command puts the files of this move in place of yours. A file that you made yourself stays:

```bash
git restore --source 03c1416124f5 --staged -- :/ && git restore --source df640e57553c --staged --worktree -- :/
```

#### What changed

- <a id="hooks-02.2-hooks-pre-commit-470a57"></a>`hooks/pre-commit`: the tests run after the check. 1 line added. [The file](https://github.com/rahuldave/tally/blob/df640e57553c144400b44e92cf33341aafd445f2/hooks/pre-commit).
  - look at `uv run python -m unittest discover -s tests -q`

<details open><summary>The patch to <code>hooks/pre-commit</code></summary>

```diff
@@ -1,3 +1,4 @@
 #!/bin/sh
 # Run before each commit: refuse it if the code does not compile.
 just check
+uv run python -m unittest discover -s tests -q
```

</details>

[This change on GitHub](https://github.com/rahuldave/tally/commit/df640e57553c144400b44e92cf33341aafd445f2). [The code after it](https://github.com/rahuldave/tally/tree/df640e57553c144400b44e92cf33341aafd445f2).
