# D ? Image & Video Embedding Deep Dive

## D) Image & Video Embedding Types — One Cell Per Subtype

Each cell below is fully standalone (imports included).

### Image Embedding Subtypes
| Subtype | What it encodes | Key use case |
|---|---|---|
| CNN Global Feature | Full image semantics | Classification, retrieval |
| HOG Descriptor | Edge/gradient structure | Pedestrian detection, OCR |
| Color Histogram | Pixel color distribution | Image deduplication, scene matching |
| ORB / BoW Visual Word | Local keypoint occurrences | Document/logo matching |
| Spatial Pyramid Pooling | Spatial layout + semantics | Fine-grained recognition |
| Attention-Weighted Image | Salient region emphasis | VQA, captioning, e-commerce |

### Video Embedding Subtypes
| Subtype | What it encodes | Key use case |
|---|---|---|
| Frame-Level (CNN per frame) | Static appearance per frame | Scene classification |
| Temporal (3D CNN) | Short-range spatio-temporal patterns | Action recognition |
| LSTM over CNN Frames | Long-range temporal dependencies | Activity/event classification |
| Optical Flow (OpenCV + TF) | Motion between consecutive frames | Motion classification, anomaly |
| Frame Difference | Coarse motion signal | Change detection, surveillance |

---

```python
# IMAGE EMBEDDING TYPE 1: CNN Global Feature Embedding
# -------------------------------------------------------
# Purpose : Summarise full-image semantics into one dense vector using
#           stacked convolutions + global pooling.
# Use case: Image retrieval, product similarity search, face verification.

import tensorflow as tf

# Simulate a small batch of RGB images (4 images, 64x64)
images = tf.random.uniform(shape=(4, 64, 64, 3), minval=0.0, maxval=1.0)

# Build a compact CNN encoder
cnn_encoder = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, 3, activation='relu', padding='same'),
    tf.keras.layers.MaxPool2D(2),
    tf.keras.layers.Conv2D(64, 3, activation='relu', padding='same'),
    tf.keras.layers.MaxPool2D(2),
    tf.keras.layers.Conv2D(64, 3, activation='relu', padding='same'),
    tf.keras.layers.GlobalAveragePooling2D(),   # collapses (H, W) -> one vector
    tf.keras.layers.Dense(64),                  # final embedding size
])

embeddings = cnn_encoder(images)
# L2-normalise so cosine similarity == dot product
embeddings = tf.math.l2_normalize(embeddings, axis=-1)
print("CNN global embedding shape:", embeddings.shape)   # (4, 64)
# Pairwise cosine similarity matrix (useful for retrieval evaluation)
sim = tf.matmul(embeddings, embeddings, transpose_b=True)
print("Similarity matrix shape:", sim.shape)             # (4, 4)
```

---

```python
# IMAGE EMBEDDING TYPE 2: HOG (Histogram of Oriented Gradients) Descriptor
# -------------------------------------------------------------------------
# Purpose : Encode local edge/gradient structure of an image as a histogram
#           vector. Captures shape without colour.
# Use case: Pedestrian detection, OCR pre-processing, object detection.

import cv2
import numpy as np
import tensorflow as tf

def hog_embed(images_np: np.ndarray, cell=(8, 8), block=(2, 2), nbins=9) -> np.ndarray:
    """Compute HOG descriptor for each grayscale image in the batch.
    Returns an array of shape (batch, descriptor_dim)."""
    win_size = (images_np.shape[2], images_np.shape[1])  # (W, H)
    hog = cv2.HOGDescriptor(
        win_size,
        (block[0] * cell[0], block[1] * cell[1]),  # blockSize
        (cell[0], cell[1]),                          # blockStride (one cell)
        (cell[0], cell[1]),                          # cellSize
        nbins,
    )
    results = []
    for img in images_np:
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY) if img.ndim == 3 else img
        desc = hog.compute(gray)
        results.append(desc.flatten())
    return np.array(results, dtype=np.float32)

# Create synthetic RGB images (4 images, 64x64)
imgs_np = (np.random.rand(4, 64, 64, 3) * 255).astype(np.uint8)
hog_vecs = hog_embed(imgs_np)
print("HOG descriptor shape:", hog_vecs.shape)   # (4, descriptor_dim)

# Optionally project to smaller embedding for a neural model
hog_t = tf.constant(hog_vecs)
hog_emb = tf.keras.layers.Dense(32, activation='relu')(hog_t)
print("HOG projected embedding:", hog_emb.shape)  # (4, 32)
```

