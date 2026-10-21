# Research and selection — 2026-10-21

Observation date: 21 October 2026 (Asia/Kolkata). GitHub REST API and live Trending pages were fetched during this session. These are point-in-time observations, not audited adoption measurements. Search-engine relative dates can lag; discussion dates and marketing claims are not treated as usage counts.

## Method and evidence

Reviewed 27 repositories across agent infrastructure, MCP tooling, API testing, Python tooling and local AI. API records retain stars, forks, last push, creation date and URLs in [repositories.json](research/repositories.json). [trends.json](research/trends.json) retains all parsed daily, weekly and monthly entries. GitHub Trending could not be opened by the web reader; direct HTTPS retrieval succeeded. No repository was cloned or implementation copied.

Total stars measure accumulated attention. Trending's period stars measure recent attention over its own windows, not an independently reconstructed star history. Neither proves adoption, code quality or organic growth. In particular, the extreme weekly count for morluto/rea warrants caution; it is not the basis of the selection.

## Repository review

| Repository | Total stars | Forks | Role / opportunity implication |
|---|---:|---:|---|
| [modelcontextprotocol/inspector](https://github.com/modelcontextprotocol/inspector) | 11,114 | 1,546 | Visual MCP inspector: established interactive debugging competition. |
| [modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk) | 24,632 | 4,065 | Python MCP SDK: installed ecosystem needs contract regression checks. |
| [modelcontextprotocol/typescript-sdk](https://github.com/modelcontextprotocol/typescript-sdk) | 13,632 | 2,318 | TypeScript MCP SDK: language-neutral exports make a portable checker useful. |
| [PrefectHQ/fastmcp](https://github.com/PrefectHQ/fastmcp) | 28,162 | 2,497 | MCP server framework: schema changes can originate in framework upgrades. |
| [TsvetanG2/mcpward](https://github.com/TsvetanG2/mcpward) | 8 | 0 | Direct competitor: security/contract drift testing; do not duplicate generic drift alerts. |
| [MCPJam/inspector](https://github.com/MCPJam/inspector) | 2,274 | 297 | Interactive testing and evaluation competitor; offline fixture evidence is a narrower workflow. |
| [getsentry/toolkit](https://github.com/getsentry/toolkit) | 936 | 165 | Production-oriented agent tooling: evidence of maintained integrations. |
| [github/github-mcp-server](https://github.com/github/github-mcp-server) | 33,829 | 5,200 | Official GitHub integration: large tool surfaces require change management. |
| [smart-mcp-proxy/mcpproxy-go](https://github.com/smart-mcp-proxy/mcpproxy-go) | 398 | 66 | Runtime proxy competition: avoid transport and deployment complexity. |
| [astral-sh/uv](https://github.com/astral-sh/uv) | 90,986 | 3,680 | Mature Python package manager: strong demand for focused developer tooling. |
| [astral-sh/ruff](https://github.com/astral-sh/ruff) | 50,203 | 2,537 | Mature linter: concise deterministic feedback is a proven UX pattern. |
| [pydantic/pydantic-ai](https://github.com/pydantic/pydantic-ai) | 20,770 | 2,984 | Typed agent framework: contract reliability complements runtime abstractions. |
| [BerriAI/litellm](https://github.com/BerriAI/litellm) | 61,740 | 12,545 | Gateway platform: provider compatibility is valuable but broad and costly to maintain. |
| [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo) | 26,241 | 2,530 | Evaluation platform: avoid building another general AI evaluation harness. |
| [simonw/llm](https://github.com/simonw/llm) | 12,648 | 1,056 | CLI LLM toolkit: local workflows remain useful alongside hosted products. |
| [coder27/mcp-provenance-proxy](https://github.com/coder27/mcp-provenance-proxy) | 0 | 0 | Provenance proxy: drift and recording already served; specialize in saved-call regressions. |
| [oasdiff/oasdiff](https://github.com/oasdiff/oasdiff) | 1,427 | 112 | OpenAPI breaking-change checker: analogous persistent need, different contract format. |
| [schemathesis/schemathesis](https://github.com/schemathesis/schemathesis) | 3,689 | 226 | API fuzz testing: generative testing competition; scoped fixture replay is simpler to inspect. |
| [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill) | 35,492 | 2,231 | Security audit skills: strong recent attention to agent reliability/security. |
| [vllm-project/vllm](https://github.com/vllm-project/vllm) | 94,768 | 23,729 | Inference engine: high adoption proxy but hardware-heavy MVP impractical here. |
| [stablyai/orca](https://github.com/stablyai/orca) | 100,922 | 6,381 | Agent fleet manager: orchestration growing, broad desktop app expensive to build well. |
| [morluto/rea](https://github.com/morluto/rea) | 355,910 | 89,382 | Agent reverse engineering: exceptional attention; unclear durable demand for a new clone. |
| [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) | 43,577 | 4,599 | Plugin directory: integrations expanding, contract management remains cross-cutting. |
| [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | 53,538 | 4,728 | Scientific agent skills: many domain interfaces, expertise-heavy maintenance. |
| [paperclipai/paperclip](https://github.com/paperclipai/paperclip) | 105,580 | 17,581 | Agent management: strong momentum but substantial existing competition. |
| [debpalash/VoiceStudio](https://github.com/debpalash/VoiceStudio) | 80,039 | 8,813 | Local voice studio: active category, model and hardware requirements outside a small MVP. |
| [vectorize-io/hindsight](https://github.com/vectorize-io/hindsight) | 52,308 | 6,197 | Agent memory: fast growth, evaluation and storage semantics are a large undertaking. |

## Current momentum versus durable need

- Daily: Cloudflare security-audit-skill +1,997; Orca +1,543; vLLM +439.
- Weekly: official Claude plugins +5,650; scientific-agent-skills +4,549; Orca +8,173.
- Monthly: Paperclip +24,372; Hindsight +28,261; VoiceStudio +45,470.
- Sources: [daily](https://github.com/trending?since=daily), [weekly](https://github.com/trending?since=weekly), [monthly](https://github.com/trending?since=monthly).

Agent ecosystems dominate this snapshot, including security, plugins, orchestration and memory. These counts support broad ecosystem relevance, not a claim that the selected niche is itself growing at those rates. MCP contract drift is a persistent software compatibility problem even if agent hype fades.

## Community and launch signals

- [HN: New MCP Roadmap](https://news.ycombinator.com/item?id=49399591): 270 points / 161 comments in retrieved page. Discussion raises interoperability and state-management complexity. Qualitative demand signal, not a representative survey.
- [HN: MCP tools with dependent types](https://news.ycombinator.com/item?id=44938963): older discussion about dynamic tool definitions and reliability; useful enduring context, not current momentum.
- [Reddit: definitions change after approval](https://www.reddit.com/r/mcp/comments/1wbcr8q/mcp_tools_can_change_their_descriptionschema/): developer reports about schema drift; self-promotion and anecdotes require caution.
- [Reddit: different client failures](https://www.reddit.com/r/mcp/comments/1x2bnc5/claude_code_and_codex_break_on_different_mcp/): recent client/schema interoperability reports; independently unverified.
- [Reddit: CI drift checker](https://www.reddit.com/r/mcp/comments/1v7kbyx/i_kept_worrying_about_mcp_servers_silently/): direct competitive evidence and discussion of parameter shape changes.
- [Product Hunt: MCPJam](https://www.producthunt.com/products/mcpjam-inspector?page=1): testing/evaluation launch, 458 followers and two reviews on fetched page. Vendor usage claims were not verified or used in scoring.
- [Product Hunt: Strata](https://www.producthunt.com/products/strata-2?launch=strata-2): discovery/orchestration launch supports interest in managing large tool sets.
- [Official MCP release post](https://blog.modelcontextprotocol.io/posts/2026-07-28/): protocol evolution and breaking changes reinforce the value of regression evidence. Toolwitness does not test transport compatibility.

## Five opportunities and weighted evaluation

Scores 1 (weak) to 5 (strong); weighted score = sum(weight × score)/5, out of 100. Judgment, not measured market forecasts. Weights: demand 15, momentum 10, differentiation 15, feasibility 15, usefulness 15, maintainability 10, testable MVP 15, community fit 5.

| Opportunity | Demand | Momentum | Difference | Feasibility | Usefulness | Maintenance | Testability | Community | /100 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| MCP saved-call contract witness | 4 | 4 | 4 | 5 | 5 | 4 | 5 | 4 | 89 |
| Agent tool-catalog token/collision budget | 4 | 4 | 3 | 5 | 4 | 4 | 4 | 4 | 80 |
| AI gateway provider compatibility replay | 5 | 4 | 3 | 3 | 5 | 2 | 3 | 4 | 73 |
| Local agent-memory retention inspector | 4 | 5 | 3 | 3 | 4 | 2 | 3 | 4 | 69 |
| Agent plugin supply-chain policy checker | 5 | 5 | 2 | 3 | 5 | 2 | 4 | 4 | 75 |

1. **Saved-call witness:** replay sanitized arguments against before/after schemas; show actual affected fixtures and uncovered changed tools. Competition: mcpward, MCP Inspector, MCPJam. Difference: offline, schema-only, fixture-backed evidence and explicit uncertainty; no server execution or LLM. Easy to exercise with known regressions; mature validator reduces maintenance.
2. **Catalog budget:** help developers with overlarge tool surfaces. Competition: MCPProxy, context-mode, Strata. Deterministic size/collision analysis feasible but token counts depend on provider and similarity heuristics can mislead; weaker uniqueness.
3. **Gateway replay:** catch provider-specific behavior changes. Competition: LiteLLM, promptfoo. Useful, but requires paid credentials and changing provider APIs; difficult to verify broadly in this environment.
4. **Memory inspector:** show stale or conflicting stored agent memories. Competition: Hindsight and existing memory dashboards. Privacy and heterogeneous storage formats make an honest useful MVP harder.
5. **Plugin policies:** flag unsafe plugin configurations. Competition: audit skills and existing account tools (onopen, permlint, skillcheck). High demand but overlaps existing work and needs continual platform-specific maintenance.

## Decision and acceptance criteria (recorded before implementation)

**Toolwitness** — tell MCP maintainers which saved calls a tool schema change breaks.

Target: server authors and platform engineers reviewing schema changes in CI. Inputs: old/new exported tools/list results and sanitized JSONL fixtures. Outputs: text, JSON and Markdown reports; observed input regressions, removed tools, newly admitted calls, invalid baseline fixtures, output-contract rejections, metadata changes and coverage gaps. Input and output results remain distinct: old outputs rejected by a new schema are historical evidence, not proof a future server will produce them.

Stack: Python 3.11+, argparse, jsonschema Draft 2020-12, pytest, Ruff, mypy; installable wheel and sdist. Use vetted schema validation rather than inventing a partial validator. No live MCP networking, credentials, telemetry or tool execution. References are local-only; payload values omitted from reports.

Acceptance: actual fixtures identify enum narrowing and new required fields; invalid old fixtures are not regressions; removed and untested tools visible; nested/local-ref schemas supported; malformed inputs and unsupported dialects fail clearly; machine reports deterministic; CLI exit policy configurable; tests exercise packaging/CLI; lint/types/build/audit and fresh installation executed. No claim of universal backward compatibility or runtime safety.

Existing account repositories were read-only inventoried; mcpscope is an interactive tracer/proxy, not this offline evidence workflow. No matching published toolwitness repository existed at selection. Active private agent intentions are not observable, so no claim of detecting every parallel project is made.
