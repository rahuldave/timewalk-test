"""Build the website of the pages that students read: each pages/ID/site, rendered by smalldocs, at _site/ID/.

_site/index.html lists the walks of toc.toml, each with its title and its kind. `just site` and the Pages workflow run it.
"""

import html
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path

SMALLDOCS = ["uvx", "--from", "smalldocs>=0.1.5", "smalldocs", "render"]


def build(
    root: Path,  # The class folder, with toc.toml and pages/
) -> Path:  # The folder of the built website, root/_site
    "Render every walk's site with smalldocs, copy each into _site/ID/, and write the front page."
    walks = tomllib.loads((root / "toc.toml").read_text())["walk"]
    out = root / "_site"
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir()
    items = []
    for walk in walks:
        site = root / "pages" / walk["id"] / "site"
        if not (site / "_smalldocs.yml").is_file():
            sys.exit(f"pages_site.py: {site} has no _smalldocs.yml; run just pages first")
        subprocess.run([*SMALLDOCS, str(site)], check=True)
        shutil.copytree(site / "_site", out / walk["id"])
        kind = "a tutorial: read it, or build it yourself" if walk.get("kind") == "tutorial" else "a narrative: read it"
        items.append(
            f'<li><a href="{html.escape(walk["id"])}/">{html.escape(walk["title"])}</a>'
            f"<br>{kind}. {html.escape(walk.get('description', ''))}</li>"
        )
    (out / "index.html").write_text(PAGE.format(items="\n".join(items)))
    return out


PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>timewalk-test: the walks</title>
<style>
body {{ font-family: system-ui, sans-serif; max-width: 42rem; margin: 2rem auto; padding: 0 1rem; line-height: 1.5; }}
li {{ margin-bottom: 1rem; }}
</style>
</head>
<body>
<h1>The walks of timewalk-test</h1>
<p>The pages that students read, one site for each walk of
<a href="https://github.com/rahuldave/timewalk-test">timewalk-test</a>.</p>
<ul>
{items}
</ul>
</body>
</html>
"""

if __name__ == "__main__":
    print(build(Path(__file__).resolve().parent))
