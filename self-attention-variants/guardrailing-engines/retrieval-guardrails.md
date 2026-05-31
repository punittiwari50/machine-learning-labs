# Retrieval Guardrails

## Scope

Ensure retrieved context is trustworthy, relevant, and safe before generation.

## Core Controls

- Trusted-source enforcement and freshness windows.
- Duplicate suppression and chunk-level quality scoring.
- Prompt-injection detection in retrieved passages.
- Evidence-citation binding between response claims and context.

## Validation Signals

- Citation precision and citation coverage.
- Retrieval poisoning detection rate.
- Unsupported-claim rate in post-answer audits.

## Realtime Enterprise Use Cases

1. Compliance Copilot Search
- Business context: Analysts query policy and regulation repositories.
- ML function: Retrieval-augmented answers with citations.
- Deployment concern: Hallucinated or stale citations.
- Validation and rollback signal: Citation precision drop below SLO; rollback retrieval index version.

2. Legal Discovery Assistant
- Business context: Large-scale document evidence search.
- ML function: Case-relevant paragraph retrieval.
- Deployment concern: Poisoned documents influence legal summaries.
- Validation and rollback signal: Poison-hit alerts in canary traffic; rollback retriever model and quarantine index shard.

3. Incident Runbook Search
- Business context: SRE teams retrieve known-fix procedures during outages.
- ML function: Rank and surface high-confidence runbook sections.
- Deployment concern: Wrong runbook snippets increase MTTR.
- Validation and rollback signal: MTTR regression with low citation coverage; rollback reranker config.
