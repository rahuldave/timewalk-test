"Several walks from toc.toml: the picker, the steps, notes and slides of each walk, the checks, and the PDF of one walk."

import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from conftest import open_windows
from pypdf import PdfReader
from test_walk import output_of, shows


@pytest.fixture
def walked(browser, kit: Path, start):
    "Your window and the Room on timewalk started with the table of contents, and --discard-edits."
    context, yours, room = open_windows(browser, start("--toc", str(kit / "toc.toml"), "--discard-edits"))
    yield yours, room
    context.close()


def steps_of(page) -> list[str]:
    return page.evaluate("[...document.querySelectorAll('#step-list button')].map((b) => b.title.split(':')[0])")


def test_the_picker_changes_the_walk_in_every_window(walked) -> None:
    "Your window lists the walks; a change gives both windows that walk's steps, notes and slides. The Room shows the title."
    yours, room = walked
    assert yours.evaluate("[...document.querySelectorAll('#walk-picker option')].map((o) => o.value)") == ["narrative", "tests", "parts", "tutorial"]
    assert room.locator("#walk-picker").is_hidden() and room.locator("#walk-title").inner_text() == "tally, step by step"
    yours.select_option("#walk-picker", "tests")
    for page in (yours, room):
        page.wait_for_function("document.querySelectorAll('#step-list button').length === 3")
        assert steps_of(page) == ["step-01", "step-02", "step-05"]
        shows(page, "#step-name", "step-01")
        shows(page, "#slide-count", "Slide 1 of 2")
    shows(room, "#walk-title", "Only the tests")
    yours.wait_for_function("document.querySelector('#notes-pane').innerText.includes('Before any test')")
    yours.mouse.click(300, 400)
    yours.keyboard.press("ArrowDown")
    for page in (yours, room):
        page.wait_for_function("document.querySelector('#slide h2')?.textContent === 'What a test is'")
        assert page.locator("#slide .slide-md").count() == 1


def test_a_walk_with_its_own_tags_moves_the_replay_copy_to_its_branch(walked, kit: Path) -> None:
    "The parts walk stands on the commits of its own tags; going back to the narrative returns to the step it was left at."
    yours, room = walked
    yours.mouse.click(300, 400)
    yours.keyboard.press("ArrowRight")
    shows(yours, "#step-name", "step-01")
    yours.keyboard.press("ArrowRight")
    shows(yours, "#step-name", "step-02")
    yours.select_option("#walk-picker", "parts")
    for page in (yours, room):
        shows(page, "#step-name", "parts-01")
    head = subprocess.run(["git", "-C", str(kit / "repo-replay"), "describe", "--tags"], capture_output=True, text=True).stdout.strip()
    assert head == "parts-01"
    yours.select_option("#walk-picker", "narrative")
    for page in (yours, room):
        shows(page, "#step-name", "step-02")


def test_a_change_of_walk_with_edits_asks_first(browser, kit: Path, start) -> None:
    "Without --discard-edits, an edit stops the change of walk until you set it aside; then it is stashed, not lost."
    context, yours, _ = open_windows(browser, start("--toc", str(kit / "toc.toml")))
    (kit / "repo-replay" / "README.md").write_text("an edit\n")
    yours.select_option("#walk-picker", "tests")
    yours.wait_for_selector("#notice button:has-text('Set the edits aside')")
    assert yours.locator("#walk-picker").input_value() == "narrative", "the picker shows the walk that is still on show"
    yours.click("#notice button:has-text('Set the edits aside')")
    shows(yours, "#step-name", "step-01")
    stash = subprocess.run(["git", "-C", str(kit / "repo-replay"), "stash", "list"], capture_output=True, text=True).stdout
    assert "timewalk: edits made at step-00" in stash
    context.close()


