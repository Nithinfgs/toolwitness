# Validation — 2026-10-21

Executed locally on macOS arm64, Python 3.14.3. Tools: pytest 9.1.1, Ruff 0.17.1,
mypy 1.20.2, jsonschema 4.26.0. Commands below ran from the project root unless noted.

| Command | Observed result |
|---|---|
| `python3 -m venv .venv` | Isolated environment created |
| `.venv/bin/python -m pip install -e '.[dev]'` | Installed project and dependencies |
| `.venv/bin/pytest --cov=toolwitness --cov-report=term-missing` | 64 passed; 96% source statement coverage |
| `.venv/bin/ruff check .` | Passed |
| `.venv/bin/ruff format --check .` | Passed |
| `.venv/bin/mypy src` | Passed, seven source files |
| `.venv/bin/python -m build` | Wheel and sdist built successfully |
| `.venv/bin/python -m pip install --upgrade pip` | Local pip upgraded to 26.2.2 |
| `.venv/bin/pip-audit --format json --output ../work/audit-fixed.json` | No known vulnerabilities found |
| `python3 -m venv .venv-wheel` | Clean wheel-test environment created |
| `.venv-wheel/bin/python -m pip install dist/toolwitness-0.1.0-py3-none-any.whl` | Fresh installation succeeded |
| `.venv-wheel/bin/toolwitness examples/before.json examples/before.json examples/calls.jsonl` | Exit 0, no observed regressions, no gaps |
| `.venv-wheel/bin/toolwitness examples/before.json examples/after.json examples/calls.jsonl --format json --fail-on none` | Exit 0, two witnessed input regressions |
| `.venv-wheel/bin/toolwitness examples/before.json examples/after.json examples/calls.jsonl --format markdown --fail-on none` | Markdown report generated |

The default breaking-demo exit 1, `--help`, invalid input exit 2 and informational exit 0
were also verified by subprocess integration tests. Tests cover nested/local-reference
schemas, composition, conditionals, enum/type/boundary changes, duplicate names and keys,
Unicode/control-character rendering, file size/nesting limits, missing schemas and
payload-value omission. The CLI subprocess tests are not included in the parent's
coverage tracing, so coverage is not claimed for those subprocess lines.

## Failures corrected during development

- Initial editable install started before README existed; metadata generation failed.
  Completed README and reran installation successfully.
- Ruff identified long lines and import formatting; formatted and corrected them,
  then reran lint and formatting checks successfully.
- Initial advisory scan found pip 25.3 advisories in the newly created virtual environment.
  Upgraded only local pip; rerun passed. No runtime dependency advisories were reported.
- All 64 tests passed. Final review identified Python boolean/number equality as a
  potential catalog-diff blind spot; canonical JSON comparison and a regression test
  were added and the full suite rerun.

## Secret and staged-file review

Gitleaks 8.30.1 was downloaded from its official GitHub release into the isolated
workspace and its archive checksum verified. The staged tree was exported with
`git checkout-index` and scanned using `gitleaks dir ... --redact`; no leaks found.
`git diff --cached --check` passed. Reviewed the tracked-file list: no credentials,
virtual environments, .env files, local paths or personal contact details were included.

## Scope

No real MCP server was contacted and no tool was executed. This is intentional: the product
validates exported contracts and saved examples. Cross-platform/runtime CI results are
reported separately after publication. Fixture coverage is not equivalent to universal
compatibility, and schema validation is not a security sandbox.
