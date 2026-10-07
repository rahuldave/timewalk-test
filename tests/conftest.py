"Fixtures: the project built fresh for each test, a copy of the class folder, a running timewalk, and Chrome."

import re
import shutil
import socket
import subprocess
import sys
from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
TIMEWALK = [sys.executable, "-m", "timewalk"]  # the timewalk that this Python imports: the branch, or TIMEWALK_LOCAL


@pytest.fixture
def kit(tmp_path: Path) -> Path:
    "A class folder in tmp_path: the notes and slides copied, and repo/ built from history/."
    shutil.copy(ROOT / "notes.md", tmp_path / "notes.md")
    shutil.copytree(ROOT / "slides", tmp_path / "slides")
    subprocess.run([sys.executable, str(ROOT / "history" / "build.py"), str(tmp_path / "repo")], check=True, capture_output=True)
    return tmp_path


def free_port() -> int:
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        return probe.getsockname()[1]


@pytest.fixture
def served(kit: Path):
    "timewalk on the kit, with the notes and slides of the default walk. Yields the address, token included."
    port = free_port()
    process = subprocess.Popen([*TIMEWALK, str(kit / "repo"), "--notes", str(kit / "notes.md"), "--slides", str(kit / "slides" / "slides.toml"),
                                "--discard-edits", "--port", str(port), "--no-open", "--assistant", ""],
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    address = None
    for line in process.stdout:
        found = re.search(r"open\s+(http://\S+)", line)
        if found:
            address = found.group(1)
            break
    assert address, "timewalk printed no address"
    yield address
    process.terminate()
    process.wait(timeout=10)


@pytest.fixture(scope="session")
def browser():
    "Chrome, headless, for the whole session."
    with sync_playwright() as p:
        chrome = p.chromium.launch(channel="chrome")
        yield chrome
        chrome.close()


@pytest.fixture
def windows(browser, served: str):
    "Two windows on the page: yours, and the Room window for the class."
    context = browser.new_context(viewport={"width": 1400, "height": 900})
    yours, room = context.new_page(), context.new_page()
    yours.goto(served)
    room.goto(served + "&room=1")
    for page in (yours, room):
        page.wait_for_selector("#tabs button")
    yield yours, room
    context.close()