def test_a_command_runs_at_the_step_of_the_walk(walked, kit: Path) -> None:
    "In the tests walk, the shell at the step is at that walk's step."
    yours, _ = walked
    yours.select_option("#walk-picker", "tests")
    shows(yours, "#step-name", "step-01")
    yours.locator("#terms .term:not([hidden])").click()
    yours.keyboard.type("git describe --tags; echo walk-$((6*7))\n")
    assert "step-01" in output_of(yours.url, "replay", "walk-42")


def check(kit: Path) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, "-m", "timewalk.walks", str(kit / "repo"), "--toc", str(kit / "toc.toml")], capture_output=True, text=True)


def test_the_checks_pass_this_class(kit: Path) -> None:
    "timewalk-check finds nothing wrong with the walks of this class."
    done = check(kit)
    assert done.returncode == 0, done.stdout
    assert "4 walks, 0 errors, 0 warnings" in done.stdout


BROKEN = [
    ("a step with no slides", "walks/tests/slides/slides.toml", lambda t: t.replace('step-05 = ["tests.md#2"]\n', ""),
     "walk tests: step-05 has no entry in slides.toml; give it at least one slide"),
    ("a note for a step not in the walk", "walks/tests/notes.md", lambda t: t + "\n## step-03 Not in this walk\n",
     "walk tests: notes.md has a section ## step-03, which is not a step of the walk"),
    ("a slide past the end of its deck", "walks/tests/slides/slides.toml", lambda t: t.replace("tests.md#2", "tests.md#5"),
     "walk tests: step-05: tests.md has 2 slides; the entry asks for slide 5"),
    ("a slide outside the class folder", "walks/parts/slides/slides.toml", lambda t: t.replace("parts.md#2", "../../../../outside.md"),
     "outside.md is outside the class folder"),
    ("a step that is not a tag", "toc.toml", lambda t: t.replace('"step-05"]', '"step-09"]'),
     "walk tests: these steps are not tags of the repository: step-09"),
    ("a move with no ### section", "walks/tutorial/notes.md", lambda t: t.replace("### step-02.2 A test of an empty text\n", ""),
     "walk tutorial: step-02.2 has no section ### step-02.2 in notes.md"),
    ("slides for a move that does not exist", "walks/tutorial/slides/slides.toml", lambda t: t.replace('"step-02.3"', '"step-02.7"'),
     "walk tutorial: slides.toml has an entry for step-02.7, which is not a step or a move of the walk"),
]


@pytest.mark.parametrize("what, file, change, says", BROKEN, ids=[b[0] for b in BROKEN])
def test_the_checks_name_each_mistake_and_timewalk_refuses_to_start(kit: Path, what: str, file: str, change, says: str) -> None:
    "Each broken copy of the class fails the check with its own message, and timewalk will not start on it."
    path = kit / file
    path.write_text(change(path.read_text()))
    done = check(kit)
    assert done.returncode == 1 and says in done.stdout, done.stdout
    started = subprocess.run([sys.executable, "-m", "timewalk", str(kit / "repo"), "--toc", str(kit / "toc.toml"), "--no-open", "--port", "1"],
                             capture_output=True, text=True, timeout=60)
    assert started.returncode != 0 and says in started.stderr + started.stdout


def test_the_pdf_of_one_walk(kit: Path) -> None:
    "timewalk-pdf --toc --walk makes that walk's slides: three steps, four slides, two of them borrowed from the narrative."
    out = kit / "build" / "tests.pdf"
    subprocess.run([sys.executable, "-m", "timewalk.slides_pdf", "--toc", str(kit / "toc.toml"), "--walk", "tests", "-o", str(out)],
                   check=True, capture_output=True)
    assert len(PdfReader(out).pages) == 4


def test_a_class_without_a_table_is_as_before(kit: Path) -> None:
    "Without toc.toml, nothing changes: the walks folder is not read."
    shutil.rmtree(kit / "walks")
    (kit / "toc.toml").unlink()
    out = kit / "build" / "slides.pdf"
    subprocess.run([sys.executable, "-m", "timewalk.slides_pdf", str(kit / "slides" / "slides.toml"), "-o", str(out)], check=True, capture_output=True)
    assert len(PdfReader(out).pages) == 7
