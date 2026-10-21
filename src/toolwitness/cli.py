"""CLI entry point."""

import argparse
import sys
from pathlib import Path

from toolwitness import __version__
from toolwitness.engine import compare, exit_code
from toolwitness.inputs import InputError, load_catalog, load_fixtures
from toolwitness.report import render


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Find fixture-backed MCP contract regressions without running a server."
    )
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument("before", type=Path, help="baseline tools/list JSON")
    parser.add_argument("after", type=Path, help="candidate tools/list JSON")
    parser.add_argument("fixtures", type=Path, help="sanitized JSONL cases")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--fail-on", choices=["regression", "review", "none"], default="regression")
    args = parser.parse_args(argv)
    try:
        result = compare(
            load_catalog(args.before), load_catalog(args.after), load_fixtures(args.fixtures)
        )
        sys.stdout.write(render(result, args.format))
        return exit_code(result, args.fail_on)
    except (InputError, RecursionError) as exc:
        print(f"toolwitness: {str(exc)!r}", file=sys.stderr)
        return 2
    except BrokenPipeError:
        return 2
