This walk takes only the tests of tally. It starts after step-01, where tally can count the words of a text. It
leaves out the formatting, the types and the report.

> Say: this walk shows a small walk with notes of its own. Each stop takes the sections of its moves from the notes
> of the tutorial, and has its own words around them.

## Three tests of counting

$ just setup

tally counts words already. step-01 made the function `count` and the command, and this walk starts there.

{{include step-02.1}}

The first test is the pattern for the next two. A test gives `count` a text, and compares what it gives back.

{{include step-02.2..step-02.3}}

Three tests now say what `count` does. It counts words, it gives nothing for an empty text, and it ignores case.

## A test of the most common words

$ just setup

Since the last stop, the walk leaves out step-03 and step-04. They add ruff, the corpus, the types and a
docstring, and they change no test. This stop starts with their code.

{{include step-05.1}}

The test of `top` has the same form as the three tests of `count`. The walk stops here, before the option
`--top` and the report.
