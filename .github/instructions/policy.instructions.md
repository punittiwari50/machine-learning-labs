---
description: "Policy and quality gates enforced across all code and notebooks in this workspace. Applies to all files — covers duplication checks, code review gates, and enterprise standards compliance."
applyTo: "**"
---

# Policy — Quality Gates & Governance

## Before Submitting Any Code or Notebook

All of the following must pass before a task is considered complete:

### 1. No-Duplication Check
- [ ] No logic, function, or code block exists more than once.
- [ ] No utility function was recreated when an equivalent exists in `foundation/`.
- [ ] No notebook copies data loading/preprocessing from another notebook instead of referencing shared helpers.

### 2. Python Quality Gates
- [ ] `flake8` passes with `--max-line-length 88` (no warnings, no errors).
- [ ] `mypy` passes with no type errors on new or modified functions.
- [ ] All new functions have type hints on parameters and return types.

### 3. Notebook Completeness
- [ ] Notebook runs cleanly from top to bottom on a fresh kernel restart.
- [ ] All sections present: imports → config → data → model → evaluation → results → summary.
- [ ] Random seeds set at the top.
- [ ] No cells in error state or `[*]` pending state.

### 4. Enterprise Standards
- [ ] No hardcoded credentials, absolute paths, or Windows-specific paths.
- [ ] No secrets or tokens are committed or pushed (API keys, access tokens, passwords, private keys).
- [ ] Error handling present at all I/O and external API boundaries.
- [ ] Meaningful variable and function names — no single-letter variables outside list comprehensions.
- [ ] No unused imports or dead code.
- [ ] Temporary debugging scripts, debug flags, and verbose debug logging are removed after issue resolution.

### 5. Architecture & Design
- [ ] High-level modules depend on Protocol/ABC abstractions, not concrete classes.
- [ ] Config objects use `dataclass(frozen=True)`.
- [ ] No circular imports.
- [ ] No cyclic dependencies between modules, classes, or services.
- [ ] No cyclic call chains (direct or indirect recursion) unless explicitly required and bounded.
- [ ] No cyclic logic flow between methods/functions (A -> B -> C -> A).
- [ ] Layered architecture respected — no skipped layers.

### 6. Performance
- [ ] No O(n²) loops over datasets with > 1 000 rows.
- [ ] `tf.data` pipelines use `.prefetch(tf.data.AUTOTUNE)`.
- [ ] Performance claims backed by benchmark cells.

### 7. Microservices (for service code)
- [ ] Every cross-service call has explicit timeout.
- [ ] Retry with exponential backoff present on all network calls.
- [ ] Structured logging with `event`, `service`, `trace_id` fields.

### 8. Build & Dependency Management (for Maven/Gradle/Python/Node.js projects)
- [ ] Parent/root project centrally manages dependency and plugin versions.
- [ ] Submodules declare dependencies only; versions are not duplicated in child modules.
- [ ] Single source of truth is used (`dependencyManagement`/BOM, `libs.versions.toml`, root `pyproject.toml`/constraints, root workspace overrides/resolutions).
- [ ] Dependencies use latest stable compatible versions.
- [ ] Project structure is modular and organized (no single flat project with everything mixed together).
- [ ] Coding structure follows clear module boundaries, ownership, and dependency direction.

### 9. Topic Context & Enterprise Mapping (for prompts, research docs, and design outputs)
- [ ] Output stays strictly in-topic; unrelated tangents are excluded or kept only as brief out-of-scope notes.
- [ ] Every major concept includes a small enterprise project usage example.
- [ ] If both Python and Node.js are used, each stack has clear enterprise responsibility boundaries.
- [ ] If both Python and Node.js are used, SOLID principles are applied in both stacks.
- [ ] Business logic is not duplicated across Python and Node.js services.

### 10. Mini Project Deployment Readiness (for research/design outputs)
- [ ] Each mini enterprise project includes a Docker Compose deployment path.
- [ ] Each mini enterprise project includes a Kubernetes deployment path.
- [ ] Docker Compose and Kubernetes deployment descriptions respect service boundaries and ownership.

### 11. Enterprise Platform Baseline (architecture-driven, for enterprise-level mini projects)
- [ ] System design includes a platform component matrix listing required components and rationale.
- [ ] Secrets management uses an enterprise secret manager (HashiCorp Vault preferred, or equivalent) with no plaintext secrets in code/manifests.
- [ ] Logging/observability includes centralized stack for logs/metrics/traces (ELK/OpenSearch and Prometheus/Grafana/OpenTelemetry as applicable).
- [ ] Runtime configuration separates secrets from non-secret config (`Secret`/secret-manager vs `ConfigMap`/env).
- [ ] Project layout includes clear ops boundaries (for example: `ops/docker/`, `ops/k8s/`, `ops/secrets/`, `ops/observability/`).
- [ ] Research output includes recommended high-trust video learning links when available.

