# The integration test of timewalk. `just test` builds the project and drives the page.
# TIMEWALK_LOCAL=~/Projects/timewalk just test   tests a working copy of timewalk in place of the branch on GitHub

set positional-arguments

# The timewalk of pyproject.toml (main on GitHub), brought up to date; or TIMEWALK_LOCAL, a working copy
timewalk_run := if env("TIMEWALK_LOCAL", "") == "" { "uv lock -q --upgrade-package timewalk && uv run --refresh-package timewalk" } else { "uv run --with-editable " + env("TIMEWALK_LOCAL") }

default:
    @just --list

# Build repo/, the project the walks step through, from history/
build:
    uv run python history/build.py

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
    [ -d repo ] || uv run python history/build.py   # build once; just build starts again from the first step
    {{ timewalk_run }} timewalk-check repo --toc toc.toml
    walk="{{ walk }}"
    {{ timewalk_run }} timewalk repo --toc toc.toml ${walk:+--walk "$walk"} --clock {{ args }}

# Check the notes and slides of every walk against the steps
check: build
    {{ timewalk_run }} timewalk-check repo --toc toc.toml

# Check the text that readers see: the README, notes, intros, slides and pages/. Not CLAUDE.md.
# walk-kit's check.py checks the form, then its review.py has a model review the writing (reports in reports/writing/).
# -v goes to check.py and adds the soft notes. WALK_KIT=PATH uses another walk-kit.
style *args:
    #!/usr/bin/env bash
    set -euo pipefail
    kit="${WALK_KIT:-$HOME/Projects/walk-kit}"
    shopt -s nullglob
    files=(README.md notes.md slides/*.md walks/*/notes.md walks/*/intro.md walks/*/slides/*.md)
    while IFS= read -r page; do files+=("$page"); done < <(find pages -name '*.md' 2>/dev/null | sort)
    python3 "$kit/style/check.py" "$@" "${files[@]}"
    python3 "$kit/scripts/review.py" --class . --repo repo "${files[@]}"

# tally on GitHub, which the pages link to and students clone. history/build.py makes repo/, and `just publish` pushes it there
project := "tally"
upstream := "rahuldave"
github := "https://github.com/" + upstream + "/" + project
# The walk repository that students fork, made by walk-kit's walk-init, beside this folder unless WALK_DIR names another
walk := env("WALK_DIR", parent_directory(justfile_directory()) / project + "-walk")

# Render the pages that students read, for every walk of toc.toml, into pages/ID: read.md, build.md and site/
pages: build
    #!/usr/bin/env bash
    set -euo pipefail
    kit="${WALK_KIT:-$HOME/Projects/walk-kit}"
    if [ -n "${TIMEWALK_LOCAL:-}" ]; then run=(uv run --with-editable "$TIMEWALK_LOCAL")
    else uv lock -q --upgrade-package timewalk; run=(uv run --refresh-package timewalk); fi
    facts=$(mktemp -d)
    trap 'rm -rf "$facts"' EXIT
    for id in $(python3 -c 'import tomllib; print(*(w["id"] for w in tomllib.load(open("toc.toml", "rb"))["walk"]))'); do
        "${run[@]}" timewalk-export repo --toc toc.toml --walk "$id" --json "$facts/$id.json" --github {{ github }}
        python3 "$kit/scripts/render.py" "$facts/$id.json" --markdown "pages/$id" --site "pages/$id/site" --repo repo
    done

# Make the PDF of one walk's slides: just pdf tutorial
pdf walk="narrative": build
    {{ timewalk_run }} timewalk-pdf --toc toc.toml --walk {{ walk }} -o build/{{ walk }}.pdf

# Build the website of pages/ into _site/, each walk at _site/ID/, and serve it at http://127.0.0.1:8000
site:
    python3 pages_site.py
    python3 -m http.server -d _site -b 127.0.0.1 8000

# Push repo/ to tally on GitHub: every branch and tag, as history/build.py made them (the tags move when the history does)
publish: build
    git -C repo push --force --prune git@github.com:{{ upstream }}/{{ project }}.git '+refs/heads/*:refs/heads/*' '+refs/tags/*:refs/tags/*'

# Make the walk repository, tally-walk, with walk-kit's walk-init. Asks before it creates it on GitHub
walk-init *args:
    python3 "${WALK_KIT:-$HOME/Projects/walk-kit}/scripts/walk_init.py" --project {{ project }} --upstream {{ upstream }} --walk {{ quote(walk) }} "$@"

# Refresh tally-walk from the notes and slides of every walk, with walk-kit's walk-update. Shows the diff, and commits on a yes
walk-update *args: build
    python3 "${WALK_KIT:-$HOME/Projects/walk-kit}/scripts/walk_update.py" --project {{ project }} --upstream {{ upstream }} --toc toc.toml --walk {{ quote(walk) }} --repo repo "$@"
