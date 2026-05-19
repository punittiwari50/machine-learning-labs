# Mini Lab Exercises

## Mini Exercises (Lab Ready)

These short exercises are designed to be runnable and easy to modify.

What you get:
- Exercise 1: Text embedding retrieval (cosine similarity)
- Exercise 2: Image embedding retrieval with TensorFlow CNN
- Exercise 3: Tabular/user-item style embedding similarity

Tip: Run in order from Exercise 1 to Exercise 3.

---

```python
# Exercise 1: Text embedding retrieval (toy)
# Goal: see which query sentence is most similar to each candidate sentence.

import tensorflow as tf

sentences = tf.constant([
    "machine learning improves ranking",
    "deep learning for computer vision",
    "tokenization and embeddings for nlp",
    "image retrieval with feature vectors",
])

query = tf.constant(["embeddings for text search"])

# Build simple token ids
all_text = tf.concat([sentences, query], axis=0)
tokens = tf.strings.split(tf.strings.lower(all_text))
flat = tokens.flat_values
uniq, _ = tf.unique(flat)
vocab = tf.concat([tf.constant(["<PAD>", "<UNK>"]), uniq], axis=0)

vocab_table = tf.lookup.StaticVocabularyTable(
    tf.lookup.KeyValueTensorInitializer(vocab, tf.range(tf.shape(vocab)[0], dtype=tf.int64)),
    num_oov_buckets=1,
)

# Convert each sentence to mean pooled token embedding
embed_dim = 24
emb = tf.keras.layers.Embedding(input_dim=4096, output_dim=embed_dim)

def sentence_embed(text_batch):
    rag = tf.strings.split(tf.strings.lower(text_batch))
    dense = rag.to_tensor(default_value="<PAD>")
    dense_ids = vocab_table.lookup(dense)
    vecs = emb(dense_ids)

    # Mask out PAD tokens before averaging
    mask = tf.cast(tf.not_equal(dense, "<PAD>"), tf.float32)
    mask = tf.expand_dims(mask, axis=-1)
    summed = tf.reduce_sum(vecs * mask, axis=1)
    counts = tf.reduce_sum(mask, axis=1) + 1e-8
    return summed / counts

sent_vecs = tf.math.l2_normalize(sentence_embed(sentences), axis=-1)
query_vec = tf.math.l2_normalize(sentence_embed(query), axis=-1)

# Cosine similarity (query vs each sentence)
scores = tf.squeeze(tf.matmul(query_vec, sent_vecs, transpose_b=True), axis=0)
best_idx = tf.argmax(scores).numpy()

print("Query:", query.numpy()[0].decode())
for i, s in enumerate(sentences.numpy()):
    print(f"  cand[{i}] score={float(scores[i]):.4f} :: {s.decode()}")
print("Best match index:", best_idx)
print("Best match text:", sentences.numpy()[best_idx].decode())
```

---

```python
# Exercise 2: Image embedding retrieval (toy)
# Goal: embed a query image and find nearest image in a small gallery.

import tensorflow as tf

# Synthetic image gallery
gallery = tf.random.uniform((6, 64, 64, 3), 0.0, 1.0)
query_img = tf.random.uniform((1, 64, 64, 3), 0.0, 1.0)

# Small CNN encoder
img_encoder = tf.keras.Sequential([
    tf.keras.layers.Conv2D(16, 3, activation="relu"),
    tf.keras.layers.MaxPool2D(),
    tf.keras.layers.Conv2D(32, 3, activation="relu"),
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dense(48),
])

gallery_vec = tf.math.l2_normalize(img_encoder(gallery), axis=-1)
query_vec = tf.math.l2_normalize(img_encoder(query_img), axis=-1)

sim = tf.squeeze(tf.matmul(query_vec, gallery_vec, transpose_b=True), axis=0)
nearest = tf.argmax(sim).numpy()

print("Similarity scores:", [round(float(v), 4) for v in sim.numpy()])
print("Nearest gallery index:", nearest)

# Optional OpenCV descriptor check (if available)
try:
    import cv2
    import numpy as np
    gray = (gallery[nearest].numpy().mean(axis=-1) * 255).astype("uint8")
    if hasattr(cv2, "ORB_create"):
        orb = cv2.ORB_create()
        kps, desc = orb.detectAndCompute(gray, None)
        print("OpenCV ORB keypoints on nearest image:", len(kps))
        print("ORB descriptor shape:", None if desc is None else desc.shape)
except Exception as e:
    print("OpenCV descriptor block skipped:", str(e)[:120])
```

---

```python
# Exercise 3: Tabular embedding similarity (user-item style)
# Goal: combine categorical + numeric features into one embedding and compare users.

import tensorflow as tf

# Toy user batch (user_id bucket, country_id, numeric activity features)
user_id = tf.constant([1, 2, 3, 4, 5], dtype=tf.int32)
country_id = tf.constant([2, 1, 2, 3, 1], dtype=tf.int32)
activity = tf.constant([
    [0.2, 1.5, 0.1],
    [0.4, 1.1, 0.3],
    [1.2, 0.1, 0.7],
    [1.0, 0.2, 0.8],
    [0.3, 1.4, 0.2],
], dtype=tf.float32)

user_emb = tf.keras.layers.Embedding(input_dim=100, output_dim=8)(user_id)
country_emb = tf.keras.layers.Embedding(input_dim=10, output_dim=4)(country_id)
num_proj = tf.keras.layers.Dense(8, activation="relu")(activity)

combined = tf.concat([user_emb, country_emb, num_proj], axis=-1)
combined = tf.math.l2_normalize(combined, axis=-1)

# Pairwise similarity matrix among users
sim_matrix = tf.matmul(combined, combined, transpose_b=True)
print("User-user similarity matrix shape:", sim_matrix.shape)
print(tf.round(sim_matrix * 1000) / 1000)

# Find nearest neighbor for user 0 (excluding self)
scores_u0 = sim_matrix[0]
scores_u0 = tf.tensor_scatter_nd_update(scores_u0, indices=[[0]], updates=[-1.0])
nn_idx = tf.argmax(scores_u0).numpy()
print("Nearest neighbor for user[0] is user[{}]".format(nn_idx))
```

---

