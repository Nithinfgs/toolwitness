"""Fixture evidence and catalog changes; never claims general schema containment."""

import json
from collections import Counter
from typing import Any

from toolwitness.schema import issues, validator

SCHEMA_FIELDS = {"inputSchema", "outputSchema"}
FAIL_STATUSES = {"regression", "tool_removed", "historical_output_rejected"}
WARNING_STATUSES = {"baseline_invalid", "baseline_unknown", "output_unverified"}


def compare(
    before: dict[str, dict[str, Any]],
    after: dict[str, dict[str, Any]],
    fixtures: list[dict[str, Any]],
) -> dict[str, Any]:
    validators = {
        (side, name, field): validator(tool[field])
        for side, catalog in (("before", before), ("after", after))
        for name, tool in catalog.items()
        for field in SCHEMA_FIELDS
        if field in tool
    }
    changes = []
    for name in sorted(before.keys() | after.keys()):
        old, new = before.get(name), after.get(name)
        if old is None or new is None:
            changes.append({"tool": name, "kind": "added" if old is None else "removed"})
            continue
        for field in sorted(old.keys() | new.keys()):
            if (field in old) != (field in new) or json.dumps(
                old.get(field), sort_keys=True
            ) != json.dumps(new.get(field), sort_keys=True):
                changes.append({"tool": name, "kind": field})
    results = []
    input_covered: set[str] = set()
    output_covered: set[str] = set()
    for fixture in fixtures:
        name = fixture["tool"]
        row: dict[str, Any] = {"id": fixture["id"], "tool": name}
        if name not in before:
            row["input"] = {"status": "baseline_unknown", "issues": []}
        else:
            old_errors = issues(validators["before", name, "inputSchema"], fixture["arguments"])
            new_errors = (
                issues(validators["after", name, "inputSchema"], fixture["arguments"])
                if name in after
                else []
            )
            if old_errors:
                status = (
                    "newly_admitted" if name in after and not new_errors else "baseline_invalid"
                )
            else:
                input_covered.add(name)
                status = (
                    "tool_removed"
                    if name not in after
                    else ("regression" if new_errors else "accepted")
                )
            row["input"] = {
                "status": status,
                "issues": new_errors,
                "baseline_issues": old_errors,
            }
        if "output" in fixture:
            old_check = validators.get(("before", name, "outputSchema"))
            new_check = validators.get(("after", name, "outputSchema"))
            old_errors = issues(old_check, fixture["output"]) if old_check else []
            new_errors = issues(new_check, fixture["output"]) if new_check else []
            if old_check is None:
                status = "output_unverified"
            elif old_errors:
                status = "baseline_invalid"
            elif new_check is None:
                status = "output_unverified"
            else:
                output_covered.add(name)
                status = "historical_output_rejected" if new_errors else "accepted"
            row["output"] = {
                "status": status,
                "issues": new_errors,
                "baseline_issues": old_errors,
            }
        results.append(row)
    gaps = []
    for name in sorted(before.keys() | after.keys()):
        if name not in input_covered:
            gaps.append({"tool": name, "contract": "input", "reason": "no_baseline_valid_fixture"})
        if any("outputSchema" in c.get(name, {}) for c in (before, after)):
            if name not in output_covered:
                gaps.append({"tool": name, "contract": "output", "reason": "no_comparable_output"})
    counts = Counter(
        r[field]["status"] for r in results for field in ("input", "output") if field in r
    )
    failed = any(counts[s] for s in FAIL_STATUSES) or any(c["kind"] == "removed" for c in changes)
    warning = bool(gaps or changes or any(counts[s] for s in WARNING_STATUSES))
    return {
        "report_version": 1,
        "verdict": "regressions" if failed else "review" if warning else "no_observed_regressions",
        "summary": {
            "fixtures": len(fixtures),
            "before_tools": len(before),
            "after_tools": len(after),
            "statuses": dict(sorted(counts.items())),
        },
        "changes": changes,
        "coverage_gaps": gaps,
        "fixtures": sorted(results, key=lambda r: r["id"]),
        "scope": (
            "Saved examples only. Passing is not proof of general compatibility or runtime safety."
        ),
    }


def exit_code(report: dict[str, Any], fail_on: str) -> int:
    if fail_on == "none":
        return 0
    if report["verdict"] == "regressions":
        return 1
    if fail_on == "review" and report["verdict"] == "review":
        return 1
    return 0
