# Generation Guardrails

## Scope

Constrain model outputs to policy-compliant, safe, and structurally valid responses.

## Core Controls

- Safety and policy classifiers on draft outputs.
- Structured output enforcement (schema, enums, required fields).
- Hallucination heuristics with low-evidence fallback templates.
- Content transformation controls (masking, refusal templates, safe rewrites).

## Validation Signals

- Policy violation rate by category.
- Schema validation pass rate.
- Hallucination proxy rate from citation mismatch checks.

## Realtime Enterprise Use Cases

1. Banking Chat Assistant
- Business context: Customers ask account and product questions.
- ML function: Natural language answer generation.
- Deployment concern: Unsafe financial advice phrasing.
- Validation and rollback signal: Policy violation trend in post-filter logs; rollback generation policy version.

2. Code Review Bot
- Business context: Engineering teams use AI for PR summaries.
- ML function: Generate review comments and risk notes.
- Deployment concern: Fabricated code references.
- Validation and rollback signal: Citation mismatch in sampled reviews; rollback decoder prompt template.

3. Insurance Claim Triage
- Business context: Claims operators need concise adjudication notes.
- ML function: Structured summary generation.
- Deployment concern: Invalid output schema breaks downstream workflow.
- Validation and rollback signal: Schema-failure rate in production queue; rollback output contract version.
