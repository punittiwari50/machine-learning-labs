---
name: ml-system-design-workshop
description: "Use when designing a new ML system from Core to Production Ready. Guides a step-by-step path across Core, Basic, Advanced, Enterprise, and Production Readiness with required artifacts and quality gates."
---

# ML System Design Workshop — Skill

## Purpose

This skill provides a complete step-by-step workshop to design and harden a new ML system until it is production ready.

Maturity path:
- Core
- Basic
- Advanced
- Enterprise
- Production Ready

## Trigger

Invoke this skill when the user says:
- "design a new ML system"
- "create system design from scratch"
- "move this ML idea to production"
- "core to enterprise architecture"
- "production-ready ML blueprint"

## Stage 1 — Core

Goal: define fundamentals and validate the problem.

Required outputs:
- problem statement and success metrics
- dataset assumptions and constraints
- baseline architecture sketch
- minimal viable pipeline flow

## Stage 2 — Basic

Goal: convert concepts into clean modular design.

Required outputs:
- bounded module map
- initial package layout
- root-managed dependency strategy
- baseline API/data contracts

## Stage 3 — Advanced

Goal: introduce engineering rigor and measurable quality.

Required outputs:
- SOLID and layered architecture alignment
- acyclic dependency/call graph
- benchmark plan and performance evidence
- fault boundaries and recovery behavior

## Stage 4 — Enterprise

Goal: harden for scale, reliability, and governance.

Required outputs:
- microservice/domain boundary map
- observability plan (logs, metrics, traces)
- security and secret-handling plan
- dependency governance and upgrade policy

## Stage 5 — Production Ready

Goal: finalize go-live readiness and controlled rollout.

Required outputs:
- production readiness checklist
- phased rollout strategy (canary or blue-green)
- rollback and incident response runbook
- SLO/SLA definitions and alert thresholds
- operations handover artifacts

## Required Design Artifacts

Produce these for every new system:
- context and bounded-context map
- component and dependency diagram
- data flow diagram
- API and schema contracts
- resilience matrix (timeouts, retries, fallback)
- performance and capacity plan
- security threat checklist
- deployment and rollback plan

## Workflow Integration

Use these prompts as accelerators:
- run deep research first using [deep-research.prompt.md](../../prompts/deep-research.prompt.md)
- generate architecture and scaffold with [system-design.prompt.md](../../prompts/system-design.prompt.md)

## Verification Gates

Before marking complete:
- all policy gates satisfied
- no duplicated logic
- no cyclic dependencies or cyclic call chains
- no secrets/tokens in code or commits
- temporary debug scripts/logs removed
- quality checks pass in WSL environment

## Done Criteria

- [ ] Core, Basic, Advanced, Enterprise, and Production Ready stages completed in order
- [ ] System design artifacts are complete and internally consistent
- [ ] Build/dependency governance follows parent-managed strategy
- [ ] Architecture is modular, layered, and cycle-free
- [ ] Production rollout, rollback, and operations handover are documented

## Standards Applied

- [python-enterprise-workflow skill](../python-enterprise-workflow/SKILL.md)
- [python-standards.instructions.md](../../instructions/python-standards.instructions.md)
- [architecture.instructions.md](../../instructions/architecture.instructions.md)
- [microservices.instructions.md](../../instructions/microservices.instructions.md)
- [performance.instructions.md](../../instructions/performance.instructions.md)
- [build-dependency-standards.instructions.md](../../instructions/build-dependency-standards.instructions.md)
- [policy.instructions.md](../../instructions/policy.instructions.md)
- [wsl-execution.instructions.md](../../instructions/wsl-execution.instructions.md)
