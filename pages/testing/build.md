<!-- Made by the walk skill's render.py from the facts of the walk. Do not edit it by hand: run just walk-update again. -->

# The tests of tally, with notes of its own

**Build it yourself.** Every command to run and every change to make by hand, to make the project yourself. [Read the tutorial](read.md) is the other way to read it.

Each part ends with a section called **What changed**. It lists every file that the part changes, with a link to the file, and then the whole diff of each file, folded. A lockfile and a binary file have a link alone. The text above it explains the change. What changed is what you check your files against.

In Build it yourself, a file that a command makes says which command. A diff that is open is a patch. Apply it with the command in the text, or make the same change in your editor.

This walk takes only the tests of tally. It begins where tally can already count the words of a text. It leaves out
the formatting, the types and the report.

## Get the project

You build the project in a clone of your own, on a branch `mine` that starts where this walk starts. Run the commands of these pages in its top folder.

```bash
git clone https://github.com/rahuldave/tally
cd tally
git switch -c mine eb951f747563
```

Then add the command `git check`, which compares your files with the project's after each move, and leaves what `git add` has staged as it was.

```bash
git config alias.check '!f() { i="$(git rev-parse --git-path check-index)" && { cp -p "$(git rev-parse --git-path index)" "$i" 2>/dev/null || rm -f "$i"; } && export GIT_INDEX_FILE="$i" && git add -A && git diff --cached --stat "$1"; }; f'
```

<a id="step-02.1-to-step-02.3"></a>

## 2.1 to 2.3 Three tests of counting

```bash
just setup
```

tally counts words already. The function `count` and the command are there, and this walk begins with them.
Nothing checks yet that they count right.

