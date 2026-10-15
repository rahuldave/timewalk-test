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
    "Your window and the Room on timewalk started with the table of contents."
    context, yours, room = open_windows(browser, start("--toc", str(kit / "toc.toml")))
    yield yours, room
    context.close()


def steps_of(page) -> list[str]:
    return page.evaluate("[...document.querySelectorAll('#step-list button')].map((b) => b.title.split(':')[0])")


def test_the_picker_changes_the_walk_in_every_window(walked) -> None:
    "Your window lists the walks; a change gives both windows that walk's steps, notes and slides. The Room shows the title."
    yours, room = walked
    assert yours.evaluate("[...document.querySelectorAll('#walk-picker option')].map((o) => o.value)") == ["narrative", "tests", "parts", "story", "tutorial", "hooks", "small", "testing", "finish", "release"]
    assert room.locator("#walk-picker").is_hidden() and room.locator("#walk-title").inner_text() == "tally, step by step (narrative)"
    yours.select_option("#walk-picker", "tests")
    for page in (yours, room):
        page.wait_for_function("document.querySelectorAll('#step-list button').length === 3")
        assert steps_of(page) == ["step-01", "step-02", "step-05"]
        shows(page, "#step-name", "step-01")
        shows(page, "#slide-count", "Slide 1 of 2")
    shows(room, "#walk-title", "Only the tests (narrative)")
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


def test_a_change_of_walk_with_edits_keeps_them_on_a_branch(browser, kit: Path, start) -> None:
    "An edit does not stop the change of walk: it is kept on timewalk/saved/step-00, and your window says so; the Room does not."
    context, yours, room = open_windows(browser, start("--toc", str(kit / "toc.toml")))
    (kit / "repo-replay" / "README.md").write_text("an edit\n")
    yours.select_option("#walk-picker", "tests")
    shows(yours, "#step-name", "step-01")
    yours.wait_for_selector("#notice:not([hidden]):has-text('timewalk/saved/step-00')")
    assert "git show timewalk/saved/step-00" in yours.locator("#notice").inner_text()
    assert room.locator("#notice").is_hidden(), "the class does not see the notice"
    kept = subprocess.run(["git", "-C", str(kit / "repo-replay"), "show", "timewalk/saved/step-00:README.md"], capture_output=True, text=True).stdout
    assert kept == "an edit\n"
    assert subprocess.run(["git", "-C", str(kit / "repo-replay"), "stash", "list"], capture_output=True, text=True).stdout == ""
    context.close()


def test_a_command_runs_at_the_step_of_the_walk(walked, kit: Path) -> None:
    "In the tests walk, the shell at the step is at that walk's step."
    yours, _ = walked
    yours.select_option("#walk-picker", "tests")
    shows(yours, "#step-name", "step-01")
    yours.locator("#terms .term:not([hidden])").click()
    yours.keyboard.type("git --no-pager tag --points-at HEAD; echo walk-$((6*7))\n")   # step-01's commit is also hooks-00
    assert "step-01" in output_of(yours.url, "replay", "walk-42")


def check(kit: Path) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, "-m", "timewalk.walks", str(kit / "repo"), "--toc", str(kit / "toc.toml")], capture_output=True, text=True)


def test_the_checks_pass_this_class(kit: Path) -> None:
    "timewalk-check finds nothing wrong with the walks of this class."
    done = check(kit)
    assert done.returncode == 0, done.stdout
    assert "10 walks, 0 errors, 0 warnings" in done.stdout


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
    assert len(PdfReader(out).pages) == 9


def test_the_menu_groups_the_walks_by_kind_and_names_the_kind_on_show(walked) -> None:
    "Narratives and tutorials each have a group in the menu; a label beside it says the kind of the walk on show."
    yours, room = walked
    groups = yours.evaluate("[...document.querySelectorAll('#walk-picker optgroup')].map((g) => g.label + ': ' + [...g.children].map((o) => o.value).join(' '))")
    assert groups == ["Narratives: narrative tests parts story", "Tutorials: tutorial hooks small testing finish release"]
    shows(yours, "#walk-kind", "Narrative")
    yours.select_option("#walk-picker", "hooks")
    shows(yours, "#walk-kind", "Tutorial")
    shows(room, "#walk-title", "A git hook, one move at a time (tutorial, watch mode)")


