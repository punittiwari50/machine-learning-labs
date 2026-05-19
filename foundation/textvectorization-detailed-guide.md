# TextVectorization Detailed Guide

This guide explains the TextVectorization section in detail for practical enterprise use.

## 1) Different Arguments, Function Inputs, and When To Use Which

TextVectorization converts raw text into model-friendly numeric features.
It has three common design layers:
- Cleaning and normalization (standardize)
- Token splitting (split)
- Numeric representation (output_mode)

### A) standardize

What it does:
- Cleans raw text before tokenization.

Input type:
- Built-in option as string (for example lower_and_strip_punctuation)
- Custom external function that takes and returns tensor-like text

When to use built-in:
- Fast baseline projects
- Common English-like cleanup

When to use custom function:
- Enterprise text has IDs, URLs, ticket numbers, email, policy codes
- You want placeholders like <ORDER_ID> and <URL>

Real example:
- Support logs: Order#9988 failed on https://ops.example.com
- Custom standardize can map to: <ORDER_ID> failed on <URL>
- Benefit: lower vocabulary explosion and better generalization

### B) split

What it does:
- Decides how text becomes tokens.

Input type:
- Built-in options such as whitespace
- Custom external split function

When to use whitespace split:
- Normal sentence data
- Quick prototypes

When to use custom split function:
- Domain patterns need custom boundaries
- Examples: SLA-breach, eu-west, error-code-500

Real example:
- If sla-breach is a single token, model learns one concept
- If split into sla and breach, model may generalize better across contexts

### C) output_mode

What it does:
- Defines the final feature format.

Main options and use cases:
- int
  - Output: token IDs sequence
  - Use for sequence models like Embedding + RNN/CNN/Transformer
- multi_hot
  - Output: one vector showing token presence
  - Use for fast baseline text classification
- count
  - Output: token frequency counts
  - Use when repeated words matter
- tf_idf
  - Output: weighted frequency, down-weights very common terms
  - Use for search/ranking/classic ML pipelines

Real example:
- Intent classification with small model: multi_hot or tf_idf can be fast and strong
- Deep sequence model: int is usually preferred

### D) output_sequence_length (mainly with int)

What it does:
- Fixes sequence length by truncation/padding.

When to use:
- Model needs fixed input shape
- Production serving needs stable tensor shape

Real example:
- Chat intent model in API needs predictable latency and shape

### E) max_tokens

What it does:
- Limits vocabulary size.

When to use:
- Memory constraints
- Avoid long-tail noisy tokens dominating vocabulary

Real example:
- Large logs include random IDs and hashes
- max_tokens keeps only most useful terms

### F) ngrams

What it does:
- Adds token combinations such as bigrams.

When to use:
- Phrase-level meaning matters
- Example: not approved vs approved

Real example:
- Fraud text: card declined and failed payment phrases carry stronger signals than single tokens

### G) vocabulary and adapt

Two patterns:
- adapt on training text
- provide fixed vocabulary directly

When to use adapt:
- Early exploration and controlled retraining

When to use fixed vocabulary:
- Strict enterprise governance
- Reproducible train-serve behavior and rollback

## 2) ML Concepts, Terms, and Keywords In Simple Words

### Token

Simple meaning:
- Small text unit after splitting (word, subword, symbol)

Example:
- payment failed quickly -> payment, failed, quickly

### Vocabulary

Simple meaning:
- List of known tokens and their IDs

Example:
- payment=8, failed=17, refund=23

### OOV (Out Of Vocabulary)

Simple meaning:
- Token not present in vocabulary

Example:
- New product codename appears in production logs

Why it matters:
- Too many OOV tokens reduce model quality

### OOV buckets

Simple meaning:
- Multiple unknown bins instead of one single unknown ID

Why useful:
- Unknown tokens are distributed, which can preserve some signal

### Embedding

Simple meaning:
- Learnable dense vector for each token ID

Example:
- payment and billing become close in vector space if used similarly

### Bag of Words

Simple meaning:
- Represent text by which words appear, not their order

Use case:
- Fast baseline classifier for support ticket routing

### TF-IDF

Simple meaning:
- Important words get higher weight, very common words get lower weight

Use case:
- Search relevance and classic ML models

### Sequence model

Simple meaning:
- Model that uses token order

Examples:
- RNN, CNN for text, Transformers

Use case:
- Sentiment or intent where order changes meaning

### Padding and truncation

Simple meaning:
- Padding adds blanks to short text; truncation cuts long text

Use case:
- Fixed input size for batched inference in production

### Train-serve skew

Simple meaning:
- Training preprocessing and production preprocessing differ

Why dangerous:
- Model behaves differently in production than during validation

How to reduce:
- Use same TextVectorization logic and same vocabulary artifact in both phases

### Data leakage

Simple meaning:
- Information from validation/test accidentally used in training setup

In TextVectorization context:
- Calling adapt on all data before split can leak knowledge

Safe practice:
- Fit or adapt only on training split

### Drift

Simple meaning:
- Live data distribution changes over time

Examples:
- New product names, slang, region-specific phrases

What to monitor:
- OOV rate, top new tokens, feature distribution shift

## Practical Selection Cheat Sheet

- Need deep model with word order: choose output_mode int, set output_sequence_length
- Need simple and fast baseline: choose multi_hot or tf_idf
- Need phrase signal: enable ngrams
- Need enterprise cleanup: use custom standardize function
- Need domain token boundaries: use custom split function
- Need strict reproducibility: use fixed vocabulary and version artifacts
- Need memory control: set max_tokens

## Real-Time Enterprise Mini Scenarios

### Scenario 1: Support Ticket Routing

Input:
- Ticket TKT-1245 failed after payment timeout on eu-west

Good setup:
- custom standardize for ticket IDs and numbers
- custom split for hyphenated region tokens
- output_mode int for sequence model

Why:
- Keeps semantic tokens stable and supports contextual understanding

### Scenario 2: Search Query Ranking

Input:
- refund card chargeback process

Good setup:
- custom standardize for noise cleanup
- output_mode tf_idf with ngrams

Why:
- Phrase weighting improves retrieval relevance

### Scenario 3: Compliance Alert Classification

Input:
- SLA breach and unauthorized access attempt

Good setup:
- custom standardize with domain placeholders
- output_mode multi_hot or int based on model complexity

Why:
- Fast baseline possible with multi_hot, and can scale to sequence model later

## Minimal Example Pattern (External Functions)

```python
import tensorflow as tf

texts = tf.constant([
    "SLA-breach on Order#9988 in EU-West",
    "Payment latency spiked on https://ops.example.com",
])

def my_standardize(x):
    x = tf.strings.lower(x)
    x = tf.strings.regex_replace(x, r"https?://\\S+", " <URL> ")
    x = tf.strings.regex_replace(x, r"order#?\\d+", " <ORDER_ID> ")
    x = tf.strings.regex_replace(x, r"[^a-z<>_\\- ]", " ")
    x = tf.strings.regex_replace(x, r"\\s+", " ")
    return tf.strings.strip(x)

def my_split(x):
    x = tf.strings.regex_replace(x, "-", " ")
    return tf.strings.split(x)

vec = tf.keras.layers.TextVectorization(
    standardize=my_standardize,
    split=my_split,
    output_mode="int",
    output_sequence_length=12,
    max_tokens=20000,
)

vec.adapt(texts)
print(vec.get_vocabulary()[:20])
print(vec(texts))
```

## Final Advice

- Start simple, then increase complexity only when metrics justify it.
- Keep preprocessing functions versioned.
- Monitor OOV and drift in production.
- Keep train and serve preprocessing identical.