"Tutorial walks: the moves of a step, in do mode (the learner makes each move by hand) and watch mode (timewalk shows each commit)."

import subprocess
from pathlib import Path

import pytest
from conftest import open_windows
from test_walk import shows


@pytest.fixture
def tutored(browser, kit: Path, start):
    "Your window and the Room on the tutorial walk, which starts in do mode."
    address = start("--toc", str(kit / "toc.toml"), "--walk", "tutorial")
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


def wait_for_done(page, kit: Path, move: str) -> None:
    "Wait until the move being worked on is the given one; on a timeout, say what the server and the page saw."
    try:
        page.wait_for_function("(m) => document.querySelector('#notes .p-move.here h3')?.textContent.startsWith(m)", arg=move, timeout=20000)
    except Exception:
        print("visibility:", page.evaluate("document.visibilityState"))
        print("match:", page.evaluate("fetch('/api/match').then((r) => r.json())"))
        print("state:", page.evaluate("fetch('/api/state').then((r) => r.json()).then((s) => [s.mode, s.done, s.move])"))
        print("terminal:", page.evaluate("(window.timewalkTerminals() || []).find((t) => t.id === 'replay')?.tail.slice(-400)"))
        raise


def notes_of(page, step: str) -> None:
    "Wait until the notes column shows the step's notes, and not those of the step before."
    page.wait_for_function("(s) => document.querySelector('#notes-title strong')?.textContent === s", arg=step)


def to_step(page, step: str) -> None:
    "Go right from step-00 to the step, and wait for its notes."
    page.mouse.click(300, 400)
    for number in range(1, int(step[-2:]) + 1):
        page.keyboard.press("ArrowRight")
        shows(page, "#step-name", f"step-{number:02d}")
    notes_of(page, step)


def to_step_02(page) -> None:
    to_step(page, "step-02")


def test_do_mode_marks_moves_done_in_order_and_never_moves_the_code(tutored, kit: Path) -> None:
    "In do mode the code stays at the step's Start; Done marks the next move; the moves after it are greyed and do nothing."
    yours, room, _ = tutored
    to_step_02(yours)
    for page in (yours, room):
        page.wait_for_selector("#moves:not([hidden])")
        page.wait_for_function("document.querySelector('#notes .p-hint')?.textContent.includes('make step-02.1 by hand')")
    assert head(kit).startswith("step-01:"), "a step starts at the code of the step before"
    assert moves_of(yours) == ["Start*", "1", "2", "3"]
    assert yours.evaluate("[...document.querySelectorAll('#moves > button:not(.nav)')].map((b) => b.disabled)") == [False, False, True, True]
    assert sections_of(yours) == "here,later,later"
    assert yours.locator("#notes .p-move.later button:not(:disabled)").count() == 0, "a move after the next waits"
    yours.click("#notes .p-move.here button:has-text('Done')")
    for page in (yours, room):
        page.wait_for_function("document.querySelector('#notes .p-move.here h3')?.textContent.startsWith('step-02.2')")
    assert sections_of(yours) == "done,here,later" and moves_of(yours) == ["Start", "1+", "2", "3"]
    assert head(kit).startswith("step-01:"), "Done does not move the code"
    yours.keyboard.press("Shift+ArrowRight")   # Shift+Right is Done in do mode
    yours.wait_for_function("document.querySelector('#notes .p-move.here h3')?.textContent.startsWith('step-02.3')")

def test_catch_me_up_sets_the_code_to_the_end_of_the_move_worked_on(tutored, kit: Path) -> None:
    "Catch me up on the move being worked on: the code is that move's commit, and the move is done."
    yours, room, _ = tutored
    to_step_02(yours)
    yours.wait_for_selector("#notes .p-move.here button:has-text('Catch me up')")
    assert yours.locator("#notes .p-move button:has-text('Catch me up')").count() == 1, "only on the move being worked on"
    yours.click("#notes .p-move.here button:has-text('Catch me up')")
    for page in (yours, room):
        page.wait_for_function("document.querySelector('#notes .p-move.here h3')?.textContent.startsWith('step-02.2')")
    assert head(kit) == "step-02.1: a test of counting"
    assert sections_of(yours) == "done,here,later"