def test_the_status_band_of_a_narrative(walked) -> None:
    "The narrative's band, in both windows: its description and what a narrative is at step-00 only; the step and Right arrow; the tag."
    yours, room = walked
    for page in (yours, room):
        page.wait_for_selector("#about:not([hidden])")
        assert page.locator("#about").inner_text().startswith("How tally, a word counter, was built: one tagged step at a time")
        assert "A narrative goes from tag to tag" in page.locator("#about").inner_text()
        shows(page, "#status", "Narrative · step-00, step 1 of 7 · Press Next step, at the end of the notes, or the Right arrow, for the next step.")
    yours.mouse.click(300, 400)
    for step in ("step-01", "step-02"):
        yours.keyboard.press("ArrowRight")
        shows(yours, "#step-name", step)
    for page in (yours, room):
        shows(page, "#status", "Narrative · step-02, step 3 of 7 · Press Next step, at the end of the notes, or the Right arrow, for the next step.")
        assert page.locator("#about").is_hidden()
        shows(page, "#tag", "Tests — Two tests, one failing, and the fix.")
        assert page.locator("#tag strong").inner_text() == "Tests"


def test_next_step_on_the_last_slide_of_a_narrative(walked) -> None:
    "step-01 has two slides: Next step shows in the slide head on the second only, and moves both windows to step-02."
    yours, room = walked
    yours.mouse.click(300, 400)
    yours.keyboard.press("ArrowRight")
    for page in (yours, room):
        shows(page, "#slide-count", "Slide 1 of 2")
    assert yours.locator("#slide-step").is_hidden()
    yours.keyboard.press("ArrowDown")
    shows(yours, "#slide-count", "Slide 2 of 2")
    shows(yours, "#slide-step", "Next step: step-02 ▶")
    yours.wait_for_selector("#notes .p-next-step button:has-text('Next step: step-02')")
    yours.click("#slide-step")
    for page in (yours, room):
        shows(page, "#step-name", "step-02")


def test_an_svg_slide_is_inverted_in_the_dark_theme(walked) -> None:
    "step-01's second slide is an SVG with no background: as it is in the light theme, inverted in the dark one."
    yours, _ = walked
    yours.keyboard.press("ArrowRight")
    shows(yours, "#step-name", "step-01")
    yours.keyboard.press("ArrowDown")
    yours.wait_for_selector("#slide img.svg")
    filter_of = "getComputedStyle(document.querySelector('#slide img.svg')).filter"
    assert yours.evaluate(filter_of) == "none"
    yours.click("#theme")
    yours.wait_for_function(f"{filter_of}.includes('invert')")


def test_the_notes_title_keeps_one_line(walked) -> None:
    "A long title is cut with an ellipsis, whole in its tooltip; it never wraps under the Top button."
    yours, _ = walked
    yours.wait_for_selector("#notes-title strong")
    title = yours.locator("#notes-title")
    assert title.evaluate("(t) => getComputedStyle(t).whiteSpace") == "nowrap"
    assert title.get_attribute("title").startswith("step-00 ")


def test_timewalk_export_writes_both_modes_and_a_site_that_builds(kit: Path, tmp_path: Path) -> None:
    "The tutorial walk as TUTORIAL-do.md and TUTORIAL-watch.md, and as a website that smalldocs builds with no broken link."
    out, site = tmp_path / "md", tmp_path / "site"
    done = subprocess.run([sys.executable, "-c", "from timewalk.export import main; main()", str(kit / "repo"), "--toc", str(kit / "toc.toml"),
                           "--walk", "tutorial", "--markdown", str(out), "--site", str(site), "--github", "https://github.com/o/tally"],
                          capture_output=True, text=True)
    assert done.returncode == 0, done.stderr
    do, watch = (out / "TUTORIAL-do.md").read_text(), (out / "TUTORIAL-watch.md").read_text()
    words = "the three lines under the docstring read the option"   # the watch block of step-05.2
    assert "if args[:1] == [\"--top\"]:" in do and words not in do
    assert words in watch and "write `main` again" not in watch
    shared = "An option, `--top N`, makes `main` print only"
    assert shared in do and shared in watch, "the problem and the change of a move are in both"
    assert "mkdir -p tests" in do and "mkdir -p tests" not in watch, "a do block's commands, in do mode only"
    assert "> Say:" not in do + watch, "the presenter's cues stay in the class"
    assert "The move ran: `uv add --dev ruff`" in watch and "\nuv add --dev ruff\n" in do, "step-03.1's do$ line follows the mode of the copy"
    assert '  - look at: ``"How many times each word of `text` appears, ignoring case."``' in watch, "a quote with a backtick, in two"
    shutil.copy(kit / "walks" / "tutorial" / "notes.md", site / "notes.md")   # the notes beside the site never become a page
    built = subprocess.run(["uvx", "--from", "smalldocs>=0.1.5,<0.2", "smalldocs", "check"], cwd=site, capture_output=True, text=True)
    assert built.returncode == 0, built.stdout + built.stderr
    assert "0 thing(s) to look at" in built.stdout + built.stderr


