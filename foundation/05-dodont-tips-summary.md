# Do & Don't / Tips / Summary

### Do and Don't by Architecture

**Lookup-table embeddings**
- Do: regularize (L2/dropout) and reserve OOV/PAD ids.
- Don't: oversize dimensions for tiny vocabularies.

**CNN embeddings**
- Do: tune kernel sizes for local pattern scales.
- Don't: ignore stride/padding effects on detail loss.

**RNN/LSTM embeddings**
- Do: use masking and consider bidirectional encoders.
- Don't: expect best long-context performance vs transformers.

**Transformer embeddings**
- Do: use proper positional encoding and attention masks.
- Don't: train from scratch on tiny datasets without transfer learning.

**Autoencoder embeddings**
- Do: validate latent space utility for downstream task, not only reconstruction loss.
- Don't: assume perfect recon implies best discriminative embedding.

**Metric-learning embeddings**
- Do: use hard/semi-hard negatives carefully.
- Don't: evaluate with classification accuracy alone; use retrieval metrics too.

**Hybrid/fusion embeddings**
- Do: calibrate each encoder scale before fusion.
- Don't: concatenate many noisy features without selection.

---

### Tips and Tricks (Global)

1. Normalize vectors when distance-based retrieval is the objective.
2. Keep a simple baseline embedding model before adding complexity.
3. Watch for train/serve skew in tokenization and image preprocessing.
4. Use ANN indexes (FAISS/ScaNN style) for large-scale embedding retrieval.
5. Track drift by monitoring nearest-neighbor quality over time.
6. Evaluate embeddings with both intrinsic and task metrics:
   - Intrinsic: cosine neighborhood quality, clustering silhouette
   - Task: recall@k, MRR, NDCG, downstream F1/AUC

---

## Final Summary

- **Modality grouping** helps decide *what unit* should be embedded (text token, image region, category id, multimodal pair).
- **Architecture grouping** helps decide *how* embeddings are learned (lookup, CNN, RNN, transformer, autoencoder, metric learning, fusion).
- In production, the highest impact comes from:
  - strict preprocessing consistency,
  - correct objective/loss for the use case,
  - robust evaluation beyond a single metric,
  - and stable serving-time vector normalization + indexing.

---