def test_files_of_a_move_open_its_change_whatever_the_code(tutored) -> None:
    "In do mode, at the start of the step, a files: link of move 1 opens what move 1 changed, in both windows."
    yours, room, _ = tutored
    to_step_02(yours)
    yours.wait_for_selector("#notes .p-move.here .p-files button")
    assert yours.locator("#notes .p-move.here .p-files button").all_inner_texts() == ["± See diff tests/test_count.py"]
    yours.click("#notes .p-move.here .p-files button")
    for page in (yours, room):
        shows(page, "#file-path", "tests/test_count.py")
        shows(page, "#view-next", "Next change: step-02.1")
    assert "def test_case" in yours.locator("#file-body").inner_text()


def test_a_moves_last_commands_are_its_anchor(tutored) -> None:
    "Each move ends with the commands that show what it did, under a label."
    yours, _, _ = tutored
    to_step_02(yours)
    yours.wait_for_selector("#notes .p-move .p-anchor")
    assert yours.locator("#notes .p-move").count() == yours.locator("#notes .p-move .p-anchor").count() == 3
    assert yours.locator("#notes .p-move").first.locator(".p-anchor-label").inner_text() == "After this move, run:"


def test_watch_mode_shows_the_moves_in_order_and_goes_back_to_the_start(tutored, kit: Path) -> None:
    "Watch: Show is on the next move only; the arrow shows the one after; Shift+Left goes back to the step's Start."
    yours, room, _ = tutored
    to_step_02(yours)
    yours.click("#move-modes button:has-text('Watch')")
    for page in (yours, room):
        page.wait_for_function("document.querySelector('#notes .p-hint')?.textContent.includes('press Show on step-02.1')")
    assert sections_of(yours) == "next,later,later"
    assert yours.locator("#notes .p-move button:has-text('Show')").count() == 1
    yours.locator("#notes .p-move").first.locator("button:has-text('Show')").click()
    for page in (yours, room):
        shows(page, "#step-name", "step-02.1")
    assert head(kit) == "step-02.1: a test of counting"
    yours.wait_for_function("(want) => [...document.querySelectorAll('#notes .p-move')].map((s) => s.className.replace('p-move', '').trim()).join(',') === want",
                            arg="here,next,later")
    yours.locator("#moves .nav").last.click()
    shows(room, "#step-name", "step-02.2")
    assert head(kit) == "step-02.2: a test of an empty text"
    yours.mouse.click(300, 400)
    yours.keyboard.press("Shift+ArrowLeft")
    shows(room, "#step-name", "step-02")
    assert head(kit).startswith("step-01:"), "back is the step's Start"

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
    context, yours, room = open_windows(browser, start("--toc", str(kit / "toc.toml"), "--walk", "hooks"))
    shows(yours, "#step-name", "hooks-00")
    yours.mouse.click(300, 400)
    yours.keyboard.press("ArrowRight")
    shows(yours, "#step-name", "hooks-01")
    assert head(kit) == "step-01: the command counts the words", "hooks-01 starts at hooks-00, which is step-01's commit"
    yours.wait_for_selector("#moves:not([hidden])")
    assert yours.locator("#move-modes button[aria-pressed=true]").inner_text() == "Watch"
    yours.keyboard.press("Shift+ArrowRight")
    for page in (yours, room):
        shows(page, "#step-name", "hooks-01.1")
    assert head(kit) == "hooks-01.1: a recipe that checks the code"
    yours.wait_for_function("[...document.querySelectorAll('#notes .p-move.here .p-item-path')].map((b) => b.textContent).join() === 'justfile'")
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


