# Machine Learning Labs — Copilot Instructions

This file is automatically loaded in every Copilot session for this workspace.
All `.instructions.md`, `.prompt.md`, `.agent.md`, and policy files in `.github/` apply throughout.

---

## Common Language (Enforced Across All Files)

1. **No duplication** — Never duplicate code, logic, or functions. Extract shared utilities; reuse existing helpers before writing new ones.
2. **Enterprise quality** — Follow PEP 8, type hints, clear naming, and proper error handling at system boundaries. Run linting and quality checks before finishing.
3. **One notebook = one complete flow** — Each `.ipynb` must contain the entire end-to-end pipeline (imports → data → model → evaluation → results). Never split a single topic across multiple notebooks.
4. **Loose coupling** — Depend on abstractions (Protocol/ABC), never on concrete implementations. Use dependency injection.
5. **Design for performance** — Measure before optimising. Use vectorisation, caching, and lazy evaluation. Profile bottlenecks before rewriting.
6. **Microservice discipline** — Each service owns its data. No shared databases. Every cross-service call has a timeout, retry, and fallback.
7. **Context lock** — Stay strictly within the requested topic. Do not drift to unrelated concepts; list non-essential tangents only as brief out-of-scope notes.
8. **Concept-to-enterprise mapping** — Every major concept must include a small enterprise project usage example.
9. **Dual-stack enterprise SOLID** — If Python and Node.js are both in scope, design both as enterprise services with SOLID boundaries, explicit contracts, and no duplicated business logic.
10. **Mini project deployment readiness** — Mini enterprise projects should include Docker Compose and Kubernetes deployment paths when applicable.
11. **Execution boundary** — Run Python/Node work in WSL Ubuntu; run Docker/Compose/Kubernetes from host Windows context.
12. **Enterprise platform baseline** — Enterprise mini projects should define architecture-driven platform components; Vault/ELK are preferred examples, and equivalent justified choices are allowed.
13. **Learning support** — Research outputs should include high-trust video links when available, including one end-to-end project/system design walkthrough.

---

## Instruction Files (Auto-Applied)

| File | Scope |
|------|-------|
| [python-standards.instructions.md](instructions/python-standards.instructions.md) | All `.py` and `.ipynb` files |
| [notebook-standards.instructions.md](instructions/notebook-standards.instructions.md) | All `.ipynb` files |
| [wsl-execution.instructions.md](instructions/wsl-execution.instructions.md) | All files — execution rules |
| [policy.instructions.md](instructions/policy.instructions.md) | All files — quality gates |
| [performance.instructions.md](instructions/performance.instructions.md) | All `.py` and `.ipynb` files |
| [architecture.instructions.md](instructions/architecture.instructions.md) | All `.py` and `.ipynb` files |
| [microservices.instructions.md](instructions/microservices.instructions.md) | All `.py` and `.ipynb` files |
| [build-dependency-standards.instructions.md](instructions/build-dependency-standards.instructions.md) | Maven/Gradle/Python/Node dependency files (`pom.xml`, `*.gradle*`, `libs.versions.toml`, `pyproject.toml`, `requirements*.txt`, `package.json`) |

---

## Execution Environment

All Python execution must happen inside **WSL Ubuntu**:

```bash
wsl -d Ubuntu -- bash -c "source ~/.bashrc_dev; source ~/APPS_VENV/python_venv/run_3_14_2/bin/activate; python <script>"
```

- Virtual env: `~/APPS_VENV/python_venv/run_3_14_2`
- Never run Python directly in Windows PowerShell or CMD.
- Chain commands with `;`, not `&&`, inside WSL.

---

## Quick Reference — Custom Agents & Prompts

| Name | Type | Purpose |
|------|------|---------|
| `@ML Lab` | Agent | Full ML lab workflow — notebooks, experiments, code generation |
| `@Code Quality` | Subagent | Read-only audit — duplicates, standards, arch, perf violations |
| `@ML Delivery Orchestrator` | Agent | Coordinates the full pipeline from topic-only input to production-ready system and CI/CD |
| `@ML Research Specialist` | Agent | Deep research by tiers: Core, Basic, Advanced, Enterprise from topic-only input |
| `@ML System Design Engineer` | Agent | Converts research into standards-compliant Core->Enterprise system design and code blueprint |
| `@ML Quality Reviewer` | Agent | Code-level validation, concept markup, best examples, and short takeaways |
| `@ML Integration Architect` | Agent | Integrates logic into traditional microservices/distributed architecture at correct stages |
| `@ML CI/CD Release Engineer` | Agent | Builds enterprise CI/CD pipeline through production rollout and rollback gates |
| `/python-enterprise-workflow` | Skill | Step-by-step ML Python workflow from Core -> Basic -> Advanced -> Enterprise, ending in new system design blueprint |
| `/ml-system-design-workshop` | Skill | End-to-end ML system design workshop from Core to Production Ready with rollout and operations gates |
| `/create-ml-notebook` | Prompt | Scaffold a complete single-notebook ML flow |
| `/code-quality-review` | Prompt | Audit a file or notebook for quality and duplication |
| `/deep-research` | Prompt | Core → Basic → Advanced → Enterprise study on any topic |
| `/system-design` | Prompt | Design an enterprise ML system with bounded contexts & scaffold |
