# Full Validation Report

- Date: 2026-05-31T21:10:40+02:00
- Scope: flake8 + mypy + guardrailing notebook sweep

## Status
- flake8: PASS
- mypy: PASS
- notebook_sweep: PASS

## flake8 output (tail)
```text
```

## mypy output (tail)
```text
Success: no issues found in 17 source files
```

## notebook sweep output (tail)
```text
Now using node v25.6.1 (npm v11.10.0)
default -> node (-> v25.6.1 *)
[RUN] self-attention-variants/guardrailing-engines/generation-guardrails.ipynb
[PASS] self-attention-variants/guardrailing-engines/generation-guardrails.ipynb
[RUN] self-attention-variants/guardrailing-engines/human-in-the-loop-guardrails.ipynb
[PASS] self-attention-variants/guardrailing-engines/human-in-the-loop-guardrails.ipynb
[RUN] self-attention-variants/guardrailing-engines/input-guardrails.ipynb
[PASS] self-attention-variants/guardrailing-engines/input-guardrails.ipynb
[RUN] self-attention-variants/guardrailing-engines/memory-management-serving-advanced-guardrails.ipynb
[PASS] self-attention-variants/guardrailing-engines/memory-management-serving-advanced-guardrails.ipynb
[RUN] self-attention-variants/guardrailing-engines/memory-management-serving-basic-guardrails.ipynb
[PASS] self-attention-variants/guardrailing-engines/memory-management-serving-basic-guardrails.ipynb
[RUN] self-attention-variants/guardrailing-engines/nim-compose-orchestration-guardrails.ipynb
[PASS] self-attention-variants/guardrailing-engines/nim-compose-orchestration-guardrails.ipynb
[RUN] self-attention-variants/guardrailing-engines/nim-kubernetes-orchestration-guardrails.ipynb
[PASS] self-attention-variants/guardrailing-engines/nim-kubernetes-orchestration-guardrails.ipynb
[RUN] self-attention-variants/guardrailing-engines/nim-multi-engine-routing-guardrails.ipynb
[PASS] self-attention-variants/guardrailing-engines/nim-multi-engine-routing-guardrails.ipynb
[RUN] self-attention-variants/guardrailing-engines/post-generation-delivery-guardrails.ipynb
[PASS] self-attention-variants/guardrailing-engines/post-generation-delivery-guardrails.ipynb
[RUN] self-attention-variants/guardrailing-engines/retrieval-guardrails.ipynb
[PASS] self-attention-variants/guardrailing-engines/retrieval-guardrails.ipynb
[RUN] self-attention-variants/guardrailing-engines/runtime-infrastructure-guardrails.ipynb
[PASS] self-attention-variants/guardrailing-engines/runtime-infrastructure-guardrails.ipynb
[RUN] self-attention-variants/guardrailing-engines/tool-action-guardrails.ipynb
[PASS] self-attention-variants/guardrailing-engines/tool-action-guardrails.ipynb
NOTEBOOK_PASS:12
NOTEBOOK_FAIL:0
```