def open_item(page, text: str) -> None:
    "Click See diff or See file on the item of the notes that names that path, in the move being worked on."
    page.locator("#notes .p-move.here .p-item", has=page.locator(".p-item-path", has_text=text)).first.locator("button").click()


def test_an_item_opens_next_change_with_its_line_marked_and_an_excerpt_in_the_notes(tutored) -> None:
    "Do mode at step-02: move 1's diff item opens Next change: step-02.1, its show: line marked; the notes draw the excerpt."
    yours, room, _ = tutored
    to_step_02(yours)
    yours.wait_for_selector("#notes .p-move.here .p-excerpt pre.diff")
    assert "count(\"A a\")" in yours.locator("#notes .p-move.here .p-excerpt").first.inner_text()
    open_item(yours, "tests/test_count.py")
    for page in (yours, room):
        page.wait_for_selector("#view-next[aria-selected=true]")
        shows(page, "#view-next", "Next change: step-02.1")
        page.wait_for_selector("#file-body .line.mark")


def test_an_item_says_see_diff_and_its_excerpt_opens_the_change_too(tutored) -> None:
    "An item is one button, ± See diff and the path, with the author's words under it; a click on its excerpt opens the change as the button does."
    yours, room, _ = tutored
    to_step_02(yours)
    item = yours.locator("#notes .p-move.here .p-item").first
    item.wait_for()
    assert item.locator("button").inner_text() == "± See diff tests/test_count.py"
    assert item.locator(".p-item-words").inner_text().startswith("two tests.")
    words, button = (item.locator(sel).bounding_box() for sel in (".p-item-words", "button"))
    assert words["y"] >= button["y"] + button["height"] - 1, "the author's words are under the button"
    yours.locator("#notes .p-move.here .p-excerpt pre.diff").first.click()
    for page in (yours, room):
        page.wait_for_selector("#view-next[aria-selected=true]")
        shows(page, "#file-path", "tests/test_count.py")
    # A move after the next one: its excerpt does nothing yet.
    yours.locator("#notes .p-move.later .p-excerpt pre.diff").first.click()
    yours.wait_for_timeout(500)
    shows(yours, "#file-path", "tests/test_count.py")


def test_apply_the_whole_move_then_the_files_match_and_the_move_is_done(tutored, kit: Path) -> None:
    "Apply types git cherry-pick into the shell; the files then match step-02.1, and move 1 is marked done by itself."
    yours, room, _ = tutored
    to_step_02(yours)
    yours.wait_for_selector("#notes .p-move.here .p-item")
    open_item(yours, "tests/test_count.py")
    yours.wait_for_selector("#apply-bar:not([hidden])")
    yours.bring_to_front()   # a hidden window does not ask whether the files match, and the Room never marks Done
    yours.click("#apply-move")
    wait_for_done(yours, kit, "step-02.2")
    room.wait_for_function("document.querySelector('#notes .p-move.here h3')?.textContent.startsWith('step-02.2')")
    assert (kit / "repo-replay" / "tests" / "test_count.py").is_file()
    assert head(kit).startswith("step-01:"), "Apply makes edits; the code is still at the step's start"


def test_apply_is_disabled_on_a_file_the_learner_changed(tutored, kit: Path) -> None:
    "The learner made tests/test_count.py their own way: Apply is disabled, and says what to do instead."
    yours, _, _ = tutored
    to_step_02(yours)
    (kit / "repo-replay" / "tests").mkdir(exist_ok=True)
    (kit / "repo-replay" / "tests" / "test_count.py").write_text("# my own try\n")
    subprocess.run(["git", "-C", str(kit / "repo-replay"), "add", "-N", "tests/test_count.py"], check=True)
    yours.wait_for_selector("#notes .p-move.here .p-item")
    yours.wait_for_function("document.querySelector('#tree')?.innerText.includes('test_count.py')")
    open_item(yours, "tests/test_count.py")
    yours.wait_for_selector("#apply-bar:not([hidden])")
    yours.wait_for_function("document.getElementById('apply-move').disabled")
    assert "Catch me up" in yours.locator("#apply-note").inner_text()


