"Tutorial walks: the moves of a step, in do mode (the learner makes each move by hand) and watch mode (timewalk shows each commit)."

import subprocess
from pathlib import Path

import pytest
from conftest import open_windows
from test_walk import shows


@pytest.fixture
def tutored(browser, kit: Path, start):
    "Your window and the Room on the tutorial walk, which starts in do mode, with --discard-edits."
    address = start("--toc", str(kit / "toc.toml"), "--walk", "tutorial", "--discard-edits")
    context, yours, room = open_windows(browser, address)
    yield yours, room, address
    context.close()


def head(kit: Path) -> str:
    "The subject of the commit the replay copy stands on."
    return subprocess.run(["git", "-C", str(kit / "repo-replay"), "log", "-1", "--format=%s"], capture_output=True, text=True).stdout.strip()


def moves_of(page) -> list[str]:
    "The move buttons of the moves row: each one's text, with * for the one on show and + for one done."
    return page.evaluate("""[...document.querySelectorAll('#moves > button:not(.nav)')]
        .map((b) => b.textContent + (b.classList.contains('here') ? '*' : '') + (b.classList.contains('done') ? '+' : ''))""")


def sections_of(page) -> str:
    "The move sections of the notes, by state: here, done, ahead or none."
    return page.evaluate("[...document.querySelectorAll('#notes .p-move')].map((s) => s.className.replace('p-move', '').trim() || '-').join(',')")


def to_step_02(page) -> None:
    page.mouse.click(300, 400)
    page.keyboard.press("ArrowRight")
    shows(page, "#step-name", "step-01")
    page.keyboard.press("ArrowRight")
    shows(page, "#step-name", "step-02")


def test_do_mode_marks_moves_done_and_never_moves_the_code(tutored, kit: Path) -> None:
    "In do mode, the code stays at the start of the step; Done marks each move, in both windows; nothing is locked or grayed."
    yours, room, _ = tutored
    to_step_02(yours)
    for page in (yours, room):
        page.wait_for_selector("#moves:not([hidden])")
        page.wait_for_function("document.querySelector('#notes .p-hint')?.textContent.startsWith('Do:')")
    assert head(kit).startswith("step-01:"), "a step starts at the code of the step before"
    assert moves_of(yours) == ["Start", "1*", "2", "3"]
    assert sections_of(yours) == "here,-,-"
    assert yours.locator("#notes .p-move button:disabled").count() == 0 and yours.locator("#notes .p-commands button:disabled").count() == 0
    yours.click("#notes .p-move.here button:has-text('Done')")
    for page in (yours, room):
        page.wait_for_function("document.querySelector('#notes .p-move.here h3')?.textContent.startsWith('step-02.2')")
    assert sections_of(yours) == "done,here,-" and moves_of(yours) == ["Start", "1+", "2*", "3"]
    assert head(kit).startswith("step-01:"), "Done does not move the code"
    yours.keyboard.press("Shift+ArrowRight")   # Shift+Right is Done in do mode
    yours.wait_for_function("document.querySelector('#notes .p-move.here h3')?.textContent.startsWith('step-02.3')")
    assert head(kit).startswith("step-01:")


def test_catch_me_up_sets_the_code_to_the_end_of_a_move(tutored, kit: Path) -> None:
    "Catch me up on move 2: the code is that move's commit, and the moves up to it are done."
    yours, room, _ = tutored
    to_step_02(yours)
    yours.wait_for_selector("#notes .p-move")
    yours.locator("#notes .p-move").nth(1).locator("button:has-text('Catch me up')").click()
    for page in (yours, room):
        page.wait_for_function("document.querySelector('#notes .p-move.here h3')?.textContent.startsWith('step-02.3')")
    assert head(kit) == "step-02.2: a test of an empty text"
    assert sections_of(yours) == "done,done,here"


def test_files_of_a_move_open_its_change_whatever_the_code(tutored) -> None:
    "In do mode, at the start of the step, a files: link of move 1 opens what move 1 changed, in both windows."
    yours, room, _ = tutored
    to_step_02(yours)
    yours.wait_for_selector("#notes .p-move.here .p-files button")
    assert yours.locator("#notes .p-move.here .p-files button").all_inner_texts() == ["tests/test_count.py"]
    yours.click("#notes .p-move.here .p-files button")
    for page in (yours, room):
        shows(page, "#file-path", "tests/test_count.py")
        shows(page, "#view-diff", "Changes in step-02.1")
    assert "def test_case" in yours.locator("#file-body").inner_text()


def test_a_moves_last_commands_are_its_anchor(tutored) -> None:
    "Each move ends with the commands that show what it did, under a label."
    yours, _, _ = tutored
    to_step_02(yours)
    yours.wait_for_selector("#notes .p-move .p-anchor")
    assert yours.locator("#notes .p-move").count() == yours.locator("#notes .p-move .p-anchor").count() == 3
    assert yours.locator("#notes .p-move").first.locator(".p-anchor-label").inner_text() == "After this move, run:"