---

```python
# IMAGE EMBEDDING TYPE 3: Color Histogram Embedding
# --------------------------------------------------
# Purpose : Represent pixel colour distribution as a histogram vector.
#           Fast, lightweight, no training needed.
# Use case: Image deduplication, scene-type matching, thumbnail comparison.

import cv2
import numpy as np
import tensorflow as tf

def color_hist_embed(images_np: np.ndarray, bins: int = 32) -> np.ndarray:
    """Compute a per-channel colour histogram and concatenate them."""
    results = []
    for img in images_np:
        channels = []
        for ch in range(img.shape[-1]):  # iterate R, G, B channels
            hist = cv2.calcHist([img], [ch], None, [bins], [0, 256])
            hist = cv2.normalize(hist, hist).flatten()
            channels.append(hist)
        results.append(np.concatenate(channels))
    return np.array(results, dtype=np.float32)

imgs_np = (np.random.rand(4, 64, 64, 3) * 255).astype(np.uint8)
hist_vecs = color_hist_embed(imgs_np, bins=32)
print("Color histogram shape:", hist_vecs.shape)  # (4, 96) = 3 x 32

# Optionally project to a smaller latent vector
hist_t = tf.constant(hist_vecs)
hist_emb = tf.keras.layers.Dense(24, activation='relu')(hist_t)
print("Color hist projected embedding:", hist_emb.shape)
```

---

```python
# IMAGE EMBEDDING TYPE 4: ORB Bag-of-Visual-Words Embedding
# ----------------------------------------------------------
# Purpose : Encode the frequency of visual "words" (quantised local keypoint
#           descriptors) as a fixed-length histogram. Translation-invariant.
# Use case: Logo/document retrieval, near-duplicate detection.

import cv2
import numpy as np
import tensorflow as tf

def orb_bow_embed(images_np: np.ndarray, vocab_size: int = 64) -> np.ndarray:
    """ORB descriptors -> mini bag-of-words via random codebook.
    In production replace the random codebook with a k-means codebook."""
    orb = cv2.ORB_create(nfeatures=200)
    rng = np.random.default_rng(42)

    # Build a random codebook (stand-in for a real k-means codebook)
    codebook = rng.standard_normal((vocab_size, 32)).astype(np.float32)

    results = []
    for img in images_np:
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        _, des = orb.detectAndCompute(gray, None)
        bow = np.zeros(vocab_size, dtype=np.float32)
        if des is not None:
            des_f = des.astype(np.float32)
            # Assign each descriptor to the nearest codebook word
            dists = np.linalg.norm(
                des_f[:, None, :] - codebook[None, :, :], axis=-1
            )  # (n_kp, vocab_size)
            words = np.argmin(dists, axis=-1)
            for w in words:
                bow[w] += 1
            bow /= (bow.sum() + 1e-8)  # normalise to frequency
        results.append(bow)
    return np.array(results, dtype=np.float32)

imgs_np = (np.random.rand(4, 64, 64, 3) * 255).astype(np.uint8)
bow_vecs = orb_bow_embed(imgs_np)
print("BoW embedding shape:", bow_vecs.shape)      # (4, 64)

# Project to a smaller latent space
bow_t = tf.constant(bow_vecs)
bow_emb = tf.keras.layers.Dense(16, activation='relu')(bow_t)
print("BoW projected embedding:", bow_emb.shape)
```

