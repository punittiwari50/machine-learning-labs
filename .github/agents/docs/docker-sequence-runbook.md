# Docker and Kubernetes Sequence Runbook

## Purpose
Provide exact ordered steps to execute delivery validation in the correct sequence.

## Step-by-Step Sequence
1. Validate runtime context
- Python and Node commands run in WSL Ubuntu.
- Docker Compose and Kubernetes commands run on host Windows.

2. Validate Compose definition
- Run: docker compose -f <compose-file>.yml config
- Expected: no schema or interpolation errors.

3. Start integration stack with Compose
- Run: docker compose -f <compose-file>.yml up -d
- Expected: all required services healthy.

4. Run integration smoke checks
- Verify API health endpoints.
- Verify model inference endpoint returns valid response.

5. Validate Kubernetes manifests
- Run: kubectl apply --dry-run=client -f <k8s-manifest-or-dir>
- Expected: no validation errors.

6. Deploy to Kubernetes staging
- Apply manifests in this order:
  a) namespace
  b) config maps and secrets references
  c) deployments and services
  d) optional ingress/hpa
- Expected: rollout status successful.

7. Run staging functional checks
- Execute test flows for 3-5 real-time use cases.
- Confirm logs, metrics, and traces are visible.

8. Production rollout
- Use canary or blue-green rollout.
- Monitor release gates and rollback triggers.

9. Post-rollout validation
- Confirm SLA/SLO targets, model metrics, and business KPIs.
- Document final status and any follow-up actions.

## Strict Rule
Do not skip, merge, or reorder these steps.
