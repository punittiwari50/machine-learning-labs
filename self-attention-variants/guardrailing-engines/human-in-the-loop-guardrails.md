# Human-in-the-Loop Guardrails

## Scope

Add human oversight where ambiguity, risk, or business-critical impact requires explicit review.

## Core Controls

- Risk-based escalation routing to reviewer queues.
- Reviewer decision capture with rationale and outcome labels.
- Feedback loops into prompt, policy, and classifier updates.
- Exception handling with explicit risk acceptance records.

## Validation Signals

- Escalation precision (how often escalations are justified).
- Reviewer agreement rate and adjudication latency.
- Post-review incident reduction after policy updates.

## Realtime Enterprise Use Cases

1. Medical Triage Assistant
- Business context: Nurse-support intake workflow.
- ML function: Suggest triage priority and next action.
- Deployment concern: High-risk misclassification.
- Validation and rollback signal: Critical disagreement rate in clinician review; rollback triage policy set.

2. Financial Advisory Drafting
- Business context: Advisor workflows for portfolio communication.
- ML function: Draft client-facing recommendations.
- Deployment concern: Non-compliant recommendations.
- Validation and rollback signal: Compliance rejection trend in reviewed drafts; rollback guidance prompt pack.

3. Public Sector Citizen Assistant
- Business context: Service eligibility and documentation support.
- ML function: Answer policy queries with decision support.
- Deployment concern: Equity-sensitive edge cases mishandled.
- Validation and rollback signal: Reviewer escalation backlog and adverse decision audits; rollback deployment ring.