def test_a_file_item_of_a_move_not_made_shows_the_answer(tutored) -> None:
    "Do mode at step-05: the file item of move 1 opens the file as step-05.1 leaves it, read only, as the tab says."
    yours, _, _ = tutored
    to_step(yours, "step-05")
    yours.wait_for_selector("#notes .p-move.here .p-item")
    open_item(yours, "tests/test_top.py")
    shows(yours, "#view-at", "At step-05.1")
    yours.wait_for_selector("#view-at[aria-selected=true]")
    assert "test_most_common_first" in yours.locator("#file-body").inner_text()


def test_your_file_offers_your_own_editor(tutored) -> None:
    "Your file has a link to open the file in your editor, at the marked line; the Room has none."
    yours, room, _ = tutored
    yours.locator("#tree .file button", has_text="README.md").first.click()
    yours.wait_for_selector("#open-editor:not([hidden])")
    assert yours.locator("#open-editor").get_attribute("href").startswith("vscode://file/")
    room.wait_for_function("document.getElementById('file-path').textContent === 'README.md'")
    assert room.locator("#open-editor").is_hidden()


def test_back_to_the_start_puts_the_code_back_in_do_mode(tutored, kit: Path) -> None:
    "After Apply and Done, Start puts the code back at the step's start, and no move is done: then just setup."
    yours, _, _ = tutored
    to_step_02(yours)
    yours.wait_for_selector("#notes .p-move.here .p-item")
    open_item(yours, "tests/test_count.py")
    yours.wait_for_selector("#apply-bar:not([hidden])")
    yours.bring_to_front()   # a hidden window does not ask whether the files match, and the Room never marks Done
    yours.click("#apply-move")
    wait_for_done(yours, kit, "step-02.2")
    yours.click("#moves button:has-text('Start')")
    yours.wait_for_function("document.querySelector('#notes .p-move.here h3')?.textContent.startsWith('step-02.1')")
    assert not (kit / "repo-replay" / "tests" / "test_count.py").exists(), "the applied file is gone from the copy"
    saved = subprocess.run(["git", "-C", str(kit / "repo-replay"), "for-each-ref", "--format=%(refname:short)", "refs/heads/timewalk/saved"],
                           capture_output=True, text=True).stdout.split()
    assert len(saved) == 1 and "def test_case" in subprocess.run(
        ["git", "-C", str(kit / "repo-replay"), "show", f"{saved[0]}:tests/test_count.py"], capture_output=True, text=True).stdout, "and kept"
    assert yours.locator("#notes .p-hint").inner_text().startswith("Run just setup. Then make step-02.1 by hand")

ABOUT_DO = ("Build tally yourself, one small commit at a time: a function, its tests, types, and a report. A tutorial has one or more "
            "steps, and each step has zero or more moves")


