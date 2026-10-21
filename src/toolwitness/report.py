"""Deterministic reports without fixture argument or output values."""

import html
import json
from typing import Any


def label(value: str) -> str:
    return json.dumps(value, ensure_ascii=True)


def render(report: dict[str, Any], style: str) -> str:
    if style == "json":
        return json.dumps(report, indent=2, sort_keys=True, ensure_ascii=True) + "\n"
    lines = [
        f"Toolwitness: {report['verdict']}",
        f"{report['summary']['fixtures']} fixtures | "
        f"{len(report['changes'])} changes | {len(report['coverage_gaps'])} coverage gaps",
        "",
    ]
    for fixture in report["fixtures"]:
        for field in ("input", "output"):
            if field not in fixture:
                continue
            result = fixture[field]
            lines.append(
                f"{label(fixture['id'])} / {label(fixture['tool'])} [{field}]: {result['status']}"
            )
            for issue in result.get("issues", []):
                lines.append(
                    f"  {issue['keyword']} at {label(issue['instance_path'] or '/')} "
                    f"(schema {label(issue['schema_path'])})"
                )
    if report["changes"]:
        lines.extend(["", "Catalog changes:"])
        lines.extend(f"  {label(c['tool'])}: {label(c['kind'])}" for c in report["changes"])
    if report["coverage_gaps"]:
        lines.extend(["", "Coverage gaps:"])
        lines.extend(
            f"  {label(g['tool'])} [{g['contract']}]: {g['reason']}"
            for g in report["coverage_gaps"]
        )
    lines.extend(["", report["scope"]])
    text = "\n".join(lines) + "\n"
    if style == "markdown":
        # HTML-escaped pre avoids fence-breaking / injected Markdown from tool or fixture names.
        return "# Toolwitness report\n\n<pre>" + html.escape(text) + "</pre>\n"
    return text
