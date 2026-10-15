"""The pages that students read, rendered by walk-kit, and every check that a class runs on them.

Each walk's Build it yourself page is followed in a clone. Then the pages of the whole class, as render.py --class writes them:
each part page of the website followed, each page to read checked by read_check.py, and the check of render.py --class.
TIMEWALK_TEST_GITHUB=1 also runs walk-kit's `just test-github`, which follows the pages of tally-walk on GitHub.
"""

import os
import shutil
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
                           "--walk", walk, "--json", str(facts), "--github", "https://github.com/o/tally"], capture_output=True, text=True, check=False)
    assert done.returncode == 0, done.stdout + done.stderr
    # --repo: render.py reads each pyproject.toml that a patch$ line changes, for the command that sets its values
    done = subprocess.run([sys.executable, str(KIT / "scripts" / "render.py"), str(facts), "--markdown", str(out), "--site", str(out / "site"),
                           "--repo", str(kit / "repo")], capture_output=True, text=True, check=False)
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
                           "--work", str(tmp_path / "work"), "--log", str(log)], capture_output=True, text=True, check=False)
    assert done.returncode == 0, done.stdout + done.stderr + (log.read_text() if log.exists() else "")


GITHUB = "https://github.com/rahuldave/tally"  # the project on GitHub, as the justfile names it
# Where render.py and read_check.py get timewalk from, with uvx: the working copy under test, or main on GitHub
ENV = {**os.environ, "TIMEWALK": os.environ.get("TIMEWALK_LOCAL") or "git+https://github.com/rahuldave/timewalk"}


def run(
    *args: str | Path,  # The command, with python3 for walk-kit's scripts
    cwd: Path | None = None,  # The folder to run it in
) -> subprocess.CompletedProcess:  # What it printed, and its exit code
    "Run a command with TIMEWALK set, and keep its output."
    return subprocess.run([str(a) for a in args], capture_output=True, text=True, env=ENV, cwd=cwd, check=False)


@pytest.fixture(scope="module")
def whole(tmp_path_factory: pytest.TempPathFactory) -> Path:
    "A class folder with repo/ built, and the pages of every walk in pages/, as render.py --class writes them for a class."
    root = tmp_path_factory.mktemp("class")
    for name in ("notes.md", "toc.toml"):
        shutil.copy(ROOT / name, root / name)
    for name in ("slides", "walks"):
        shutil.copytree(ROOT / name, root / name)
    subprocess.run([sys.executable, str(ROOT / "history" / "build.py"), str(root / "repo")], check=True, capture_output=True)
    done = run(sys.executable, KIT / "scripts" / "render.py", "--class", root, "--repo", root / "repo", "--github", GITHUB, "--pages", root / "pages")
    assert done.returncode == 0, done.stdout + done.stderr
    return root


def test_class_check(whole: Path) -> None:
    "render.py --class, the check of `just check` in a class: 0 problems for every walk."
    done = run(sys.executable, KIT / "scripts" / "render.py", "--class", whole, "--repo", whole / "repo", "--github", GITHUB)
    assert done.returncode == 0, done.stdout + done.stderr
    assert " 0 problems" in done.stdout + done.stderr


@pytest.mark.timeout(1800)  # every part page runs its commands from a fresh clone
def test_part_pages(whole: Path, tmp_path: Path) -> None:
    "Each part page of each walk's website, followed as a student who starts at that part: every check passes."
    pages = sorted((whole / "pages").glob("site/build/*.qmd")) + sorted((whole / "pages").glob("sites/*/build/*.qmd"))
    assert pages, "render.py wrote no part page"
    failed = []
    for page in pages:
        name = f"{page.parent.parent.name}-{page.stem}"
        done = run(sys.executable, KIT / "scripts" / "follow.py", page, "--repo", whole / "repo", "--work", tmp_path / name)
        if done.returncode:
            failed.append(f"{name}:\n{done.stdout[-3000:]}{done.stderr[-3000:]}")
    assert not failed, "\n\n".join(failed)


def test_read_pages(whole: Path) -> None:
    "Every page to read, read.md and each read/ page of the websites, passes read_check.py: nothing to run, every move, every link."
    if not (KIT / "scripts" / "read_check.py").exists():
        pytest.skip(f"walk-kit has no scripts/read_check.py in {KIT}")
    pages = whole / "pages"
    files = sorted(pages.glob("walks/*/read.md")) + sorted(pages.glob("site/read/*.qmd")) + sorted(pages.glob("sites/*/read/*.qmd"))
    assert files, "render.py wrote no page to read"
    done = run(sys.executable, KIT / "scripts" / "read_check.py", *files, "--repo", whole / "repo", "--toc", whole / "toc.toml",
               "--project-url", GITHUB)
    assert done.returncode == 0, "\n".join(line for line in (done.stdout + done.stderr).splitlines() if not line.startswith("ok "))


@pytest.mark.github
@pytest.mark.timeout(3600)
@pytest.mark.skipif(os.environ.get("TIMEWALK_TEST_GITHUB") != "1", reason="set TIMEWALK_TEST_GITHUB=1 to follow tally-walk on GitHub")
def test_github() -> None:
    "walk-kit's `just test-github`: the pages of tally-walk on GitHub, followed and checked against GitHub itself."
    done = run("just", "test-github", cwd=KIT)
    assert done.returncode == 0, done.stdout[-6000:] + done.stderr[-3000:]
