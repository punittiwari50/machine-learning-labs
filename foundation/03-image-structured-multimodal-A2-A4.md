# A2?A4 Image / Structured / Multi-Modal

### A2. Image Embeddings

| Subtype | Purpose | Typical Tools |
|---|---|---|
| CNN feature embeddings | Compact semantic image features for classification/retrieval | TensorFlow CNN backbones |
| Patch embeddings | Represent local patches (e.g., ViT style) | TensorFlow Conv/Dense patch projectors |
| Keypoint descriptor embeddings | Match local regions across images | OpenCV SIFT/ORB descriptors |
| Region embeddings | Encode object/ROI level features | OpenCV ROI + TF encoder |

---

```python
# Example: global image embedding with a tiny CNN in TensorFlow
images = tf.random.uniform(shape=(4, 64, 64, 3), minval=0.0, maxval=1.0)

cnn_embedder = tf.keras.Sequential([
    tf.keras.layers.Conv2D(16, 3, activation='relu'),
    tf.keras.layers.MaxPool2D(),
    tf.keras.layers.Conv2D(32, 3, activation='relu'),
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dense(64)  # final image embedding size
])

image_embeddings = cnn_embedder(images)
print('Image embedding shape:', image_embeddings.shape)

# Optional OpenCV local descriptor example
if OPENCV_AVAILABLE:
    # Create a synthetic grayscale image for feature extraction demo
    img = (np.random.rand(128, 128) * 255).astype(np.uint8)

    if hasattr(cv2, 'ORB_create'):
        orb = cv2.ORB_create()
        keypoints, descriptors = orb.detectAndCompute(img, None)
        desc_shape = None if descriptors is None else descriptors.shape
        print('ORB keypoints:', len(keypoints), '| descriptor shape:', desc_shape)
    else:
        print('ORB not available in this OpenCV build.')
```

---

**Do (Image Embeddings):**
- Keep preprocessing identical for training/inference (resize, color conversion, normalization).
- Use data augmentation for robust embeddings.
- L2-normalize embeddings for cosine-based retrieval systems.

**Don't (Image Embeddings):**
- Do not compare embeddings from differently preprocessed pipelines.
- Do not evaluate only top-1 accuracy if your goal is retrieval quality.

**Tips and Tricks:**
- Start from pretrained backbones and fine-tune.
- For low-latency search, use smaller dimensions with metric-learning loss.
- In OpenCV pipelines, ORB is faster while SIFT is often more robust.

**Summary:** Image embeddings transform pixels or local descriptors into vectors suitable for semantic matching and downstream vision tasks.

**Application Use Cases:** visual similarity search, product matching, face/person retrieval, industrial defect lookup.

---

### A3. Structured Data Embeddings (Categorical, Numerical, Time)

| Subtype | Purpose | Typical Tools |
|---|---|---|
| Categorical embeddings | Replace one-hot with dense vectors for high-cardinality features | TensorFlow Embedding layer |
| Numerical projection embeddings | Project normalized continuous features to latent space | Dense projection layers |
| Time-series embeddings | Represent windows/temporal patterns compactly | 1D CNN/RNN/Transformer in TF |

---

```python
# Example: categorical + numerical embeddings for tabular ML
batch_size = 5

# Two categorical features (e.g., user_id_bucket, country_id)
cat1 = tf.constant([1, 3, 2, 5, 4], dtype=tf.int32)
cat2 = tf.constant([2, 2, 1, 3, 4], dtype=tf.int32)

# Numerical features
num = tf.random.normal((batch_size, 3))

cat_emb1 = tf.keras.layers.Embedding(input_dim=100, output_dim=8)(cat1)
cat_emb2 = tf.keras.layers.Embedding(input_dim=20, output_dim=4)(cat2)
num_proj = tf.keras.layers.Dense(8, activation='relu')(num)

# Concatenate into one unified embedding vector
final_tabular_embedding = tf.concat([cat_emb1, cat_emb2, num_proj], axis=-1)
print('Tabular embedding shape:', final_tabular_embedding.shape)
```

---

**Do (Structured Embeddings):**
- Handle unseen category ids with OOV buckets.
- Normalize numerical features before projection.
- For time series, align windowing and forecasting horizon correctly.

**Don't (Structured Embeddings):**
- Do not leak future information in temporal features.
- Do not use huge embedding dimensions for low-cardinality features.

**Tips and Tricks:**
- Rule-of-thumb for categorical dim: min(50, round(cardinality^0.25)).
- Share embeddings for semantically related categorical fields when valid.

**Summary:** Structured embeddings let mixed feature types live in one latent space, improving model capacity and memory efficiency.

**Application Use Cases:** recommender systems, churn prediction, fraud detection, demand forecasting.

---

### A4. Multi-Modal Embeddings

| Subtype | Purpose | Typical Tools |
|---|---|---|
| Text-Image joint embeddings | Place text and images in one semantic space | TF dual-encoders + OpenCV preprocessing |
| Sensor-image-text fusion embeddings | Unified representation from multiple data channels | TF feature fusion networks |

---

```python
# Example: simple dual-encoder style fusion (toy)
text_vec = tf.random.normal((4, 64))   # pretend this came from a text encoder
img_vec = tf.random.normal((4, 64))    # pretend this came from an image encoder

# Project both to the same space and normalize for cosine similarity
proj = tf.keras.layers.Dense(32)
text_proj = tf.math.l2_normalize(proj(text_vec), axis=-1)
img_proj = tf.math.l2_normalize(proj(img_vec), axis=-1)

# Similarity matrix between text and images
similarity = tf.linalg.matmul(text_proj, img_proj, transpose_b=True)
print('Similarity matrix shape:', similarity.shape)
```

---

**Do (Multi-Modal Embeddings):**
- Align training pairs carefully (text-image pairing quality matters).
- Use temperature scaling in contrastive objectives.
- Evaluate both retrieval directions (text->image and image->text).

**Don't (Multi-Modal Embeddings):**
- Do not rely only on one modality at inference if both are expected.
- Do not ignore modality-specific normalization/preprocessing.

**Tips and Tricks:**
- Hard-negative mining usually improves retrieval quality.
- Batch size strongly impacts contrastive learning stability.

**Summary:** Multi-modal embeddings create a shared semantic geometry across heterogeneous inputs.

**Application Use Cases:** text-image search, visual question retrieval, product catalog matching with image and description.

---