def test_the_status_band_says_where_you_are_and_what_to_do(tutored) -> None:
    "The band, in both windows: the walk's description at its first step only; then the mode, the step, the moves made and the next thing; the tag."
    yours, room, _ = tutored
    for page in (yours, room):
        page.wait_for_selector("#note:not([hidden]) #about:not([hidden])")
        assert page.locator("#about").inner_text().startswith(ABOUT_DO)
        assert "In do mode, you make each move by hand" in page.locator("#about").inner_text()
        shows(page, "#status", "Tutorial, do mode · step-00, step 1 of 6 · no moves · Run just setup and the commands in the notes. "
              "Press Next step, at the end of the notes, or the Right arrow, for the next step.")
        assert page.locator("#tag strong").inner_text() == "Where it starts"
        assert page.locator("#tag").inner_text() == "Where it starts — A project with a command that does nothing yet."
    to_step(yours, "step-01")
    do = "Tutorial, do mode · step-01, step 2 of 6 · 0 of 2 moves made · Run just setup. Then make step-01.1 by hand, " \
         "run the command at the end of its section, and press Done."
    for page in (yours, room):
        shows(page, "#status", do)
        assert page.locator("#about").is_hidden(), "the description is for the walk's first step"
        shows(page, "#tag", "Counting — The command counts words, one line per word.")
    yours.click("#move-modes button:has-text('Watch')")
    for page in (yours, room):
        shows(page, "#status", "Tutorial, watch mode · step-01, step 2 of 6 · 0 of 2 moves made · Run just setup. Then press Show "
              "on step-01.1 (Shift+Right), and run the command at the end of its section.")
    yours.keyboard.press("Shift+ArrowRight")
    for page in (yours, room):
        shows(page, "#status", "Tutorial, watch mode · step-01, step 2 of 6 · 1 of 2 moves made · Press Show on step-01.2 "
              "(Shift+Right), and run the command at the end of its section.")


def test_a_shown_move_keeps_a_grayed_shown_button_and_restart_step_goes_back(tutored, kit: Path) -> None:
    "Watch mode at step-01: after Show, move 1 keeps Shown, disabled; Restart step goes back to the Start in both windows, and Show comes back."
    yours, room, _ = tutored
    to_step(yours, "step-01")
    yours.click("#move-modes button:has-text('Watch')")
    yours.wait_for_selector("#notes .p-move.next button:has-text('Show')")
    assert yours.locator("#notes .p-restart").count() == 0, "nothing to restart at the Start"
    yours.locator("#notes .p-move.next button:has-text('Show')").click()
    for page in (yours, room):
        shows(page, "#step-name", "step-01.1")
        page.wait_for_selector("#notes .p-move.here button:has-text('Shown')")
    assert head(kit) == "step-01.1: a function that counts"
    shown = yours.locator("#notes .p-move.here .p-move-actions button")
    assert shown.all_inner_texts() == ["Shown ✓"] and shown.is_disabled()
    assert yours.locator("#notes .p-move.next button:has-text('Show ▶')").is_enabled(), "the next move has Show"
    assert yours.locator("#notes .p-move.here .p-restart button").inner_text() == "↺ Restart step"
    yours.wait_for_timeout(600)   # past the moment when the page's own scroll to the move is not sent on
    yours.hover("#notes-body")
    yours.mouse.wheel(0, 400)   # the server remembers this scroll for the step; the Start must still go to the top
    yours.wait_for_function("document.getElementById('notes-body').scrollTop > 100")
    yours.wait_for_timeout(800)
    yours.click("#notes .p-move.here .p-restart button")
    for page in (yours, room):
        shows(page, "#step-name", "step-01")
        page.wait_for_function("document.querySelector('#notes .p-move.next h3')?.textContent.startsWith('step-01.1')")
    assert head(kit).startswith("step-00:"), "the Start is the code of the step before"
    assert yours.locator("#notes .p-move.next button:has-text('Show ▶')").is_enabled()
    assert yours.locator("#notes button:has-text('Shown')").count() == 0
    for page in (yours, room):
        page.wait_for_timeout(500)
        assert page.evaluate("document.getElementById('notes-body').scrollTop") == 0, "at the Start, the notes are at the top"


def test_restart_step_in_do_mode_undoes_the_moves_marked_done(tutored) -> None:
    "Do mode at step-01: Done on move 1 leaves Done, grayed, and Restart step; Restart step makes move 1 the one worked on again."
    yours, room, _ = tutored
    to_step(yours, "step-01")
    assert yours.locator("#notes .p-restart").count() == 0, "nothing to restart before a move is made"
    yours.click("#notes .p-move.here button:has-text('Done')")
    for page in (yours, room):
        page.wait_for_function("document.querySelector('#notes .p-move.here h3')?.textContent.startsWith('step-01.2')")
    done = yours.locator("#notes .p-move.done .p-move-actions button")
    assert done.all_inner_texts() == ["Made ✓"] and done.is_disabled()
    yours.locator("#notes .p-move.done .p-restart button").click()
    for page in (yours, room):
        page.wait_for_function("document.querySelector('#notes .p-move.here h3')?.textContent.startsWith('step-01.1')")
        assert page.locator("#notes .p-move.done").count() == 0
    assert yours.locator("#notes .p-move.here button.primary").inner_text() == "Done ✓"


