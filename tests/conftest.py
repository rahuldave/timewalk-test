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
    "A class folder in tmp_path: the notes, slides, table of contents and walks copied, and repo/ built from history/."
    for name in ("notes.md", "toc.toml"):
        shutil.copy(ROOT / name, tmp_path / name)
    for name in ("slides", "walks"):
        shutil.copytree(ROOT / name, tmp_path / name)
    subprocess.run([sys.executable, str(ROOT / "history" / "build.py"), str(tmp_path / "repo")], check=True, capture_output=True)
    return tmp_path


def free_port() -> int:
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        return probe.getsockname()[1]


@pytest.fixture
def start(kit: Path):
    "A function that starts timewalk on the kit with the given options and returns its address, token included."
    processes = []

    def run(*options: str) -> str:
        process = subprocess.Popen([*TIMEWALK, str(kit / "repo"), *options, "--port", str(free_port()), "--no-open", "--assistant", ""],
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        processes.append(process)
        seen = []
        for line in process.stdout:
            seen.append(line)
            found = re.search(r"open\s+(http://\S+)", line)
            if found:
                return found.group(1)
        raise AssertionError("timewalk printed no address:\n" + "".join(seen))

    yield run
    for process in processes:
        process.terminate()
        process.wait(timeout=10)


@pytest.fixture
def served(kit: Path, start) -> str:
    "timewalk on the kit, without a table: the notes and slides of the default walk, and --discard-edits."
    return start("--notes", str(kit / "notes.md"), "--slides", str(kit / "slides" / "slides.toml"), "--discard-edits")


@pytest.fixture(scope="session")
def browser():
    "Chrome, headless, for the whole session."
    with sync_playwright() as p:
        chrome = p.chromium.launch(channel="chrome")
        yield chrome
        chrome.close()


def open_windows(browser, address: str):
    "Your window and the Room window on the page, each ready."
    context = browser.new_context(viewport={"width": 1400, "height": 900})
    yours, room = context.new_page(), context.new_page()
    yours.goto(address)
    room.goto(address + "&room=1")
    for page in (yours, room):
        page.wait_for_selector("#tabs button")
    return context, yours, room


@pytest.fixture
def windows(browser, served: str):
    "Two windows on the page: yours, and the Room window for the class."
    context, yours, room = open_windows(browser, served)
    yield yours, room
    context.close()
