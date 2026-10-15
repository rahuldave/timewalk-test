<!-- Made by the walk skill's render.py from the facts of the walk. Do not edit it by hand: run just walk-update again. -->

# Tests first, on the parts branch

**Read the tutorial.** Each change explained, with the code to look at.

Each part ends with a section called **What changed**. It lists every file that the part changes, with a link to the file, and then the whole diff of each file, folded. A lockfile and a binary file have a link alone. The text above it explains the change.

We build the same counting code as the main history of tally, in another order. Here each test comes with the code
that it tests, and not after it. This history is on a branch of its own, `parts`, which leaves `main` where the
project begins.

<a id="parts-01"></a>

## 1 The code, with its test

```bash
just setup
```

Code and its test arrive together, so the test checks the code from the first day. Read `tests/test_count.py`,
then `count`.

```bash
uv run python -m unittest discover -s tests -v
git log --oneline --graph --all | head -12
```

Both tests pass. The graph shows the branch `parts`, which leaves `main` where the project begins.

> Ask: is it easier to read a test before the code, or after?

### What changed

- <a id="parts-01-.gitignore-a5cc29"></a>`.gitignore`: New, 10 lines. [The file](https://github.com/rahuldave/tally/blob/e416331e1414a145c9a4e84a49ccd119cbaf2168/.gitignore).
- <a id="parts-01-.python-version-7696e9"></a>`.python-version`: New, 1 line. [The file](https://github.com/rahuldave/tally/blob/e416331e1414a145c9a4e84a49ccd119cbaf2168/.python-version).
- <a id="parts-01-README.md-8ec9a0"></a>`README.md`: New, 3 lines. [The file](https://github.com/rahuldave/tally/blob/e416331e1414a145c9a4e84a49ccd119cbaf2168/README.md).
- <a id="parts-01-justfile-424f0b"></a>`justfile`: adds `recipe default`, `recipe run`, `recipe setup`, `recipe test`. New, 15 lines. [The file](https://github.com/rahuldave/tally/blob/e416331e1414a145c9a4e84a49ccd119cbaf2168/justfile).
- <a id="parts-01-pyproject.toml-5d07e7"></a>`pyproject.toml`: New, 14 lines. [The file](https://github.com/rahuldave/tally/blob/e416331e1414a145c9a4e84a49ccd119cbaf2168/pyproject.toml).
- <a id="parts-01-src-tally-__init__.py-b5485b"></a>`src/tally/__init__.py`: `count`, which ignores case from the first day, and the command. New, 16 lines. [The file](https://github.com/rahuldave/tally/blob/e416331e1414a145c9a4e84a49ccd119cbaf2168/src/tally/__init__.py).
  - look at `for word in text.lower().split():`
- <a id="parts-01-src-tally-__main__.py-534c24"></a>`src/tally/__main__.py`: New, 3 lines. [The file](https://github.com/rahuldave/tally/blob/e416331e1414a145c9a4e84a49ccd119cbaf2168/src/tally/__main__.py).
- <a id="parts-01-tests-test_count.py-e674f6"></a>`tests/test_count.py`: a test of counting, and a test of case. New, 11 lines. [The file](https://github.com/rahuldave/tally/blob/e416331e1414a145c9a4e84a49ccd119cbaf2168/tests/test_count.py).
  - look at `self.assertEqual(count("A a"), {"a": 2})`
- <a id="parts-01-uv.lock-8356d8"></a>`uv.lock`: New, 8 lines. [The file](https://github.com/rahuldave/tally/blob/e416331e1414a145c9a4e84a49ccd119cbaf2168/uv.lock).

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

[The code](https://github.com/rahuldave/tally/tree/e416331e1414a145c9a4e84a49ccd119cbaf2168).

<a id="parts-02"></a>

## 2 One more test

```bash
just setup
```

An empty text has no words, and `count` must give an empty dictionary for it. A test of an empty text says so. It
passes at once, because `count` already handles it.

```bash
uv run python -m unittest discover -s tests -v
echo "" | uv run tally && echo "(nothing, as the test says)"
```

The three tests pass, and tally prints nothing for an empty text.

### What changed

- <a id="parts-02-tests-test_empty.py-ffb51e"></a>`tests/test_empty.py`: an empty text counts nothing. New, 8 lines. [The file](https://github.com/rahuldave/tally/blob/2792637d83ba3d968e83427f008dc24b2517b400/tests/test_empty.py).
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

[This change on GitHub](https://github.com/rahuldave/tally/compare/e416331e1414a145c9a4e84a49ccd119cbaf2168...2792637d83ba3d968e83427f008dc24b2517b400). [The code after it](https://github.com/rahuldave/tally/tree/2792637d83ba3d968e83427f008dc24b2517b400).
