# C ? Per-Type: Text Embedding Subtypes

## C) Separate Code Cell Per Modality Subtype

Each subtype below is isolated in its own code cell and includes comments explaining purpose and behavior.

---

```python
# C1) Text Token Embedding
# Purpose: map token IDs to dense vectors for NLP models.

tok_ids = tf.constant([[1, 2, 3], [2, 4, 0]], dtype=tf.int32)
tok_vec = tf.keras.layers.Embedding(input_dim=50, output_dim=8)(tok_ids)
print('token embedding shape:', tok_vec.shape)
```

---

```python
# C2) Text Subword Embedding
# Purpose: represent subword pieces to handle rare/OOV terms.

sub_tokens = tf.constant([[b'mach', b'ine', b'learn'], [b'deep', b'learn', b'ing']])
sub_flat = tf.reshape(sub_tokens, [-1])
sub_vocab, _ = tf.unique(sub_flat)
sub_table = tf.lookup.StaticVocabularyTable(
    tf.lookup.KeyValueTensorInitializer(sub_vocab, tf.range(tf.shape(sub_vocab)[0], dtype=tf.int64)),
    num_oov_buckets=1,
)
sub_ids = sub_table.lookup(sub_tokens)
sub_vec = tf.keras.layers.Embedding(input_dim=200, output_dim=8)(sub_ids)
print('subword embedding shape:', sub_vec.shape)
```

---

```python
# C3) Text Character Embedding
# Purpose: robustly encode words at character level.

chars = tf.constant([[b'm', b'l', b'\x00'], [b'n', b'l', b'p']])
char_flat = tf.reshape(chars, [-1])
char_vocab, _ = tf.unique(char_flat)
char_table = tf.lookup.StaticVocabularyTable(
    tf.lookup.KeyValueTensorInitializer(char_vocab, tf.range(tf.shape(char_vocab)[0], dtype=tf.int64)),
    num_oov_buckets=1,
)
char_ids = char_table.lookup(chars)
char_vec = tf.keras.layers.Embedding(input_dim=128, output_dim=6)(char_ids)
print('character embedding shape:', char_vec.shape)
```

---

```python
# C4) Sentence Embedding
# Purpose: generate one vector for a full sentence (good for retrieval/classification).

sent_ids = tf.constant([[1, 4, 3, 0], [2, 2, 5, 6]], dtype=tf.int32)
sent_tok = tf.keras.layers.Embedding(input_dim=100, output_dim=10)(sent_ids)
sent_vec = tf.reduce_mean(sent_tok, axis=1)
print('sentence embedding shape:', sent_vec.shape)
```

---

```python
# C5) Contextual Text Embedding (Transformer-style)
# Purpose: token vectors depend on surrounding tokens via self-attention.

ctx_ids = tf.constant([[1, 2, 3, 4], [4, 3, 2, 1]], dtype=tf.int32)
ctx_tok = tf.keras.layers.Embedding(input_dim=100, output_dim=12)(ctx_ids)
ctx_attn = tf.keras.layers.MultiHeadAttention(num_heads=2, key_dim=6)(ctx_tok, ctx_tok)
ctx_vec = tf.keras.layers.GlobalAveragePooling1D()(ctx_attn)
print('contextual sentence embedding shape:', ctx_vec.shape)
```

---

