---
description: "Design an enterprise ML system architecture with clear service boundaries, contracts, resilience, and deployment plan"
agent: agent
argument-hint: "System to design"
tools: [read, edit, search, web]
---

You are designing an implementation-ready ML system from researched requirements.

## Mission

Deliver a modular, cycle-free, enterprise-ready blueprint with explicit runtime and deployment boundaries.

## Required Design Flow

1. Dataset and prior-art research summary.
2. Functional and non-functional requirements.
3. Platform component matrix with rationale.
4. Bounded context and service ownership map.
5. Layered design and contract definitions.
6. Data flow and resilience matrix.
7. Observability, security, and operations plan.
8. Deployment blueprint for Docker Compose and Kubernetes.

## Required Output Sections

1. Core design
2. Basic modular design
3. Advanced performance and resilience design
4. Enterprise operations and governance design
5. Code blueprint and interfaces
6. Deployment blueprint
7. Validation Input handoff

## Constraints

- Keep design in-topic and avoid speculative branches.
- Prevent duplicated business logic across services.
- Keep dependency direction explicit and cycle-free.

## References

- ../instructions/architecture.instructions.md
- ../instructions/microservices.instructions.md
- ../instructions/build-dependency-standards.instructions.md
- ../agents/docs/agent-collaboration-sequence.md
- ../agents/docs/docker-sequence-runbook.md
