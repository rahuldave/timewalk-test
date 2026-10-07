# The integration test of timewalk. `just test` builds the project and drives the page.
# TIMEWALK_LOCAL=~/Projects/timewalk just test   tests a working copy of timewalk in place of the branch on GitHub

set positional-arguments

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

# Open the default walk in a browser, as a class would
present *args: build
    uv run --refresh-package timewalk timewalk repo --notes notes.md --slides slides/slides.toml --discard-edits --clock "$@"