---

```python
# IMAGE EMBEDDING TYPE 5: Spatial Pyramid Pooling (SPP) Embedding
# ----------------------------------------------------------------
# Purpose : Pool features at multiple spatial scales so the embedding
#           captures both global layout and fine-grained local structure.
# Use case: Fine-grained recognition (car model, bird species), multi-scale retrieval.

import tensorflow as tf

images = tf.random.uniform(shape=(3, 64, 64, 3))

# Shared CNN backbone — produces a feature map
backbone = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, 3, activation='relu', padding='same'),
    tf.keras.layers.MaxPool2D(2),
    tf.keras.layers.Conv2D(64, 3, activation='relu', padding='same'),
])
feat_map = backbone(images)  # (3, 32, 32, 64)

# SPP: pool at 3 scales (1x1, 2x2, 4x4) and concatenate
def spp_pool(feat, levels=(1, 2, 4)):
    parts = []
    for l in levels:
        # AdaptiveAvgPool approximation via strided average pooling
        pooled = tf.keras.layers.AveragePooling2D(
            pool_size=(feat.shape[1] // l, feat.shape[2] // l),
            strides=(feat.shape[1] // l, feat.shape[2] // l),
        )(feat)
        parts.append(tf.reshape(pooled, (tf.shape(pooled)[0], -1)))
    return tf.concat(parts, axis=-1)

spp_vec = spp_pool(feat_map)
print("SPP vector shape:", spp_vec.shape)     # (3, 64*(1+4+16))=1344

# Final projection to fixed embedding size
spp_emb = tf.keras.layers.Dense(64)(spp_vec)
print("SPP embedding shape:", spp_emb.shape)  # (3, 64)
```

---

```python
# IMAGE EMBEDDING TYPE 6: Attention-Weighted Image Embedding
# -----------------------------------------------------------
# Purpose : Apply spatial self-attention to a CNN feature map so the
#           embedding emphasises salient regions rather than averaging uniformly.
# Use case: Visual question answering, product attribute focus, captioning support.

import tensorflow as tf

images = tf.random.uniform(shape=(3, 64, 64, 3))

# CNN backbone producing spatial feature map
backbone = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, 3, activation='relu', padding='same'),
    tf.keras.layers.MaxPool2D(2),
    tf.keras.layers.Conv2D(32, 3, activation='relu', padding='same'),
])
feat_map = backbone(images)                         # (3, 32, 32, 32)
B, H, W, C = tf.shape(feat_map)[0], 32, 32, 32

# Flatten spatial dims -> sequence of (H*W) position vectors
seq = tf.reshape(feat_map, (B, H * W, C))          # (3, 1024, 32)

# Attention score per spatial position
attn_scores = tf.keras.layers.Dense(1)(seq)         # (3, 1024, 1)
attn_weights = tf.nn.softmax(attn_scores, axis=1)   # normalise over positions

# Weighted sum: focus on attended regions
attended = tf.reduce_sum(seq * attn_weights, axis=1)  # (3, 32)

# Final projection
attn_emb = tf.keras.layers.Dense(24)(attended)
print("Attention-weighted embedding shape:", attn_emb.shape)  # (3, 24)
```

---

### Video Embedding Subtypes

---

