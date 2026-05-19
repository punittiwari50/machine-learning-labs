# B Embeddings by Architecture

## B) Grouped by Model Architecture

Architecture-first view of embeddings and their purpose.

---

| Architecture Subtype | Purpose | Typical Libraries |
|---|---|---|
| Lookup-table embeddings | Learn vector per discrete id | TensorFlow Embedding |
| CNN embeddings | Learn local-to-global visual/text patterns | TensorFlow Keras CNN |
| RNN/LSTM embeddings | Sequence-order-aware representations | TensorFlow Keras RNN |
| Transformer embeddings | Contextual, long-range dependency encoding | TensorFlow Transformer blocks, tensorflow-text tokenization |
| Autoencoder embeddings | Compressed latent representation via reconstruction | TensorFlow encoder-decoder |
| Metric-learning embeddings | Geometry optimized by distance constraints | TF custom training (triplet/contrastive losses) |
| Graph embeddings (conceptual) | Node/edge semantics in latent space | TF-GNN style ecosystems |
| Hybrid/fusion embeddings | Combine multiple encoders/modalities | TensorFlow + OpenCV preprocessing |

---

### B2. Separate Code Cell Per Architecture Type

Each architecture embedding subtype below has its own standalone code cell with inline comments and purpose.

---

```python
# Lookup-table Embedding
# Purpose: map discrete IDs (tokens/categories) into trainable dense vectors.

x_ids = tf.constant([[1, 2, 3], [3, 4, 0]], dtype=tf.int32)
lookup_emb = tf.keras.layers.Embedding(input_dim=100, output_dim=16)(x_ids)
lookup_pooled = tf.reduce_mean(lookup_emb, axis=1)  # sequence -> fixed-size embedding
print('lookup_pooled shape:', lookup_pooled.shape)
```

---

```python
# CNN Embedding
# Purpose: learn local patterns and compress them into a semantic vector.

cnn_out = tf.keras.Sequential([
    tf.keras.layers.Conv1D(32, 3, activation='relu'),
    tf.keras.layers.GlobalMaxPool1D(),
    tf.keras.layers.Dense(16)
])(lookup_emb)
print('cnn_out shape:', cnn_out.shape)
```

---

```python
# Autoencoder Embedding
# Purpose: compress features into a latent vector that reconstructs inputs.

dense_in = tf.random.normal((2, 20))
latent = tf.keras.layers.Dense(8, activation='relu')(dense_in)
recon = tf.keras.layers.Dense(20)(latent)
print('latent shape:', latent.shape)
print('recon shape:', recon.shape)
```

---

```python
# Transformer Embedding
# Purpose: produce contextual embeddings using self-attention across the sequence.

attn = tf.keras.layers.MultiHeadAttention(num_heads=2, key_dim=8)(lookup_emb, lookup_emb)
tfm_out = tf.keras.layers.GlobalAveragePooling1D()(attn)
print('tfm_out shape:', tfm_out.shape)
```

---

```python
# RNN/LSTM Embedding
# Purpose: encode order-sensitive sequential context into a dense representation.

rnn_out = tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(12))(lookup_emb)
print('rnn_out shape:', rnn_out.shape)
```

---

```python
# Hybrid/Fusion Embedding
# Purpose: fuse embeddings from different encoders/modalities into one joint vector.

text_emb = tf.random.normal((3, 16))
image_emb = tf.random.normal((3, 16))

fusion_in = tf.concat([text_emb, image_emb], axis=-1)
fusion_emb = tf.keras.layers.Dense(20, activation='relu')(fusion_in)
print('fusion_emb shape:', fusion_emb.shape)
```

---

```python
# Graph Embedding (Conceptual GNN-style)
# Purpose: combine node features with graph structure to get node embeddings.

num_nodes = 5
node_feat = tf.random.normal((num_nodes, 8))
adj = tf.constant([
    [1, 1, 0, 0, 0],
    [1, 1, 1, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 1, 1, 1],
    [0, 0, 0, 1, 1],
], dtype=tf.float32)

# One message-passing step: aggregate neighbor features, then project
agg = tf.matmul(adj, node_feat)
node_emb = tf.keras.layers.Dense(8, activation='relu')(agg)
print('node_emb shape:', node_emb.shape)
```

---

```python
# Metric-Learning Embedding
# Purpose: shape embedding geometry so similar pairs are close and dissimilar pairs are far.

a = tf.random.normal((4, 16))
p = a + 0.05 * tf.random.normal((4, 16))      # positive samples near anchors
n = tf.random.normal((4, 16))                  # negatives sampled independently

# Triplet loss (toy): max(0, d(a,p) - d(a,n) + margin)
margin = 0.2
d_ap = tf.norm(a - p, axis=-1)
d_an = tf.norm(a - n, axis=-1)
triplet_loss = tf.reduce_mean(tf.nn.relu(d_ap - d_an + margin))
print('triplet_loss:', float(triplet_loss))
```

---

