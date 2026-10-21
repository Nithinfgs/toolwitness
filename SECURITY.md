# Security

Toolwitness 0.1.x is the currently supported release line. Do not put credentials or
personal data in issues. Use GitHub's private vulnerability reporting if enabled;
otherwise open an issue requesting a private contact without disclosing exploit details.

Toolwitness does not execute MCP tools or retrieve schemas. Reports suppress argument/output
values but can include property names, tool names and fixture IDs. It is not a secret scanner
or sandbox. Malicious regexes and recursive schemas may exhaust resources; use reviewed schemas
or OS-level CPU/memory isolation. Dependency advisories should be checked with `pip-audit`.
