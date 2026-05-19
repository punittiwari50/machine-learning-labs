# A1 Text Embeddings (Modality)

## A) Grouped by Data Type (Modality)

Below is a modality-first view of embedding subtypes and their purpose.

---

### A1. Text Embeddings

| Subtype | Purpose | Typical Tools |
|---|---|---|
| Token embeddings | Map discrete tokens to dense vectors for neural models | TensorFlow Embedding layer |
| Subword embeddings | Handle OOV and morphology using pieces (WordPiece/BPE-like) | tensorflow-text tokenizers + Embedding |
| Character embeddings | Robustness to typos/noise and morphology | TF strings + char lookup |
| Sentence embeddings | Encode sentence-level semantics for similarity/retrieval | Pooling over token states / encoders |
| Contextual embeddings | Dynamic token meaning based on context | Transformer encoders |

---

```python
# Example: token/subword style pipeline with TensorFlow + tensorflow-text style ops
texts = tf.constant([
    'machine learning improves search',
    'deep learning powers modern NLP'
])

# Basic whitespace split (works without tensorflow-text)
tokens = tf.strings.split(texts)
flat_tokens = tokens.flat_values

# Build a simple vocab from observed tokens for demonstration
unique_tokens, _ = tf.unique(flat_tokens)
vocab = tf.concat([tf.constant(['<PAD>', '<UNK>']), unique_tokens], axis=0)

# Map tokens -> ids
table = tf.lookup.StaticVocabularyTable(
    tf.lookup.KeyValueTensorInitializer(vocab, tf.range(tf.shape(vocab)[0], dtype=tf.int64)),
    num_oov_buckets=1
)
token_ids = table.lookup(flat_tokens)

# Token embedding layer
embedding_dim = 16
emb_layer = tf.keras.layers.Embedding(input_dim=int(vocab.shape[0]) + 1, output_dim=embedding_dim)
embedded_tokens = emb_layer(token_ids)

print('Vocab size:', int(vocab.shape[0]))
print('Token IDs shape:', token_ids.shape)
print('Embedded shape:', embedded_tokens.shape)
```

---

**Do (Text Embeddings):**
- Normalize text consistently (case, punctuation, unicode strategy).
- Reserve OOV and PAD ids explicitly.
- Tune embedding dimension to data scale (small data -> smaller dims).
- Use subwords when domain has misspellings or many rare words.

**Don't (Text Embeddings):**
- Do not mix tokenization methods between training and serving.
- Do not assume larger dimension always improves generalization.
- Do not ignore sequence length truncation effects in production.

**Tips and Tricks:**
- Start with 64 to 256 dims for medium-size corpora; shrink if overfitting.
- Use average pooling baseline before complex attention heads.
- Monitor nearest neighbors qualitatively for embedding health checks.

**Summary:** Text embeddings map language units to vectors that capture semantics and syntax at different granularities.

**Application Use Cases:** semantic search, intent classification, duplicate question detection, recommendation ranking.

---

