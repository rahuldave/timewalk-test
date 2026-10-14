This walk takes the end of tally. It adds types and a docstring, and then the report. It begins where tally counts,
and has its tests, ruff and a corpus.

## Types and a docstring

This part is whole. It adds the types, then the docstring.

> Say: a whole step brings the text at the top of its section, so `$ just setup` comes with it.

{{include step-04}}

`count` now says what it takes and what it gives, in its signature and in its docstring. Its body did not change,
so the tests pass as before.

## A report of the corpus

$ just setup

Since the last part, the walk leaves out the function `top`, its test, and the option `--top`. This part begins
with their code.

{{include step-05.3}}

::: do
Open `build/top.txt`, and compare it with what `uv run tally --top 10 data/corpus.txt` prints.
:::

::: watch
The report is the ten most common words of the corpus, the same list that `--top 10` prints.
:::

tally is now finished. It counts, it has tests and types, and `just setup` makes its report.
