"The facts of each kind of walk, from timewalk-export --json: the layout of the schema, the parts of the notes, the files of each change."

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest
import timewalk


def valid(
    value: object,  # A part of the facts
    schema: dict,  # The part of the schema that it must follow
    root: dict,  # The whole schema, for its $defs
    where: str = "facts",  # Where the value is, for the message
) -> None:
    "Check a value against the parts of JSON Schema that the facts' schema uses, and say where it fails."
    if "$ref" in schema:
        schema = root["$defs"][schema["$ref"].rsplit("/", 1)[1]]
    if "oneOf" in schema:
        fits = 0
        for choice in schema["oneOf"]:
            try:
                valid(value, choice, root, where)
                fits += 1
            except AssertionError:
                pass
        assert fits == 1, f"{where}: fits {fits} of the choices"
        return
    kinds = schema.get("type")
    if kinds:
        names = {"object": dict, "array": list, "string": str, "integer": int, "boolean": bool, "null": type(None)}
        assert any(isinstance(value, names[k]) and not (k == "integer" and isinstance(value, bool)) for k in ([kinds] if isinstance(kinds, str) else kinds)), \
            f"{where}: {value!r:.80} is not {kinds}"
    if "const" in schema:
        assert value == schema["const"], f"{where}: {value!r} is not {schema['const']!r}"
    if "enum" in schema:
        assert value in schema["enum"], f"{where}: {value!r} is not one of {schema['enum']}"
    if "pattern" in schema and isinstance(value, str):
        assert re.search(schema["pattern"], value), f"{where}: {value!r} does not match {schema['pattern']}"
    if isinstance(value, dict):
        for key in schema.get("required", []):
            assert key in value, f"{where}: has no {key}"
        known = schema.get("properties", {})
        for key, inner in value.items():
            if key in known:
                valid(inner, known[key], root, f"{where}.{key}")
            elif isinstance(schema.get("additionalProperties"), dict):
                valid(inner, schema["additionalProperties"], root, f"{where}.{key}")
            else:
                assert schema.get("additionalProperties", True) is not False, f"{where}: has {key}, which the schema does not"
    if isinstance(value, list) and "items" in schema:
        for at, inner in enumerate(value):
            valid(inner, schema["items"], root, f"{where}[{at}]")


def facts_of(
    kit: Path,  # The class folder
    walk: str,  # A walk of its toc.toml
    out: Path,  # The file to write
) -> dict:  # The facts, checked against the schema
    "Write the facts of one walk with timewalk-export --json, check them against timewalk's schema, and read them."
    done = subprocess.run([sys.executable, "-c", "from timewalk.export import main; main()", str(kit / "repo"), "--toc", str(kit / "toc.toml"),
                           "--walk", walk, "--json", str(out), "--github", "https://github.com/o/tally"], capture_output=True, text=True)
    assert done.returncode == 0, done.stderr
    facts = json.loads(out.read_text())
    schema = json.loads((Path(timewalk.__file__).parent / "facts.schema.json").read_text())
    valid(facts, schema, schema)
    return facts


def prose(
    parts: list[dict],  # Parts of the facts
) -> str:  # All the text that a reader reads in them, in any mode
    "Join the text of the parts."
    return "\n".join(part.get("text") or part.get("words") or "" for part in parts)