def test_text_before_the_first_move_is_a_section_of_its_own(tutored) -> None:
    "At step-01, just setup and the words before step-01.1 are in Before the moves; step-00 has no moves, and no such section."
    yours, _, _ = tutored
    yours.wait_for_selector("#notes .p-hint")
    assert yours.locator("#notes .p-bridge").count() == 0
    to_step(yours, "step-01")
    bridge = yours.locator("#notes .p-bridge")
    assert bridge.locator(".p-bridge-label").text_content() == "Before the moves"
    assert "Two moves: first a function that counts" in bridge.inner_text()
    assert bridge.locator(".p-commands button").first.inner_text().startswith("just setup")
    assert yours.evaluate("document.querySelector('#notes').firstElementChild.className") == "p-hint"
    assert yours.locator("#notes .p-move").count() == 2


def test_next_step_at_the_end_of_the_notes_moves_both_windows(tutored) -> None:
    "step-00 has no moves: Next step ends the notes, and the slide head offers it too. At step-01 it waits until both moves are done."
    yours, room, _ = tutored
    yours.wait_for_selector("#notes .p-next-step button.go")
    assert yours.locator("#notes").evaluate("(n) => n.lastElementChild.className") == "p-next-step"
    assert yours.locator("#notes .p-next-step button").inner_text() == "Next step: step-01 ▶"
    yours.wait_for_selector("#slide-step:not([hidden])")   # step-00 has one slide, so it is the last
    shows(yours, "#slide-step", "Next step: step-01 ▶")
    assert room.locator("#slide-step").is_hidden(), "the Room window has no Next step in the slide head"
    yours.click("#notes .p-next-step button")
    for page in (yours, room):
        shows(page, "#step-name", "step-01")
    notes_of(yours, "step-01")
    assert yours.locator("#notes .p-next-step").count() == 0 and yours.locator("#slide-step").is_hidden(), "two moves to make first"
    for move in ("step-01.1", "step-01.2"):
        yours.wait_for_function("(m) => document.querySelector('#notes .p-move.here h3')?.textContent.startsWith(m)", arg=move)
        yours.click("#notes .p-move.here button.primary:has-text('Done')")
    yours.wait_for_selector("#notes .p-next-step button.go")
    yours.wait_for_selector("#slide-step:not([hidden])")
    shows(yours, "#slide-step", "Next step: step-02 ▶")
    yours.click("#move-modes button:has-text('Watch')")   # in watch mode no move is shown yet: no Next step anywhere
    yours.wait_for_selector("#slide-step[hidden]", state="attached")
    assert yours.locator("#notes .p-next-step").count() == 0
    yours.click("#move-modes button:has-text('Do')")
    yours.wait_for_selector("#slide-step:not([hidden])")
    yours.click("#slide-step")
    for page in (yours, room):
        shows(page, "#step-name", "step-02")


