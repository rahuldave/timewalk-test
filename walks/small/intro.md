This walk takes two parts of tally alone. The first part is the test of an empty text and the fix of case. The
second part is the function for the most common words. Each part begins with the code as it was just before it.

The walk leaves out the rest of tally:

- Before the first part, it leaves out the project, the function `count` and the command that reads a file. It also
  leaves out the first file of tests, `tests/test_count.py`. The first part begins with all of them in place.
- Between the two parts, it leaves out ruff, the corpus, the types and the docstring. The second part begins with their code.
- After the second part, it leaves out the option `--top`, the report, and the section of the README that says how to
  run tally.

> Say: ask the class what the parts that the walk leaves out did. The code of each part has them already.
