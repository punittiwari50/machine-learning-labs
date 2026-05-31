# Guardrailing Engines Benchmark Dashboard

**Date**: 2026-05-31
**Scope**: Consolidated benchmark and verification dashboard for guardrail notebooks.

## Validation Method
- Source of metrics: executed outputs in tested notebooks under self-attention-variants/guardrailing-engines/tested.
- Benchmarks tracked per notebook:
  - mean_latency_ms
  - p95_latency_ms
  - throughput_rows_per_sec
- Quality gate inference:
  - assertions_passed = true when no AssertionError or traceback appears in notebook outputs.

## Threshold Policy
- P95 latency threshold: < 450.0 ms
- Throughput threshold: > 250.0 rows/s

## Consolidated Benchmark Table

| Notebook | Mean Latency (ms) | P95 Latency (ms) | Throughput (rows/s) | P95 Threshold | Throughput Threshold | Threshold Status | Trend Mean Latency | Trend Throughput | Assertions |
|---|---:|---:|---:|---:|---:|---|---|---|---|
| input-guardrails_tested.ipynb | 2.0403 | 2.7308 | 147040.5564 | < 450.0 | > 250.0 | PASS | +0.0000 ms | +0.0000 rows/s | PASS |
| retrieval-guardrails_tested.ipynb | 1.7826 | 1.9974 | 168293.4976 | < 450.0 | > 250.0 | PASS | +0.0000 ms | +0.0000 rows/s | PASS |
| generation-guardrails_tested.ipynb | 1.9548 | 2.4373 | 153465.9753 | < 450.0 | > 250.0 | PASS | +0.0000 ms | +0.0000 rows/s | PASS |
| tool-action-guardrails_tested.ipynb | 1.8914 | 2.3115 | 158609.7356 | < 450.0 | > 250.0 | PASS | +0.0000 ms | +0.0000 rows/s | PASS |
| post-generation-delivery-guardrails_tested.ipynb | 1.9937 | 2.5835 | 150475.1881 | < 450.0 | > 250.0 | PASS | +0.0000 ms | +0.0000 rows/s | PASS |
| runtime-infrastructure-guardrails_tested.ipynb | 1.8628 | 2.2601 | 161050.2019 | < 450.0 | > 250.0 | PASS | +0.0000 ms | +0.0000 rows/s | PASS |
| human-in-the-loop-guardrails_tested.ipynb | 1.9372 | 2.2430 | 154864.7909 | < 450.0 | > 250.0 | PASS | +0.0000 ms | +0.0000 rows/s | PASS |

## NVIDIA NIM Orchestration Consolidated Verification

This section tracks the three type-separated NVIDIA NIM orchestration notebooks.

| Notebook | Type | Code Cells | Cells With Outputs | Error Cells | Status |
|---|---|---:|---:|---:|---|
| nim-compose-orchestration-guardrails_tested.ipynb | Compose | 11 | 9 | 0 | PASS |
| nim-kubernetes-orchestration-guardrails_tested.ipynb | Kubernetes | 11 | 9 | 0 | PASS |
| nim-multi-engine-routing-guardrails_tested.ipynb | Multi-Engine Routing | 11 | 9 | 0 | PASS |

Validation outcome: ALL_TESTED_NOTEBOOKS_VALID

## Notes
- Trend columns are automatically computed against the prior snapshot/report values.
- Snapshot is updated after each report generation at self-attention-variants/guardrailing-engines/tested/benchmark-snapshot.json.
