import json
import subprocess
import sys
from pathlib import Path

import pytest

from toolwitness.cli import main
from toolwitness.inputs import InputError, load_catalog, load_fixtures, parse_json, read_text

ROOT = Path(__file__).resolve().parents[1]


def write(tmp_path, data):
    p = tmp_path / "input.json"
    p.write_text(json.dumps(data), encoding="utf-8")
    return p


@pytest.mark.parametrize("text", ['{"a":1,"a":2}', "NaN", "Infinity", "1e9999", "{bad", "[" * 1000])
def test_strict_json(text):
    with pytest.raises(InputError):
        parse_json(text, "test")


def test_depth_limit():
    with pytest.raises(InputError, match="nesting"):
        parse_json("[" * 81 + "0" + "]" * 81, "test")


def test_envelope(tmp_path):
    p = write(
        tmp_path,
        {"jsonrpc": "2.0", "id": 1, "result": {"tools": [{"name": "foo", "inputSchema": {}}]}},
    )
    assert "foo" in load_catalog(p)


@pytest.mark.parametrize(
    "data",
    [
        {},
        {"tools": {}},
        {"tools": [{"name": "x"}]},
        {"tools": [{"name": "", "inputSchema": {}}]},
        {"tools": [{"name": "x", "inputSchema": {}, "outputSchema": False}]},
        {"tools": [], "nextCursor": "more"},
        {"result": {"tools": []}, "error": {}},
        {"tools": [{"name": "x", "inputSchema": {}}, {"name": "x", "inputSchema": {}}]},
    ],
)
def test_invalid_catalog(tmp_path, data):
    with pytest.raises(InputError):
        load_catalog(write(tmp_path, data))


@pytest.mark.parametrize(
    "data",
    [
        [],
        {},
        {"id": "a", "tool": "t", "arguments": []},
        {"id": "a", "tool": "t", "arguments": {}, "unknown": 5},
        {"id": "", "tool": "t", "arguments": {}},
    ],
)
def test_invalid_fixture(tmp_path, data):
    with pytest.raises(InputError):
        load_fixtures(write(tmp_path, data))


def test_duplicate_and_empty_fixture(tmp_path):
    p = write(tmp_path, {"id": "a", "tool": "t", "arguments": {}})
    p.write_text(p.read_text() + "\n" + p.read_text())
    with pytest.raises(InputError, match="duplicate"):
        load_fixtures(p)
    p.write_text("\n  \n")
    with pytest.raises(InputError, match="at least"):
        load_fixtures(p)


def test_io_errors_and_limit(tmp_path):
    with pytest.raises(InputError):
        read_text(tmp_path / "missing")
    p = tmp_path / "large"
    p.write_bytes(b"x" * (10 * 1024 * 1024 + 1))
    with pytest.raises(InputError, match="limit"):
        read_text(p)
    p.write_bytes(b"\xff")
    with pytest.raises(InputError):
        read_text(p)


def test_fixture_limit(tmp_path):
    p = tmp_path / "cases"
    p.write_text(
        "".join(
            json.dumps({"id": str(i), "tool": "t", "arguments": {}}) + "\n" for i in range(10001)
        )
    )
    with pytest.raises(InputError, match="10000"):
        load_fixtures(p)


def command(*extra):
    return [
        sys.executable,
        "-m",
        "toolwitness",
        str(ROOT / "examples/before.json"),
        str(ROOT / "examples/after.json"),
        str(ROOT / "examples/calls.jsonl"),
        *extra,
    ]


def test_cli_end_to_end():
    result = subprocess.run(command("--format", "json"), capture_output=True, text=True)
    assert result.returncode == 1
    assert json.loads(result.stdout)["summary"]["statuses"]["regression"] == 2
    assert not result.stderr
    result = subprocess.run(command("--fail-on", "none"), capture_output=True, text=True)
    assert result.returncode == 0
    assert "maximum" in result.stdout


def test_invalid_input_exit(tmp_path, capsys):
    p = write(tmp_path, {})
    assert main([str(p), str(p), str(p)]) == 2
    assert "toolwitness:" in capsys.readouterr().err


def test_cli_baseline_and_help():
    args = command()
    args[4] = args[3]
    result = subprocess.run(args, capture_output=True, text=True)
    assert result.returncode == 0
    assert "no_observed_regressions" in result.stdout
    assert (
        subprocess.run(
            [sys.executable, "-m", "toolwitness", "--help"], capture_output=True
        ).returncode
        == 0
    )
