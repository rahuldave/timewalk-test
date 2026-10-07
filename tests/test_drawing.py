"A terminal draws only while it shows: a hidden tab stops drawing, keeps reading its output, and shows all of it when it comes back."

import pytest
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
    yours.wait_for_timeout(300)
    before = yours.evaluate("window.timewalkPicture('runs')")
    until(yours, f"{terminal(yours, 'runs')}?.tail.includes('late-42')", timeout=10000)  # read while hidden
    yours.wait_for_timeout(300)
    assert yours.evaluate("window.timewalkPicture('runs')") == before, "a hidden terminal does not draw what arrives"
    yours.locator("#tabs button", has_text="Runs").click()
    for page in (yours, room):
        until(page, f"{terminal(page, 'runs')}?.drawing === true && {terminal(page, 'runs')}.tail.includes('late-42')")
    until(yours, "(was) => window.timewalkPicture('runs') !== was", before)  # it draws the output once shown


def test_a_hidden_window_stops_drawing_and_draws_again_when_shown(windows) -> None:
    "When the browser hides the window, no terminal draws; when it shows the window again, the one in front draws."
    yours, _ = windows
    until(yours, f"{terminal(yours)}?.drawing === true")
    yours.evaluate("Object.defineProperty(document, 'visibilityState', {value: 'hidden', configurable: true}); document.dispatchEvent(new Event('visibilitychange'))")
    until(yours, f"{terminal(yours)}?.drawing === false")
    yours.evaluate("Object.defineProperty(document, 'visibilityState', {value: 'visible', configurable: true}); document.dispatchEvent(new Event('visibilitychange'))")
    until(yours, f"{terminal(yours)}?.drawing === true")


COUNT_CANVAS_SIZES = """
window.canvasSizes = 0;
const width = Object.getOwnPropertyDescriptor(HTMLCanvasElement.prototype, "width");
Object.defineProperty(HTMLCanvasElement.prototype, "width", {
  get() { return width.get.call(this); },
  set(value) { window.canvasSizes++; width.set.call(this, value); },
});
"""


@pytest.mark.parametrize("ratio", [1, 2, 1.1, 2.2])
def test_a_terminal_does_not_remake_its_canvas_every_frame_at_any_pixel_ratio(browser, served: str, ratio: float) -> None:
    "A zoomed window or a scaled screen gives a fractional pixel ratio; the terminal still sets its canvas size only when it changes."
    context = browser.new_context(viewport={"width": 1400, "height": 900}, device_scale_factor=ratio)
    context.add_init_script(COUNT_CANVAS_SIZES)
    page = context.new_page()
    page.goto(served)
    page.wait_for_selector("#tabs button")
    until(page, f"{terminal(page)}?.drawing === true")
    page.wait_for_timeout(1000)
    before = page.evaluate("window.canvasSizes")
    page.wait_for_timeout(2000)
    assert page.evaluate("window.canvasSizes") - before <= 2, "a still terminal does not resize its canvas"
    context.close()
