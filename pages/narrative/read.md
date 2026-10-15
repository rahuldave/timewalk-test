<!-- Made by the walk skill's render.py from the facts of the walk. Do not edit it by hand: run just walk-update again. -->

# tally, step by step

**Read the tutorial.** Each change explained, with the code to look at.

Each part ends with a section called **What changed**. It lists every file that the part changes, with a link to the file, and then the whole diff of each file, folded. A lockfile and a binary file have a link alone. The text above it explains the change. What changed is what you check your files against.

We follow tally, a word counter, from a project that does nothing to a command with tests, types and a report.
tally is a uv project from the beginning. Every command runs through `uv run`, in the project's own `.venv`, and
never in the Python of the system. Each part begins with `just setup`, which brings the environment and the files
that the code needs up to date. `just setup` never changes git.

<a id="step-00"></a>

## 0 Where it starts

```bash
just setup
```

A project needs a place for its code, a command to run, and the same packages for everyone. tally is a uv project,
as `uv init --package` makes one. In `pyproject.toml`, the table `[project.scripts]` makes a command called
`tally`, and the table `[build-system]` lets uv install the project into its own `.venv`. `.python-version` and
`uv.lock` are in git, so every learner gets the same Python and the same packages.

`just setup` ran `uv sync`, which made `.venv`. git ignores `.venv`, so it stays as it is when the code changes.

```bash
uv run tally
ls -a
```

The command prints `tally: nothing to count yet`. The project has a command, and the command has no work.

```bash
# in the project, where you started
git log --oneline --decorate --all | head -20
```

> Ask: what should "the" and "The" count as?

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

A word counter must count. A function, `count`, splits a text into words and counts each one. `main` reads a
file, or the standard input when you give no file, and prints each word with its count.

```bash
echo "a b a" | uv run tally
echo "The the THE" | uv run tally
```

The first command prints `2 a` and `1 b`. The second prints three words of one each, because tally does not know
yet that they are one word. The second slide is a picture of what `count` does.

> Ask: is that a bug, and who decides?

### What changed

