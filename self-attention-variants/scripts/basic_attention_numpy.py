from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from shared_text_preprocessing import PreprocessingConfig, prepare_text_data


@dataclass(frozen=True)
class ExperimentConfig:
    d_model: int = 32
    num_heads: int = 4
    local_window: int = 4
    learning_rate: float = 0.2
    epochs: int = 120
    seed: int = 42


def build_embeddings(
    token_ids: np.ndarray,
    vocab_size: int,
    d_model: int,
    rng: np.random.Generator,
) -> np.ndarray:
    emb_table = rng.normal(0.0, 0.2, (vocab_size, d_model)).astype(np.float32)
    return emb_table[token_ids]


def project_qkv(
    x: np.ndarray,
    d_model: int,
    rng: np.random.Generator,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    w_q = rng.normal(0.0, 0.2, (d_model, d_model)).astype(np.float32)
    w_k = rng.normal(0.0, 0.2, (d_model, d_model)).astype(np.float32)
    w_v = rng.normal(0.0, 0.2, (d_model, d_model)).astype(np.float32)
    return x @ w_q, x @ w_k, x @ w_v


def softmax(x: np.ndarray, axis: int = -1) -> np.ndarray:
    z = x - x.max(axis=axis, keepdims=True)
    exp_z = np.exp(z)
    return exp_z / exp_z.sum(axis=axis, keepdims=True)


def scaled_dot_product_attention(
    q: np.ndarray,
    k: np.ndarray,
    v: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    scores = (q @ np.swapaxes(k, -1, -2)) / math.sqrt(q.shape[-1])
    weights = softmax(scores, axis=-1)
    output = weights @ v
    return output, weights


def multi_head_attention(
    q: np.ndarray,
    k: np.ndarray,
    v: np.ndarray,
    num_heads: int,
) -> tuple[np.ndarray, np.ndarray]:
    batch, seq_len, d_model = q.shape
    if d_model % num_heads != 0:
        raise ValueError(
            f"d_model ({d_model}) must be divisible by num_heads ({num_heads})."
        )

    head_dim = d_model // num_heads
    qh = q.reshape(batch, seq_len, num_heads, head_dim).transpose(0, 2, 1, 3)
    kh = k.reshape(batch, seq_len, num_heads, head_dim).transpose(0, 2, 1, 3)
    vh = v.reshape(batch, seq_len, num_heads, head_dim).transpose(0, 2, 1, 3)

    outputs: list[np.ndarray] = []
    weights_all: list[np.ndarray] = []
    for head in range(num_heads):
        out_h, w_h = scaled_dot_product_attention(qh[:, head], kh[:, head], vh[:, head])
        outputs.append(out_h)
        weights_all.append(w_h)

    out = (
        np.stack(outputs, axis=1).transpose(0, 2, 1, 3).reshape(batch, seq_len, d_model)
    )
    weights = np.stack(weights_all, axis=1)
    return out, weights


def pooled_features(attn_out: np.ndarray) -> np.ndarray:
    return attn_out.mean(axis=1)


def train_binary_head(
    x_feat_train: np.ndarray,
    y_train: np.ndarray,
    learning_rate: float,
    epochs: int,
) -> tuple[np.ndarray, np.ndarray]:
    w = np.zeros((x_feat_train.shape[1], 1), dtype=np.float32)
    b = np.zeros((1,), dtype=np.float32)
    y_train_f = y_train.astype(np.float32).reshape(-1, 1)

    for _ in range(epochs):
        logits = x_feat_train @ w + b
        probs = 1.0 / (1.0 + np.exp(-logits))
        error = probs - y_train_f
        grad_w = (x_feat_train.T @ error) / x_feat_train.shape[0]
        grad_b = error.mean(axis=0)
        w -= learning_rate * grad_w
        b -= learning_rate * grad_b

    return w, b


def evaluate_binary_classifier(
    x_feat: np.ndarray,
    y_true: np.ndarray,
    w: np.ndarray,
    b: np.ndarray,
) -> dict[str, float]:
    logits = x_feat @ w + b
    probs = 1.0 / (1.0 + np.exp(-logits))
    preds = (probs >= 0.5).astype(np.int64).reshape(-1)
    accuracy = float((preds == y_true).mean())
    return {"accuracy": accuracy}


def run_pipeline() -> dict[str, float]:
    exp_cfg = ExperimentConfig()
    prep_cfg = PreprocessingConfig(num_samples=256, seq_len=24)
    rng = np.random.default_rng(exp_cfg.seed)

    data = prepare_text_data(prep_cfg, seed=exp_cfg.seed)

    x_train = build_embeddings(
        data.train_token_ids, len(data.vocab), exp_cfg.d_model, rng
    )
    x_test = build_embeddings(
        data.test_token_ids, len(data.vocab), exp_cfg.d_model, rng
    )

    q_train, k_train, v_train = project_qkv(x_train, exp_cfg.d_model, rng)
    q_test, k_test, v_test = project_qkv(x_test, exp_cfg.d_model, rng)

    attn_train, _ = multi_head_attention(q_train, k_train, v_train, exp_cfg.num_heads)
    attn_test, _ = multi_head_attention(q_test, k_test, v_test, exp_cfg.num_heads)

    x_feat_train = pooled_features(attn_train)
    x_feat_test = pooled_features(attn_test)

    w, b = train_binary_head(
        x_feat_train,
        data.y_train,
        exp_cfg.learning_rate,
        exp_cfg.epochs,
    )
    metrics = evaluate_binary_classifier(x_feat_test, data.y_test, w, b)
    return metrics


def main() -> None:
    metrics = run_pipeline()
    print({"library": "numpy", **metrics})


if __name__ == "__main__":
    main()
