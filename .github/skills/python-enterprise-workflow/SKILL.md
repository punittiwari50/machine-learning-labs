---
name: python-enterprise-workflow
description: "Use when building ML systems in Python from core to enterprise maturity. Enforces step-by-step progression (Core, Basic, Advanced, Enterprise), modular project structure, parent-managed dependencies, SOLID architecture, cycle-free design, and WSL quality gates."
---

# Python Enterprise Workflow — Skill

## Purpose

This skill standardizes how ML systems are designed and implemented in this workspace through a maturity ladder:
- Core
- Basic
- Advanced
- Enterprise

It ensures each stage is completed in order, with concrete outputs and quality gates, before moving to the next stage.

## Trigger

Invoke this skill when the user says:
- "build a Python service"
- "refactor this Python project"
- "set up Python project structure"
- "make this production ready"
- "organize this Python codebase"
- "teach from core to advanced"
- "step by step ML system design"
- "design a new ML system"

## Workflow

### Stage 1 — Core Foundations

Goal: establish concepts, domain vocabulary, and smallest working unit.

Required outputs:
- clear problem statement and success criteria
- minimal baseline implementation
- dataset assumptions and constraints
- glossary of core concepts for the topic

Rules:
- keep this stage simple and testable
- avoid premature abstractions

### Stage 2 — Basic Implementation

Goal: convert baseline into a clean modular Python project.

Required outputs:
- modular project structure
- parent-managed dependency strategy for Python
- first version of domain, application, and infra boundaries
- baseline tests and lint/type checks

### Stage 3 — Advanced Engineering

Goal: apply robust engineering patterns and performance improvements.

Required outputs:
- SOLID-compliant abstractions
- cycle-free imports and call graph
- measured performance improvements with benchmark evidence
- fault-tolerant I/O boundaries and clear error contracts

### Stage 4 — Enterprise Hardening

Goal: make the solution production-ready.

Required outputs:
- security and secrets hygiene checks
- observability plan (logs, metrics, trace context)
- dependency governance and upgrade strategy
- cleanup of all temporary debug scripts and debug logs

### Stage 5 — New System Design Blueprint

Goal: create a step-by-step architecture for a new ML system using the completed stages.

Required outputs:
- bounded context map
- module ownership map
- dependency direction map
- phased implementation plan (MVP -> scalable -> enterprise)
- risk register and mitigation plan

Use this sequence for every new system design:
1. Core problem framing
2. Basic modular build
3. Advanced quality/performance pass
4. Enterprise resilience/security pass
5. Blueprint and rollout plan

## Implementation Controls

### Step A — Scope and Boundaries

Define clear module boundaries before coding:
- module purpose and ownership
- dependency direction
- public API for each module
- shared components in `shared_core` or equivalent shared package

Do not allow a flat single-project layout with mixed unrelated responsibilities.

### Step B — Project Structure

Use organized package layout with clear ownership:

```text
root/
  pyproject.toml
  packages/
    shared_core/
    shared_observability/
    service_a/
    service_b/
  tests/
```

Rules:
- one module = one business responsibility
- no random cross-imports
- no god modules

### Step C — Dependency Governance (Python)

Apply parent-managed dependency strategy:
- root `pyproject.toml` or root constraints is the version source of truth
- child modules declare only module-specific dependencies
- avoid re-pinning centrally managed versions in child modules
- use latest stable versions after compatibility verification

### Step D — Architecture and Coding Standards

Enforce:
- SOLID principles
- loose coupling via ABC/protocol boundaries
- layered structure (`domain`, `application`, `infra`, `api`)
- acyclic imports and acyclic call flow
- type hints on all new functions
- meaningful naming and PEP 8 alignment

### Step E — Security and Hygiene

Enforce:
- no secrets/tokens in code, commits, or pushes
- remove temporary debugging scripts/log lines after issue resolution
- remove TODO leftovers before completion

### Step F — Performance and Reliability

Enforce:
- profile before optimizing
- no avoidable O(n^2) loops on large datasets
- appropriate caching/vectorization/lazy evaluation
- robust error handling at I/O and API boundaries

### Step G — Verification in WSL (Required)

Run in WSL Ubuntu with workspace environment:

```bash
wsl -d Ubuntu -- bash -c "source ~/.bashrc_dev; source ~/APPS_VENV/python_venv/run_3_14_2/bin/activate; flake8 . --max-line-length 88 --exclude .git,__pycache__; mypy . --ignore-missing-imports; python -m pylint . --disable=all --enable=cyclic-import --ignore=.git,__pycache__; python -m pip check; python -m pip list --outdated"
```

### Step H — Final Audit

Delegate read-only audit to `Code Quality` agent and resolve all violations before completion.

## Done Criteria

- [ ] Core -> Basic -> Advanced -> Enterprise progression completed in order
- [ ] New system design blueprint is produced with phased rollout plan
- [ ] Modular project structure is in place (no flat mixed project)
- [ ] Parent-managed Python dependency strategy is applied
- [ ] No duplication, no cyclic imports/calls, no architecture violations
- [ ] No secrets/tokens and no temporary debug artifacts
- [ ] Required WSL quality gates completed successfully

## Standards Applied

- [python-standards.instructions.md](../../instructions/python-standards.instructions.md)
- [architecture.instructions.md](../../instructions/architecture.instructions.md)
- [performance.instructions.md](../../instructions/performance.instructions.md)
- [build-dependency-standards.instructions.md](../../instructions/build-dependency-standards.instructions.md)
- [policy.instructions.md](../../instructions/policy.instructions.md)
- [wsl-execution.instructions.md](../../instructions/wsl-execution.instructions.md)