def test_step_01_moves_in_do_mode_by_hand_and_when_the_files_match(tutored, kit: Path) -> None:
    "Do mode at step-01: Done marks move 1 by hand; then the learner writes move 2's file, the files match, and move 2 is done by itself."
    yours, room, _ = tutored
    to_step(yours, "step-01")
    assert head(kit).startswith("step-00:"), "step-01 starts at step-00's code"
    assert moves_of(yours) == ["Start*", "1", "2"] and sections_of(yours) == "here,later"
    yours.click("#notes .p-move.here button.primary:has-text('Done')")
    for page in (yours, room):
        page.wait_for_function("document.querySelector('#notes .p-move.here h3')?.textContent.startsWith('step-01.2')")
    assert moves_of(yours) == ["Start", "1+", "2"]
    tagged = subprocess.run(["git", "-C", str(kit / "repo"), "show", "step-01:src/tally/__init__.py"], capture_output=True, text=True, check=True).stdout
    yours.bring_to_front()   # a hidden window does not ask whether the files match
    (kit / "repo-replay" / "src" / "tally" / "__init__.py").write_text(tagged)
    yours.wait_for_function("document.querySelectorAll('#notes .p-move.done').length === 2", timeout=20000)
    room.wait_for_function("document.querySelectorAll('#notes .p-move.done').length === 2")
    shows(yours, "#status", "Tutorial, do mode · step-01, step 2 of 6 · 2 of 2 moves made · Every move is made. "
          "Press Next step, at the end of the notes, or the Right arrow, for the next step.")
    yours.wait_for_selector("#notes .p-next-step button:has-text('Next step: step-02')")


def saved_branches(kit: Path) -> list[str]:
    "The branches timewalk/saved/... in the replay copy, where the learner's work is kept."
    out = subprocess.run(["git", "-C", str(kit / "repo-replay"), "for-each-ref", "--format=%(refname:short)", "refs/heads/timewalk/saved"],
                         capture_output=True, text=True, check=True).stdout
    return out.split()


def test_catch_me_up_over_a_file_made_by_hand_keeps_it_and_goes_on(tutored, kit: Path) -> None:
    """Do mode at step-02: the learner writes the move's new file by hand, then Catch me up. The move's file takes its place,
    and the learner's is kept on timewalk/saved/<place>; your window says where, and the Room does not."""
    yours, room, _ = tutored
    to_step_02(yours)
    yours.wait_for_selector("#notes .p-move.here button:has-text('Catch me up')")
    (kit / "repo-replay" / "tests").mkdir(exist_ok=True)
    (kit / "repo-replay" / "tests" / "test_count.py").write_text("# my own try\n")
    yours.click("#notes .p-move.here button:has-text('Catch me up')")
    for page in (yours, room):
        shows(page, "#step-name", "step-02.1")
    assert head(kit) == "step-02.1: a test of counting"
    assert "def test_case" in (kit / "repo-replay" / "tests" / "test_count.py").read_text()
    [branch] = saved_branches(kit)
    kept = subprocess.run(["git", "-C", str(kit / "repo-replay"), "show", f"{branch}:tests/test_count.py"], capture_output=True, text=True).stdout
    assert kept == "# my own try\n"
    yours.wait_for_selector(f"#notice:not([hidden]):has-text('{branch}')")
    assert room.locator("#notice").is_hidden()


def test_restart_step_keeps_the_edits_made_by_hand(tutored, kit: Path) -> None:
    "Do mode at step-01: an edit by hand, Done, then Restart step. The code is the step's Start, and the edit is on a saved branch."
    yours, room, _ = tutored
    to_step(yours, "step-01")
    init = kit / "repo-replay" / "src" / "tally" / "__init__.py"
    init.write_text(init.read_text() + "\n# my edit\n")
    yours.click("#notes .p-move.here button.primary:has-text('Done')")
    yours.wait_for_selector("#notes .p-move.done .p-restart button")
    yours.click("#notes .p-move.done .p-restart button")
    for page in (yours, room):
        page.wait_for_function("document.querySelector('#notes .p-move.here h3')?.textContent.startsWith('step-01.1')")
    assert "# my edit" not in init.read_text()
    [branch] = saved_branches(kit)
    assert "# my edit" in subprocess.run(["git", "-C", str(kit / "repo-replay"), "show", f"{branch}:src/tally/__init__.py"],
                                         capture_output=True, text=True).stdout
    yours.wait_for_selector(f"#notice:not([hidden]):has-text('{branch}')")
