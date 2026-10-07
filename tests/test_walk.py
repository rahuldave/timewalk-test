"The default walk, a narrative of tagged steps, in two windows: the step, the slides and a shell."

import subprocess
import sys
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from websockets.sync.client import connect
from pypdf import PdfReader

STEPS = [f"step-0{i}" for i in range(6)]
SLIDES = {"step-02": 2}  # every other step has one slide


def shows(page, selector: str, text: str) -> None:
    "Wait until the element's text is exactly text."
    page.wait_for_function("([s, t]) => document.querySelector(s)?.textContent.trim() === t", arg=[selector, text], timeout=15000)


def test_the_room_follows_every_step_and_slide(windows) -> None:
    "Right moves both windows to the next step; Down moves both to the next slide of a step with two."
    yours, room = windows
    yours.mouse.click(300, 300)  # the keys go to the page, not to a terminal
    for step in STEPS:
        for page in (yours, room):
            shows(page, "#step-name", step)
        count = SLIDES.get(step, 1)
        for page in (yours, room):
            shows(page, "#slide-count", f"Slide 1 of {count}")
        if count > 1:
            yours.keyboard.press("ArrowDown")
            for page in (yours, room):
                shows(page, "#slide-count", f"Slide 2 of {count}")
        yours.keyboard.press("ArrowRight")


def output_of(address: str, shell: str, marker: str) -> str:
    "Connect to a shell as a page does, and read its output until the marker appears."
    parts = urlparse(address)
    token = parse_qs(parts.query)["t"][0]
    with connect(f"ws://{parts.netloc}/ws/term/{shell}?t={token}") as socket:
        seen = ""
        while marker not in seen:
            data = socket.recv(timeout=15)
            seen += data.decode("utf-8", "replace") if isinstance(data, bytes) else data
        return seen


def test_a_command_typed_in_your_window_runs_in_the_shell_at_the_step(windows, served: str) -> None:
    "Typed into the terminal of your window, a command runs in the replay copy, at the step."
    yours, _ = windows
    yours.locator("#terms .term:not([hidden])").click()
    yours.keyboard.type("git describe --tags; echo tw-marker-$((6*7))\n")
    seen = output_of(served, "replay", "tw-marker-42")
    assert "step-00" in seen


def test_the_pdf_has_one_page_per_slide(kit: Path) -> None:
    "timewalk-pdf makes one page for each of the seven slides."
    out = kit / "build" / "slides.pdf"
    subprocess.run([sys.executable, "-m", "timewalk.slides_pdf", str(kit / "slides" / "slides.toml"), "--notes", str(kit / "notes.md"), "-o", str(out)],
                   check=True, capture_output=True)
    assert len(PdfReader(out).pages) == 7
