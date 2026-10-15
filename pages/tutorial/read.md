<!-- Made by the walk skill's render.py from the facts of the walk. Do not edit it by hand: run just walk-update again. -->

# tally, one move at a time

**Read the tutorial.** Each change explained, with the code to look at. [Build it yourself](build.md) is the other way to read it.

Each part ends with a section called **What changed**. It lists every file that the part changes, with a link to the file, and then the whole diff of each file, folded. A lockfile and a binary file have a link alone. The text above it explains the change.

We build tally, a small word counter, one change at a time. It begins as a command with nothing to count. At the
end, it counts the words of a file, has tests and types, and writes a report of the most common words. Every
command runs through uv, in the project's own environment.

We make tally in moves. A move is one small change, made by one patch or by one command. A patch changes a file, and
a command such as `uv add` writes the files it needs.

Each move first says what problem it solves. Then it gives the change, piece by piece. Last, a command checks the
result, and a list names each file that changed, with what to look for in it.

<a id="step-00"></a>

## 0 Where it starts

```bash
just setup
```

tally is a uv project with one command, `tally`, which has nothing to count yet. `just setup` makes the
environment of the project, `.venv`, with `uv sync`. Run the command, to see where we begin.

```bash
uv run tally
```

It prints `tally: nothing to count yet`.

### What changed

