"The pages that students read, rendered by walk-kit for every walk, and each Build it yourself page followed in a clone."

import os
import subprocess
import sys
import tomllib
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
KIT = Path(os.environ.get("WALK_KIT", Path.home() / "Projects" / "walk-kit")).expanduser()  # walk-kit, the `walk` skill
WALKS = tomllib.loads((ROOT / "toc.toml").read_text())["walk"]

pytestmark = [
    pytest.mark.pages,
    pytest.mark.timeout(900),  # a tutorial runs every command of its Build it yourself page
    pytest.mark.skipif(not (KIT / "scripts" / "render.py").exists(), reason=f"no walk-kit in {KIT}: set WALK_KIT"),
]


def render(
    kit: Path,  # The class folder, with repo/ built
    walk: str,  # The id of the walk
    out: Path,  # The folder for read.md, build.md and site/
) -> None:
    "Write the facts of a walk with timewalk-export, and render its pages with walk-kit's render.py."
    facts = out / "facts.json"
    out.mkdir(parents=True)
    done = subprocess.run([sys.executable, "-c", "from timewalk.export import main; main()", str(kit / "repo"), "--toc", str(kit / "toc.toml"),
                           "--walk", walk, "--json", str(facts), "--github", "https://github.com/o/tally"], capture_output=True, text=True)
    assert done.returncode == 0, done.stdout + done.stderr
    # --repo: render.py runs uv lock --check at each commit, and gives git check --stale-lock where the project's uv.lock is out of date
    done = subprocess.run([sys.executable, str(KIT / "scripts" / "render.py"), str(facts), "--markdown", str(out), "--site", str(out / "site"),
                           "--repo", str(kit / "repo")], capture_output=True, text=True)
    assert done.returncode == 0, done.stdout + done.stderr


@pytest.mark.parametrize("walk", WALKS, ids=[w["id"] for w in WALKS])
def test_pages(kit: Path, tmp_path: Path, walk: dict) -> None:
    "Every walk gets read.md and a site; a tutorial also gets build.md, and following it in a clone passes every check."
    out = tmp_path / "pages" / walk["id"]
    render(kit, walk["id"], out)
    assert (out / "read.md").is_file() and (out / "site" / "index.qmd").is_file()
    if walk["kind"] != "tutorial":
        assert not (out / "build.md").exists()
        return
    assert (out / "build.md").is_file()
    if not (KIT / "scripts" / "follow.py").exists():
        pytest.skip(f"walk-kit has no scripts/follow.py in {KIT}: set WALK_KIT to a walk-kit that has it")
    log = tmp_path / "follow.log"
    done = subprocess.run([sys.executable, str(KIT / "scripts" / "follow.py"), str(out / "build.md"), "--repo", str(kit / "repo"),
                           "--work", str(tmp_path / "work"), "--log", str(log)], capture_output=True, text=True)
    assert done.returncode == 0, done.stdout + done.stderr + (log.read_text() if log.exists() else "")