- <a id="step-01-src-tally-__init__.py-b5485b"></a>`src/tally/__init__.py`: `count`, and a `main` that reads the text and prints the counts. 12 lines added, 1 removed. [The file](https://github.com/rahuldave/tally/blob/eb951f74756383392f528427a0cf44e135d5c64f/src/tally/__init__.py).
  - look at `counts[word] = counts.get(word, 0) + 1`

<details><summary>The diff of <code>src/tally/__init__.py</code></summary>

```diff
@@ -1,5 +1,16 @@
 """tally: count the words in a text."""
 
+import sys
+
+
+def count(text):
+    counts = {}
+    for word in text.split():
+        counts[word] = counts.get(word, 0) + 1
+    return counts
+
 
 def main() -> None:
-    print("tally: nothing to count yet")
+    text = open(sys.argv[1]).read() if len(sys.argv) > 1 else sys.stdin.read()
+    for word, n in sorted(count(text).items()):
+        print(n, word)
```

</details>

[This change on GitHub](https://github.com/rahuldave/tally/compare/6a63758166d3aeee516faa6244414d7b54b5a730...eb951f74756383392f528427a0cf44e135d5c64f). [The code after it](https://github.com/rahuldave/tally/tree/eb951f74756383392f528427a0cf44e135d5c64f).

<a id="step-02"></a>

## 2 Tests

```bash
just setup
```

We cannot tell whether `count` still works after a change, unless we try it by hand each time. Tests try it for
us. Two files of tests hold three tests, and one of them fails until counting ignores case. The fix is one word in
`count`, `lower()`. Read `tests/test_count.py` first, then the fix.

```bash
uv run python -m unittest discover -s tests -q
echo "The the THE" | uv run tally
```

The tests pass, and the second command now prints `3 the`.

A code block in the notes is code to read, not a command to run:

```
$ this line is not a button
```

### What changed

- <a id="step-02-src-tally-__init__.py-b5485b"></a>`src/tally/__init__.py`: the fix, one word. 1 line added, 1 removed. [The file](https://github.com/rahuldave/tally/blob/bfcbe07463b5c6f3c0764e4ac19a054cb0acee20/src/tally/__init__.py).
  - look at `for word in text.lower().split():`
- <a id="step-02-tests-test_count.py-e674f6"></a>`tests/test_count.py`: two tests, and `test_case` is the one that failed. New, 11 lines. [The file](https://github.com/rahuldave/tally/blob/bfcbe07463b5c6f3c0764e4ac19a054cb0acee20/tests/test_count.py).
- <a id="step-02-tests-test_empty.py-ffb51e"></a>`tests/test_empty.py`: an empty text counts nothing. New, 8 lines. [The file](https://github.com/rahuldave/tally/blob/bfcbe07463b5c6f3c0764e4ac19a054cb0acee20/tests/test_empty.py).
  - look at `self.assertEqual(count(""), {})`

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

<a id="step-03"></a>

## 3 Formatting, and a corpus

```bash
just setup
```

Code in one style is easier to read and to change, and a count of three words shows little. So ruff, a formatter
and linter, comes in as a tool for development. `uv add --dev ruff` wrote it into the group `dev` of
`pyproject.toml`, and into `uv.lock`, and `just setup` installs it. ruff also gets a line length in
`pyproject.toml`.

And `just setup` now makes an artifact, `data/corpus.txt`, a text of 2000 words, with `scripts/corpus.py`. An
artifact is a file that the project makes and git does not hold. `.gitignore` names `data/`, so git leaves the
corpus alone, and it stays when the code changes.

```bash
uv run ruff format --check
head -3 data/corpus.txt
uv run tally data/corpus.txt | sort -rn | head -5
just setup
```

The second `just setup` prints `data/corpus.txt is there`, and leaves the corpus alone.

Edit the code, as a learner would. This command adds a comment at the end of `src/tally/__init__.py`:

```bash
printf '\n# an edit made in class\n' >> src/tally/__init__.py
```

### What changed

- <a id="step-03-.gitignore-a5cc29"></a>`.gitignore`: git does not hold the corpus. 3 lines added. [The file](https://github.com/rahuldave/tally/blob/1568a522d23312c59c6e42cb027ec25ba3ae8b35/.gitignore).
  - look at `data/`
- <a id="step-03-justfile-424f0b"></a>`justfile`: `just setup` runs the script. 1 line added. [The file](https://github.com/rahuldave/tally/blob/1568a522d23312c59c6e42cb027ec25ba3ae8b35/justfile).
  - look at `uv run python scripts/corpus.py data/corpus.txt`
- <a id="step-03-pyproject.toml-5d07e7"></a>`pyproject.toml`: the group `dev`, with ruff, and the line length. 8 lines added. [The file](https://github.com/rahuldave/tally/blob/1568a522d23312c59c6e42cb027ec25ba3ae8b35/pyproject.toml).
  - look at `line-length = 100`
- <a id="step-03-scripts-corpus.py-ab344b"></a>`scripts/corpus.py`: writes the same 2000 words each time, and leaves a corpus that is there alone. New, 25 lines. [The file](https://github.com/rahuldave/tally/blob/1568a522d23312c59c6e42cb027ec25ba3ae8b35/scripts/corpus.py).
- <a id="step-03-uv.lock-8356d8"></a>`uv.lock`: the exact version of ruff. 35 lines added. [The file](https://github.com/rahuldave/tally/blob/1568a522d23312c59c6e42cb027ec25ba3ae8b35/uv.lock).
  - look at `name = "ruff"`

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

[This change on GitHub](https://github.com/rahuldave/tally/compare/bfcbe07463b5c6f3c0764e4ac19a054cb0acee20...1568a522d23312c59c6e42cb027ec25ba3ae8b35). [The code after it](https://github.com/rahuldave/tally/tree/1568a522d23312c59c6e42cb027ec25ba3ae8b35).

<a id="step-04"></a>

## 4 Types and docs

```bash
just setup
```

To learn what `count` takes and gives, a reader had to read its body. Now its signature says so, with types, and a
docstring says in one line what it does. What `count` does is the same.

```bash
uv run python -c "import tally; help(tally.count)" | head -6
uv run python -m unittest discover -s tests -q
```

`help` prints the signature and the docstring, and the tests pass as before.

> Ask: who reads a type hint, the person, the editor, or Python?

### What changed

- <a id="step-04-src-tally-__init__.py-b5485b"></a>`src/tally/__init__.py`: the types in the signature of `count`, and its docstring. 2 lines added, 1 removed. [The file](https://github.com/rahuldave/tally/blob/f79588d3b046ec2787725cdb6e3fcf952014e078/src/tally/__init__.py).
  - look at `def count(text: str) -> dict[str, int]:`

<details><summary>The diff of <code>src/tally/__init__.py</code></summary>

```diff
@@ -3,7 +3,8 @@
 import sys
 
 
-def count(text):
+def count(text: str) -> dict[str, int]:
+    "How many times each word of `text` appears, ignoring case."
     counts = {}
     for word in text.lower().split():
         counts[word] = counts.get(word, 0) + 1
```

</details>

[This change on GitHub](https://github.com/rahuldave/tally/compare/1568a522d23312c59c6e42cb027ec25ba3ae8b35...f79588d3b046ec2787725cdb6e3fcf952014e078). [The code after it](https://github.com/rahuldave/tally/tree/f79588d3b046ec2787725cdb6e3fcf952014e078).

<a id="step-05"></a>

## 5 The most common words

```bash
just setup
```

A reader of a long text wants the most common words first, and only a few. `top` returns the most common words,
`tally --top N` prints them, and `just report` writes them to `build/top.txt`. That report is an artifact too.
`just setup` makes it when it is missing, so a learner who comes straight here still has it.

```bash
cat build/top.txt
uv run tally --top 3 data/corpus.txt
just test
```

A long command runs in a terminal of its own, so the first terminal stays free. A second long command runs in a
third terminal:

```bash
# in a second terminal
for i in 1 2 3 4 5; do echo "epoch $i"; sleep 1; done
for i in 1 2 3; do echo "sweep $i"; sleep 2; done
rm build/top.txt; just setup; ls build
```

### What changed

- <a id="step-05-justfile-424f0b"></a>`justfile`: the recipe `report`, and the line of `setup` that runs it. 6 lines added. [The file](https://github.com/rahuldave/tally/blob/9e37b6eed29516f62bc176d1eaa66bf4e86683a6/justfile).
  - look at `test -f build/top.txt || just report`
- <a id="step-05-src-tally-__init__.py-b5485b"></a>`src/tally/__init__.py`: `top`, and the option `--top` of `main`. 13 lines added, 3 removed. [The file](https://github.com/rahuldave/tally/blob/9e37b6eed29516f62bc176d1eaa66bf4e86683a6/src/tally/__init__.py).
  - look at `if args[:1] == ["--top"]:`
- <a id="step-05-tests-test_top.py-1f85fe"></a>`tests/test_top.py`: the test of `top`. New, 8 lines. [The file](https://github.com/rahuldave/tally/blob/9e37b6eed29516f62bc176d1eaa66bf4e86683a6/tests/test_top.py).

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

<details><summary>The diff of <code>src/tally/__init__.py</code></summary>

```diff
@@ -11,7 +11,17 @@ def count(text: str) -> dict[str, int]:
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

[This change on GitHub](https://github.com/rahuldave/tally/compare/f79588d3b046ec2787725cdb6e3fcf952014e078...9e37b6eed29516f62bc176d1eaa66bf4e86683a6). [The code after it](https://github.com/rahuldave/tally/tree/9e37b6eed29516f62bc176d1eaa66bf4e86683a6).

<a id="step-06"></a>

## 6 How to run it

```bash
just setup
```

A new user does not know which commands to run first. The README now says how to run tally, its tests and its
report. Only `README.md` changes, so the code is as it was.

```bash
uv run tally --top 3 data/corpus.txt
```

> Ask: what else would a new user ask before they run it?

### What changed

- <a id="step-06-README.md-8ec9a0"></a>`README.md`: a section, "Run it", with the commands that a new user needs first. 10 lines added. [The file](https://github.com/rahuldave/tally/blob/974d653080b0bd7dd06741b60225518cfecc908e/README.md).
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