def test_watch_mode_shows_any_moves_commit_from_the_notes_or_the_arrows(tutored, kit: Path) -> None:
    "Switch to Watch: Show on move 2 checks out its commit, skipping move 1; the arrow goes on to move 3; both windows follow."
    yours, room, _ = tutored
    to_step_02(yours)
    yours.click("#move-modes button:has-text('Watch')")
    for page in (yours, room):
        page.wait_for_function("document.querySelector('#notes .p-hint')?.textContent.startsWith('Watch:')")
    assert sections_of(yours) == "ahead,ahead,ahead"
    yours.locator("#notes .p-move").nth(1).locator("button:has-text('Show')").click()
    for page in (yours, room):
        shows(page, "#step-name", "step-02.2")
    assert head(kit) == "step-02.2: a test of an empty text"
    yours.wait_for_function("(want) => [...document.querySelectorAll('#notes .p-move')].map((s) => s.className.replace('p-move', '').trim()).join(',') === want",
                            arg="done,here,ahead")
    yours.locator("#moves .nav").last.click()
    shows(room, "#step-name", "step-02.3")
    assert head(kit).startswith("step-02:")
    yours.keyboard.press("Shift+ArrowLeft")
    shows(room, "#step-name", "step-02.2")


def test_watch_mode_slides_follow_the_moves(tutored) -> None:
    "In watch mode with sync, showing move 1 shows its own slide."
    yours, room, _ = tutored
    to_step_02(yours)
    yours.click("#move-modes button:has-text('Watch')")
    yours.wait_for_selector("#notes .p-move button:has-text('Show')")
    yours.locator("#notes .p-move").first.locator("button:has-text('Show')").click()
    for page in (yours, room):
        page.wait_for_function("document.querySelector('#slide h1')?.textContent === 'Move one'")


def test_alt_shift_right_works_from_inside_a_terminal(tutored) -> None:
    "With the keys in a terminal, Alt+Shift+Right marks the move done in do mode."
    yours, _, _ = tutored
    to_step_02(yours)
    yours.wait_for_selector("#notes .p-move.here")
    yours.locator("#terms .term:not([hidden])").click()
    yours.keyboard.press("Alt+Shift+ArrowRight")
    yours.wait_for_function("document.querySelector('#notes .p-move.here h3')?.textContent.startsWith('step-02.2')")


def test_alt_shift_right_in_the_notes_editor_selects_and_does_not_move(tutored, kit: Path) -> None:
    "In the Edit box of the notes, Option+Shift+Right selects a word, as in any text field; nothing changes."
    yours, _, _ = tutored
    to_step_02(yours)
    yours.wait_for_selector("#notes .p-move.here")
    yours.click("#notes-edit")
    yours.locator("#notes-text").evaluate("e => { e.focus(); e.setSelectionRange(0, 0); }")
    yours.keyboard.press("Alt+Shift+ArrowRight")
    yours.wait_for_timeout(500)
    assert head(kit).startswith("step-01:")
    assert yours.locator("#notes-editor").is_visible()


def test_the_hooks_walk_starts_in_watch_mode_on_tags_of_its_own(browser, kit: Path, start) -> None:
    "The hooks walk: moves between hooks-00 and hooks-01 on its branch, in watch mode; with sync off, Down pages the slides only."
    context, yours, room = open_windows(browser, start("--toc", str(kit / "toc.toml"), "--walk", "hooks", "--discard-edits"))
    shows(yours, "#step-name", "hooks-00")
    yours.mouse.click(300, 400)
    yours.keyboard.press("ArrowRight")
    shows(yours, "#step-name", "hooks-01")
    assert head(kit) == "step-01: count the words", "hooks-01 starts at hooks-00, which is step-01's commit"
    yours.wait_for_selector("#moves:not([hidden])")
    assert yours.locator("#move-modes button[aria-pressed=true]").inner_text() == "Watch"
    yours.keyboard.press("Shift+ArrowRight")
    for page in (yours, room):
        shows(page, "#step-name", "hooks-01.1")
    assert head(kit) == "hooks-01.1: a recipe that checks the code"
    yours.wait_for_function("[...document.querySelectorAll('#notes .p-move.here .p-files button')].map((b) => b.textContent).join() === 'justfile'")
    shows(yours, "#slide-count", "Slide 1 of 3")
    yours.keyboard.press("ArrowDown")
    yours.keyboard.press("ArrowDown")
    shows(yours, "#slide-count", "Slide 3 of 3")   # move 3's slide, shown without making move 3: sync is off
    assert head(kit) == "hooks-01.1: a recipe that checks the code"
    context.close()


def test_the_mode_shows_at_every_step_of_a_tutorial(tutored) -> None:
    "At step-00, which has no moves, the Do / Watch switch already shows and works; the Room names the mode in its title."
    yours, room, _ = tutored
    yours.wait_for_selector("#move-modes:not([hidden])")
    assert yours.locator("#moves").is_hidden(), "step-00 has no moves"
    assert yours.locator("#move-modes button[aria-pressed=true]").inner_text() == "Do"
    shows(room, "#walk-title", "tally, one move at a time (tutorial, do mode)")
    yours.click("#move-modes button:has-text('Watch')")
    yours.wait_for_selector("#move-modes button[data-mode=watch][aria-pressed=true]")
    shows(room, "#walk-title", "tally, one move at a time (tutorial, watch mode)")
    assert room.locator("#move-modes").is_hidden()
