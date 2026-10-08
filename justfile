# The integration test of timewalk. `just test` builds the project and drives the page.
# TIMEWALK_LOCAL=~/Projects/timewalk just test   tests a working copy of timewalk in place of the branch on GitHub

set positional-arguments

# The timewalk of pyproject.toml (the walks branch on GitHub), brought up to date; or TIMEWALK_LOCAL, a working copy
timewalk_run := if env("TIMEWALK_LOCAL", "") == "" { "uv lock -q --upgrade-package timewalk && uv run --refresh-package timewalk" } else { "uv run --with-editable " + env("TIMEWALK_LOCAL") }

default:
    @just --list

# Build repo/, the project the walks step through, from history/
build:
    python3 history/build.py

# Run every test against the timewalk named in pyproject.toml, or TIMEWALK_LOCAL
test *args: build
    #!/usr/bin/env bash
    set -euo pipefail
    extra=()
    if [ -n "${TIMEWALK_LOCAL:-}" ]; then extra=(--with-editable "$TIMEWALK_LOCAL"); fi
    uv lock -q --upgrade-package timewalk
    uv run --refresh-package timewalk ${extra[@]+"${extra[@]}"} pytest -q "$@"

# Open the walks in a browser, as a class would: just present, or just present tutorial for another walk
present walk="" *args:
    #!/usr/bin/env bash
    set -euo pipefail
    [ -d repo ] || python3 history/build.py   # build once; just build starts again from the first step
    {{ timewalk_run }} timewalk-check repo --toc toc.toml
    walk="{{ walk }}"
    {{ timewalk_run }} timewalk repo --toc toc.toml ${walk:+--walk "$walk"} --discard-edits --clock {{ args }}

# Check the notes and slides of every walk against the steps
check: build
    {{ timewalk_run }} timewalk-check repo --toc toc.toml

# Make the PDF of one walk's slides: just pdf tutorial
pdf walk="narrative": build
    {{ timewalk_run }} timewalk-pdf --toc toc.toml --walk {{ walk }} -o build/{{ walk }}.pdf
