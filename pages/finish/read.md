<!-- Made by the walk skill's render.py from the facts of the walk. Do not edit it by hand: run just walk-update again. -->

# Types, then the report, with notes of its own

**Read the tutorial.** Each change explained, with the code to look at. [Build it yourself](build.md) is the other way to read it.

Each part ends with a section called **What changed**. It lists every file that the part changes, with a link to the file, and then the whole diff of each file, folded. A lockfile and a binary file have a link alone. The text above it explains the change. What changed is what you check your files against.

This walk takes the end of tally. It adds types and a docstring, and then the report. It begins where tally counts,
and has its tests, ruff and a corpus.

<a id="step-04"></a>

## 4 Types and a docstring

This part is whole. It adds the types, then the docstring.

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

`count` now says what it takes and what it gives, in its signature and in its docstring. Its body did not change.

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

<a id="step-05.3"></a>

## 5.3 A report of the corpus

```bash
just setup
```

Since the last part, the walk leaves out the function `top`, its test, and the option `--top`. This part begins
with their code.

[The code before this part](https://github.com/rahuldave/tally/tree/c4b92c9bd158cd85d783cf17adc6bedc76c9ba0d). [The code after it](https://github.com/rahuldave/tally/tree/9e37b6eed29516f62bc176d1eaa66bf4e86683a6).

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

The report is the ten most common words of the corpus, the same list that `--top 10` prints.

tally is now finished. It counts, it has tests and types, and `just setup` makes its report.

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