[The code before this part](https://github.com/rahuldave/tally/tree/eb951f74756383392f528427a0cf44e135d5c64f). [The code after it](https://github.com/rahuldave/tally/tree/bfcbe07463b5c6f3c0764e4ac19a054cb0acee20).

<a id="step-02.1"></a>

### 2.1 A test of counting

Nothing checks yet that `count` gives the right counts. A test of `unittest`, the test library of Python, calls
`count` on a short text and compares the result with the dictionary that it expects. The tests go in a new folder,
`tests`.

Make the folder, and run the tests in it. The folder has no tests yet, so unittest prints `NO TESTS RAN`.

```bash
mkdir -p tests
uv run python -m unittest discover -s tests -q
```

The first file of tests, `tests/test_count.py`, has two tests. `test_words` counts `a b a`. `test_case` counts
`A a`, and expects the one word `a`, twice. The code cannot do this yet.

Apply the patch to [`tests/test_count.py`](#step-02.1-tests-test_count.py-e674f6), from the top of the project:

```bash
curl -fsSL https://github.com/rahuldave/tally/commit/6a4b1a0e50035c4060f84b50770e234b2156be10.diff | git apply --include=tests/test_count.py
```

The patch makes the file `tests/test_count.py`, with the class `Count` and its two tests.

```bash
uv run python -m unittest discover -s tests -q
```

One test fails. `test_case` expects `{'a': 2}`, and gets `{'A': 1, 'a': 1}`. The failure is a question that the
code has not answered yet.

The first two tests are the pattern for the third. A test gives `count` a text, and compares what `count` gives back
with the counts that it must give.

Check your files against this move. The command prints nothing when they match, and otherwise shows what differs:

```bash
git check 6a4b1a0e5003
```

If you are stuck, this command puts the files of this move in place of yours. A file that you made yourself stays:

```bash
git restore --source eb951f747563 --staged -- :/ && git restore --source 6a4b1a0e5003 --staged --worktree -- :/
```

#### What changed

- <a id="step-02.1-tests-test_count.py-e674f6"></a>`tests/test_count.py`: two tests. The second asks for something the code cannot do yet. New, 11 lines. [The file](https://github.com/rahuldave/tally/blob/6a4b1a0e50035c4060f84b50770e234b2156be10/tests/test_count.py).
  - look at `self.assertEqual(count("A a"), {"a": 2})`

<details open><summary>The patch to <code>tests/test_count.py</code></summary>

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

Apply the patch to [`tests/test_empty.py`](#step-02.2-tests-test_empty.py-ffb51e), from the top of the project:

```bash
curl -fsSL https://github.com/rahuldave/tally/commit/4f9bfa3d9c08307287e81a631039894490a3e590.diff | git apply --include=tests/test_empty.py
```

The patch makes the file `tests/test_empty.py`, with the class `Empty` and its test.

```bash
uv run python -m unittest discover -s tests -q
```

The new test passes at once, because `split()` finds no words in an empty text. `test_case` still fails.

Check your files against this move. The command prints nothing when they match, and otherwise shows what differs:

```bash
git check 4f9bfa3d9c08
```

If you are stuck, this command puts the files of this move in place of yours. A file that you made yourself stays:

```bash
git restore --source 6a4b1a0e5003 --staged -- :/ && git restore --source 4f9bfa3d9c08 --staged --worktree -- :/
```

#### What changed

- <a id="step-02.2-tests-test_empty.py-ffb51e"></a>`tests/test_empty.py`: an empty text counts nothing. New, 8 lines. [The file](https://github.com/rahuldave/tally/blob/4f9bfa3d9c08307287e81a631039894490a3e590/tests/test_empty.py).
  - look at `self.assertEqual(count(""), {})`

<details open><summary>The patch to <code>tests/test_empty.py</code></summary>

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

Apply the patch to [`src/tally/__init__.py`](#step-02.3-src-tally-__init__.py-b5485b), from the top of the project:

```bash
curl -fsSL https://github.com/rahuldave/tally/commit/bfcbe07463b5c6f3c0764e4ac19a054cb0acee20.diff | git apply --include=src/tally/__init__.py
```

In `count`, the patch puts `text.lower().split()` in place of `text.split()`.

```bash
uv run python -m unittest discover -s tests -q
echo "The the" | uv run tally
```

All three tests pass, and the command prints `2 the` for "The the".

Three tests now say what `count` does. It counts words, it gives nothing for an empty text, and it ignores case.

Check your files against this move. The command prints nothing when they match, and otherwise shows what differs:

```bash
git check bfcbe07463b5
```

If you are stuck, this command puts the files of this move in place of yours. A file that you made yourself stays:

```bash
git restore --source 4f9bfa3d9c08 --staged -- :/ && git restore --source bfcbe07463b5 --staged --worktree -- :/
```

#### What changed

- <a id="step-02.3-src-tally-__init__.py-b5485b"></a>`src/tally/__init__.py`: one word, `lower()`, answers the failing test. 1 line added, 1 removed. [The file](https://github.com/rahuldave/tally/blob/bfcbe07463b5c6f3c0764e4ac19a054cb0acee20/src/tally/__init__.py).
  - look at `for word in text.lower().split():`

<details open><summary>The patch to <code>src/tally/__init__.py</code></summary>

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

## 5.1 A test of the most common words

This part does not start where the part before it ends, because the walk skips some changes. This command puts the files that this part starts from in place of yours. Run it, and then go on:

```bash
git restore --source bfcbe07463b5 --staged -- :/ && git restore --source f79588d3b046 --staged --worktree -- :/
```

```bash
just setup
```

Since the last part, the walk leaves out ruff, the corpus, the types and the docstring. None of them changes a
test. This part begins with their code.

[The code before this part](https://github.com/rahuldave/tally/tree/f79588d3b046ec2787725cdb6e3fcf952014e078). [The code after it](https://github.com/rahuldave/tally/tree/72a0129dcee765132ad267788636ff4af9066369).

### 5.1 A function for the most common words

`count` gives the counts in no useful order. To find the most common words, tally must sort the counts, most common
first, and keep the first few. A function, `top`, does it. It sorts by count, highest first, and then by the
word, so that two words with the same count keep one order. Then it keeps the first `n`.

Apply the patch to [`src/tally/__init__.py`](#step-05.1-src-tally-__init__.py-b5485b), from the top of the project:

```bash
curl -fsSL https://github.com/rahuldave/tally/commit/72a0129dcee765132ad267788636ff4af9066369.diff | git apply --include=src/tally/__init__.py
```

The patch puts `top` after `count` and before `main`, with two blank lines around it.

A test says what `top` must give. It gives `top` three words with their counts, and asks for the two most common.

Apply the patch to [`tests/test_top.py`](#step-05.1-tests-test_top.py-1f85fe), from the top of the project:

```bash
curl -fsSL https://github.com/rahuldave/tally/commit/72a0129dcee765132ad267788636ff4af9066369.diff | git apply --include=tests/test_top.py
```

The patch makes the file `tests/test_top.py`, with its one test.

```bash
uv run python -m unittest discover -s tests -q
```

The four tests pass.

The test of `top` has the same form as the three tests of `count`. The walk stops here, before the option
`--top` and the report.

Check your files against this move. The command prints nothing when they match, and otherwise shows what differs:

```bash
git check 72a0129dcee7
```

If you are stuck, this command puts the files of this move in place of yours. A file that you made yourself stays:

```bash
git restore --source f79588d3b046 --staged -- :/ && git restore --source 72a0129dcee7 --staged --worktree -- :/
```

#### What changed

- <a id="step-05.1-src-tally-__init__.py-b5485b"></a>`src/tally/__init__.py`: sort by count, most common first, then by the word. 5 lines added. [The file](https://github.com/rahuldave/tally/blob/72a0129dcee765132ad267788636ff4af9066369/src/tally/__init__.py).
  - look at `return sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))[:n]`
- <a id="step-05.1-tests-test_top.py-1f85fe"></a>`tests/test_top.py`: its test, with three words. New, 8 lines. [The file](https://github.com/rahuldave/tally/blob/72a0129dcee765132ad267788636ff4af9066369/tests/test_top.py).

<details open><summary>The patch to <code>src/tally/__init__.py</code></summary>

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

<details open><summary>The patch to <code>tests/test_top.py</code></summary>

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
