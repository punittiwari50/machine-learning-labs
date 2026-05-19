# C ? Per-Type: Structured & Multi-Modal

```python
# C10) Structured Categorical Embedding
# Purpose: replace sparse one-hot categorical features with dense vectors.

cat_ids = tf.constant([1, 5, 2, 7], dtype=tf.int32)
cat_vec = tf.keras.layers.Embedding(input_dim=100, output_dim=8)(cat_ids)
print('categorical embedding shape:', cat_vec.shape)
```

---

```python
# C11) Structured Numerical Projection Embedding
# Purpose: project normalized continuous features into latent space.

num_feat = tf.random.normal((4, 5))
num_vec = tf.keras.layers.Dense(8, activation='relu')(num_feat)
print('numerical projection shape:', num_vec.shape)
```

---

```python
# C12) Time-Series Embedding
# Purpose: encode temporal windows into fixed-size vectors.

ts = tf.random.normal((3, 20, 4))  # batch, time, features
ts_vec = tf.keras.Sequential([
    tf.keras.layers.Conv1D(16, 3, activation='relu'),
    tf.keras.layers.GlobalAveragePooling1D(),
    tf.keras.layers.Dense(10),
])(ts)
print('time-series embedding shape:', ts_vec.shape)
```

---

```python
# C13) Multi-Modal Text-Image Joint Embedding
# Purpose: place text and image into the same vector space.

t_vec = tf.random.normal((3, 16))
i_vec = tf.random.normal((3, 16))
proj_layer = tf.keras.layers.Dense(12)
t_joint = tf.math.l2_normalize(proj_layer(t_vec), axis=-1)
i_joint = tf.math.l2_normalize(proj_layer(i_vec), axis=-1)
sim_joint = tf.matmul(t_joint, i_joint, transpose_b=True)
print('joint similarity matrix shape:', sim_joint.shape)
```

---

```python
# C14) Multi-Modal Sensor-Image-Text Fusion Embedding
# Purpose: fuse multiple modality vectors into one representation.

sensor_vec = tf.random.normal((3, 6))
text_vec = tf.random.normal((3, 10))
image_vec = tf.random.normal((3, 12))

fusion_input = tf.concat([sensor_vec, text_vec, image_vec], axis=-1)
fusion_out = tf.keras.layers.Dense(16, activation='relu')(fusion_input)
print('sensor-image-text fusion shape:', fusion_out.shape)
```

---

