# Guardrailing Engines

This directory breaks the guardrailing topic into separate files so each control
layer can be reviewed and updated independently.

## Contents

- `input-guardrails.md`: Validate prompts, payloads, and other untrusted inputs.
- `input-guardrails.ipynb`: Runnable notebook for input validation and normalization.
- `retrieval-guardrails.md`: Filter retrieval sources and protect evidence quality.
- `retrieval-guardrails.ipynb`: Runnable notebook for retrieval scoring and filtering.
- `generation-guardrails.md`: Constrain model drafts before they leave the model.
- `generation-guardrails.ipynb`: Runnable notebook for generation-time policy checks.
- `tool-action-guardrails.md`: Control tool use, side effects, and approvals.
- `tool-action-guardrails.ipynb`: Runnable notebook for tool authorization decisions.
- `post-generation-delivery-guardrails.md`: Sanitize and gate responses before delivery.
- `post-generation-delivery-guardrails.ipynb`: Runnable notebook for final response sanitation and rollout checks.
- `memory-management-serving-basic-guardrails.md`: Basic memory budgets, truncation, and cache TTL controls during serving.
- `memory-management-serving-basic-guardrails.ipynb`: Runnable notebook for foundational serving-time memory guardrails.
- `memory-management-serving-advanced-guardrails.md`: Advanced KV-cache orchestration, offload, and admission controls.
- `memory-management-serving-advanced-guardrails.ipynb`: Runnable notebook for enterprise-grade memory management during serving.
- `nim-multi-engine-routing-guardrails.md`: Multi-engine routing policy and fallback controls for NIM deployments.
- `nim-multi-engine-routing-guardrails.ipynb`: Runnable notebook for NIM multi-engine routing guardrails.
- `nim-compose-orchestration-guardrails.md`: Docker Compose orchestration guardrails for NIM services.
- `nim-compose-orchestration-guardrails.ipynb`: Runnable notebook for Compose-based NIM guardrail validation.
- `nim-kubernetes-orchestration-guardrails.md`: Kubernetes orchestration guardrails for NIM services.
- `nim-kubernetes-orchestration-guardrails.ipynb`: Runnable notebook for Kubernetes NIM guardrail validation.
- `nim-containerized-orchestration-copilot.md`: Copilot runbook for NVIDIA NIM orchestration verification and testing.
- `runtime-infrastructure-guardrails.md`: Add runtime resilience, budgets, and tracing.
- `runtime-infrastructure-guardrails.ipynb`: Runnable notebook for runtime budgets and tracing.
- `human-in-the-loop-guardrails.md`: Route ambiguous or high-risk cases to reviewers.
- `human-in-the-loop-guardrails.ipynb`: Runnable notebook for review routing.

## Suggested Reading Order

1. Start with `input-guardrails.ipynb`.
2. Move to `retrieval-guardrails.ipynb`.
3. Continue through `generation-guardrails.ipynb` and `tool-action-guardrails.ipynb`.
4. Add delivery and serving-memory controls with `post-generation-delivery-guardrails.ipynb`, `memory-management-serving-basic-guardrails.ipynb`, and `memory-management-serving-advanced-guardrails.ipynb`.
5. Add orchestration controls with `nim-multi-engine-routing-guardrails.ipynb`, `nim-compose-orchestration-guardrails.ipynb`, and `nim-kubernetes-orchestration-guardrails.ipynb`.
6. Finish with runtime and human review notebooks.

## Agent Workflow

1. Use `@ML Lab` to draft or expand the guardrail examples.
2. Use `@Code Quality` for read-only policy and consistency review.
3. Use `@ML Integration Architect` when wiring guardrails into distributed ML services.
4. Use `@ML CI/CD Release Engineer` to enforce release gates and deployment checks.
5. Use `@NIM Orchestration Guardrails` for NVIDIA NIM type-specific orchestration validation.

## Minimal Guardrail Checklist

- Every external boundary has explicit validation or filtering.
- Retrieval sources are trusted, fresh, and traceable.
- Generation outputs are validated before downstream consumption.
- Tool execution is constrained by least privilege and approval rules.
- Delivery paths apply final sanitization and observability.
- High-risk cases have a human review fallback.
