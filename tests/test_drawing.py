"A terminal draws only while it shows: a hidden tab stops drawing, keeps reading its output, and shows all of it when it comes back."

from test_shell import terminal, until


def test_only_the_terminal_in_front_draws(windows) -> None:
    "Open Runs, then go back: Runs stops drawing and At this step draws. In the Room too."
    yours, room = windows
    yours.locator("#tabs button", has_text="Runs").click()
    for page in (yours, room):
        until(page, f"{terminal(page, 'runs')}?.drawing === true")
    yours.locator("#tabs button", has_text="At this step").click()
    for page in (yours, room):
        until(page, f"{terminal(page, 'runs')}?.drawing === false && {terminal(page, 'replay')}?.drawing === true")


def test_output_that_arrives_while_hidden_is_there_when_the_tab_comes_back(windows) -> None:
    "A command in Runs prints after its tab is hidden; brought back, the tab draws again and the output is in it."
    yours, room = windows
    yours.locator("#tabs button", has_text="Runs").click()
    yours.locator("#terms .term:not([hidden])").click()
    yours.keyboard.type("sleep 2; echo late-$((6*7))\n")
    yours.locator("#tabs button", has_text="At this step").click()
    until(yours, f"{terminal(yours, 'runs')}?.drawing === false")
    until(yours, f"{terminal(yours, 'runs')}?.tail.includes('late-42')", timeout=10000)  # read while hidden
    yours.locator("#tabs button", has_text="Runs").click()
    for page in (yours, room):
        until(page, f"{terminal(page, 'runs')}?.drawing === true && {terminal(page, 'runs')}.tail.includes('late-42')")


def test_a_hidden_window_stops_drawing_and_draws_again_when_shown(windows) -> None:
    "When the browser hides the window, no terminal draws; when it shows the window again, the one in front draws."
    yours, _ = windows
    until(yours, f"{terminal(yours)}?.drawing === true")
    yours.evaluate("Object.defineProperty(document, 'visibilityState', {value: 'hidden', configurable: true}); document.dispatchEvent(new Event('visibilitychange'))")
    until(yours, f"{terminal(yours)}?.drawing === false")
    yours.evaluate("Object.defineProperty(document, 'visibilityState', {value: 'visible', configurable: true}); document.dispatchEvent(new Event('visibilitychange'))")
    until(yours, f"{terminal(yours)}?.drawing === true")
