# Tool and Action Guardrails

## Scope

Control what tools can be used, how parameters are validated, and when human approval is required.

## Core Controls

- Capability allowlist by role, task, and environment.
- Parameter constraints: budget limits, timeout caps, side-effect scope.
- Idempotency and dry-run requirement for risky actions.
- Human approval gates for irreversible operations.

## Validation Signals

- Blocked high-risk action count.
- Unauthorized tool attempt rate.
- Approved-vs-rejected action ratio by risk class.

## Realtime Enterprise Use Cases

1. SRE Remediation Agent
- Business context: AI assistant executes operational runbooks.
- ML function: Plan and invoke diagnostic/remediation tools.
- Deployment concern: Unsafe production action execution.
- Validation and rollback signal: Increase in blocked critical actions or incidents; rollback tool policy package.

2. FinOps Automation Assistant
- Business context: Cost optimization actions in cloud environments.
- ML function: Suggest and execute rightsizing operations.
- Deployment concern: Accidental service disruption from aggressive actions.
- Validation and rollback signal: Error-budget burn increase after actions; rollback action permissions.

3. Data Pipeline Operator Bot
- Business context: Data team restarts jobs and backfills partitions.
- ML function: Invoke orchestration APIs with parameterized commands.
- Deployment concern: Wrong partition range causes data corruption risk.
- Validation and rollback signal: Validation-rule violations in action logs; rollback policy and enforce human approval.
