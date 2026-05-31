# Memory Management during Serving (Basic)

## Scope

Establish foundational memory controls for online inference so response quality stays stable under concurrent traffic.

## Core Controls

- Per-request memory budget checks before inference starts.
- Session-context token window limits with deterministic truncation.
- Early rejection when projected memory exceeds configured budget.
- TTL-based cache eviction for short-lived serving state.

## Validation Signals

- Memory budget pass rate at admission.
- Context truncation rate by traffic segment.
- OOM prevention success rate.
- P95 latency delta under budget pressure.

## Realtime Enterprise Use Cases

1. Internal IT Helpdesk Assistant
- Business context: Employees query operational runbooks throughout the day.
- ML function: Multi-turn retrieval-augmented response serving.
- Deployment concern: Long chats push context memory past safe limits.
- Validation and rollback signal: Truncation and rejection rates spike; rollback window-size policy.

2. Retail Product Support Bot
- Business context: Customers ask troubleshooting questions during peak hours.
- ML function: Real-time response generation with bounded context history.
- Deployment concern: Concurrent sessions exceed host memory budget.
- Validation and rollback signal: Admission failures climb above SLO; rollback budget thresholds.

3. Insurance FAQ Assistant
- Business context: Policyholders request claim and coverage clarifications.
- ML function: Session-based answer serving with cache reuse.
- Deployment concern: Stale cache entries consume memory and degrade throughput.
- Validation and rollback signal: Cache-hit quality drops and latency rises; rollback cache TTL profile.
