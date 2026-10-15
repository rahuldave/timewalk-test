<!-- Made by the walk skill's render.py from the facts of the walk. Do not edit it by hand: run just walk-update again. -->

# A bigger tally, with the author's exact versions

**Read the tutorial.** Each change explained, with the code to look at. [Build it yourself](build.md) is the other way to read it.

Each part ends with a section called **What changed**. It lists every file that the part changes, with a link to the file, and then the whole diff of each file, folded. A lockfile and a binary file have a link alone. The text above it explains the change.

tally counts words, has tests, and writes a report. Now it grows as a real project does. It gets a dependency with
a range of versions, and a tool for its docs in a group of its own. It gets a page of docs with a picture, and a
library of its own in the same workspace. Then ruff passes its code. Last, it drops a dependency that it no longer
needs.

We make each change in moves. A move is one small change, made by one patch or by one command. You make each move,
and the page checks your files against it.

<a id="extra-00"></a>

## 0 Where it starts

```bash
just setup
```

tally counts the words of a file, and `--top N` keeps the most common. Run it on the corpus, to see where we begin.

```bash
uv run tally --top 3 data/corpus.txt
```

It prints `127 line`, `126 class` and `125 word`, one to a line.

### What changed

- <a id="extra-00-.gitignore-a5cc29"></a>`.gitignore`: New, 13 lines. [The file](https://github.com/rahuldave/tally/blob/974d653080b0bd7dd06741b60225518cfecc908e/.gitignore).
- <a id="extra-00-.python-version-7696e9"></a>`.python-version`: New, 1 line. [The file](https://github.com/rahuldave/tally/blob/974d653080b0bd7dd06741b60225518cfecc908e/.python-version).
- <a id="extra-00-README.md-8ec9a0"></a>`README.md`: New, 13 lines. [The file](https://github.com/rahuldave/tally/blob/974d653080b0bd7dd06741b60225518cfecc908e/README.md).
- <a id="extra-00-justfile-424f0b"></a>`justfile`: adds `recipe default`, `recipe report`, `recipe run`, `recipe setup`, `recipe test`. New, 22 lines. [The file](https://github.com/rahuldave/tally/blob/974d653080b0bd7dd06741b60225518cfecc908e/justfile).
- <a id="extra-00-pyproject.toml-5d07e7"></a>`pyproject.toml`: New, 22 lines. [The file](https://github.com/rahuldave/tally/blob/974d653080b0bd7dd06741b60225518cfecc908e/pyproject.toml).
- <a id="extra-00-scripts-corpus.py-ab344b"></a>`scripts/corpus.py`: adds `main`. New, 25 lines. [The file](https://github.com/rahuldave/tally/blob/974d653080b0bd7dd06741b60225518cfecc908e/scripts/corpus.py).
- <a id="extra-00-src-tally-__init__.py-b5485b"></a>`src/tally/__init__.py`: adds `count`, `main`, `top`. New, 27 lines. [The file](https://github.com/rahuldave/tally/blob/974d653080b0bd7dd06741b60225518cfecc908e/src/tally/__init__.py).
- <a id="extra-00-src-tally-__main__.py-534c24"></a>`src/tally/__main__.py`: New, 3 lines. [The file](https://github.com/rahuldave/tally/blob/974d653080b0bd7dd06741b60225518cfecc908e/src/tally/__main__.py).
- <a id="extra-00-tests-test_count.py-e674f6"></a>`tests/test_count.py`: adds `class Count`, `test_case`, `test_words`. New, 11 lines. [The file](https://github.com/rahuldave/tally/blob/974d653080b0bd7dd06741b60225518cfecc908e/tests/test_count.py).
- <a id="extra-00-tests-test_empty.py-ffb51e"></a>`tests/test_empty.py`: adds `class Empty`, `test_empty`. New, 8 lines. [The file](https://github.com/rahuldave/tally/blob/974d653080b0bd7dd06741b60225518cfecc908e/tests/test_empty.py).
- <a id="extra-00-tests-test_top.py-1f85fe"></a>`tests/test_top.py`: adds `class Top`, `test_most_common_first`. New, 8 lines. [The file](https://github.com/rahuldave/tally/blob/974d653080b0bd7dd06741b60225518cfecc908e/tests/test_top.py).
- <a id="extra-00-uv.lock-8356d8"></a>`uv.lock`: New, 43 lines. [The file](https://github.com/rahuldave/tally/blob/974d653080b0bd7dd06741b60225518cfecc908e/uv.lock).

<details><summary>The diff of <code>.gitignore</code></summary>

```diff
@@ -0,0 +1,13 @@
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
+
+# Artifacts that just setup makes: they are not in git
+data/
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
@@ -0,0 +1,13 @@
+# tally
+
+Count the words in a text.
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

<details><summary>The diff of <code>justfile</code></summary>

```diff
@@ -0,0 +1,22 @@
+# The recipes of tally. Each one runs through uv, in the project's own environment.
+default:
+    @just --list
+
+# Make the environment of this step: the first command of every step
+setup:
+    uv sync
+    uv run python scripts/corpus.py data/corpus.txt
+    test -f build/top.txt || just report
+
+# Count the words of a file
+run file:
+    uv run tally {{ file }}
+
+# Run the tests
+test:
+    uv run python -m unittest discover -s tests -q
+
+# Write the ten most common words of the corpus to build/top.txt
+report:
+    mkdir -p build
+    uv run tally --top 10 data/corpus.txt > build/top.txt
```

</details>

<details><summary>The diff of <code>pyproject.toml</code></summary>

```diff
@@ -0,0 +1,22 @@
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
@@ -0,0 +1,27 @@
+"""tally: count the words in a text."""
+
+import sys
+
+
+def count(text: str) -> dict[str, int]:
+    "How many times each word of `text` appears, ignoring case."
+    counts = {}
+    for word in text.lower().split():
+        counts[word] = counts.get(word, 0) + 1
+    return counts
+
+
+def top(counts: dict[str, int], n: int) -> list[tuple[str, int]]:
+    "The n most common words, most common first."
+    return sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))[:n]
+
+
+def main() -> None:
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

[The code](https://github.com/rahuldave/tally/tree/974d653080b0bd7dd06741b60225518cfecc908e).

<a id="extra-01"></a>

## 1 A table, and a tool for the docs

```bash
just setup
```

A list of counts is hard to read at a glance. A table lines up the words and the counts. A small package,
tabulate, draws tables, so tally depends on it. The docs come later, and their tool comes now, in a group of its own.

[The code before this part](https://github.com/rahuldave/tally/tree/974d653080b0bd7dd06741b60225518cfecc908e). [The code after it](https://github.com/rahuldave/tally/tree/ec6a8aa7f9a8b81ef07c6c8ec69f01307482dc32).

<a id="extra-01.1"></a>

### 1.1 tabulate, in a range of versions

tally needs tabulate to draw a table. A new version 1.0 of tabulate could change how it draws one, so tally takes
any 0.9 version, and no later one. `uv add` with a range of versions puts the range in `pyproject.toml`, and the
exact version in `uv.lock`:

This change came from running `uv add "tabulate>=0.9,<0.10"`.

In `pyproject.toml`, the list `dependencies` now holds `tabulate>=0.9,<0.10`. In `uv.lock`, tabulate has the version
0.9.0, the one version in that range.

```bash
uv run python -c "import tabulate; print(tabulate.__version__)"
```

It prints `0.9.0`.

#### What changed

- <a id="extra-01.1-pyproject.toml-5d07e7"></a>`pyproject.toml`: tabulate, with the range of its versions. 3 lines added, 1 removed. It comes from `uv add "tabulate>=0.9,<0.10"`. [The file](https://github.com/rahuldave/tally/blob/418e7fd88a3f64b2a5a0f2ebd14b301694ce821e/pyproject.toml).
  - look at `"tabulate>=0.9,<0.10",`
- <a id="extra-01.1-uv.lock-8356d8"></a>`uv.lock`: the exact version of tabulate. 13 lines added. It comes from `uv add "tabulate>=0.9,<0.10"`. [The file](https://github.com/rahuldave/tally/blob/418e7fd88a3f64b2a5a0f2ebd14b301694ce821e/uv.lock).

<details><summary>The diff of <code>pyproject.toml</code></summary>

```diff
@@ -4,7 +4,9 @@ version = "0.1.0"
 description = "Count the words in a text"
 readme = "README.md"
 requires-python = ">=3.12"
-dependencies = []
+dependencies = [
+    "tabulate>=0.9,<0.10",
+]
 
 [project.scripts]
 tally = "tally:main"
```

</details>

[This change on GitHub](https://github.com/rahuldave/tally/commit/418e7fd88a3f64b2a5a0f2ebd14b301694ce821e). [The code after it](https://github.com/rahuldave/tally/tree/418e7fd88a3f64b2a5a0f2ebd14b301694ce821e).

<a id="extra-01.2"></a>

### 1.2 tally --table

tally prints one line for each word, with the count first. A new option, `--table`, prints the same counts as a
table, with a header. `main` takes the option out of the arguments, and passes the rows to `tabulate`.

A patch to [`src/tally/__init__.py`](#extra-01.2-src-tally-__init__.py-b5485b).

In `main` of `src/tally/__init__.py`, the flag `as_table` is true when the arguments hold `--table`. The rows then go
to `tabulate`, with the header `word` and `times`.

```bash
uv run tally --top 3 --table data/corpus.txt
```

It prints a header, `word` and `times`, a line of dashes, and the three words with their counts in a column on the
right.

#### What changed

- <a id="extra-01.2-src-tally-__init__.py-b5485b"></a>`src/tally/__init__.py`: the option `--table`, which prints the rows with tabulate. 11 lines added, 3 removed. [The file](https://github.com/rahuldave/tally/blob/5051c3ff6e71020d5458c29a2e4a1f358d361b16/src/tally/__init__.py).
  - look at `print(tabulate(rows, headers=["word", "times"]))`

<details><summary>The diff of <code>src/tally/__init__.py</code></summary>

```diff
@@ -2,6 +2,8 @@
 
 import sys
 
+from tabulate import tabulate
+
 
 def count(text: str) -> dict[str, int]:
     "How many times each word of `text` appears, ignoring case."
@@ -17,11 +19,17 @@ def top(counts: dict[str, int], n: int) -> list[tuple[str, int]]:
 
 
 def main() -> None:
-    "Count the words of a file, or of the standard input. With --top N, only the N most common."
-    args, n = sys.argv[1:], None
+    "Count the words of a file, or of the standard input. Options: --top N, and --table."
+    args = sys.argv[1:]
+    as_table = "--table" in args
+    args, n = [arg for arg in args if arg != "--table"], None
     if args[:1] == ["--top"]:
         n, args = int(args[1]), args[2:]
     text = open(args[0]).read() if args else sys.stdin.read()
     counts = count(text)
-    for word, times in top(counts, n) if n else sorted(counts.items()):
+    rows = top(counts, n) if n else sorted(counts.items())
+    if as_table:
+        print(tabulate(rows, headers=["word", "times"]))
+        return
+    for word, times in rows:
         print(times, word)
```

</details>

[This change on GitHub](https://github.com/rahuldave/tally/commit/5051c3ff6e71020d5458c29a2e4a1f358d361b16). [The code after it](https://github.com/rahuldave/tally/tree/5051c3ff6e71020d5458c29a2e4a1f358d361b16).

<a id="extra-01.3"></a>

### 1.3 mdformat, in the group docs

The docs will be Markdown files. mdformat formats Markdown, and its option `--check` says whether a file is
formatted. Only the people who write the docs need it, so it goes in a group of its own, `docs`:

This change came from running `uv add --group docs mdformat`.

`uv sync` installs the group `dev` and no other group, unless the project names more. One more line in the table
`[tool.uv]` of `pyproject.toml` names both groups, so that `just setup` installs mdformat too.

A patch to [`pyproject.toml`](#extra-01.3-pyproject.toml-5d07e7).

`pyproject.toml` has a group `docs` with mdformat, and at its end a table `[tool.uv]` whose `default-groups` names
`dev` and `docs`.

```bash
uv sync -q && uv run --no-sync mdformat --version
```

`uv sync` installs mdformat. Then `uv run --no-sync` runs it without another sync, and it prints `mdformat 1.0.0`, or a
newer version.

#### What changed

- <a id="extra-01.3-pyproject.toml-5d07e7"></a>`pyproject.toml`: the group `docs`, and the groups that `uv sync` installs. 6 lines added. It comes from `uv add --group docs mdformat`. [The file](https://github.com/rahuldave/tally/blob/ec6a8aa7f9a8b81ef07c6c8ec69f01307482dc32/pyproject.toml).
  - look at `default-groups = ["dev", "docs"]`
- <a id="extra-01.3-uv.lock-8356d8"></a>`uv.lock`: the exact versions of mdformat and of the packages it needs. 37 lines added. It comes from `uv add --group docs mdformat`. [The file](https://github.com/rahuldave/tally/blob/ec6a8aa7f9a8b81ef07c6c8ec69f01307482dc32/uv.lock).

<details><summary>The diff of <code>pyproject.toml</code></summary>

```diff
@@ -19,6 +19,12 @@ build-backend = "uv_build"
 dev = [
     "ruff>=0.17.0",
 ]
+docs = [
+    "mdformat>=1.0.0",
+]
 
 [tool.ruff]
 line-length = 100
+
+[tool.uv]
+default-groups = ["dev", "docs"]
```

</details>

[This change on GitHub](https://github.com/rahuldave/tally/commit/ec6a8aa7f9a8b81ef07c6c8ec69f01307482dc32). [The code after it](https://github.com/rahuldave/tally/tree/ec6a8aa7f9a8b81ef07c6c8ec69f01307482dc32).

<a id="extra-02"></a>

## 2 The docs

```bash
just setup
```

The README says in a few lines how to run tally. A user who wants more needs a page of docs. We write it piece by
piece, with a picture. The README then shows how to count from Python, and a recipe checks that the docs are
formatted.

[The code before this part](https://github.com/rahuldave/tally/tree/ec6a8aa7f9a8b81ef07c6c8ec69f01307482dc32). [The code after it](https://github.com/rahuldave/tally/tree/d6f47209c66d7bb88e4e389e2eb9bc495694df55).

<a id="extra-02.1"></a>

### 2.1 A page on how to run tally

A user who opens the folder `docs` wants one page on how to run tally. Its name has spaces in it, `how to run.md`,
as the names of pages often do.

A patch to [`docs/how to run.md`](#extra-02.1-docs-how-to-run.md-3d8176).

The new page `docs/how to run.md` has two sections, each with a command in a fenced block of `sh`.

```bash
uv run mdformat --check docs
```

It prints nothing, because the page is formatted as mdformat formats it.

#### What changed

- <a id="extra-02.1-docs-how-to-run.md-3d8176"></a>`docs/how to run.md`: the page, with how to set up and how to count. New, 19 lines. [The file](https://github.com/rahuldave/tally/blob/17ec79e65166fe1f93c13f94b35e909ca1e36a3c/docs/how%20to%20run.md).
  - look at `# How to run tally`

<details><summary>The diff of <code>docs/how to run.md</code></summary>

````diff
@@ -0,0 +1,19 @@
+# How to run tally
+
+tally counts the words of a text file.
+
+## Set up
+
+Run this once, and again after each change of the project:
+
+```sh
+just setup
+```
+
+## Count the words of a file
+
+```sh
+uv run tally data/corpus.txt
+```
+
+It prints each word with its count, one word to a line, in the order of the alphabet.
````

</details>

[This change on GitHub](https://github.com/rahuldave/tally/commit/17ec79e65166fe1f93c13f94b35e909ca1e36a3c). [The code after it](https://github.com/rahuldave/tally/tree/17ec79e65166fe1f93c13f94b35e909ca1e36a3c).

<a id="extra-02.2"></a>

### 2.2 The most common words

The page does not say how to keep only the most common words. A section says it, with the option `--top`.

A patch to [`docs/how to run.md`](#extra-02.2-docs-how-to-run.md-3d8176).

At the end of `docs/how to run.md`, the section "Only the most common words" runs `uv run tally --top 10`.

```bash
uv run tally --top 10 data/corpus.txt
```

It prints the ten lines that the section promises, from `127 line` down to `110 code`.

#### What changed

- <a id="extra-02.2-docs-how-to-run.md-3d8176"></a>`docs/how to run.md`: the option `--top`. 8 lines added. [The file](https://github.com/rahuldave/tally/blob/4a4de50fdb3f29580f612015d62ca81b6c9afe07/docs/how%20to%20run.md).
  - look at `## Only the most common words`

<details><summary>The diff of <code>docs/how to run.md</code></summary>

````diff
@@ -17,3 +17,11 @@ uv run tally data/corpus.txt
 ```
 
 It prints each word with its count, one word to a line, in the order of the alphabet.
+
+## Only the most common words
+
+```sh
+uv run tally --top 10 data/corpus.txt
+```
+
+It prints the ten most common words, the most common first.
````

</details>

[This change on GitHub](https://github.com/rahuldave/tally/commit/4a4de50fdb3f29580f612015d62ca81b6c9afe07). [The code after it](https://github.com/rahuldave/tally/tree/4a4de50fdb3f29580f612015d62ca81b6c9afe07).

<a id="extra-02.3"></a>

### 2.3 The table

The option `--table` is new, and the page does not name it. A section names it.

A patch to [`docs/how to run.md`](#extra-02.3-docs-how-to-run.md-3d8176).

At the end of `docs/how to run.md`, the section "A table" runs tally with `--top 10 --table`.

```bash
uv run mdformat --check docs
```

It prints nothing, so the page is still formatted.

#### What changed

- <a id="extra-02.3-docs-how-to-run.md-3d8176"></a>`docs/how to run.md`: the option `--table`. 8 lines added. [The file](https://github.com/rahuldave/tally/blob/fea3c9b91e4687bfdd1d528ad230890d5b6df4c9/docs/how%20to%20run.md).
  - look at `## A table`

<details><summary>The diff of <code>docs/how to run.md</code></summary>

````diff
@@ -25,3 +25,11 @@ uv run tally --top 10 data/corpus.txt
 ```
 
 It prints the ten most common words, the most common first.
+
+## A table
+
+```sh
+uv run tally --top 10 --table data/corpus.txt
+```
+
+It prints the same words as a table, with a header.
````

</details>

[This change on GitHub](https://github.com/rahuldave/tally/commit/fea3c9b91e4687bfdd1d528ad230890d5b6df4c9). [The code after it](https://github.com/rahuldave/tally/tree/fea3c9b91e4687bfdd1d528ad230890d5b6df4c9).

<a id="extra-02.4"></a>

### 2.4 A picture of the most common words

A picture tells at a glance that the ten most common words have about the same count. A file `docs/tally.png`
draws them as ten blue bars. The file is binary, so its patch has no lines to read.

A patch to [`docs/tally.png`](#extra-02.4-docs-tally.png-f53d72).

The new file `docs/tally.png` is a picture of ten blue bars, one for each of the most common words.

```bash
file docs/tally.png
```

It prints `docs/tally.png: PNG image data, 60 x 30, 8-bit/color RGB, non-interlaced`.

#### What changed

- <a id="extra-02.4-docs-tally.png-f53d72"></a>`docs/tally.png`: ten bars, one for each of the most common words. A binary file. [The file](https://github.com/rahuldave/tally/blob/62a45097ffcb393715eff9da3826926582b2fa8b/docs/tally.png).

[This change on GitHub](https://github.com/rahuldave/tally/commit/62a45097ffcb393715eff9da3826926582b2fa8b). [The code after it](https://github.com/rahuldave/tally/tree/62a45097ffcb393715eff9da3826926582b2fa8b).

<a id="extra-02.5"></a>

### 2.5 The page shows the picture

The picture is in the folder `docs`, but no page shows it. The section on the most common words shows it, under
its command.

A patch to [`docs/how to run.md`](#extra-02.5-docs-how-to-run.md-3d8176).

In `docs/how to run.md`, the section "Only the most common words" shows `tally.png`, with words that say what it
draws.

```bash
grep -n 'tally.png' "docs/how to run.md"
```

It prints the line of the picture, with its number.

#### What changed

- <a id="extra-02.5-docs-how-to-run.md-3d8176"></a>`docs/how to run.md`: the picture, in its section. 2 lines added. [The file](https://github.com/rahuldave/tally/blob/3f033b6e57ab1b04706ab3efe288701b3a7848ef/docs/how%20to%20run.md).
  - look at `![The ten most common words of the corpus, as bars](tally.png)`

<details><summary>The diff of <code>docs/how to run.md</code></summary>

````diff
@@ -26,6 +26,8 @@ uv run tally --top 10 data/corpus.txt
 
 It prints the ten most common words, the most common first.
 
+![The ten most common words of the corpus, as bars](tally.png)
+
 ## A table
 
 ```sh
````

</details>

[This change on GitHub](https://github.com/rahuldave/tally/commit/3f033b6e57ab1b04706ab3efe288701b3a7848ef). [The code after it](https://github.com/rahuldave/tally/tree/3f033b6e57ab1b04706ab3efe288701b3a7848ef).

<a id="extra-02.6"></a>

### 2.6 Count from Python

tally is a library as well as a command. A user who writes Python wants to call `count` and `top`. A new section of
the README shows how, in a fenced block of Python.

A patch to [`README.md`](#extra-02.6-README.md-8ec9a0).

At the end of `README.md`, the section "Count from Python" counts the words of `"the cat and the hat"`, and keeps
the two most common.

```bash
uv run python -c "from tally import count, top; print(top(count('the cat and the hat'), 2))"
```

It prints `[('the', 2), ('and', 1)]`, as the README says.

#### What changed

- <a id="extra-02.6-README.md-8ec9a0"></a>`README.md`: the section "Count from Python", with its block of code. 13 lines added. [The file](https://github.com/rahuldave/tally/blob/4cf104b7cd816370bd0a34efc7ff2d2be39f6abb/README.md).
  - look at `print(top(counts, 2))`

<details><summary>The diff of <code>README.md</code></summary>

````diff
@@ -11,3 +11,16 @@ Make the environment, the corpus and the report first. Then count the words of a
 
 `uv run tally --top 10 data/corpus.txt` prints only the ten most common words. `just test` runs the tests, and
 `just report` writes the ten most common words of the corpus to `build/top.txt`.
+
+## Count from Python
+
+tally is a library too. `count` counts the words of a text, and `top` keeps the most common:
+
+```python
+from tally import count, top
+
+counts = count("the cat and the hat")
+print(top(counts, 2))
+```
+
+It prints `[('the', 2), ('and', 1)]`.
````

</details>

[This change on GitHub](https://github.com/rahuldave/tally/commit/4cf104b7cd816370bd0a34efc7ff2d2be39f6abb). [The code after it](https://github.com/rahuldave/tally/tree/4cf104b7cd816370bd0a34efc7ff2d2be39f6abb).

<a id="extra-02.7"></a>

### 2.7 The README links to the page

A reader of the README does not know that the page exists. A link at the end of the README names it. The path has
spaces, so the link writes each one as `%20`.

A patch to [`README.md`](#extra-02.7-README.md-8ec9a0).

The last sentence of `README.md` links to the page `docs/how to run.md`, with `%20` for each space.

```bash
grep -o 'docs/how%20to%20run.md' README.md
```

It prints the path of the link, `docs/how%20to%20run.md`.

#### What changed

- <a id="extra-02.7-README.md-8ec9a0"></a>`README.md`: a link to the page. 2 lines added. [The file](https://github.com/rahuldave/tally/blob/1fac49bff15eb93b2e294c28a89ad85c4ec196c1/README.md).
  - look at `The page [How to run tally](docs/how%20to%20run.md) says more, with a picture of the most common words.`

<details><summary>The diff of <code>README.md</code></summary>

````diff
@@ -24,3 +24,5 @@ print(top(counts, 2))
 ```
 
 It prints `[('the', 2), ('and', 1)]`.
+
+The page [How to run tally](docs/how%20to%20run.md) says more, with a picture of the most common words.
````

</details>

[This change on GitHub](https://github.com/rahuldave/tally/commit/1fac49bff15eb93b2e294c28a89ad85c4ec196c1). [The code after it](https://github.com/rahuldave/tally/tree/1fac49bff15eb93b2e294c28a89ad85c4ec196c1).

<a id="extra-02.8"></a>

### 2.8 The picture in green

The blue bars look like links on a page of blue links. Green bars stand apart. The patch replaces the picture.

A patch to [`docs/tally.png`](#extra-02.8-docs-tally.png-f53d72).

`docs/tally.png` has the same ten bars, now green.

```bash
file docs/tally.png
```

It prints `docs/tally.png: PNG image data, 60 x 30, 8-bit/color RGB, non-interlaced`, as before. Only the colour
changed.

#### What changed

- <a id="extra-02.8-docs-tally.png-f53d72"></a>`docs/tally.png`: the bars, in green. A binary file. [The file](https://github.com/rahuldave/tally/blob/2476ccb77ac1f9119d5993ed9daa59363092b454/docs/tally.png).

[This change on GitHub](https://github.com/rahuldave/tally/commit/2476ccb77ac1f9119d5993ed9daa59363092b454). [The code after it](https://github.com/rahuldave/tally/tree/2476ccb77ac1f9119d5993ed9daa59363092b454).

<a id="extra-02.9"></a>

### 2.9 Count a file from Python

A short text in the README shows little. The block of Python now counts the corpus, and keeps the three most common
words.

A patch to [`README.md`](#extra-02.9-README.md-8ec9a0).

The block of Python in `README.md` reads `data/corpus.txt` with `Path`, and prints the three most common words.

This command takes the block of Python out of the README, and runs it:

```bash
sed -n '/^```python$/,/^```$/p' README.md | sed '1d;$d' | uv run python -
```

It prints `[('line', 127), ('class', 126), ('word', 125)]`, as the README says.

#### What changed

- <a id="extra-02.9-README.md-8ec9a0"></a>`README.md`: the block of Python counts the corpus. 5 lines added, 3 removed. [The file](https://github.com/rahuldave/tally/blob/a0cde9c7cdd6520d1e82207d6ea78bfc3dba99eb/README.md).
  - look at `counts = count(Path("data/corpus.txt").read_text())`

<details><summary>The diff of <code>README.md</code></summary>

````diff
@@ -17,12 +17,14 @@ Make the environment, the corpus and the report first. Then count the words of a
 tally is a library too. `count` counts the words of a text, and `top` keeps the most common:
 
 ```python
+from pathlib import Path
+
 from tally import count, top
 
-counts = count("the cat and the hat")
-print(top(counts, 2))
+counts = count(Path("data/corpus.txt").read_text())
+print(top(counts, 3))
 ```
 
-It prints `[('the', 2), ('and', 1)]`.
+It prints `[('line', 127), ('class', 126), ('word', 125)]`, the three most common words of the corpus.
 
 The page [How to run tally](docs/how%20to%20run.md) says more, with a picture of the most common words.
````

</details>

[This change on GitHub](https://github.com/rahuldave/tally/commit/a0cde9c7cdd6520d1e82207d6ea78bfc3dba99eb). [The code after it](https://github.com/rahuldave/tally/tree/a0cde9c7cdd6520d1e82207d6ea78bfc3dba99eb).

<a id="extra-02.10"></a>

### 2.10 A recipe that checks the docs

Nobody remembers to run mdformat on each page. A recipe, `just docs`, checks the README and the folder `docs` in one
command.

A patch to [`justfile`](#extra-02.10-justfile-424f0b).

At the end of the `justfile`, the recipe `docs` runs `mdformat --check` on `README.md` and on `docs`.

```bash
just docs
```

It fails, with exit code 1. mdformat says that `README.md` is not formatted. The section "Run it" has a block of
code indented by four spaces, and mdformat writes a fenced block.

#### What changed

- <a id="extra-02.10-justfile-424f0b"></a>`justfile`: the recipe `docs`. 4 lines added. [The file](https://github.com/rahuldave/tally/blob/cdde9a53f40f29d93721cc8defb7717ea5fb4d93/justfile).
  - look at `uv run mdformat --check README.md docs`

<details><summary>The diff of <code>justfile</code></summary>

```diff
@@ -20,3 +20,7 @@ test:
 report:
     mkdir -p build
     uv run tally --top 10 data/corpus.txt > build/top.txt
+
+# Check that the README and the docs are formatted as mdformat formats them
+docs:
+    uv run mdformat --check README.md docs
```

</details>

[This change on GitHub](https://github.com/rahuldave/tally/commit/cdde9a53f40f29d93721cc8defb7717ea5fb4d93). [The code after it](https://github.com/rahuldave/tally/tree/cdde9a53f40f29d93721cc8defb7717ea5fb4d93).

<a id="extra-02.11"></a>

### 2.11 The README as mdformat writes it

The check fails on the README. mdformat without `--check` formats the file in place:

This change came from running `uv run mdformat README.md`.

In the section "Run it" of `README.md`, the two indented lines are now a fenced block.

```bash
just docs
```

It prints the command of the recipe, and mdformat prints nothing. The README and the page are formatted.

#### What changed

- <a id="extra-02.11-README.md-8ec9a0"></a>`README.md`: a fenced block in place of the indented lines. 4 lines added, 2 removed. It comes from `uv run mdformat README.md`. [The file](https://github.com/rahuldave/tally/blob/b8347ac5868ce45524fd7f226379fbbeef48b461/README.md).

<details><summary>The diff of <code>README.md</code></summary>

````diff
@@ -6,8 +6,10 @@ Count the words in a text.
 
 Make the environment, the corpus and the report first. Then count the words of a file:
 
-    just setup
-    uv run tally data/corpus.txt
+```
+just setup
+uv run tally data/corpus.txt
+```
 
 `uv run tally --top 10 data/corpus.txt` prints only the ten most common words. `just test` runs the tests, and
 `just report` writes the ten most common words of the corpus to `build/top.txt`.
````

</details>

[This change on GitHub](https://github.com/rahuldave/tally/commit/b8347ac5868ce45524fd7f226379fbbeef48b461). [The code after it](https://github.com/rahuldave/tally/tree/b8347ac5868ce45524fd7f226379fbbeef48b461).

<a id="extra-02.12"></a>

### 2.12 The page says how to check the docs

A writer of the docs needs to know that the recipe exists. A last section of the page names it.

A patch to [`docs/how to run.md`](#extra-02.12-docs-how-to-run.md-3d8176).

At the end of `docs/how to run.md`, the section "Check the docs" runs `just docs`, and says what it prints.

```bash
just docs
```

mdformat prints nothing, so the new section is formatted too.

#### What changed

- <a id="extra-02.12-docs-how-to-run.md-3d8176"></a>`docs/how to run.md`: how to check the docs. 8 lines added. [The file](https://github.com/rahuldave/tally/blob/d6f47209c66d7bb88e4e389e2eb9bc495694df55/docs/how%20to%20run.md).
  - look at `## Check the docs`

<details><summary>The diff of <code>docs/how to run.md</code></summary>

````diff
@@ -35,3 +35,11 @@ uv run tally --top 10 --table data/corpus.txt
 ```
 
 It prints the same words as a table, with a header.
+
+## Check the docs
+
+```sh
+just docs
+```
+
+It prints nothing when every page of the docs is formatted as mdformat formats it.
````

</details>

[This change on GitHub](https://github.com/rahuldave/tally/commit/d6f47209c66d7bb88e4e389e2eb9bc495694df55). [The code after it](https://github.com/rahuldave/tally/tree/d6f47209c66d7bb88e4e389e2eb9bc495694df55).

<a id="extra-03"></a>

## 3 A library

```bash
just setup
```

`top` keeps the most common words of any counts. Another program that counts words could use it too. So it goes
into a library of its own, `talib`, in the same workspace. A workspace is a set of packages that share one
`uv.lock`.

[The code before this part](https://github.com/rahuldave/tally/tree/d6f47209c66d7bb88e4e389e2eb9bc495694df55). [The code after it](https://github.com/rahuldave/tally/tree/909df18d1c02f51f42154cdded5a8ef515482057).

<a id="extra-03.1"></a>

### 3.1 A library, with uv init

`uv init --lib` makes a library. In a folder of a project, it also makes the library a member of the project's
workspace. `--author-from none` leaves out the name of the author, which uv would take from your git settings.

This change came from running `uv init --lib --author-from none packages/talib`.

The folder `packages/talib` holds a new project, with its own `pyproject.toml` and a function `hello`. The
`pyproject.toml` of tally names it under `[tool.uv.workspace]`.

`uv.lock` does not name talib yet, so it is out of date until the next move. A `uv run` would lock it again, so the
check reads the file:

```bash
grep -A2 'tool.uv.workspace' pyproject.toml
```

It prints the table `[tool.uv.workspace]`, with `members = [` and `"packages/talib",` under it.

#### What changed

- <a id="extra-03.1-packages-talib-README.md-78b878"></a>`packages/talib/README.md`: empty, for the words about the library. New, 0 lines. It comes from `uv init --lib --author-from none packages/talib`. [The file](https://github.com/rahuldave/tally/blob/f154823215af08326941369c87bdd501eaebc7ad/packages/talib/README.md).
- <a id="extra-03.1-packages-talib-pyproject.toml-4fa4f2"></a>`packages/talib/pyproject.toml`: the project of the library. New, 11 lines. It comes from `uv init --lib --author-from none packages/talib`. [The file](https://github.com/rahuldave/tally/blob/f154823215af08326941369c87bdd501eaebc7ad/packages/talib/pyproject.toml).
- <a id="extra-03.1-packages-talib-src-talib-__init__.py-01f6a2"></a>`packages/talib/src/talib/__init__.py`: a first function, `hello`. New, 2 lines. It comes from `uv init --lib --author-from none packages/talib`. [The file](https://github.com/rahuldave/tally/blob/f154823215af08326941369c87bdd501eaebc7ad/packages/talib/src/talib/__init__.py).
- <a id="extra-03.1-packages-talib-src-talib-py.typed-4fc88d"></a>`packages/talib/src/talib/py.typed`: empty, to say that the library has types. New, 0 lines. It comes from `uv init --lib --author-from none packages/talib`. [The file](https://github.com/rahuldave/tally/blob/f154823215af08326941369c87bdd501eaebc7ad/packages/talib/src/talib/py.typed).
- <a id="extra-03.1-pyproject.toml-5d07e7"></a>`pyproject.toml`: the workspace, with talib as its member. 5 lines added. It comes from `uv init --lib --author-from none packages/talib`. [The file](https://github.com/rahuldave/tally/blob/f154823215af08326941369c87bdd501eaebc7ad/pyproject.toml).
  - look at `"packages/talib",`

<details><summary>The diff of <code>packages/talib/pyproject.toml</code></summary>

```diff
@@ -0,0 +1,11 @@
+[project]
+name = "talib"
+version = "0.1.0"
+description = "Add your description here"
+readme = "README.md"
+requires-python = ">=3.12"
+dependencies = []
+
+[build-system]
+requires = ["uv_build>=0.12.13,<0.13.0"]
+build-backend = "uv_build"
```

</details>

<details><summary>The diff of <code>packages/talib/src/talib/__init__.py</code></summary>

```diff
@@ -0,0 +1,2 @@
+def hello() -> str:
+    return "Hello from talib!"
```

</details>

<details><summary>The diff of <code>pyproject.toml</code></summary>

```diff
@@ -28,3 +28,8 @@ line-length = 100
 
 [tool.uv]
 default-groups = ["dev", "docs"]
+
+[tool.uv.workspace]
+members = [
+    "packages/talib",
+]
```

</details>

[This change on GitHub](https://github.com/rahuldave/tally/commit/f154823215af08326941369c87bdd501eaebc7ad). [The code after it](https://github.com/rahuldave/tally/tree/f154823215af08326941369c87bdd501eaebc7ad).

<a id="extra-03.2"></a>

### 3.2 tally depends on talib

tally cannot import talib until it depends on it. `uv add` finds talib in the workspace, and takes it from there:

This change came from running `uv add talib`.

`pyproject.toml` lists `talib` under `dependencies`, and a table `[tool.uv.sources]` says that it comes from the
workspace. `uv.lock` names both packages.

```bash
uv run python -c "import talib; print(talib.hello())"
```

It prints `Hello from talib!`.

#### What changed

- <a id="extra-03.2-pyproject.toml-5d07e7"></a>`pyproject.toml`: talib, from the workspace. 4 lines added. It comes from `uv add talib`. [The file](https://github.com/rahuldave/tally/blob/de7bf1a4a64c1c6f40718889ced3592c21113636/pyproject.toml).
  - look at `talib = { workspace = true }`
- <a id="extra-03.2-uv.lock-8356d8"></a>`uv.lock`: talib, as a member of the workspace. 16 lines added, 1 removed. It comes from `uv add talib`. [The file](https://github.com/rahuldave/tally/blob/de7bf1a4a64c1c6f40718889ced3592c21113636/uv.lock).

<details><summary>The diff of <code>pyproject.toml</code></summary>

```diff
@@ -6,6 +6,7 @@ readme = "README.md"
 requires-python = ">=3.12"
 dependencies = [
     "tabulate>=0.9,<0.10",
+    "talib",
 ]
 
 [project.scripts]
@@ -33,3 +34,6 @@ default-groups = ["dev", "docs"]
 members = [
     "packages/talib",
 ]
+
+[tool.uv.sources]
+talib = { workspace = true }
```

</details>

[This change on GitHub](https://github.com/rahuldave/tally/commit/de7bf1a4a64c1c6f40718889ced3592c21113636). [The code after it](https://github.com/rahuldave/tally/tree/de7bf1a4a64c1c6f40718889ced3592c21113636).

<a id="extra-03.3"></a>

### 3.3 top goes into talib

`top` is still in tally, and talib has only `hello`. One patch moves `top` across, in both packages.

A patch to [`packages/talib/src/talib/__init__.py`](#extra-03.3-packages-talib-src-talib-__init__.py-01f6a2).

A patch to [`src/tally/__init__.py`](#extra-03.3-src-tally-__init__.py-b5485b).

`top` is now in `packages/talib/src/talib/__init__.py`. `src/tally/__init__.py` imports it from talib, so the tests
that import `top` from tally still find it.

```bash
uv run python -m unittest discover -s tests -q
```

All four tests pass.

```bash
head -4 packages/talib/src/talib/__init__.py
```

```text
"""talib: small helpers for the counts of words."""


def top(counts: dict[str, int], n: int) -> list[tuple[str, int]]:
```

It prints the docstring of the library, two blank lines, and the first line of `top`.

#### What changed

- <a id="extra-03.3-packages-talib-src-talib-__init__.py-01f6a2"></a>`packages/talib/src/talib/__init__.py`: `top`, in place of `hello`. 6 lines added, 2 removed. [The file](https://github.com/rahuldave/tally/blob/909df18d1c02f51f42154cdded5a8ef515482057/packages/talib/src/talib/__init__.py).
  - look at `def top(counts: dict[str, int], n: int) -> list[tuple[str, int]]:`
- <a id="extra-03.3-src-tally-__init__.py-b5485b"></a>`src/tally/__init__.py`: `top` comes from talib. 1 line added, 5 removed. [The file](https://github.com/rahuldave/tally/blob/909df18d1c02f51f42154cdded5a8ef515482057/src/tally/__init__.py).
  - look at `from talib import top`

<details><summary>The diff of <code>packages/talib/src/talib/__init__.py</code></summary>

```diff
@@ -1,2 +1,6 @@
-def hello() -> str:
-    return "Hello from talib!"
+"""talib: small helpers for the counts of words."""
+
+
+def top(counts: dict[str, int], n: int) -> list[tuple[str, int]]:
+    "The n most common words, most common first."
+    return sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))[:n]
```

</details>

<details><summary>The diff of <code>src/tally/__init__.py</code></summary>

```diff
@@ -3,6 +3,7 @@
 import sys
 
 from tabulate import tabulate
+from talib import top
 
 
 def count(text: str) -> dict[str, int]:
@@ -13,11 +14,6 @@ def count(text: str) -> dict[str, int]:
     return counts
 
 
-def top(counts: dict[str, int], n: int) -> list[tuple[str, int]]:
-    "The n most common words, most common first."
-    return sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))[:n]
-
-
 def main() -> None:
     "Count the words of a file, or of the standard input. Options: --top N, and --table."
     args = sys.argv[1:]
```

</details>

[This change on GitHub](https://github.com/rahuldave/tally/commit/909df18d1c02f51f42154cdded5a8ef515482057). [The code after it](https://github.com/rahuldave/tally/tree/909df18d1c02f51f42154cdded5a8ef515482057).

<a id="extra-03b"></a>

## 3b Lint

```bash
just setup
```

ruff finds code that works but could be better, such as a file that nobody closes. It fixes some of what it finds
by itself, and leaves the rest to us.

[The code before this part](https://github.com/rahuldave/tally/tree/909df18d1c02f51f42154cdded5a8ef515482057). [The code after it](https://github.com/rahuldave/tally/tree/25f4f751628b8461806074ef35b6cd489e7c9ce8).

<a id="extra-03b.1"></a>

### 3b.1 What ruff fixes

`ruff check --fix` fixes what it can, and lists the rest. It writes its fixes, and then exits with code 1, because
one problem is left.

This change came from running `uv run ruff check --fix`.

In `scripts/corpus.py`, ruff wrote the list `WORDS` as a list of strings, in place of a string that the code split.

```bash
uv run ruff check --statistics
```

It fails, with exit code 1. It prints one line for the rule `SIM115`, open-file-with-context-handler, and then
`Found 1 error.` `main` opens a file and never closes it, and ruff cannot fix that.

#### What changed

- <a id="extra-03b.1-scripts-corpus.py-ab344b"></a>`scripts/corpus.py`: a list of words, as ruff writes it. 1 line added, 1 removed. It comes from `uv run ruff check --fix`. [The file](https://github.com/rahuldave/tally/blob/429a292239114c0e1263db0992fbd0365164ba2f/scripts/corpus.py).
  - look at `WORDS = ["the", "a", "word", "count", "text", "tally", "test", "step", "move", "commit", "tag", "note", "slide", "class", "shell", "file", "line", "code"]`

<details><summary>The diff of <code>scripts/corpus.py</code></summary>

```diff
@@ -3,7 +3,7 @@
 import sys
 from pathlib import Path
 
-WORDS = "the a word count text tally test step move commit tag note slide class shell file line code".split()
+WORDS = ["the", "a", "word", "count", "text", "tally", "test", "step", "move", "commit", "tag", "note", "slide", "class", "shell", "file", "line", "code"]
 
 
 def main() -> None:
```

</details>

[This change on GitHub](https://github.com/rahuldave/tally/commit/429a292239114c0e1263db0992fbd0365164ba2f). [The code after it](https://github.com/rahuldave/tally/tree/429a292239114c0e1263db0992fbd0365164ba2f).

<a id="extra-03b.2"></a>

### 3b.2 main closes its file

ruff cannot fix SIM115. A `with` block closes the file when the block ends.

A patch to [`src/tally/__init__.py`](#extra-03b.2-src-tally-__init__.py-b5485b).

`main` in `src/tally/__init__.py` reads the file in a `with` block, and reads the standard input when there is no
file.

```bash
uv run ruff check
```

It prints `All checks passed!`.

#### What changed

- <a id="extra-03b.2-src-tally-__init__.py-b5485b"></a>`src/tally/__init__.py`: a `with` block, which closes the file. 5 lines added, 1 removed. [The file](https://github.com/rahuldave/tally/blob/25f4f751628b8461806074ef35b6cd489e7c9ce8/src/tally/__init__.py).
  - look at `with open(args[0]) as file:`

<details><summary>The diff of <code>src/tally/__init__.py</code></summary>

```diff
@@ -21,7 +21,11 @@ def main() -> None:
     args, n = [arg for arg in args if arg != "--table"], None
     if args[:1] == ["--top"]:
         n, args = int(args[1]), args[2:]
-    text = open(args[0]).read() if args else sys.stdin.read()
+    if args:
+        with open(args[0]) as file:
+            text = file.read()
+    else:
+        text = sys.stdin.read()
     counts = count(text)
     rows = top(counts, n) if n else sorted(counts.items())
     if as_table:
```

</details>

[This change on GitHub](https://github.com/rahuldave/tally/commit/25f4f751628b8461806074ef35b6cd489e7c9ce8). [The code after it](https://github.com/rahuldave/tally/tree/25f4f751628b8461806074ef35b6cd489e7c9ce8).

<a id="extra-04"></a>

## 4 One dependency less

```bash
just setup
```

tally uses tabulate for one table, of two columns. A few lines of its own draw the same table, and the project
needs one package less.

[The code before this part](https://github.com/rahuldave/tally/tree/25f4f751628b8461806074ef35b6cd489e7c9ce8). [The code after it](https://github.com/rahuldave/tally/tree/818eaf0e0f7c19b85c5ff03b2ada94c58afbd299).

<a id="extra-04.1"></a>

### 4.1 tally draws its own table

A function `table` draws the header, the rule of dashes, and the rows, with the same widths as tabulate.

A patch to [`src/tally/__init__.py`](#extra-04.1-src-tally-__init__.py-b5485b).

`src/tally/__init__.py` has a function `table`, and `main` prints `table(rows)`. Nothing imports tabulate now.

```bash
uv run tally --top 3 --table data/corpus.txt
```

It prints the same table as tabulate printed. It has the header `word` and `times`, a rule of dashes, and three
rows.

#### What changed

- <a id="extra-04.1-src-tally-__init__.py-b5485b"></a>`src/tally/__init__.py`: the function `table`, in place of tabulate. 10 lines added, 2 removed. [The file](https://github.com/rahuldave/tally/blob/72b6c553d362423f55d6cf57aefbd53b5588beba/src/tally/__init__.py).
  - look at `def table(rows: list[tuple[str, int]]) -> str:`

<details><summary>The diff of <code>src/tally/__init__.py</code></summary>

```diff
@@ -2,7 +2,6 @@
 
 import sys
 
-from tabulate import tabulate
 from talib import top
 
 
@@ -14,6 +13,15 @@ def count(text: str) -> dict[str, int]:
     return counts
 
 
+def table(rows: list[tuple[str, int]]) -> str:
+    "The rows under a header and a rule: the words on the left, the counts on the right."
+    left = max([len("word") + 2, *(len(word) for word, _ in rows)])
+    right = max([len("times") + 2, *(len(str(times)) for _, times in rows)])
+    lines = [f"{'word':<{left}}  {'times':>{right}}", f"{'-' * left}  {'-' * right}"]
+    lines += [f"{word:<{left}}  {times:>{right}}" for word, times in rows]
+    return "\n".join(lines)
+
+
 def main() -> None:
     "Count the words of a file, or of the standard input. Options: --top N, and --table."
     args = sys.argv[1:]
@@ -29,7 +37,7 @@ def main() -> None:
     counts = count(text)
     rows = top(counts, n) if n else sorted(counts.items())
     if as_table:
-        print(tabulate(rows, headers=["word", "times"]))
+        print(table(rows))
         return
     for word, times in rows:
         print(times, word)
```

</details>

[This change on GitHub](https://github.com/rahuldave/tally/commit/72b6c553d362423f55d6cf57aefbd53b5588beba). [The code after it](https://github.com/rahuldave/tally/tree/72b6c553d362423f55d6cf57aefbd53b5588beba).

<a id="extra-04.2"></a>

### 4.2 tabulate goes

Nothing imports tabulate now, but the project still depends on it. `uv remove` takes it out of `pyproject.toml`
and `uv.lock`:

This change came from running `uv remove tabulate`.

`pyproject.toml` no longer lists tabulate, and `uv.lock` no longer has it.

```bash
uv run python -m unittest discover -s tests -q
```

All four tests pass, without tabulate.

#### What changed

- <a id="extra-04.2-pyproject.toml-5d07e7"></a>`pyproject.toml`: tabulate is gone. 0 lines added, 1 removed. It comes from `uv remove tabulate`. [The file](https://github.com/rahuldave/tally/blob/818eaf0e0f7c19b85c5ff03b2ada94c58afbd299/pyproject.toml).
- <a id="extra-04.2-uv.lock-8356d8"></a>`uv.lock`: tabulate is gone. 1 line added, 14 removed. It comes from `uv remove tabulate`. [The file](https://github.com/rahuldave/tally/blob/818eaf0e0f7c19b85c5ff03b2ada94c58afbd299/uv.lock).

<details><summary>The diff of <code>pyproject.toml</code></summary>

```diff
@@ -5,7 +5,6 @@ description = "Count the words in a text"
 readme = "README.md"
 requires-python = ">=3.12"
 dependencies = [
-    "tabulate>=0.9,<0.10",
     "talib",
 ]
 
```

</details>

[This change on GitHub](https://github.com/rahuldave/tally/commit/818eaf0e0f7c19b85c5ff03b2ada94c58afbd299). [The code after it](https://github.com/rahuldave/tally/tree/818eaf0e0f7c19b85c5ff03b2ada94c58afbd299).