def test_the_facts_of_the_tutorial(kit: Path, tmp_path: Path) -> None:
    "Every step and move of the history, each move with its files and whole diffs, and parts for both modes; no private line, and the same bytes twice."
    facts = facts_of(kit, "tutorial", tmp_path / "tutorial.json")
    assert facts["walk"]["kind"] == "tutorial" and facts["walk"]["github"] == "https://github.com/o/tally" and facts["errors"] == []
    assert [stop["name"] for stop in facts["stops"]] == [f"step-0{n}" for n in range(7)]
    moves = [move for stop in facts["stops"] for move in stop["moves"]]
    assert len(moves) == 13 and all(move["files"] for move in moves), "every move changes a file"
    assert all(stop["tag"]["name"] == stop["name"] for stop in facts["stops"]), "a whole step stands on its tag"
    assert all(facts["history"][move["name"]] == move["commit"] for move in moves)
    modes = {part["mode"] for move in moves for part in move["parts"]}
    assert modes == {"shared", "do", "watch"}, "one file serves both modes"
    every = [part for move in moves for part in move["parts"]]
    assert {part["kind"] for part in every} >= {"prose", "command", "item"}
    for move in moves:   # a diff is whole, from its first hunk, and its counts agree with it
        for found in move["files"]:
            if found["diff"]:
                lines = found["diff"].split("\n")
                assert lines[0].startswith("@@") and sum(line.startswith("+") for line in lines) == found["added"], (move["name"], found["path"])
    notes = (kit / "walks" / "tutorial" / "notes.md").read_text()
    cues = [line.split(":", 1)[1].strip() for line in notes.splitlines() if re.match(r"^\s*>\s*(Say|Note):", line)]
    text = (tmp_path / "tutorial.json").read_text()
    assert cues and not any(cue and cue in text for cue in cues), "the presenter's cues are left out"
    assert str(kit) not in text, "no path of this machine"
    again = facts_of(kit, "tutorial", tmp_path / "again.json")
    assert again == facts and (tmp_path / "again.json").read_bytes() == (tmp_path / "tutorial.json").read_bytes()


def test_the_facts_of_a_narrative(kit: Path, tmp_path: Path) -> None:
    "A narrative's stops have no moves, and each has the files of its change from the stop before."
    facts = facts_of(kit, "narrative", tmp_path / "narrative.json")
    assert facts["walk"]["kind"] == "narrative" and facts["walk"]["mode"] == "watch"
    assert all(stop["moves"] == [] for stop in facts["stops"])
    assert facts["stops"][0]["start"] is None and all(stop["start"] for stop in facts["stops"][1:])
    assert all(stop["files"] for stop in facts["stops"]), "each stop has what its step changed"


@pytest.mark.parametrize("walk, first", [("small", "step-02.2 to step-02.3"), ("testing", "step-02.1 to step-02.3")])
def test_the_facts_of_a_small_walk(kit: Path, tmp_path: Path, walk: str, first: str) -> None:
    "A walk with select, or with notes of its own: a small step starts at the commit before its first move, and leads with the step's setup."
    facts = facts_of(kit, walk, tmp_path / f"{walk}.json")
    stop = facts["stops"][0]
    assert stop["name"] == first and stop["tag"] is None
    first_move = stop["moves"][0]
    assert stop["start"] == first_move["parent"], "it starts where its first move starts"
    assert any(part["kind"] == "command" and part["text"] == "just setup" for part in stop["parts"])
    assert facts["intro"], "the walk's intro"
    if walk == "testing":
        assert stop["own"] and stop["own"]["title"] == stop["title"] and "{{include" not in stop["own"]["text"]
        own = (kit / "walks" / "testing" / "notes.md").read_text()
        intro = own.split("\n## ", 1)[0]
        assert prose(facts["intro"]).split("\n")[0] in intro, "the intro is the own notes' text before the first stop"
    else:
        assert stop["own"] is None


def test_the_facts_of_a_narrative_that_stops_at_moves(kit: Path, tmp_path: Path) -> None:
    "A narrative with select: a stop at a move has that move's text and files, and a stop at a step its whole change."
    facts = facts_of(kit, "story", tmp_path / "story.json")
    assert [stop["name"] for stop in facts["stops"]] == ["step-01.1", "step-02", "step-05.2"]
    one, two, _ = facts["stops"]
    assert one["tag"] is None and two["tag"]["name"] == "step-02"
    assert [f["path"] for f in one["files"]] and len(two["files"]) > len(one["files"]), "a step's change is all of its moves'"
