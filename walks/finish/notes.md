This walk takes the end of tally. It adds types and a docstring, and then the report. It starts after step-03, where
tally counts and has its tests, ruff and a corpus.

## Types and a docstring

This stop is all of step-04, with its two moves.

> Say: a whole step brings the text at the top of its section, so `$ just setup` comes with it.

{{include step-04}}

`count` now says what it takes and what it gives, in its signature and in its docstring. Its body did not change,
so the tests pass as before.

## A report of the corpus

$ just setup

Since the last stop, the walk leaves out step-05.1 and step-05.2. They add the function `top`, its test, and the
option `--top`. This stop starts with their code.

{{include step-05.3}}

::: do
Open `build/top.txt`, and compare it with what `uv run tally --top 10` prints for the corpus.
:::

::: watch
The report is the ten most common words of the corpus, the same list that `--top 10` prints.
:::

tally is now finished. It counts, it has tests and types, and `just setup` makes its report.
