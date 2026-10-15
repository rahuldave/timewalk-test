<!-- Made by the walk skill's render.py from the facts of the walk. Do not edit it by hand: run just walk-update again. -->

# Two parts of tally, one move at a time

**Read the tutorial.** Each change explained, with the code to look at. [Build it yourself](build.md) is the other way to read it.

Each part ends with a section called **What changed**. It lists every file that the part changes, with a link to the file, and then the whole diff of each file, folded. A lockfile and a binary file have a link alone. The text above it explains the change. What changed is what you check your files against.

This walk takes two parts of tally alone. The first part is the test of an empty text and the fix of case. The
second part is the function for the most common words. Each part begins with the code as it was just before it.

The walk leaves out the rest of tally:

- Before the first part, it leaves out the first file of tests, `tests/test_count.py`. The first part begins with it in place.
- Between the two parts, it leaves out ruff, the corpus, the types and the docstring. The second part begins with their code.
- After the second part, it leaves out the option `--top` and the report.

<a id="step-02.2-to-step-02.3"></a>

## 2.2 to 2.3 An empty text, and case

```bash
just setup
```

[The code before this part](https://github.com/rahuldave/tally/tree/6a4b1a0e50035c4060f84b50770e234b2156be10). [The code after it](https://github.com/rahuldave/tally/tree/bfcbe07463b5c6f3c0764e4ac19a054cb0acee20).

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

<a id="step-05.1"></a>

## 5.1 A function for the most common words

```bash
just setup
```

[The code before this part](https://github.com/rahuldave/tally/tree/f79588d3b046ec2787725cdb6e3fcf952014e078). [The code after it](https://github.com/rahuldave/tally/tree/72a0129dcee765132ad267788636ff4af9066369).

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
