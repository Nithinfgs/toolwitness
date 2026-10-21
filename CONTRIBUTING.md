# Contributing

Use Python 3.11+ and an isolated virtual environment. Install `python -m pip install -e '.[dev]'`.
Run `pytest`, `ruff check .`, `ruff format --check .`, and `mypy src` before proposing a change.

Add a regression fixture that demonstrates the real failure. Keep example payloads synthetic.
Preserve the distinction between witnessed regressions, invalid baseline examples and unknown
compatibility. New schema support must preserve the local-only reference policy.

Discuss new transports, automatic log imports and generated examples before implementation;
they change the privacy or evidence model. Small, focused pull requests are welcome.
