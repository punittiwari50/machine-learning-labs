# ML Delivery Orchestrator Playbook

## Goal
Run the full ML delivery flow from topic input to production-ready deployment plan with explicit stage gates.

## Ordered Stages
1. Research stage
- Agent: ML Research Specialist
- Output: topic research, concept depth, source set, and system-design input.
- Gate: topic scope complete and citations present.

2. System design stage
- Agent: ML System Design Engineer
- Output: architecture and code blueprint with deployment blueprint.
- Gate: modular design, SOLID boundaries, and no cycle risk.

3. Quality validation stage
- Agent: ML Quality Reviewer
- Output: code-level findings, concept markup notes, source-quality findings, and integration input.
- Gate: major issues identified with clear severity and fix direction.

4. Integration stage
- Agent: ML Integration Architect
- Output: service integration map, data contracts, and CICD input.
- Gate: runtime-stage ownership and integration order defined.

5. CI/CD stage
- Agent: ML CI/CD Release Engineer
- Output: pipeline architecture, release gates, rollback plan, and deployment strategy.
- Gate: all required quality and release checks mapped.

6. End-to-end validation stage
- Agent: ML E2E Delivery Validator
- Output: full functional verification report from ML code through CI/CD deployment readiness.
- Gate: functional use cases validated across all stages.

## Required Handoff Package
Each stage must pass these fields to next stage:
- assumptions
- constraints
- acceptance criteria
- unresolved risks
- required follow-up checks

## Completion Criteria
- All stage gates pass.
- Final report includes Docker Compose and Kubernetes step sequence.
- Report includes 3-5 real-time enterprise use cases.
- Report includes concise concept markup and code-comment expectations.
