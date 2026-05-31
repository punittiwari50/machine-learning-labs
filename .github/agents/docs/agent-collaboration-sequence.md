# Agent Collaboration Sequence

## Objective
Ensure agents collaborate in strict order and complete all required handoffs.

## Collaboration Chain
1. ML Delivery Orchestrator starts workflow.
2. ML Research Specialist produces research package.
3. ML System Design Engineer consumes research package and outputs Validation Input.
4. ML Quality Reviewer consumes Validation Input and outputs Integration Input.
5. ML Integration Architect consumes Integration Input and outputs CICD Input.
6. ML CI/CD Release Engineer consumes CICD Input and outputs release plan and rollout gates.
7. ML E2E Delivery Validator validates full flow from ML code to CI/CD delivery readiness.
8. ML Delivery Orchestrator compiles final consolidated report.

## Required Handoff Checks
At each handoff, receiving agent must verify:
- required sections exist
- acceptance criteria are testable
- unresolved risks are clearly listed
- next-stage instructions are actionable

## Failure Handling
- If a handoff is incomplete, return to previous stage with exact missing items.
- Do not advance stages on partial or ambiguous outputs.
