---
description: "Deep research on any ML, Python, or system topic — produces a structured progression from core fundamentals through basic, advanced, and enterprise levels with working code examples"
agent: agent
argument-hint: "Topic to research deeply, e.g. 'attention mechanisms' or 'distributed feature stores'"
tools: [read, search, web, edit]
---

You are performing a **deep, structured research study** on the topic provided. Produce a complete, layered knowledge document covering all four tiers.

Use **easy and simple words** suitable for learners. Keep explanations clear, practical, and beginner-friendly without losing technical correctness.

## Context Lock (Required)

- Stay strictly within the user topic and its directly relevant subtopics.
- Do not drift into unrelated concepts, tools, or architectures.
- If a useful but out-of-scope idea appears, list it under `Out-of-Scope Notes` (1-3 bullets) without expanding it.

## Source Quality Rules (Required)

Use trusted sources in this order of preference:
1. Peer-reviewed papers and preprints from recognized venues/repositories (arXiv, NeurIPS, ICML, ICLR, ACL, CVPR, IEEE, ACM).
2. Official documentation and official websites (framework docs, vendor docs, standards bodies).
3. Official repositories and maintainer-authored content on GitHub.
4. Hugging Face docs/model cards/datasets where relevant.
5. YouTube only from credible channels (official conferences, framework maintainers, recognized researchers/organizations).

Avoid low-trust sources, uncited claims, and anonymous opinion posts.

Minimum citation requirements per topic:
- Include as many high-quality research papers as feasible for the topic.
- Minimum 10 research papers when available.
- If fewer than 10 credible papers exist for a niche topic, include all available credible papers and explicitly explain the gap.
- At least 2 official documentation sources.
- At least 1 GitHub repository.
- At least 1 Hugging Face source (if topic is model/data relevant).
- Include recommended video learning references when available, using only high-trust channels.
- Target 3-7 video links per topic when available, including at least one end-to-end project/system design walkthrough.

Paper quality guidance:
- Prefer recent and influential papers, plus canonical foundational papers.
- Prioritize recognized venues and well-cited work.
- Cover both theory and practical/engineering papers where possible.

For every major claim, add an inline citation marker like `[S1]`, `[S2]` and include a `Sources` section at the end.
Each source entry must include: title, organization/author, URL, and why it is trusted.
For research papers also include year and venue.

## Output Structure (Required — Do Not Skip Any Tier)

---

### 🔬 Tier 1 — Core Fundamentals

Answer these questions:
- What is this? (one-paragraph definition)
- Why does it exist? (the problem it solves)
- Why is it useful in real ML products/business systems?
- What are the foundational mathematical or conceptual primitives?
- What are the key terms and their precise definitions?

Include a minimal working example — the simplest possible code that demonstrates the concept.

Also include a `Mini Enterprise Project` block (very small) showing where this concept is used in a real company setting.

---

### 📘 Tier 2 — Basic Implementation

- Standard use cases and common workflows.
- Most frequently used APIs, classes, and functions.
- Common configuration options and their effects.
- Typical pitfalls for beginners and how to avoid them.

Include a complete, runnable code example (executable in WSL with the project venv).

Also include a `Mini Enterprise Project` block (very small) showing practical business usage.

---

### ⚙️ Tier 3 — Advanced Techniques

- Non-obvious features and patterns that experts use.
- Performance optimisation strategies specific to this topic.
- Relevant design patterns (Strategy, Factory, Pipeline, etc.) applied to this domain.
- Integration with other systems or libraries.
- Known failure modes, edge cases, and debugging approaches.

Include an advanced code example with proper type hints, abstraction layers, and error handling.

Also include a `Mini Enterprise Project` block (very small) showing advanced production usage.

---

### 🏢 Tier 4 — Enterprise Production

- How this is deployed and scaled in production systems.
- Observability: what to log, what metrics to expose, what to trace.
- Resilience: failure modes, circuit breakers, graceful degradation.
- Security considerations: input validation, secrets management, access control.
- Operational concerns: versioning, rollback, blue-green deployment.
- Real-world architecture diagram (ASCII) showing where this fits in the larger system.

Include enterprise-grade code: config as frozen dataclass, protocol-based abstraction, structured logging, metrics, retry logic.

Also include a `Mini Enterprise Project` block (very small) showing enterprise rollout context.

### Mini Enterprise Project Format (Required)

For each `Mini Enterprise Project` block, include:
- Business problem (1-2 lines)
- Service boundary and ownership summary
- SOLID mapping (which class/service boundary demonstrates SRP, OCP, DIP)
- Platform component list required by this design (only what is needed):
	- API gateway/BFF, service runtime, queue/stream, database/store, cache
	- feature store, model registry, experiment tracking, artifact registry
	- secrets manager, observability stack, CI/CD, deployment orchestrator
- Secret-management plan (Vault preferred, or enterprise equivalent) with injection method
- Observability plan for logs + metrics + traces (ELK/OpenSearch and Prometheus/Grafana/OpenTelemetry as applicable)
- Deployment path:
	- Docker Compose option (service list + network + environment variables)
	- Kubernetes option (Deployment + Service + ConfigMap/Secret + HPA when relevant)
- Run/verification note (how to validate the mini project starts and is healthy)
- Command context note (which commands run in WSL vs host Windows)

### Dual-Technology Rule (Python + Node)

When the topic requires both Python and Node.js:
- Design both as enterprise components with SOLID principles.
- Separate responsibilities clearly:
	- Python service(s): ML/data/model-heavy logic.
	- Node.js service(s): API gateway/BFF/orchestration/realtime interface where applicable.
- Define clear contracts between services (API/events), ownership boundaries, and dependency direction.
- Avoid duplicating business logic across both stacks.

---

## Code Requirements for Every Example

All code must:
- Run inside WSL: `source ~/.bashrc_dev; source ~/APPS_VENV/python_venv/run_3_14_2/bin/activate`
- Have full type hints on all functions.
- Follow PEP 8 with 88-char line limit.
- Use meaningful names — no single-letter variables outside comprehensions.
- Demonstrate the design pattern from `architecture.instructions.md` most relevant to this topic.

---

## Output Format

Save outputs to two separate files:

1. Research document: `foundation/research/<kebab-case-topic>.md`
2. Mind map document: `foundation/research/<kebab-case-topic>-mindmap.md`

The mind map file must include:
- a concise plain-language summary
- a Mermaid mind map block (`mindmap`) covering Core -> Basic -> Advanced -> Enterprise
- key real-world use cases
- short learner takeaways

The research file and mind map file must both use simple and clear language.

End with a **Summary Table**:

| Tier | Key Concept | Pattern Used | Code Example |
|------|-------------|--------------|--------------|
| Core | ... | — | minimal snippet |
| Basic | ... | — | standard snippet |
| Advanced | ... | Strategy/Factory/etc. | advanced snippet |
| Enterprise | ... | DI + Observability | production snippet |

Add a final section:

## Why This Topic Is Useful
- <business and engineering value summary>

Add another final section:

## Recommended Videos (High-Trust)
- [V1] <title> — <channel/org> — <url> — <why this helps>
- [V2] ...
- Include at least one end-to-end project/system design video when available.

Add a final section:

## Sources
- [S1] <title> — <author/org> — <url> — <trust reason>
- [S2] ...

Add one more final section:

## Out-of-Scope Notes
- <short bullet, only if needed>
