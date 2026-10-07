"The Shell toggle, the keys for every toggle, and what the Room window shares of a terminal: its scroll and its size."

import time

from test_walk import output_of


def same_size(yours, room, timeout: float = 15) -> dict:
    "Wait until your window's terminal has the Room's rows and columns, both read fresh each time. Returns the Room's."
    deadline = time.time() + timeout
    while True:
        theirs, mine = room.evaluate(terminal(room)), yours.evaluate(terminal(yours))
        if theirs and mine and (theirs["rows"], theirs["cols"]) == (mine["rows"], mine["cols"]):
            return theirs
        assert time.time() < deadline, f"your terminal is {mine}, the Room's is {theirs}"
        time.sleep(0.2)


def until(page, script: str, arg=None, timeout: int = 15000) -> None:
    "Wait until the script, run in the page, returns something true."
    page.wait_for_function(script, arg=arg, timeout=timeout)


def terminal(page, name: str = "replay") -> str:
    "A script that finds one terminal's facts, through the page's read-only hook."
    return f"(window.timewalkTerminals?.() || []).find((t) => t.id === {name!r})"


def test_shell_gives_the_terminal_the_room_of_the_slides_and_files_in_both_windows(windows) -> None:
    "The Shell button hides the slides and files and lets the terminal fill the space, in both windows; again, back."
    yours, room = windows
    yours.click("#shell-toggle")
    for page in (yours, room):
        until(page, "document.body.classList.contains('shell-mode')")
        until(page, "document.querySelector('#term-pane').getBoundingClientRect().height > 0.6 * innerHeight")
        assert not page.locator("#slide-pane").is_visible()
    assert room.locator("#shell-toggle").is_hidden(), "the Room window has no Shell button"
    yours.click("#shell-toggle")
    for page in (yours, room):
        until(page, "!document.body.classList.contains('shell-mode') && document.querySelector('#slide-pane').offsetParent !== null")


def test_alt_keys_switch_the_toggles_even_inside_a_terminal(windows) -> None:
    "Alt+Enter is Shell; Alt+1, 2, 3 are Slides, Both, Code; Alt+` is Slides or Code; Alt+N hides the notes of this window only."
    yours, room = windows
    yours.locator("#terms .term:not([hidden])").click()  # the terminal has the keys
    yours.keyboard.press("Alt+Enter")
    for page in (yours, room):
        until(page, "document.body.classList.contains('shell-mode')")
    yours.keyboard.press("Alt+Enter")
    for page in (yours, room):
        until(page, "!document.body.classList.contains('shell-mode')")
    for key, layout in (("Alt+3", "code"), ("Alt+1", "slides"), ("Alt+Backquote", "code"), ("Alt+Backquote", "slides"), ("Alt+2", "split")):
        yours.keyboard.press(key)
        for page in (yours, room):
            until(page, "(want) => document.body.dataset.layout === want", layout)
    assert room.locator("#notes-pane").is_visible()
    yours.keyboard.press("Alt+KeyN")
    until(yours, "document.querySelector('#notes-pane').hidden")
    assert room.locator("#notes-pane").is_visible(), "the notes are hidden in your window only"


def test_in_shell_mode_the_room_sizes_the_shell_and_your_window_follows(windows, served: str) -> None:
    "The Room is larger than your window. In Shell mode the shell takes the Room's size, and your terminal shows the same rows and columns."
    yours, room = windows
    room.set_viewport_size({"width": 1920, "height": 1080})
    yours.set_viewport_size({"width": 1280, "height": 800})
    yours.click("#shell-toggle")
    until(room, "document.body.classList.contains('shell-mode')")
    size = same_size(yours, room)
    assert yours.evaluate(terminal(yours))["fontSize"] < 14, "your window scales its font down to fit the Room's columns"
    yours.locator("#terms .term:not([hidden])").click()
    yours.keyboard.type("stty size; echo size-$((6*7))\n")
    assert f"{size['rows']} {size['cols']}" in output_of(served, "replay", "size-42")
    yours.click("#shell-toggle")
    until(yours, "!document.body.classList.contains('shell-mode')")
    until(yours, f"{terminal(yours)}?.fontSize === 14")


def test_a_terminal_scrolled_back_in_your_window_is_scrolled_back_in_the_room(windows, served: str) -> None:
    "Scroll the terminal back in your window: the Room scrolls the same shell back as many lines, and follows you to the bottom."
    yours, room = windows
    yours.locator("#terms .term:not([hidden])").click()
    yours.keyboard.type("seq 1 400; echo done-$((6*7))\n")
    output_of(served, "replay", "done-42")
    box = yours.locator("#terms .term:not([hidden])").bounding_box()
    yours.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
    yours.mouse.wheel(0, -800)
    until(yours, f"{terminal(yours)}?.scrolledBack > 0")
    until(room, "(want) => (window.timewalkTerminals() || []).find((t) => t.id === 'replay')?.scrolledBack === want",
          yours.evaluate(f"(async () => {{ await new Promise((r) => setTimeout(r, 800)); return {terminal(yours)}.scrolledBack; }})()"))
    yours.mouse.wheel(0, 5000)
    until(yours, f"{terminal(yours)}?.scrolledBack === 0")
    until(room, f"{terminal(room)}?.scrolledBack === 0")