- <a id="step-00-.gitignore-a5cc29"></a>`.gitignore`: the files that git does not hold, such as `.venv`. New, 10 lines. [The file](https://github.com/rahuldave/tally/blob/6a63758166d3aeee516faa6244414d7b54b5a730/.gitignore).
- <a id="step-00-.python-version-7696e9"></a>`.python-version`: the version of Python that uv uses. New, 1 line. [The file](https://github.com/rahuldave/tally/blob/6a63758166d3aeee516faa6244414d7b54b5a730/.python-version).
- <a id="step-00-README.md-8ec9a0"></a>`README.md`: one line about tally. New, 3 lines. [The file](https://github.com/rahuldave/tally/blob/6a63758166d3aeee516faa6244414d7b54b5a730/README.md).
- <a id="step-00-justfile-424f0b"></a>`justfile`: the recipes, with `setup` first. New, 15 lines. [The file](https://github.com/rahuldave/tally/blob/6a63758166d3aeee516faa6244414d7b54b5a730/justfile).
- <a id="step-00-pyproject.toml-5d07e7"></a>`pyproject.toml`: the project, and the table `[project.scripts]` that makes the command `tally`. New, 14 lines. [The file](https://github.com/rahuldave/tally/blob/6a63758166d3aeee516faa6244414d7b54b5a730/pyproject.toml).
  - look at `tally = "tally:main"`
- <a id="step-00-src-tally-__init__.py-b5485b"></a>`src/tally/__init__.py`: `main`, which has nothing to count yet. New, 5 lines. [The file](https://github.com/rahuldave/tally/blob/6a63758166d3aeee516faa6244414d7b54b5a730/src/tally/__init__.py).
- <a id="step-00-src-tally-__main__.py-534c24"></a>`src/tally/__main__.py`: lets `python -m tally` run `main` too. New, 3 lines. [The file](https://github.com/rahuldave/tally/blob/6a63758166d3aeee516faa6244414d7b54b5a730/src/tally/__main__.py).
- <a id="step-00-uv.lock-8356d8"></a>`uv.lock`: the exact packages, the same for every learner. New, 8 lines. [The file](https://github.com/rahuldave/tally/blob/6a63758166d3aeee516faa6244414d7b54b5a730/uv.lock).

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
@@ -0,0 +1,5 @@
+"""tally: count the words in a text."""
+
+
+def main() -> None:
+    print("tally: nothing to count yet")
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

[The code](https://github.com/rahuldave/tally/tree/6a63758166d3aeee516faa6244414d7b54b5a730).

<a id="step-01"></a>

## 1 Counting

```bash
just setup
```

tally must count the words of a text. First we write a function that counts, and try it alone. Then the command
reads a text, and prints what the function counts.

[The code before this part](https://github.com/rahuldave/tally/tree/6a63758166d3aeee516faa6244414d7b54b5a730). [The code after it](https://github.com/rahuldave/tally/tree/eb951f74756383392f528427a0cf44e135d5c64f).

<a id="step-01.1"></a>

### 1.1 A function that counts

A word counter needs a way to count. A function, `count`, takes a text and gives a dictionary from each word to how
many times it appears. It goes in `src/tally/__init__.py`, above `main`. The command does not use it yet.

A patch to [`src/tally/__init__.py`](#step-01.1-src-tally-__init__.py-b5485b).

In `src/tally/__init__.py`, `count` now stands above `main`. It splits the text at every space, tab and end of line. For each word, it
adds 1 to the count so far, and `counts.get(word, 0)` gives 0 for a word it has not seen.

```bash
uv run python -c "from tally import count; print(count('a b a'))"
```

It prints `{'a': 2, 'b': 1}`, two of `a` and one of `b`. So the function works, though the command still has
nothing to count.

#### What changed

- <a id="step-01.1-src-tally-__init__.py-b5485b"></a>`src/tally/__init__.py`: a dictionary from each word to how many times it appears. 7 lines added. [The file](https://github.com/rahuldave/tally/blob/12fcbe75226dde15e7500b71439bad84712fd2b0/src/tally/__init__.py).
  - look at `counts[word] = counts.get(word, 0) + 1`

<details><summary>The diff of <code>src/tally/__init__.py</code></summary>

```diff
@@ -1,5 +1,12 @@
 """tally: count the words in a text."""
 
 
+def count(text):
+    counts = {}
+    for word in text.split():
+        counts[word] = counts.get(word, 0) + 1
+    return counts
+
+
 def main() -> None:
     print("tally: nothing to count yet")
```

</details>

[This change on GitHub](https://github.com/rahuldave/tally/commit/12fcbe75226dde15e7500b71439bad84712fd2b0). [The code after it](https://github.com/rahuldave/tally/tree/12fcbe75226dde15e7500b71439bad84712fd2b0).

<a id="step-01.2"></a>

### 1.2 The command counts

`count` works, but the command still prints that it has nothing to count. `main` must read a text and print the
counts. It reads the file that the command names, or the standard input when the command names no file. The module
`sys` gives both the arguments of the command and the standard input.

A patch to [`src/tally/__init__.py`](#step-01.2-src-tally-__init__.py-b5485b).

In `src/tally/__init__.py`, `import sys` now stands under the docstring of the module. The first line of `main`
reads the text, from the file named in `sys.argv[1]` or from the standard input. The loop prints each word with
its count. `sorted` puts the words in alphabetical order.

```bash
echo "a b a" | uv run tally
```

It prints `2 a` and then `1 b`. The command now counts.

#### What changed

- <a id="step-01.2-src-tally-__init__.py-b5485b"></a>`src/tally/__init__.py`: `main` reads the text and prints the counts. 5 lines added, 1 removed. [The file](https://github.com/rahuldave/tally/blob/eb951f74756383392f528427a0cf44e135d5c64f/src/tally/__init__.py).
  - look at `for word, n in sorted(count(text).items()):`

<details><summary>The diff of <code>src/tally/__init__.py</code></summary>

```diff
@@ -1,5 +1,7 @@
 """tally: count the words in a text."""
 
+import sys
+
 
 def count(text):
     counts = {}
@@ -9,4 +11,6 @@ def count(text):
 
 
 def main() -> None:
-    print("tally: nothing to count yet")
+    text = open(sys.argv[1]).read() if len(sys.argv) > 1 else sys.stdin.read()
+    for word, n in sorted(count(text).items()):
+        print(n, word)
```

</details>

[This change on GitHub](https://github.com/rahuldave/tally/commit/eb951f74756383392f528427a0cf44e135d5c64f). [The code after it](https://github.com/rahuldave/tally/tree/eb951f74756383392f528427a0cf44e135d5c64f).

<a id="step-02"></a>

## 2 Tests, one at a time

```bash
just setup
```

We cannot tell whether `count` still works after a change, unless we try it by hand each time. Tests try it for us.
Each test gives `count` a text, and compares what it gives back with what we expect.
We add the tests one file at a time, and run them after each. One test asks for something that `count` cannot do yet. It asks `count` to count
"The" and "the" as one word.

[The code before this part](https://github.com/rahuldave/tally/tree/eb951f74756383392f528427a0cf44e135d5c64f). [The code after it](https://github.com/rahuldave/tally/tree/bfcbe07463b5c6f3c0764e4ac19a054cb0acee20).

<a id="step-02.1"></a>

### 2.1 A test of counting

Nothing checks yet that `count` gives the right counts. A test of `unittest`, the test library of Python, calls
`count` on a short text and compares the result with the dictionary that it expects. The tests go in a new folder,
`tests`.

The first file of tests, `tests/test_count.py`, has two tests. `test_words` counts `a b a`. `test_case` counts
`A a`, and expects the one word `a`, twice. The code cannot do this yet.

A patch to [`tests/test_count.py`](#step-02.1-tests-test_count.py-e674f6).

In [the change of `tests/test_count.py`](#step-02.1-tests-test_count.py-e674f6), look at `test_case`. It is the test that fails below.

```bash
uv run python -m unittest discover -s tests -q
```

One test fails. `test_case` expects `{'a': 2}`, and gets `{'A': 1, 'a': 1}`. The failure is a question that the
code has not answered yet.

#### What changed

- <a id="step-02.1-tests-test_count.py-e674f6"></a>`tests/test_count.py`: two tests. The second asks for something the code cannot do yet. New, 11 lines. [The file](https://github.com/rahuldave/tally/blob/6a4b1a0e50035c4060f84b50770e234b2156be10/tests/test_count.py).
  - look at `self.assertEqual(count("A a"), {"a": 2})`

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

[This change on GitHub](https://github.com/rahuldave/tally/commit/6a4b1a0e50035c4060f84b50770e234b2156be10). [The code after it](https://github.com/rahuldave/tally/tree/6a4b1a0e50035c4060f84b50770e234b2156be10).

<a id="step-02.2"></a>

### 2.2 A test of an empty text

An empty file is a text with no words. `count` must give an empty dictionary for it, and not fail. A test in a
file of its own, `tests/test_empty.py`, says so, and keeps it true after later changes.

A patch to [`tests/test_empty.py`](#step-02.2-tests-test_empty.py-ffb51e).

The new file `tests/test_empty.py` holds one test, `test_empty`. It gives `count` the empty text `""`, and
expects the empty dictionary `{}`.

```bash
uv run python -m unittest discover -s tests -q
```

The new test passes at once, because `split()` finds no words in an empty text. `test_case` still fails.

#### What changed

- <a id="step-02.2-tests-test_empty.py-ffb51e"></a>`tests/test_empty.py`: an empty text counts nothing. New, 8 lines. [The file](https://github.com/rahuldave/tally/blob/4f9bfa3d9c08307287e81a631039894490a3e590/tests/test_empty.py).
  - look at `self.assertEqual(count(""), {})`

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

[This change on GitHub](https://github.com/rahuldave/tally/commit/4f9bfa3d9c08307287e81a631039894490a3e590). [The code after it](https://github.com/rahuldave/tally/tree/4f9bfa3d9c08307287e81a631039894490a3e590).

<a id="step-02.3"></a>

### 2.3 Case does not matter

`test_case` fails, because `count` counts `A` and `a` as two words. When `count` puts the text in lower case before
it splits it, every word is counted in lower case. One word in the loop of `count`, `lower()`, does it.

A patch to [`src/tally/__init__.py`](#step-02.3-src-tally-__init__.py-b5485b).

In `count`, in `src/tally/__init__.py`, the loop now splits `text.lower()`, and not `text`. So `A` and `a` are
the same word.

```bash
uv run python -m unittest discover -s tests -q
echo "The the" | uv run tally
```

All three tests pass, and the command prints `2 the` for "The the".

#### What changed

- <a id="step-02.3-src-tally-__init__.py-b5485b"></a>`src/tally/__init__.py`: one word, `lower()`, answers the failing test. 1 line added, 1 removed. [The file](https://github.com/rahuldave/tally/blob/bfcbe07463b5c6f3c0764e4ac19a054cb0acee20/src/tally/__init__.py).
  - look at `for word in text.lower().split():`

<details><summary>The diff of <code>src/tally/__init__.py</code></summary>

```diff
@@ -5,7 +5,7 @@ import sys
 
 def count(text):
     counts = {}
-    for word in text.split():
+    for word in text.lower().split():
         counts[word] = counts.get(word, 0) + 1
     return counts
 
```

</details>

[This change on GitHub](https://github.com/rahuldave/tally/commit/bfcbe07463b5c6f3c0764e4ac19a054cb0acee20). [The code after it](https://github.com/rahuldave/tally/tree/bfcbe07463b5c6f3c0764e4ac19a054cb0acee20).

<a id="step-03"></a>

## 3 Formatting, and a corpus

```bash
just setup
```

tally works, and it has tests. Two things help the work ahead. Code in one style is easier to read and to change,
so we install ruff, a formatter and linter. And a count of three words shows little, so `just setup` makes a
corpus, a text of 2000 words to count.

[The code before this part](https://github.com/rahuldave/tally/tree/bfcbe07463b5c6f3c0764e4ac19a054cb0acee20). [The code after it](https://github.com/rahuldave/tally/tree/1568a522d23312c59c6e42cb027ec25ba3ae8b35).

<a id="step-03.1"></a>

### 3.1 ruff, a tool for development

Each person writes code in a style of their own, with other quotes, blank lines and lengths of line. A formatter
writes every file in one style. A linter reads the code, and reports mistakes that the tests do not find. ruff is
both. It goes in the group `dev` of the project. The group `dev` is for the people who work on tally, so a user
who installs tally does not get ruff.

One command does it all. `uv add` writes ruff into `pyproject.toml` and `uv.lock`, and installs it in `.venv`.

This change came from running `uv add --dev ruff`.

In `pyproject.toml`, a new table `[dependency-groups]` has the group `dev`, with the line `"ruff>=0.17.0",`. In
`uv.lock`, the entry `name = "ruff"` gives the exact version, and the files of ruff for each system.

```bash
uv run ruff format --check
```

ruff reads every Python file of the project, and prints `5 files already formatted`.

#### What changed

- <a id="step-03.1-pyproject.toml-5d07e7"></a>`pyproject.toml`: ruff, in a group of its own. The version is the newest on the day that ruff was added. 5 lines added. It comes from `uv add --dev ruff`. [The file](https://github.com/rahuldave/tally/blob/edb9544c04d29869122cfcef2a0c2173b94c3b06/pyproject.toml).
  - look at `"ruff>=0.17.0",`
- <a id="step-03.1-uv.lock-8356d8"></a>`uv.lock`: the exact version of ruff, which every learner gets with `just setup`. 35 lines added. It comes from `uv add --dev ruff`. [The file](https://github.com/rahuldave/tally/blob/edb9544c04d29869122cfcef2a0c2173b94c3b06/uv.lock).
  - look at `name = "ruff"`

<details><summary>The diff of <code>pyproject.toml</code></summary>

```diff
@@ -12,3 +12,8 @@ tally = "tally:main"
 [build-system]
 requires = ["uv_build>=0.12.13,<0.13.0"]
 build-backend = "uv_build"
+
+[dependency-groups]
+dev = [
+    "ruff>=0.17.0",
+]
```

</details>

[This change on GitHub](https://github.com/rahuldave/tally/commit/edb9544c04d29869122cfcef2a0c2173b94c3b06). [The code after it](https://github.com/rahuldave/tally/tree/edb9544c04d29869122cfcef2a0c2173b94c3b06).

<a id="step-03.2"></a>

### 3.2 A line length for ruff

ruff and each editor have their own idea of how long a line can be. A setting in `pyproject.toml` makes them agree.
It is a table `[tool.ruff]`, with a line length of 100.

A patch to [`pyproject.toml`](#step-03.2-pyproject.toml-5d07e7).

At the end of `pyproject.toml`, the table `[tool.ruff]` sets `line-length = 100`. The linter and the formatter
both read it.

```bash
uv run ruff check --show-settings src | grep line_length
uv run ruff format --check
```

The first command prints `linter.line_length = 100`, so ruff reads the setting. The code still fits, and every file
is already formatted.

#### What changed

- <a id="step-03.2-pyproject.toml-5d07e7"></a>`pyproject.toml`: one setting, for the linter and the formatter both. 3 lines added. [The file](https://github.com/rahuldave/tally/blob/0b7b0a80e5804523e11cc5f5d4d334f4a9dc8327/pyproject.toml).
  - look at `line-length = 100`

<details><summary>The diff of <code>pyproject.toml</code></summary>

```diff
@@ -17,3 +17,6 @@ build-backend = "uv_build"
 dev = [
     "ruff>=0.17.0",
 ]
+
+[tool.ruff]
+line-length = 100
```

</details>

[This change on GitHub](https://github.com/rahuldave/tally/commit/0b7b0a80e5804523e11cc5f5d4d334f4a9dc8327). [The code after it](https://github.com/rahuldave/tally/tree/0b7b0a80e5804523e11cc5f5d4d334f4a9dc8327).

<a id="step-03.3"></a>

### 3.3 A corpus, which just setup makes

A count of `a b a` shows little. tally needs a long text to count, the same for every learner. A script,
`scripts/corpus.py`, writes `data/corpus.txt`, 2000 words from a short list, in the same order each time. The
script comes whole, as a patch.

A patch to [`scripts/corpus.py`](#step-03.3-scripts-corpus.py-ab344b).

The corpus is an artifact, a file that the project makes and git does not hold. So `.gitignore` names the folder
`data/`. git leaves an ignored file alone, so the corpus stays when the code changes.

A patch to [`.gitignore`](#step-03.3-.gitignore-a5cc29).

`just setup` makes the environment, and now it runs the script too. So every learner has the corpus. The script
does not touch a corpus that is already there, so a second `just setup` writes nothing.

A patch to [`justfile`](#step-03.3-justfile-424f0b).

The new file `scripts/corpus.py` picks each word from the list `WORDS`, with a number that it works out from the
number before it. The first number is always 7, so the words are the same each time. `.gitignore` now ends with
`data/`, and the recipe `setup` of the `justfile` runs the script after `uv sync`.

```bash
just setup
uv run tally data/corpus.txt | sort -rn | head -3
```

`just setup` prints `wrote data/corpus.txt: 2000 words`. `sort -rn` puts the lines of tally in order of count, highest
first, and `head -3` keeps the first three. They are `127 line`, `126 class` and `125 word`.

#### What changed

- <a id="step-03.3-.gitignore-a5cc29"></a>`.gitignore`: git does not hold the corpus. 3 lines added. [The file](https://github.com/rahuldave/tally/blob/1568a522d23312c59c6e42cb027ec25ba3ae8b35/.gitignore).
  - look at `data/`
- <a id="step-03.3-justfile-424f0b"></a>`justfile`: `just setup` now makes the corpus too. 1 line added. [The file](https://github.com/rahuldave/tally/blob/1568a522d23312c59c6e42cb027ec25ba3ae8b35/justfile).
  - look at `uv run python scripts/corpus.py data/corpus.txt`
- <a id="step-03.3-scripts-corpus.py-ab344b"></a>`scripts/corpus.py`: the script writes the same 2000 words each time, and does not touch a corpus that is already there. New, 25 lines. [The file](https://github.com/rahuldave/tally/blob/1568a522d23312c59c6e42cb027ec25ba3ae8b35/scripts/corpus.py).
  - look at `if target.exists():`

<details><summary>The diff of <code>.gitignore</code></summary>

```diff
@@ -8,3 +8,6 @@ wheels/
 
 # Virtual environments
 .venv
+
+# Artifacts that just setup makes: they are not in git
+data/
```

</details>

<details><summary>The diff of <code>justfile</code></summary>

```diff
@@ -5,6 +5,7 @@ default:
 # Make the environment of this step: the first command of every step
 setup:
     uv sync
+    uv run python scripts/corpus.py data/corpus.txt
 
 # Count the words of a file
 run file:
```

</details>

<details><summary>The diff of <code>scripts/corpus.py</code></summary>

```diff
@@ -0,0 +1,25 @@
+"""Write data/corpus.txt, a text of 2000 words to count, the same every time. Leave it alone if it is there."""
+
+import sys
+from pathlib import Path
+
+WORDS = "the a word count text tally test step move commit tag note slide class shell file line code".split()
+
+
+def main() -> None:
+    target = Path(sys.argv[1] if len(sys.argv) > 1 else "data/corpus.txt")
+    if target.exists():
+        print(f"{target} is there")
+        return
+    seed, words = 7, []
+    for _ in range(2000):
+        seed = (seed * 1103515245 + 12345) % 2**31
+        words.append(WORDS[seed % len(WORDS)])
+    target.parent.mkdir(parents=True, exist_ok=True)
+    lines = (" ".join(words[i : i + 12]) for i in range(0, len(words), 12))
+    target.write_text("\n".join(lines) + "\n")
+    print(f"wrote {target}: {len(words)} words")
+
+
+if __name__ == "__main__":
+    main()
```

</details>

[This change on GitHub](https://github.com/rahuldave/tally/commit/1568a522d23312c59c6e42cb027ec25ba3ae8b35). [The code after it](https://github.com/rahuldave/tally/tree/1568a522d23312c59c6e42cb027ec25ba3ae8b35).

<a id="step-04"></a>

## 4 Types, then a docstring

```bash
just setup
```

To learn what `count` takes and what it gives, a reader must now read its body. Its signature can say it at a
glance, and an editor can check it. One line under the signature can say what the function does. Neither changes
what `count` does, so the tests pass as before.

[The code before this part](https://github.com/rahuldave/tally/tree/1568a522d23312c59c6e42cb027ec25ba3ae8b35). [The code after it](https://github.com/rahuldave/tally/tree/f79588d3b046ec2787725cdb6e3fcf952014e078).

<a id="step-04.1"></a>

### 4.1 Types

The signature `def count(text):` does not say what `text` is, or what `count` gives back. Types say it. `count`
takes a `str`, and gives a `dict[str, int]`, a dictionary from words to counts. The body stays the same.

A patch to [`src/tally/__init__.py`](#step-04.1-src-tally-__init__.py-b5485b).

In `src/tally/__init__.py`, the signature of `count` now says `text: str`, and `-> dict[str, int]` for what it
gives back. The body is the same.

```bash
uv run python -m unittest discover -s tests -q
```

The three tests pass as before, because types change what the code says, not what it does.

#### What changed

- <a id="step-04.1-src-tally-__init__.py-b5485b"></a>`src/tally/__init__.py`: the signature says what goes in and what comes out. 1 line added, 1 removed. [The file](https://github.com/rahuldave/tally/blob/a7606fcc89be70f26f75353333a506e9891a6ea1/src/tally/__init__.py).
  - look at `def count(text: str) -> dict[str, int]:`

<details><summary>The diff of <code>src/tally/__init__.py</code></summary>

```diff
@@ -3,7 +3,7 @@
 import sys
 
 
-def count(text):
+def count(text: str) -> dict[str, int]:
     counts = {}
     for word in text.lower().split():
         counts[word] = counts.get(word, 0) + 1
```

</details>

[This change on GitHub](https://github.com/rahuldave/tally/commit/a7606fcc89be70f26f75353333a506e9891a6ea1). [The code after it](https://github.com/rahuldave/tally/tree/a7606fcc89be70f26f75353333a506e9891a6ea1).

<a id="step-04.2"></a>

### 4.2 A docstring

The types say what `count` takes and gives, but not what it does with the text. A docstring says it. It is a string on
the first line of a function. Python keeps it in `count.__doc__`, and `help(count)` prints it.

A patch to [`src/tally/__init__.py`](#step-04.2-src-tally-__init__.py-b5485b).

In `src/tally/__init__.py`, the first line of `count` is now its docstring. It says that `count` ignores case.

```bash
uv run python -c "import tally; print(tally.count.__doc__)"
```

It prints the docstring, ``How many times each word of `text` appears, ignoring case.``

#### What changed

- <a id="step-04.2-src-tally-__init__.py-b5485b"></a>`src/tally/__init__.py`: one line under the signature says what the function does. 1 line added. [The file](https://github.com/rahuldave/tally/blob/f79588d3b046ec2787725cdb6e3fcf952014e078/src/tally/__init__.py).
  - look at ``"How many times each word of `text` appears, ignoring case."``

<details><summary>The diff of <code>src/tally/__init__.py</code></summary>

```diff
@@ -4,6 +4,7 @@ import sys
 
 
 def count(text: str) -> dict[str, int]:
+    "How many times each word of `text` appears, ignoring case."
     counts = {}
     for word in text.lower().split():
         counts[word] = counts.get(word, 0) + 1
```

</details>

[This change on GitHub](https://github.com/rahuldave/tally/commit/f79588d3b046ec2787725cdb6e3fcf952014e078). [The code after it](https://github.com/rahuldave/tally/tree/f79588d3b046ec2787725cdb6e3fcf952014e078).

<a id="step-05"></a>

## 5 The most common words, and a report

```bash
just setup
```

tally prints a line for every word, in alphabetical order. A reader of a long text wants the most common words
first, and only a few of them. A function finds them, and an option of the command prints them. A recipe writes a
report of the ten most common words of the corpus.

[The code before this part](https://github.com/rahuldave/tally/tree/f79588d3b046ec2787725cdb6e3fcf952014e078). [The code after it](https://github.com/rahuldave/tally/tree/9e37b6eed29516f62bc176d1eaa66bf4e86683a6).

<a id="step-05.1"></a>

### 5.1 A function for the most common words

`count` gives the counts in no useful order. To find the most common words, tally must sort the counts, most common
first, and keep the first few. A function, `top`, does it. It sorts by count, highest first, and then by the
word, so that two words with the same count keep one order. Then it keeps the first `n`.

A patch to [`src/tally/__init__.py`](#step-05.1-src-tally-__init__.py-b5485b).

A test says what `top` must give. It gives `top` three words with their counts, and asks for the two most common.

A patch to [`tests/test_top.py`](#step-05.1-tests-test_top.py-1f85fe).

In `src/tally/__init__.py`, `top` stands between `count` and `main`. It sorts with the key `(-pair[1], pair[0])`.
The key is the count with a minus sign, so that the highest count comes first, and then the word. The new file
`tests/test_top.py` has one test, `test_most_common_first`.

```bash
uv run python -m unittest discover -s tests -q
```

The four tests pass.

#### What changed

- <a id="step-05.1-src-tally-__init__.py-b5485b"></a>`src/tally/__init__.py`: sort by count, most common first, then by the word. 5 lines added. [The file](https://github.com/rahuldave/tally/blob/72a0129dcee765132ad267788636ff4af9066369/src/tally/__init__.py).
  - look at `return sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))[:n]`
- <a id="step-05.1-tests-test_top.py-1f85fe"></a>`tests/test_top.py`: its test, with three words. New, 8 lines. [The file](https://github.com/rahuldave/tally/blob/72a0129dcee765132ad267788636ff4af9066369/tests/test_top.py).

<details><summary>The diff of <code>src/tally/__init__.py</code></summary>

```diff
@@ -11,6 +11,11 @@ def count(text: str) -> dict[str, int]:
     return counts
 
 
+def top(counts: dict[str, int], n: int) -> list[tuple[str, int]]:
+    "The n most common words, most common first."
+    return sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))[:n]
+
+
 def main() -> None:
     text = open(sys.argv[1]).read() if len(sys.argv) > 1 else sys.stdin.read()
     for word, n in sorted(count(text).items()):
```

</details>

<details><summary>The diff of <code>tests/test_top.py</code></summary>

```diff
@@ -0,0 +1,8 @@
+import unittest
+
+from tally import top
+
+
+class Top(unittest.TestCase):
+    def test_most_common_first(self):
+        self.assertEqual(top({"a": 1, "b": 3, "c": 2}, 2), [("b", 3), ("c", 2)])
```

</details>

[This change on GitHub](https://github.com/rahuldave/tally/commit/72a0129dcee765132ad267788636ff4af9066369). [The code after it](https://github.com/rahuldave/tally/tree/72a0129dcee765132ad267788636ff4af9066369).

<a id="step-05.2"></a>

### 5.2 tally --top N

tally prints every word of a text, and the corpus fills the screen. An option, `--top N`, makes `main` print only the
`N` most common words, with `top`. Without the option, `main` prints every count, as before. `main` reads the
option before the name of the file, so the command is `tally --top 3 data/corpus.txt`.

A patch to [`src/tally/__init__.py`](#step-05.2-src-tally-__init__.py-b5485b).

In `src/tally/__init__.py`, `main` now has a docstring, and the three lines under the docstring read the option.
When the first argument is `--top`, the second is the number `N`, and the name of the file comes after them. The
loop prints `top(counts, n)` when there is an `N`, and every count when there is not.

```bash
uv run tally --top 3 data/corpus.txt
```

The command prints three lines, the most common word first. They are `127 line`, `126 class` and `125 word`.

#### What changed

- <a id="step-05.2-src-tally-__init__.py-b5485b"></a>`src/tally/__init__.py`: `main` reads the option before the name of the file. 8 lines added, 3 removed. [The file](https://github.com/rahuldave/tally/blob/c4b92c9bd158cd85d783cf17adc6bedc76c9ba0d/src/tally/__init__.py).
  - look at `if args[:1] == ["--top"]:`

<details><summary>The diff of <code>src/tally/__init__.py</code></summary>

```diff
@@ -17,6 +17,11 @@ def top(counts: dict[str, int], n: int) -> list[tuple[str, int]]:
 
 
 def main() -> None:
-    text = open(sys.argv[1]).read() if len(sys.argv) > 1 else sys.stdin.read()
-    for word, n in sorted(count(text).items()):
-        print(n, word)
+    "Count the words of a file, or of the standard input. With --top N, only the N most common."
+    args, n = sys.argv[1:], None
+    if args[:1] == ["--top"]:
+        n, args = int(args[1]), args[2:]
+    text = open(args[0]).read() if args else sys.stdin.read()
+    counts = count(text)
+    for word, times in top(counts, n) if n else sorted(counts.items()):
+        print(times, word)
```

</details>

[This change on GitHub](https://github.com/rahuldave/tally/commit/c4b92c9bd158cd85d783cf17adc6bedc76c9ba0d). [The code after it](https://github.com/rahuldave/tally/tree/c4b92c9bd158cd85d783cf17adc6bedc76c9ba0d).

<a id="step-05.3"></a>

### 5.3 A report, which just setup makes

The most common words of the corpus make a report, which others want to read without running tally. A recipe of
the `justfile`, `report`, writes the ten most common words to `build/top.txt`. The recipe has two lines, and `just`
prints each line before it runs it. The second line has two parts.

- **`mkdir -p build`** makes the folder `build`, and does nothing when the folder is there.
- **`uv run tally --top 10 data/corpus.txt`** counts the corpus, and keeps the ten most common words.
- **`> build/top.txt`** sends what tally prints to the file, in place of the terminal.

A patch to [`justfile`](#step-05.3-justfile-424f0b).

The report is an artifact, as the corpus is. git ignores the folder `build/`, so git holds the recipe, and not the
report. `just setup` makes the report when the file is missing. `test -f build/top.txt` is true when the file is
there, and `||` runs `just report` only when it is not.

At the end of the `justfile`, the new recipe `report` makes the folder `build`, and writes the report into it. In
the recipe `setup`, the new last line runs `just report` when `build/top.txt` is missing.

A report from an earlier run stays, because git ignores it. So remove the report first, and then `just setup` makes
it again:

```bash
rm -f build/top.txt
just setup
cat build/top.txt
```

The file has ten lines, the most common word first.

#### What changed

- <a id="step-05.3-justfile-424f0b"></a>`justfile`: the report, and the line in `setup` that makes it when it is missing. 6 lines added. [The file](https://github.com/rahuldave/tally/blob/9e37b6eed29516f62bc176d1eaa66bf4e86683a6/justfile).
  - look at `uv run tally --top 10 data/corpus.txt > build/top.txt`
  - look at `test -f build/top.txt || just report`

<details><summary>The diff of <code>justfile</code></summary>

```diff
@@ -6,6 +6,7 @@ default:
 setup:
     uv sync
     uv run python scripts/corpus.py data/corpus.txt
+    test -f build/top.txt || just report
 
 # Count the words of a file
 run file:
@@ -14,3 +15,8 @@ run file:
 # Run the tests
 test:
     uv run python -m unittest discover -s tests -q
+
+# Write the ten most common words of the corpus to build/top.txt
+report:
+    mkdir -p build
+    uv run tally --top 10 data/corpus.txt > build/top.txt
```

</details>

[This change on GitHub](https://github.com/rahuldave/tally/commit/9e37b6eed29516f62bc176d1eaa66bf4e86683a6). [The code after it](https://github.com/rahuldave/tally/tree/9e37b6eed29516f62bc176d1eaa66bf4e86683a6).

<a id="step-06"></a>

## 6 How to run it

```bash
just setup
```

A new user of tally does not know which commands to run, or in which order. The README gets a section, "Run it",
that says how to run tally, its tests and its report. The code does not change.

A patch to [`README.md`](#step-06-README.md-8ec9a0).

At the end of `README.md`, the new section "Run it" gives the two commands to run first, `just setup` and then
tally on the corpus. Under them, it names the option `--top`, the tests and the report.

```bash
uv run tally --top 3 data/corpus.txt
just test
```

The command prints the three most common words of the corpus, and the tests pass. tally is finished.

### What changed

- <a id="step-06-README.md-8ec9a0"></a>`README.md`: the commands that a new user needs first, in the order to run them. 10 lines added. [The file](https://github.com/rahuldave/tally/blob/974d653080b0bd7dd06741b60225518cfecc908e/README.md).
  - look at `## Run it`

<details><summary>The diff of <code>README.md</code></summary>

```diff
@@ -1,3 +1,13 @@
 # tally
 
 Count the words in a text.
+
+## Run it
+
+Make the environment, the corpus and the report first. Then count the words of a file:
+
+    just setup
+    uv run tally data/corpus.txt
+
+`uv run tally --top 10 data/corpus.txt` prints only the ten most common words. `just test` runs the tests, and
+`just report` writes the ten most common words of the corpus to `build/top.txt`.
```

</details>

[This change on GitHub](https://github.com/rahuldave/tally/compare/9e37b6eed29516f62bc176d1eaa66bf4e86683a6...974d653080b0bd7dd06741b60225518cfecc908e). [The code after it](https://github.com/rahuldave/tally/tree/974d653080b0bd7dd06741b60225518cfecc908e).
