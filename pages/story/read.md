<!-- Made by the walk skill's render.py from the facts of the walk. Do not edit it by hand: run just walk-update again. -->

# How tally counts, in three stops

**Read the tutorial.** Each change explained, with the code to look at.

Each part ends with a section called **What changed**. It lists every file that the part changes, with a link to the file, and then the whole diff of each file, folded. A lockfile and a binary file have a link alone. The text above it explains the change.

The story of how tally counts, in three parts. They are the function that counts, the tests, and the option `--top`.

Each part shows the code as it was then. The walk leaves out the other changes. They made the command that reads a file, ruff and the corpus, and the types
and the docstring. They also made the function `top` and the report. The third part uses some of them.

<a id="step-01.1"></a>

## 1.1 A function that counts

```bash
just setup
```

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

### What changed

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

[This change on GitHub](https://github.com/rahuldave/tally/compare/6a63758166d3aeee516faa6244414d7b54b5a730...12fcbe75226dde15e7500b71439bad84712fd2b0). [The code after it](https://github.com/rahuldave/tally/tree/12fcbe75226dde15e7500b71439bad84712fd2b0).

<a id="step-02"></a>

## 2 Tests, one at a time

```bash
just setup
```

We cannot tell whether `count` still works after a change, unless we try it by hand each time. Tests try it for us.
Each test gives `count` a text, and compares what it gives back with what we expect.
We add the tests one file at a time, and run them after each. One test asks for something that `count` cannot do yet. It asks `count` to count
"The" and "the" as one word.

### What changed

- <a id="step-02-src-tally-__init__.py-b5485b"></a>`src/tally/__init__.py`: changes `count`. 1 line added, 1 removed. [The file](https://github.com/rahuldave/tally/blob/bfcbe07463b5c6f3c0764e4ac19a054cb0acee20/src/tally/__init__.py).
- <a id="step-02-tests-test_count.py-e674f6"></a>`tests/test_count.py`: adds `class Count`, `test_case`, `test_words`. New, 11 lines. [The file](https://github.com/rahuldave/tally/blob/bfcbe07463b5c6f3c0764e4ac19a054cb0acee20/tests/test_count.py).
- <a id="step-02-tests-test_empty.py-ffb51e"></a>`tests/test_empty.py`: adds `class Empty`, `test_empty`. New, 8 lines. [The file](https://github.com/rahuldave/tally/blob/bfcbe07463b5c6f3c0764e4ac19a054cb0acee20/tests/test_empty.py).

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

<a id="step-05.2"></a>

## 5.2 tally --top N

```bash
just setup
```

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

### What changed

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

[This change on GitHub](https://github.com/rahuldave/tally/compare/72a0129dcee765132ad267788636ff4af9066369...c4b92c9bd158cd85d783cf17adc6bedc76c9ba0d). [The code after it](https://github.com/rahuldave/tally/tree/c4b92c9bd158cd85d783cf17adc6bedc76c9ba0d).
