# C ? Per-Type: Image Embedding Subtypes

```python
# C6) Image CNN Feature Embedding
# Purpose: encode full image semantics into a compact vector.

img_batch = tf.random.uniform((2, 64, 64, 3))
img_vec = tf.keras.Sequential([
    tf.keras.layers.Conv2D(16, 3, activation='relu'),
    tf.keras.layers.MaxPool2D(),
    tf.keras.layers.Conv2D(32, 3, activation='relu'),
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dense(24),
])(img_batch)
print('cnn image embedding shape:', img_vec.shape)
```

---

```python
# C7) Image Patch Embedding
# Purpose: represent local image patches as vectors (ViT-style building block).

img = tf.random.uniform((1, 32, 32, 3))
# Conv with stride=patch size acts as patch projector
patch_proj = tf.keras.layers.Conv2D(filters=16, kernel_size=8, strides=8)(img)
# Flatten spatial grid to sequence of patch vectors
patch_seq = tf.reshape(patch_proj, (1, -1, 16))
print('patch sequence shape:', patch_seq.shape)
```

---

```python
# C8) Image Keypoint Descriptor Embedding (OpenCV ORB)
# Purpose: encode local keypoints for matching/retrieval.

if OPENCV_AVAILABLE:
    rnd = (np.random.rand(128, 128) * 255).astype(np.uint8)
    orb_local = cv2.ORB_create()
    kp, des = orb_local.detectAndCompute(rnd, None)
    print('num keypoints:', len(kp))
    print('descriptor shape:', None if des is None else des.shape)
else:
    print('OpenCV not available')
```

---

```python
# C9) Image Region Embedding (ROI)
# Purpose: embed a selected region-of-interest rather than full image.

full_img = tf.random.uniform((1, 64, 64, 3))
roi = full_img[:, 16:48, 16:48, :]  # center crop as ROI
roi_vec = tf.keras.Sequential([
    tf.keras.layers.Conv2D(16, 3, activation='relu'),
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dense(12),
])(roi)
print('roi embedding shape:', roi_vec.shape)
```

---

