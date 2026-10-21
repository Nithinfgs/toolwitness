"""Bounded, strict file parsing. No network or tool execution."""

import json
from pathlib import Path
from typing import Any

MAX_BYTES = 10 * 1024 * 1024
MAX_FIXTURES = 10_000


class InputError(ValueError):
    """An input cannot be safely or unambiguously interpreted."""


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise InputError("duplicate JSON object key")
        result[key] = value
    return result


def _constant(value: str) -> Any:
    raise InputError("non-finite JSON numbers are not supported")


def _depth(value: Any, level: int = 0) -> None:
    if level > 80:
        raise InputError("JSON nesting exceeds 80 levels")
    if isinstance(value, dict):
        for item in value.values():
            _depth(item, level + 1)
    elif isinstance(value, list):
        for item in value:
            _depth(item, level + 1)
    elif isinstance(value, float):
        import math

        if not math.isfinite(value):
            raise InputError("non-finite JSON numbers are not supported")


def parse_json(text: str, location: str) -> Any:
    try:
        value = json.loads(text, object_pairs_hook=_pairs, parse_constant=_constant)
        _depth(value)
        return value
    except (ValueError, RecursionError) as exc:
        # Do not echo JSONDecodeError.doc or payload content.
        reason = str(exc) if isinstance(exc, InputError) else "invalid JSON"
        raise InputError(f"{location}: {reason}") from None


def read_text(path: Path) -> str:
    try:
        with path.open("rb") as stream:
            data = stream.read(MAX_BYTES + 1)
        if len(data) > MAX_BYTES:
            raise InputError("file exceeds 10 MiB limit")
        return data.decode("utf-8")
    except (OSError, UnicodeError) as exc:
        raise InputError(f"cannot read UTF-8 file {str(path)!r}: {type(exc).__name__}") from None


def load_catalog(path: Path) -> dict[str, dict[str, Any]]:
    raw = parse_json(read_text(path), str(path))
    if isinstance(raw, dict) and "result" in raw:
        if "error" in raw:
            raise InputError("catalog contains a JSON-RPC error")
        raw = raw["result"]
    if not isinstance(raw, dict) or not isinstance(raw.get("tools"), list):
        raise InputError("catalog must be a tools/list result or JSON-RPC result envelope")
    if raw.get("nextCursor") is not None:
        raise InputError("paginated catalog is incomplete; combine all pages and omit nextCursor")
    tools: dict[str, dict[str, Any]] = {}
    for tool in raw["tools"]:
        if not isinstance(tool, dict) or not isinstance(tool.get("name"), str) or not tool["name"]:
            raise InputError("every tool needs a nonempty string name")
        name = tool["name"]
        if name in tools:
            raise InputError("duplicate tool name; compare one server's catalog at a time")
        if not isinstance(tool.get("inputSchema"), dict):
            raise InputError("every tool needs an inputSchema object")
        if "outputSchema" in tool and not isinstance(tool["outputSchema"], dict):
            raise InputError("outputSchema must be an object")
        tools[name] = tool
    return tools


def load_fixtures(path: Path) -> list[dict[str, Any]]:
    fixtures = []
    ids = set()
    for line_number, line in enumerate(read_text(path).splitlines(), 1):
        if not line.strip():
            continue
        raw = parse_json(line, f"fixture line {line_number}")
        if not isinstance(raw, dict):
            raise InputError(f"fixture line {line_number}: expected object")
        if set(raw) - {"id", "tool", "arguments", "output"}:
            raise InputError(f"fixture line {line_number}: unknown fields")
        for key in ("id", "tool"):
            if not isinstance(raw.get(key), str) or not raw[key]:
                raise InputError(f"fixture line {line_number}: {key} must be a nonempty string")
        if not isinstance(raw.get("arguments"), dict):
            raise InputError(f"fixture line {line_number}: arguments must be an object")
        if raw["id"] in ids:
            raise InputError("duplicate fixture id")
        ids.add(raw["id"])
        fixtures.append(raw)
        if len(fixtures) > MAX_FIXTURES:
            raise InputError("more than 10000 fixtures")
    if not fixtures:
        raise InputError("fixtures file must contain at least one case")
    return fixtures
