import copy
import json

import pytest

from toolwitness.engine import compare, exit_code
from toolwitness.inputs import InputError
from toolwitness.report import render


def catalog(schema=None, **extra):
    return {"search": {"name": "search", "inputSchema": schema or {"type": "object"}, **extra}}


def case(arguments=None, **extra):
    return {"id": "one", "tool": "search", "arguments": arguments or {}, **extra}


def status(before, after, fixture):
    return compare(before, after, [fixture])["fixtures"][0]["input"]["status"]


def test_new_required_field_is_witnessed():
    old = catalog()
    new = catalog({"type": "object", "required": ["query"]})
    report = compare(old, new, [case()])
    assert report["fixtures"][0]["input"]["status"] == "regression"
    assert report["fixtures"][0]["input"]["issues"][0]["schema_path"] == "/required"
    assert exit_code(report, "regression") == 1


@pytest.mark.parametrize(
    "new_schema,args",
    [
        ({"properties": {"n": {"maximum": 5}}}, {"n": 10}),
        ({"properties": {"n": {"enum": ["a"]}}}, {"n": "b"}),
        ({"properties": {"n": {"type": "integer"}}}, {"n": "string"}),
        ({"additionalProperties": False}, {"n": True}),
        ({"properties": {"n": {"minItems": 2}}}, {"n": [1]}),
        ({"properties": {"n": {"pattern": "^a"}}}, {"n": "bbb"}),
        ({"properties": {"n": {"not": {"const": 4}}}}, {"n": 4}),
        ({"properties": {"n": False}}, {"n": None}),
        ({"dependentRequired": {"a": ["b"]}}, {"a": True}),
        ({"if": {"required": ["a"]}, "then": {"required": ["b"]}}, {"a": True}),
    ],
)
def test_real_schema_semantics(new_schema, args):
    assert status(catalog(), catalog(new_schema), case(args)) == "regression"


def test_baseline_invalid_is_not_regression():
    old = catalog({"required": ["q"]})
    result = compare(old, old, [case()])
    assert result["fixtures"][0]["input"]["status"] == "baseline_invalid"
    assert result["verdict"] == "review"
    assert exit_code(result, "regression") == 0
    assert exit_code(result, "review") == 1


def test_newly_admitted_and_unknown():
    assert status(catalog({"required": ["q"]}), catalog(), case()) == "newly_admitted"
    assert status({}, catalog(), case()) == "baseline_unknown"


def test_removal_fails_even_without_covered_fixture():
    old = catalog()
    old["other"] = {"name": "other", "inputSchema": {}}
    report = compare(old, catalog(), [case()])
    assert report["verdict"] == "regressions"
    assert {"tool": "other", "kind": "removed"} in report["changes"]
    assert status(catalog(), {}, case()) == "tool_removed"


def test_metadata_and_uncovered_changes():
    old = catalog()
    after = catalog(description="new")
    report = compare(old, after, [case()])
    assert report["verdict"] == "review"
    assert report["changes"] == [{"tool": "search", "kind": "description"}]
    assert report["coverage_gaps"] == []


def test_output_is_distinct_from_input():
    old = catalog(outputSchema={"type": "object"})
    new = catalog(outputSchema={"required": ["new"]})
    report = compare(old, new, [case(output={})])
    row = report["fixtures"][0]
    assert row["input"]["status"] == "accepted"
    assert row["output"]["status"] == "historical_output_rejected"
    assert report["verdict"] == "regressions"
    assert report["coverage_gaps"] == []


@pytest.mark.parametrize(
    "old_output,new_output,output,expected",
    [
        (None, {}, {}, "output_unverified"),
        ({}, None, {}, "output_unverified"),
        ({"type": "string"}, {}, 5, "baseline_invalid"),
        ({}, {}, None, "accepted"),
    ],
)
def test_output_missing_or_invalid(old_output, new_output, output, expected):
    old = catalog(**({"outputSchema": old_output} if old_output is not None else {}))
    new = catalog(**({"outputSchema": new_output} if new_output is not None else {}))
    assert compare(old, new, [case(output=output)])["fixtures"][0]["output"]["status"] == expected


def test_nested_local_ref_and_pointer_escaping():
    schema = {
        "$defs": {"positive": {"type": "integer", "minimum": 1}},
        "properties": {"a/b~c": {"$ref": "#/$defs/positive"}},
    }
    report = compare(catalog(), catalog(schema), [case({"a/b~c": 0})])
    assert report["fixtures"][0]["input"]["issues"][0]["instance_path"] == "/a~1b~0c"


def test_compositions():
    schema = {"oneOf": [{"required": ["a"]}, {"required": ["b"]}]}
    assert status(catalog(), catalog(schema), case({"a": 1, "b": 1})) == "regression"
    assert status(catalog(), catalog(schema), case({"a": 1})) == "accepted"


@pytest.mark.parametrize(
    "schema",
    [
        {"$ref": "https://example.com/private"},
        {"$ref": "file:///etc/passwd"},
        {"$id": "file:///tmp/foo"},
        {"$schema": "http://json-schema.org/draft-07/schema#"},
        {"$dynamicRef": "#node"},
        {"properties": {"a": {"$ref": "https://example.com"}}},
        {"type": "made-up-type"},
        {"allOf": "invalid"},
    ],
)
def test_rejected_schemas(schema):
    with pytest.raises(InputError):
        compare(catalog(), catalog(schema), [case()])


def test_unresolved_local_ref_fails_closed():
    with pytest.raises(InputError, match="evaluation failed"):
        compare(catalog(), catalog({"$ref": "#/$defs/missing"}), [case()])


def test_format_is_annotation():
    schema = {"properties": {"email": {"type": "string", "format": "email"}}}
    assert status(catalog(), catalog(schema), case({"email": "not-email"})) == "accepted"


def test_no_fixture_values_in_reports():
    report = compare(
        catalog(),
        catalog({"properties": {"secret": {"const": "expected-secret"}}}),
        [case({"secret": "private-secret"})],
    )
    for style in ("json", "text", "markdown"):
        rendered = render(report, style)
        assert "private-secret" not in rendered
        assert "expected-secret" not in rendered


def test_report_order_is_deterministic_and_input_not_mutated():
    old = catalog()
    fixtures = [case(), case(id="two")]
    saved = copy.deepcopy(fixtures)
    a = compare(old, old, fixtures)
    b = compare(old, old, list(reversed(fixtures)))
    assert render(a, "json") == render(b, "json")
    assert fixtures == saved
    assert a["verdict"] == "no_observed_regressions"
    assert exit_code(a, "review") == 0


def test_control_characters_and_markdown_escaped():
    report = compare(catalog(), catalog(), [case(id="\x1b[31m</pre><script>bad</script>")])
    assert "\x1b" not in render(report, "text")
    assert "<script>" not in render(report, "markdown")
    assert json.loads(render(report, "json"))["report_version"] == 1


def test_none_gate_does_not_fail_findings():
    assert exit_code(compare(catalog(), {}, [case()]), "none") == 0


def test_json_boolean_and_number_are_distinct_catalog_changes():
    old = catalog({"properties": {"flag": {"const": 1}}})
    new = catalog({"properties": {"flag": {"const": True}}})
    report = compare(old, new, [case()])
    assert report["changes"] == [{"tool": "search", "kind": "inputSchema"}]
    assert report["verdict"] == "review"