### 12. Execution Boundary Governance
- [ ] Python and Node.js commands are executed in WSL Ubuntu.
- [ ] Docker/Compose/Kubernetes commands are executed from host Windows context.
- [ ] No mixed runtime ambiguity in docs/runbooks (command context is explicit).

## Enforcement Commands

Run verification in the correct execution context before finishing:

```bash
# Linting
wsl -d Ubuntu -- bash -c "source ~/.bashrc_dev; source ~/APPS_VENV/python_venv/run_3_14_2/bin/activate; flake8 . --max-line-length 88 --exclude .git,__pycache__"

# Type checking
wsl -d Ubuntu -- bash -c "source ~/.bashrc_dev; source ~/APPS_VENV/python_venv/run_3_14_2/bin/activate; mypy . --ignore-missing-imports"

# Circular import check
wsl -d Ubuntu -- bash -c "source ~/.bashrc_dev; source ~/APPS_VENV/python_venv/run_3_14_2/bin/activate; python -m pylint . --disable=all --enable=cyclic-import --ignore=.git,__pycache__"

# Notebook execution test
wsl -d Ubuntu -- bash -c "source ~/.bashrc_dev; source ~/APPS_VENV/python_venv/run_3_14_2/bin/activate; jupyter nbconvert --to notebook --execute <notebook>.ipynb --output <notebook>_tested.ipynb"

# Maven (multi-module): dependency convergence and parent-managed versions
wsl -d Ubuntu -- bash -c "mvn -q -DskipTests enforcer:enforce -Denforcer.rules=dependencyConvergence"

# Maven: show available dependency/plugin updates (upgrade centrally in parent only)
wsl -d Ubuntu -- bash -c "mvn -q -DskipTests versions:display-dependency-updates versions:display-plugin-updates"

# Gradle (multi-module): dependency updates report (upgrade centrally in version catalog/root)
wsl -d Ubuntu -- bash -c "./gradlew -q dependencyUpdates"

# Gradle: inspect resolved dependency graph for all modules
wsl -d Ubuntu -- bash -c "./gradlew -q dependencies"

# Python: validate dependency graph and check outdated packages (upgrade centrally)
wsl -d Ubuntu -- bash -c "source ~/.bashrc_dev; source ~/APPS_VENV/python_venv/run_3_14_2/bin/activate; python -m pip check; python -m pip list --outdated"

# Node.js: inspect outdated packages and dependency tree (upgrade centrally at workspace root)
wsl -d Ubuntu -- bash -c "npm outdated; npm ls --all"

# Secret manager CLI sanity (host context; example with Vault)
vault status

# Docker Compose: validate compose definition syntax (host context)
docker compose -f <compose-file>.yml config

# Kubernetes: client-side validation of manifests (host context)
kubectl apply --dry-run=client -f <k8s-manifest-or-dir>
```

## Non-Negotiable Rules

1. **Never** introduce a dependency without adding it to `requirements.txt` or noting it in the notebook setup cell.
2. **Never** leave TODO comments in committed code — complete the task or open a tracked issue.
3. **Never** push notebooks with large embedded outputs — clear outputs before committing.
4. **Never** commit or push any secret or token (API keys, access tokens, passwords, private keys, connection strings).
5. **Never** introduce cyclic logic, cyclic dependencies, or cyclic method/function calls.
6. **Never** commit temporary debugging scripts or temporary debug logging once debugging is complete.
7. **Never** duplicate centrally managed dependency versions across Maven/Gradle/Python/Node.js submodules or workspace packages.
8. **Never** keep unrelated subprojects and dependencies in one flat module; organize into clear modules/packages.
9. **Always** prefer existing stdlib or well-known ML libraries over custom implementations.
10. **Never** drift off-topic in research/design outputs; keep non-topic notes brief and clearly marked out-of-scope.
11. **Never** leave a major concept without a small enterprise project usage example.
12. **Never** duplicate shared business logic across Python and Node.js in dual-stack solutions.
13. **Never** leave mini enterprise projects without at least one Docker Compose or Kubernetes deployment path (prefer both).
14. **Never** store secrets in source code, committed `.env` files, Docker Compose files, or Kubernetes manifests; use Vault references/injection.
15. **Never** ship enterprise mini projects without centralized observability plan for logs, metrics, and traces.
16. **Never** force unnecessary platform components; every selected component must be justified by system design.