def test_timewalk_export_writes_the_small_walks_and_their_sites_build(kit: Path, tmp_path: Path) -> None:
    "The small tutorial has a copy for each mode, the small narrative one; each starts with its intro, and smalldocs builds each site."
    for walk, files in (("small", ["TUTORIAL-do.md", "TUTORIAL-watch.md"]), ("story", ["TUTORIAL.md"])):
        out, site = tmp_path / walk / "md", tmp_path / walk / "site"
        done = subprocess.run([sys.executable, "-c", "from timewalk.export import main; main()", str(kit / "repo"), "--toc", str(kit / "toc.toml"),
                               "--walk", walk, "--markdown", str(out), "--site", str(site), "--github", "https://github.com/o/tally"],
                              capture_output=True, text=True)
        assert done.returncode == 0, done.stderr
        assert sorted(p.name for p in out.iterdir()) == files
        text = (out / files[0]).read_text()
        intro = (kit / "walks" / walk / "intro.md").read_text().split("\n")[0]
        assert intro in text and "We build tally, a small word counter" not in text, "the walk's intro, in place of the notes' opening"
        built = subprocess.run(["uvx", "--from", "smalldocs>=0.1.5,<0.2", "smalldocs", "check"], cwd=site, capture_output=True, text=True)
        assert built.returncode == 0 and "0 thing(s) to look at" in built.stdout + built.stderr, built.stdout + built.stderr
    small = (tmp_path / "small" / "md" / "TUTORIAL-watch.md").read_text()
    assert "## step-02.2 to step-02.3 An empty text, and case" in small, "the title of the range, from select"
    assert "[The code at its Start]" in small and "### step-02.1" not in small
    assert "The walk leaves out the rest of tally" in small and "> Say:" not in small, "the intro, without its cue"


def test_timewalk_export_writes_the_walks_with_their_own_notes(kit: Path, tmp_path: Path) -> None:
    "The testing walk's copies have its intro, and at each stop its own words around the move sections it includes; its site builds."
    out, site = tmp_path / "md", tmp_path / "site"
    done = subprocess.run([sys.executable, "-c", "from timewalk.export import main; main()", str(kit / "repo"), "--toc", str(kit / "toc.toml"),
                           "--walk", "testing", "--markdown", str(out), "--site", str(site), "--github", "https://github.com/o/tally"],
                          capture_output=True, text=True)
    assert done.returncode == 0, done.stderr
    for name in ("TUTORIAL-do.md", "TUTORIAL-watch.md"):
        text = (out / name).read_text()
        assert text.index("This walk takes only the tests of tally") < text.index("## step-02.1 to step-02.3 Three tests of counting")
        assert "> Say:" not in text and "{{include" not in text
        order = ["tally counts words already", "### step-02.1", "The first two tests are the pattern", "### step-02.2", "### step-02.3",
                 "Three tests now say what", "## step-05.1 A test of the most common words", "Since the last part", "### step-05.1", "The walk stops here"]
        assert [text.index(t) for t in order] == sorted(text.index(t) for t in order)
        assert "### step-05.2" not in text and "one file at a time" not in text
    built = subprocess.run(["uvx", "--from", "smalldocs>=0.1.5,<0.2", "smalldocs", "check"], cwd=site, capture_output=True, text=True)
    assert built.returncode == 0 and "0 thing(s) to look at" in built.stdout + built.stderr, built.stdout + built.stderr
    out = tmp_path / "finish"
    done = subprocess.run([sys.executable, "-c", "from timewalk.export import main; main()", str(kit / "repo"), "--toc", str(kit / "toc.toml"),
                           "--walk", "finish", "--markdown", str(out), "--github", "https://github.com/o/tally"], capture_output=True, text=True)
    assert done.returncode == 0, done.stderr
    do, watch = ((out / name).read_text() for name in ("TUTORIAL-do.md", "TUTORIAL-watch.md"))
    assert "## step-04 Types and a docstring\n\n[The code at its Start]" in do and "### step-04.1" in do and "### step-04.2" in do
    assert "Open `build/top.txt`" in do and "Open `build/top.txt`" not in watch and "the same list that" in watch