```python
# VIDEO EMBEDDING TYPE 1: Frame-Level CNN Embedding + Mean Pooling
# -----------------------------------------------------------------
# Purpose : Extract a CNN feature per video frame, then average across time
#           to produce a single clip embedding. Simple and fast.
# Use case: Scene-type classification, short clip retrieval.

import tensorflow as tf

# Simulate a mini-batch of 2 video clips, each with 8 frames of 32x32 RGB
# In production these would be actual decoded video frames.
videos = tf.random.uniform(shape=(2, 8, 32, 32, 3))

# A shared CNN frame encoder — weights are shared across all time steps
frame_encoder = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, 3, activation='relu', padding='same'),
    tf.keras.layers.MaxPool2D(2),
    tf.keras.layers.GlobalAveragePooling2D(),   # (H, W, C) -> (C,) per frame
    tf.keras.layers.Dense(64, activation='relu'),
])

# Apply the frame encoder independently to each of the 8 frames
# TimeDistributed wraps any layer to run it per time-step
td_encoder = tf.keras.layers.TimeDistributed(frame_encoder)
frame_embs = td_encoder(videos)               # (2, 8, 64)

# Temporal mean pooling: collapse 8 frame embeddings -> 1 clip embedding
clip_emb = tf.reduce_mean(frame_embs, axis=1)  # (2, 64)
clip_emb = tf.math.l2_normalize(clip_emb, axis=-1)
print("Frame-level CNN clip embedding shape:", clip_emb.shape)  # (2, 64)
```

---

```python
# VIDEO EMBEDDING TYPE 2: 3D CNN (C3D-style) Spatio-Temporal Embedding
# ----------------------------------------------------------------------
# Purpose : Apply 3-D convolutions across (T, H, W) to jointly model
#           spatial appearance and short-range temporal patterns in one pass.
# Use case: Action recognition, gesture detection, sport highlight detection.

import tensorflow as tf

# Simulate a mini-batch: 2 clips, 8 frames, 32x32 RGB
clips = tf.random.uniform(shape=(2, 8, 32, 32, 3))

# 3-D convolution: kernel spans time (t), height (h), width (w)
c3d_net = tf.keras.Sequential([
    # First 3D conv block — captures short-range motion (e.g. 3-frame window)
    tf.keras.layers.Conv3D(16, kernel_size=(3, 3, 3), activation='relu', padding='same'),
    tf.keras.layers.MaxPool3D(pool_size=(1, 2, 2)),   # only halve spatial, keep time
    # Second 3D conv block — larger receptive field over time
    tf.keras.layers.Conv3D(32, kernel_size=(3, 3, 3), activation='relu', padding='same'),
    tf.keras.layers.MaxPool3D(pool_size=(2, 2, 2)),   # halve both spatial and temporal
    # Collapse all dimensions to a fixed embedding
    tf.keras.layers.GlobalAveragePooling3D(),
    tf.keras.layers.Dense(64, activation='relu'),     # (batch, 64)
])

clip_emb = c3d_net(clips)
print("3D-CNN clip embedding shape:", clip_emb.shape)  # (2, 64)
```

---

```python
# VIDEO EMBEDDING TYPE 3: LSTM over CNN Frame Embeddings
# -------------------------------------------------------
# Purpose : Run a recurrent (LSTM) layer over the sequence of per-frame CNN
#           embeddings so the model can track long-range temporal dependencies.
# Use case: Activity/event classification, video-level sentiment, sport analysis.

import tensorflow as tf

# Simulate 2 clips, 12 frames each, 32x32 RGB
videos = tf.random.uniform(shape=(2, 12, 32, 32, 3))

# Step 1: shared CNN encodes each frame to a 64-d vector
frame_cnn = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, 3, activation='relu', padding='same'),
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dense(64, activation='relu'),
])
# TimeDistributed applies the CNN to every time-step independently
frame_seq = tf.keras.layers.TimeDistributed(frame_cnn)(videos)  # (2, 12, 64)

# Step 2: LSTM reads the frame sequence and summarises it
# return_sequences=False => only the final hidden state is output
lstm_emb = tf.keras.layers.LSTM(48, return_sequences=False)(frame_seq)  # (2, 48)
# Bidirectional LSTM is also common — it reads forward and backward:
# lstm_emb = tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(48))(frame_seq)

lstm_emb = tf.math.l2_normalize(lstm_emb, axis=-1)
print("LSTM video embedding shape:", lstm_emb.shape)  # (2, 48)
```

---

