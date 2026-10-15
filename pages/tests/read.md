<!-- Made by the walk skill's render.py from the facts of the walk. Do not edit it by hand: run just walk-update again. -->

# Only the tests

**Read the tutorial.** Each change explained, with the code to look at.

Each part ends with a section called **What changed**. It lists every file that the part changes, with a link to the file, and then the whole diff of each file, folded. A lockfile and a binary file have a link alone. The text above it explains the change. What changed is what you check your files against.

We follow tally, a word counter, through the three places where its tests matter. We see it before any test, then
when the tests come, and last when new code comes with a test of its own. Every command runs through uv.

<a id="step-01"></a>

## 1 Before any test

```bash
just setup
```

tally counts words, and nothing checks it. Read `count` in `src/tally/__init__.py`, and ask what could go wrong.

```bash
echo "a b a" | uv run tally
echo "The the" | uv run tally
```

The second command counts "The" and "the" as two words. Nothing says whether that is right.

> Ask: write down one test you would add, before we look at ours.

### What changed

- <a id="step-01-.gitignore-a5cc29"></a>`.gitignore`: New, 10 lines. [The file](https://github.com/rahuldave/tally/blob/eb951f74756383392f528427a0cf44e135d5c64f/.gitignore).
- <a id="step-01-.python-version-7696e9"></a>`.python-version`: New, 1 line. [The file](https://github.com/rahuldave/tally/blob/eb951f74756383392f528427a0cf44e135d5c64f/.python-version).
- <a id="step-01-README.md-8ec9a0"></a>`README.md`: New, 3 lines. [The file](https://github.com/rahuldave/tally/blob/eb951f74756383392f528427a0cf44e135d5c64f/README.md).
- <a id="step-01-justfile-424f0b"></a>`justfile`: adds `recipe default`, `recipe run`, `recipe setup`, `recipe test`. New, 15 lines. [The file](https://github.com/rahuldave/tally/blob/eb951f74756383392f528427a0cf44e135d5c64f/justfile).
- <a id="step-01-pyproject.toml-5d07e7"></a>`pyproject.toml`: New, 14 lines. [The file](https://github.com/rahuldave/tally/blob/eb951f74756383392f528427a0cf44e135d5c64f/pyproject.toml).
- <a id="step-01-src-tally-__init__.py-b5485b"></a>`src/tally/__init__.py`: `count`, and the command that uses it. New, 16 lines. [The file](https://github.com/rahuldave/tally/blob/eb951f74756383392f528427a0cf44e135d5c64f/src/tally/__init__.py).
  - look at `for word in text.split():`
- <a id="step-01-src-tally-__main__.py-534c24"></a>`src/tally/__main__.py`: New, 3 lines. [The file](https://github.com/rahuldave/tally/blob/eb951f74756383392f528427a0cf44e135d5c64f/src/tally/__main__.py).
- <a id="step-01-uv.lock-8356d8"></a>`uv.lock`: New, 8 lines. [The file](https://github.com/rahuldave/tally/blob/eb951f74756383392f528427a0cf44e135d5c64f/uv.lock).

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

<a id="step-02"></a>

## 2 Two tests

```bash
just setup
```

A test gives `count` a text, and compares what it gives back with what we expect. `tests/test_count.py` holds two
tests, and `tests/test_empty.py` one. The test of case failed until `count` ignored case, with one word, `lower()`.

```bash
uv run python -m unittest discover -s tests -v
echo "The the" | uv run tally
```

All three tests pass, and the command now prints `2 the` for "The the".

### What changed

- <a id="step-02-src-tally-__init__.py-b5485b"></a>`src/tally/__init__.py`: the word that answers the test of case. 1 line added, 1 removed. [The file](https://github.com/rahuldave/tally/blob/bfcbe07463b5c6f3c0764e4ac19a054cb0acee20/src/tally/__init__.py).
  - look at `for word in text.lower().split():`
- <a id="step-02-tests-test_count.py-e674f6"></a>`tests/test_count.py`: a test of counting, and a test of case. New, 11 lines. [The file](https://github.com/rahuldave/tally/blob/bfcbe07463b5c6f3c0764e4ac19a054cb0acee20/tests/test_count.py).
  - look at `self.assertEqual(count("A a"), {"a": 2})`
- <a id="step-02-tests-test_empty.py-ffb51e"></a>`tests/test_empty.py`: an empty text counts nothing. New, 8 lines. [The file](https://github.com/rahuldave/tally/blob/bfcbe07463b5c6f3c0764e4ac19a054cb0acee20/tests/test_empty.py).

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

[This change on GitHub](https://github.com/rahuldave/tally/compare/eb951f74756383392f528427a0cf44e135d5c64f...bfcbe07463b5c6f3c0764e4ac19a054cb0acee20). [The code after it](https://github.com/rahuldave/tally/tree/bfcbe07463b5c6f3c0764e4ac19a054cb0acee20).

<a id="step-05"></a>

## 5 Still green

```bash
just setup
```

Much later, `top` comes with a test of its own, and the old tests still pass. The types and the docstring that came
in between did not change a test. The tests check what the code does, and not how it says it.

```bash
uv run python -m unittest discover -s tests -v
uv run tally --top 3 data/corpus.txt
```

The four tests pass, and the command prints the three most common words of the corpus.

### What changed

- <a id="step-05-.gitignore-a5cc29"></a>`.gitignore`: git does not hold the corpus. 3 lines added. [The file](https://github.com/rahuldave/tally/blob/9e37b6eed29516f62bc176d1eaa66bf4e86683a6/.gitignore).
- <a id="step-05-justfile-424f0b"></a>`justfile`: `just setup` makes the corpus and the report. 7 lines added. [The file](https://github.com/rahuldave/tally/blob/9e37b6eed29516f62bc176d1eaa66bf4e86683a6/justfile).
- <a id="step-05-pyproject.toml-5d07e7"></a>`pyproject.toml`: ruff, and its line length. 8 lines added. [The file](https://github.com/rahuldave/tally/blob/9e37b6eed29516f62bc176d1eaa66bf4e86683a6/pyproject.toml).
- <a id="step-05-scripts-corpus.py-ab344b"></a>`scripts/corpus.py`: the script that writes the corpus. New, 25 lines. [The file](https://github.com/rahuldave/tally/blob/9e37b6eed29516f62bc176d1eaa66bf4e86683a6/scripts/corpus.py).
- <a id="step-05-src-tally-__init__.py-b5485b"></a>`src/tally/__init__.py`: types, a docstring, `top` and the option `--top`. 15 lines added, 4 removed. [The file](https://github.com/rahuldave/tally/blob/9e37b6eed29516f62bc176d1eaa66bf4e86683a6/src/tally/__init__.py).
- <a id="step-05-tests-test_top.py-1f85fe"></a>`tests/test_top.py`: the new test, of `top`. New, 8 lines. [The file](https://github.com/rahuldave/tally/blob/9e37b6eed29516f62bc176d1eaa66bf4e86683a6/tests/test_top.py).
- <a id="step-05-uv.lock-8356d8"></a>`uv.lock`: the exact version of ruff. 35 lines added. [The file](https://github.com/rahuldave/tally/blob/9e37b6eed29516f62bc176d1eaa66bf4e86683a6/uv.lock).

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
@@ -5,6 +5,8 @@ default:
 # Make the environment of this step: the first command of every step
 setup:
     uv sync
+    uv run python scripts/corpus.py data/corpus.txt
+    test -f build/top.txt || just report
 
 # Count the words of a file
 run file:
@@ -13,3 +15,8 @@ run file:
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

<details><summary>The diff of <code>pyproject.toml</code></summary>

```diff
@@ -12,3 +12,11 @@ tally = "tally:main"
 [build-system]
 requires = ["uv_build>=0.12.13,<0.13.0"]
 build-backend = "uv_build"
+
+[dependency-groups]
+dev = [
+    "ruff>=0.17.0",
+]
+
+[tool.ruff]
+line-length = 100
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

<details><summary>The diff of <code>src/tally/__init__.py</code></summary>

```diff
@@ -3,14 +3,25 @@
 import sys
 
 
-def count(text):
+def count(text: str) -> dict[str, int]:
+    "How many times each word of `text` appears, ignoring case."
     counts = {}
     for word in text.lower().split():
         counts[word] = counts.get(word, 0) + 1
     return counts
 
 
+def top(counts: dict[str, int], n: int) -> list[tuple[str, int]]:
+    "The n most common words, most common first."
+    return sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))[:n]
+
+
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

[This change on GitHub](https://github.com/rahuldave/tally/compare/bfcbe07463b5c6f3c0764e4ac19a054cb0acee20...9e37b6eed29516f62bc176d1eaa66bf4e86683a6). [The code after it](https://github.com/rahuldave/tally/tree/9e37b6eed29516f62bc176d1eaa66bf4e86683a6).
