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

# Check the notes and slides of every walk against the steps, and a tutorial's moves, and then the pages that students read
check: build
    #!/usr/bin/env bash
    set -euo pipefail
    {{ timewalk_run }} timewalk-check repo --toc toc.toml
    # The pages that students read, as a class's check does: every line in Build it yourself, and the writing guide
    TIMEWALK="${TIMEWALK_LOCAL:-git+https://github.com/rahuldave/timewalk}" \
        python3 "${WALK_KIT:-$HOME/Projects/walk-kit}/scripts/render.py" --class . --repo repo --github {{ github }}

# Check the README, notes and slides against the writing guide: their form, then a review by a model. -v shows the soft notes, --all reviews each file whole
style *args:
    #!/usr/bin/env bash
    set -euo pipefail
    # The recipe of a class made with walk-kit. WALK_KIT=PATH uses another walk-kit
    kit="${WALK_KIT:-$HOME/Projects/walk-kit}"
    test -f "$kit/scripts/style.py" || { echo "style: no walk-kit in $kit; set WALK_KIT" >&2; exit 1; }
    python3 "$kit/scripts/style.py" --class . --repo repo "$@"

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
    # each walk with the title that toc.toml gives it, as walk-update does: two walks on the same notes have names of their own
    python3 -c 'import tomllib; [print(w["id"], w.get("title", ""), sep="\t") for w in tomllib.load(open("toc.toml", "rb"))["walk"]]' |
    while IFS=$'\t' read -r id title; do
        "${run[@]}" timewalk-export repo --toc toc.toml --walk "$id" --json "$facts/$id.json" --github {{ github }} ${title:+--title "$title"}
        python3 "$kit/scripts/render.py" "$facts/$id.json" --markdown "pages/$id" --site "pages/$id/site" --repo repo
    done

# Follow every Build it yourself page in a scratch clone, as a student would: every git check must pass. Logs go to build/follow.
# Then each part page of the website, as a student who starts at that part. just follow --github fetches from GitHub, as a student does
follow *args: build
    #!/usr/bin/env bash
    set -euo pipefail
    # The recipe of a class made with walk-kit, with the pages rendered into build/pages, and not into tally-walk
    kit="${WALK_KIT:-$HOME/Projects/walk-kit}"
    export TIMEWALK="${TIMEWALK_LOCAL:-git+https://github.com/rahuldave/timewalk}"
    out=build/pages
    python3 "$kit/scripts/render.py" --class . --repo repo --github {{ github }} --pages "$out" > /dev/null
    # With Claude Code, a model also checks the text against the output, into reports/follow/
    check=()
    if command -v claude > /dev/null; then check=(--check-output --report-dir .); fi
    scratch=$(mktemp -d)
    trap 'rm -rf "$scratch"' EXIT
    shopt -s nullglob
    mkdir -p build/follow
    failed=0
    for page in "$out"/walks/*/build.md; do
        id=$(basename "$(dirname "$page")")
        echo "follow: walk $id"
        python3 "$kit/scripts/follow.py" "$page" --repo repo --work "$scratch/$id" --log "build/follow/$id.md" \
            ${check[@]+"${check[@]}"} "$@" || failed=1
    done
    # A narrative has no Build it yourself page: each part's commands run at its code, and the model checks the text
    for page in "$out"/walks/*/read.md; do
        [ -f "$(dirname "$page")/build.md" ] && continue
        id=$(basename "$(dirname "$page")")
        echo "follow: narrative $id"
        python3 "$kit/scripts/follow.py" "$page" --narrative --repo repo --work "$scratch/narrative-$id" --log "build/follow/$id.md" \
            ${check[@]+"${check[@]}"} "$@" || failed=1
    done
    # A part page has the same text as its part of build.md, so the model does not check it again
    for page in "$out"/site/build/*.qmd "$out"/site/*/build/*.qmd; do
        name=$(basename "$(dirname "$(dirname "$page")")")-$(basename "$page" .qmd)
        echo "follow: part page $name"
        python3 "$kit/scripts/follow.py" "$page" --repo repo --work "$scratch/part-$name" --log "build/follow/part-$name.md" "$@" \
            || failed=1
    done
    # The pages to read: nothing to run, every move and diff, every link; with --github, every link to GitHub answers
    online=()
    for word in "$@"; do if [ "$word" = --github ]; then online=(--github); fi; done
    echo "follow: the pages to read"
    python3 "$kit/scripts/read_check.py" "$out"/walks/*/read.md "$out"/site/read/*.qmd "$out"/site/*/read/*.qmd --repo repo \
        --toc toc.toml --project-url {{ quote(github) }} ${online[@]+"${online[@]}"} || failed=1
    exit "$failed"

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