```python
# VIDEO EMBEDDING TYPE 4: Optical Flow Embedding (OpenCV + TF Dense Projection)
# -------------------------------------------------------------------------------
# Purpose : Compute dense per-pixel motion vectors (optical flow) between
#           consecutive frames, then project them into a latent embedding.
#           Captures how pixels move — pure motion, no appearance bias.
# Use case: Action recognition (tennis swing vs. golf swing), anomaly detection,
#           robotics visual odometry.

import cv2
import numpy as np
import tensorflow as tf

def compute_flow_batch(frames_np: np.ndarray) -> np.ndarray:
    """Compute Farneback dense optical flow between consecutive frames.
    frames_np: (T, H, W, 3) uint8 for a single clip.
    Returns mean flow magnitude per consecutive pair, shape (T-1, H*W).
    """
    flows = []
    for t in range(len(frames_np) - 1):
        prev = cv2.cvtColor(frames_np[t], cv2.COLOR_RGB2GRAY)
        nxt  = cv2.cvtColor(frames_np[t + 1], cv2.COLOR_RGB2GRAY)
        flow = cv2.calcOpticalFlowFarneback(
            prev, nxt, None,
            pyr_scale=0.5, levels=3, winsize=15, iterations=3,
            poly_n=5, poly_sigma=1.2, flags=0,
        )  # (H, W, 2): dx, dy per pixel
        mag = np.sqrt(flow[..., 0] ** 2 + flow[..., 1] ** 2).flatten()
        flows.append(mag)
    return np.array(flows, dtype=np.float32)  # (T-1, H*W)

# Simulate 4 video clips with 5 frames each
T, H, W = 5, 32, 32
clips_np = [(np.random.rand(T, H, W, 3) * 255).astype(np.uint8) for _ in range(4)]

all_flow_vecs = []
for clip in clips_np:
    flow_seq = compute_flow_batch(clip)           # (T-1, H*W)
    # Aggregate: mean over temporal pairs -> (H*W,) per clip
    clip_flow = flow_seq.mean(axis=0)
    all_flow_vecs.append(clip_flow)

flow_batch = tf.constant(np.array(all_flow_vecs))  # (4, H*W)
print("Raw flow vector shape:", flow_batch.shape)    # (4, 1024)

# Project into a compact embedding
flow_emb = tf.keras.layers.Dense(48, activation='relu')(flow_batch)
print("Optical flow embedding shape:", flow_emb.shape)  # (4, 48)
```

---

```python
# VIDEO EMBEDDING TYPE 5: Frame Difference (Temporal Gradient) Embedding
# -----------------------------------------------------------------------
# Purpose : Compute pixel-wise absolute difference between consecutive frames.
#           Lightweight motion signal — no optical flow solver required.
# Use case: Change/anomaly detection, surveillance (motion trigger),
#           fast pre-filter before a heavier model.

import numpy as np
import tensorflow as tf

# Simulate 4 clips, 6 frames each, 32x32 greyscale
T, H, W = 6, 32, 32
clips_np = np.random.rand(4, T, H, W, 1).astype(np.float32)

# Frame difference: |frame[t+1] - frame[t]| for each consecutive pair
diff = np.abs(clips_np[:, 1:, :, :, :] - clips_np[:, :-1, :, :, :])
# diff shape: (4, T-1, H, W, 1)

# Aggregate motion energy: mean over time and space -> (4, 1) per clip
motion_energy = diff.mean(axis=(1, 2, 3, 4), keepdims=True)  # (4, 1)

# Flatten each difference frame to a vector, then pool
diff_flat = diff.reshape(4, T - 1, H * W)               # (4, T-1, H*W)
diff_mean = diff_flat.mean(axis=1)                        # (4, H*W)

diff_t = tf.constant(diff_mean)
# Project to compact embedding
diff_emb = tf.keras.layers.Dense(32, activation='relu')(diff_t)
print("Frame difference embedding shape:", diff_emb.shape)   # (4, 32)
print("Mean motion energy per clip:", motion_energy.squeeze().tolist())
```

---

