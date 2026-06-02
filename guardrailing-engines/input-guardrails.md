# Input Guardrails

## Scope

Protect the system before model execution by validating requests, filtering unsafe inputs, and normalizing payloads.

## Core Controls

- Schema and payload checks: structure, size, encoding, locale.
- Prompt-injection and jailbreak pattern detection.
- PII and secret scanning with redaction or hard block.
- Domain routing policy (allowlist and denylist by topic/risk level).

## Validation Signals

- Input rejection rate by category.
- Redaction precision and recall from labeled audit sets.
- False-block review rate from human triage.

## Realtime Enterprise Use Cases

1. Payment API Front Door
- Business context: Public checkout gateway receives mixed quality requests.
- ML function: Fraud and intent triage request pre-processing.
- Deployment concern: Attackers bypass input schema checks.
- Validation and rollback signal: Rejection spike with latency regression; rollback policy bundle on threshold breach.

2. Healthcare Intake Assistant
- Business context: Patient chat intake in regulated environment.
- ML function: Symptom text understanding and routing.
- Deployment concern: Accidental PHI leakage to downstream logs.
- Validation and rollback signal: Redaction miss count from audit sample; rollback if any critical PHI leak is detected.

3. Enterprise Support Portal
- Business context: Global support prompts across multiple products.
- ML function: Intent and severity pre-classification.
- Deployment concern: Overblocking valid customer prompts.
- Validation and rollback signal: False-block rate from manual review queue; rollback when sustained beyond policy target.
