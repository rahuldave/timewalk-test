"A tutorial walk: the moves of a step, one at a time, in both windows, with the notes, the slides and the files of each move."

import subprocess
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import pytest
from conftest import open_windows
from test_walk import shows


@pytest.fixture
def tutored(browser, kit: Path, start):
    "Your window and the Room on the tutorial walk, with --discard-edits."
    address = start("--toc", str(kit / "toc.toml"), "--walk", "tutorial", "--discard-edits")
    context, yours, room = open_windows(browser, address)
    yield yours, room, address
    context.close()


def head(kit: Path) -> str:
    "The subject of the commit the replay copy stands on."
    return subprocess.run(["git", "-C", str(kit / "repo-replay"), "log", "-1", "--format=%s"], capture_output=True, text=True).stdout.strip()


def moves_of(page) -> list[str]:
    "The moves row as the page draws it: each button's text, with * for the one on show and - for one that is closed."
    return page.evaluate("""[...document.querySelectorAll('#moves button')]
        .map((b) => b.textContent + (b.classList.contains('here') ? '*' : '') + (b.disabled ? '-' : ''))""")


def to_step_02(page) -> None:
    page.mouse.click(300, 400)
    page.keyboard.press("ArrowRight")
    shows(page, "#step-name", "step-01")
    page.keyboard.press("ArrowRight")
    shows(page, "#step-name", "step-02")


def test_a_step_starts_before_its_first_move_and_the_moves_go_one_at_a_time(tutored, kit: Path) -> None:
    "At step-02, both windows show its moves; Shift+Right makes the next, the code follows, and only the next move is open."
    yours, room, _ = tutored
    for page in (yours, room):
        assert page.locator("#moves").is_hidden(), "step-00 has no moves"
    to_step_02(yours)
    assert head(kit).startswith("step-01:"), "a step starts at the code of the step before"
    for page in (yours, room):
        page.wait_for_selector("#moves:not([hidden])")
        assert moves_of(page) == ["Start*", "1", "2-", "3-"]
    yours.keyboard.press("Shift+ArrowRight")
    for page in (yours, room):
        shows(page, "#step-name", "step-02.1")
        page.wait_for_function("document.querySelector('#slide h1')?.textContent === 'Move one'")
        assert moves_of(page) == ["Start", "1*", "2", "3-"]
    assert head(kit) == "step-02.1: a test of counting"
    yours.keyboard.press("Shift+ArrowRight")
    yours.keyboard.press("Shift+ArrowRight")
    for page in (yours, room):
        shows(page, "#step-name", "step-02.3")
        page.wait_for_function("document.querySelector('#slide h1')?.textContent === 'Move three'")
    assert head(kit).startswith("step-02:"), "the last move is the step's own commit"
    yours.keyboard.press("Shift+ArrowLeft")
    shows(room, "#step-name", "step-02.2")
    assert head(kit) == "step-02.2: a test of an empty text"


def test_the_notes_gray_the_moves_still_to_make_and_list_each_moves_files(tutored) -> None:
    "Each move has a section; the later ones are grayed with their buttons off. files: opens a file of that move."
    yours, room, _ = tutored
    to_step_02(yours)
    yours.keyboard.press("Shift+ArrowRight")
    shows(yours, "#step-name", "step-02.1")
    sections = "[...document.querySelectorAll('#notes .p-move')].map((s) => s.className.replace('p-move ', ''))"
    yours.wait_for_function(f"{sections}.join() === 'here,later,later'")
    assert yours.locator("#notes .p-move.later .p-commands button").first.is_disabled()
    assert yours.locator("#notes .p-move.here .p-files button").all_inner_texts() == ["tests/test_count.py"]
    yours.click("#notes .p-move.here .p-files button")
    for page in (yours, room):
        shows(page, "#file-path", "tests/test_count.py")


def test_down_past_a_move_without_slides_makes_that_move_first(tutored, kit: Path) -> None:
    "From move 1, the next slide is move three's; move 2 has none. Down makes move 2 and keeps the slide; Down again makes move 3."
    yours, room, _ = tutored
    to_step_02(yours)
    yours.keyboard.press("Shift+ArrowRight")
    shows(yours, "#step-name", "step-02.1")
    yours.keyboard.press("ArrowDown")
    for page in (yours, room):
        shows(page, "#step-name", "step-02.2")
        page.wait_for_function("document.querySelector('#slide h1')?.textContent === 'Move one'")
    yours.keyboard.press("ArrowDown")
    for page in (yours, room):
        shows(page, "#step-name", "step-02.3")
        page.wait_for_function("document.querySelector('#slide h1')?.textContent === 'Move three'")
    assert head(kit).startswith("step-02:")


def test_alt_shift_right_makes_a_move_from_inside_a_terminal(tutored) -> None:
    "With the keys in a terminal, Alt+Shift+Right still makes the next move."
    yours, _, _ = tutored
    to_step_02(yours)
    yours.locator("#terms .term:not([hidden])").click()
    yours.keyboard.press("Alt+Shift+ArrowRight")
    shows(yours, "#step-name", "step-02.1")


def test_the_api_refuses_a_jump_over_a_move(tutored) -> None:
    "The order holds for every window: the server refuses move 3 from the start of the step."
    yours, _, address = tutored
    to_step_02(yours)
    token = parse_qs(urlparse(address).query)["t"][0]
    status = yours.evaluate("""async (t) => (await fetch('/api/move?t=' + t, {method: 'POST', headers: {'content-type': 'application/json'},
                               body: JSON.stringify({to: 2, move: 3})})).status""", token)
    assert status == 409


def test_alt_shift_right_in_the_notes_editor_selects_and_does_not_move(tutored, kit: Path) -> None:
    "In the Edit box of the notes, Option+Shift+Right selects a word, as in any text field; the tutorial stays where it is."
    yours, _, _ = tutored
    to_step_02(yours)
    yours.click("#notes-edit")
    yours.locator("#notes-text").evaluate("e => { e.focus(); e.setSelectionRange(0, 0); }")
    yours.keyboard.press("Alt+Shift+ArrowRight")
    yours.wait_for_timeout(500)
    shows(yours, "#step-name", "step-02")
    assert head(kit).startswith("step-01:")
