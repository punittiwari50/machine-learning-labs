# Basic Self-Attention Variants

## 1. Scaled Dot-Product Self-Attention

- Computes attention weights using query-key similarity, then aggregates values.
- Scale factor `1/sqrt(d_k)` stabilizes gradients.

When to use:
- Baseline transformer blocks.
- Short to moderate context workloads.

Pros:
- Strong quality and generalization.
- Standard and widely supported.

Cons:
- Quadratic memory and compute with sequence length.

Enterprise usage example:
- Internal document classification using a standard encoder transformer.

## 2. Multi-Head Self-Attention (MHSA)

- Runs attention in multiple learned subspaces (heads) and concatenates outputs.
- Each head captures different token relationships.

When to use:
- Most NLP and multimodal transformer architectures.
- Tasks requiring richer relational modeling.

Pros:
- Better representational capacity.
- Robust across many domains.

Cons:
- Extra compute and parameters compared to single-head attention.

Enterprise usage example:
- Contract analytics where separate heads learn entities, obligations, and temporal references.

## 3. Causal (Masked) Self-Attention

- Uses an autoregressive mask so each token attends only to previous tokens.
- Prevents future-token leakage during generation.

When to use:
- Text generation, code generation, and chat completion.

Pros:
- Correct autoregressive training objective.
- Works well with decoder-only LLMs.

Cons:
- Still quadratic within visible context.

Enterprise usage example:
- Internal code-assistant model for developer productivity.

## 4. Cross-Attention (Encoder-Decoder Attention)

- Queries come from decoder tokens; keys/values come from encoder outputs.
- Lets generated output condition on source input.

When to use:
- Translation, summarization, and sequence-to-sequence tasks.

Pros:
- Strong source-target alignment.
- Clear separation between input encoding and output generation.

Cons:
- Additional memory and latency from encoder-decoder stack.

Enterprise usage example:
- Multi-lingual customer support response generation from source tickets.

## 5. Local Window Attention

- Restricts attention to nearby tokens within a fixed window.
- Reduces cost from global pairwise interactions.

When to use:
- Long documents where local context dominates.
- Resource-constrained deployments.

Pros:
- Lower memory and latency than full attention.
- Scales to longer sequences.

Cons:
- May miss long-range dependencies.

Enterprise usage example:
- Processing very long audit logs with near-term event dependency patterns.

## 6. Global + Local Hybrid Attention

- Combines local windows with selected global tokens.
- Preserves long-range information paths at lower cost.

When to use:
- Long-context tasks needing both local detail and document-level signals.

Pros:
- Better long-range reasoning than local-only attention.
- More efficient than full global attention.

Cons:
- Requires careful selection of global tokens.

Enterprise usage example:
- Policy QA where section headers and key clauses act as global anchor tokens.

## 7. Guardrailing Engines (Canonical Index)

Guardrailing content is maintained in a dedicated module to avoid taxonomy drift.

Core guardrail notebooks:
1. [input-guardrails.ipynb](../guardrailing-engines/input-guardrails.ipynb)
2. [retrieval-guardrails.ipynb](../guardrailing-engines/retrieval-guardrails.ipynb)
3. [generation-guardrails.ipynb](../guardrailing-engines/generation-guardrails.ipynb)
4. [tool-action-guardrails.ipynb](../guardrailing-engines/tool-action-guardrails.ipynb)
5. [post-generation-delivery-guardrails.ipynb](../guardrailing-engines/post-generation-delivery-guardrails.ipynb)
6. [runtime-infrastructure-guardrails.ipynb](../guardrailing-engines/runtime-infrastructure-guardrails.ipynb)
7. [human-in-the-loop-guardrails.ipynb](../guardrailing-engines/human-in-the-loop-guardrails.ipynb)

Extended serving and orchestration guardrails:
1. [memory-management-serving-basic-guardrails.ipynb](../guardrailing-engines/memory-management-serving-basic-guardrails.ipynb)
2. [memory-management-serving-advanced-guardrails.ipynb](../guardrailing-engines/memory-management-serving-advanced-guardrails.ipynb)
3. [nim-multi-engine-routing-guardrails.ipynb](../guardrailing-engines/nim-multi-engine-routing-guardrails.ipynb)
4. [nim-compose-orchestration-guardrails.ipynb](../guardrailing-engines/nim-compose-orchestration-guardrails.ipynb)
5. [nim-kubernetes-orchestration-guardrails.ipynb](../guardrailing-engines/nim-kubernetes-orchestration-guardrails.ipynb)

Canonical source of truth:
- [README.md](../guardrailing-engines/README.md)
