"""Draft 2020-12 validation with explicit local-only reference policy."""

from typing import Any

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError
from referencing import Registry

from toolwitness.inputs import InputError

DIALECT = "https://json-schema.org/draft/2020-12/schema"
MAPS = {"properties", "patternProperties", "$defs", "dependentSchemas"}
SINGLES = {
    "additionalProperties",
    "unevaluatedProperties",
    "propertyNames",
    "items",
    "unevaluatedItems",
    "contains",
    "not",
    "if",
    "then",
    "else",
    "contentSchema",
}
ARRAYS = {"allOf", "anyOf", "oneOf", "prefixItems"}


def _policy(schema: Any) -> None:
    if isinstance(schema, bool):
        return
    if not isinstance(schema, dict):
        raise InputError("invalid subschema")
    if "$schema" in schema and schema["$schema"] != DIALECT:
        raise InputError("only JSON Schema Draft 2020-12 is supported")
    if "$id" in schema or "$dynamicRef" in schema or "$dynamicAnchor" in schema:
        raise InputError("$id and dynamic references are unsupported; bundle with local $defs")
    if "$ref" in schema:
        ref = schema["$ref"]
        if not isinstance(ref, str) or not ref.startswith("#"):
            raise InputError("external references are forbidden; use local # references")
    for key in MAPS & schema.keys():
        if not isinstance(schema[key], dict):
            raise InputError("schema map must be an object")
        for child in schema[key].values():
            _policy(child)
    for key in SINGLES & schema.keys():
        _policy(schema[key])
    for key in ARRAYS & schema.keys():
        if not isinstance(schema[key], list):
            raise InputError("schema composition must be an array")
        for child in schema[key]:
            _policy(child)


def validator(schema: dict[str, Any]) -> Draft202012Validator:
    _policy(schema)
    try:
        Draft202012Validator.check_schema(schema)
    except (SchemaError, RecursionError):
        raise InputError("invalid Draft 2020-12 schema") from None
    # An explicit registry never retrieves external resources.
    return Draft202012Validator(schema, registry=Registry())


def pointer(parts: Any) -> str:
    return "".join("/" + str(p).replace("~", "~0").replace("/", "~1") for p in parts)


def issues(checker: Draft202012Validator, value: Any) -> list[dict[str, str]]:
    try:
        # Messages can embed secrets. Only report keyword and structural paths.
        result = [
            {
                "instance_path": pointer(e.absolute_path),
                "schema_path": pointer(e.absolute_schema_path),
                "keyword": str(e.validator),
            }
            for e in checker.iter_errors(value)
        ]
        return sorted(result, key=lambda e: (e["instance_path"], e["schema_path"]))
    except Exception as exc:
        # jsonschema wraps reference-resolution failures in implementation-specific exceptions.
        raise InputError(
            f"schema evaluation failed ({type(exc).__name__}); check references"
        ) from None
