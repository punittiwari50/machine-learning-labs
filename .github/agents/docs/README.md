# Agent Delivery Docs

This folder contains the delivery-orchestrator and CI/CD runbooks used by agent workflows.

## Files
- delivery-orchestrator-playbook.md: End-to-end stage orchestration, handoffs, and completion checks.
- cicd-release-playbook.md: CI/CD stage design, release gates, rollback policy, and validation points.
- docker-sequence-runbook.md: Ordered Docker Compose and Kubernetes execution steps.
- agent-collaboration-sequence.md: Which agent calls which agent, and required handoff payloads.
- code-generation-documentation-standard.md: Required code-level comments, markup notes, and use-case formatting.

## Usage Rule
Agents must follow these docs in sequence. Do not skip stages or reorder deployment validation checks.
