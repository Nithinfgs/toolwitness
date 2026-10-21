# Dependency and license review

Runtime dependencies observed on 2026-10-21: jsonschema 4.26.0, referencing 0.37.0,
attrs 26.1.0, jsonschema-specifications 2025.9.1 and rpds-py 2026.9.1.
Each declares the MIT license in installed package metadata. Toolwitness is MIT;
third-party packages retain their own copyrights and licenses. No third-party source
was vendored. Development tools are installed separately and not bundled in the wheel.

`requirements-dev.lock` records exact installed development/runtime package versions
(without the editable project or local paths). It is a version snapshot, not a hashed
supply-chain lock. Runtime dependency ranges are in pyproject.toml. Build isolation
resolved hatchling 1.32.4 for the verified build.

The first environment audit reported advisories in bundled pip 25.3. Updating pip
inside the project virtual environment to 26.2.2 resolved those findings. The subsequent
full environment `pip-audit` reported no known vulnerabilities. This is advisory-database
coverage at the observation date, not a guarantee of absence of vulnerabilities.
