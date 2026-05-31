from __future__ import annotations

# mypy: ignore-errors

import math
import os
from dataclasses import dataclass

import numpy as np
import tensorflow as tf

from shared_text_preprocessing import PreprocessingConfig, prepare_text_data


@dataclass(frozen=True)
class ExperimentConfig:
    d_model: int = 32
    num_heads: int = 4
    learning_rate: float = 0.05
    epochs: int = 120
    seed: int = 42


def parse_use_gpu_flag(raw_value: str) -> bool:
    normalized = raw_value.strip().lower()
    return normalized not in {"0", "false", "no", "off"}


def configure_runtime(seed: int) -> str:
    tf.random.set_seed(seed)
    use_gpu = parse_use_gpu_flag(os.getenv("USE_GPU", "1"))
    has_gpu = bool(tf.config.list_physical_devices("GPU"))
    runtime_device = "cuda" if use_gpu and has_gpu else "cpu"
    return runtime_device


def build_embeddings(
    token_ids: np.ndarray,
    vocab_size: int,
    d_model: int,
    seed: int,
) -> tf.Tensor:
    embedding = tf.keras.layers.Embedding(
        input_dim=vocab_size,
        output_dim=d_model,
        embeddings_initializer=tf.keras.initializers.RandomNormal(
            mean=0.0,
            stddev=0.2,
            seed=seed,
        ),
    )
    token_tensor = tf.convert_to_tensor(token_ids, dtype=tf.int32)
    return embedding(token_tensor)


def project_qkv(
    x: tf.Tensor, d_model: int, seed: int
) -> tuple[tf.Tensor, tf.Tensor, tf.Tensor]:
    w_q = tf.random.normal((d_model, d_model), stddev=0.2, seed=seed)
    w_k = tf.random.normal((d_model, d_model), stddev=0.2, seed=seed + 1)
    w_v = tf.random.normal((d_model, d_model), stddev=0.2, seed=seed + 2)
    return tf.linalg.matmul(x, w_q), tf.linalg.matmul(x, w_k), tf.linalg.matmul(x, w_v)


def scaled_dot_product_attention(
    q: tf.Tensor,
    k: tf.Tensor,
    v: tf.Tensor,
) -> tuple[tf.Tensor, tf.Tensor]:
    scores = tf.linalg.matmul(q, k, transpose_b=True) / math.sqrt(float(q.shape[-1]))
    weights = tf.nn.softmax(scores, axis=-1)
    return tf.linalg.matmul(weights, v), weights


def multi_head_attention(
    q: tf.Tensor,
    k: tf.Tensor,
    v: tf.Tensor,
    num_heads: int,
) -> tuple[tf.Tensor, tf.Tensor]:
    shape = tf.shape(q)
    batch = shape[0]
    seq_len = shape[1]
    d_model = q.shape[-1]
    if d_model is None:
        raise ValueError("d_model must be statically known for this demo.")
    if d_model % num_heads != 0:
        raise ValueError(
            f"d_model ({d_model}) must be divisible by num_heads ({num_heads})."
        )

    head_dim = d_model // num_heads

    qh = tf.transpose(
        tf.reshape(q, (batch, seq_len, num_heads, head_dim)),
        perm=(0, 2, 1, 3),
    )
    kh = tf.transpose(
        tf.reshape(k, (batch, seq_len, num_heads, head_dim)),
        perm=(0, 2, 1, 3),
    )
    vh = tf.transpose(
        tf.reshape(v, (batch, seq_len, num_heads, head_dim)),
        perm=(0, 2, 1, 3),
    )

    scores = tf.linalg.matmul(qh, kh, transpose_b=True) / math.sqrt(float(head_dim))
    weights = tf.nn.softmax(scores, axis=-1)
    out = tf.linalg.matmul(weights, vh)
    out = tf.reshape(tf.transpose(out, perm=(0, 2, 1, 3)), (batch, seq_len, d_model))
    return out, weights


def pooled_features(attn_out: tf.Tensor) -> tf.Tensor:
    return tf.reduce_mean(attn_out, axis=1)


def train_binary_head(
    x_feat_train: tf.Tensor,
    y_train: np.ndarray,
    learning_rate: float,
    epochs: int,
) -> tf.keras.layers.Dense:
    head = tf.keras.layers.Dense(1)
    optimizer = tf.keras.optimizers.SGD(learning_rate=learning_rate)
    y_train_t = tf.convert_to_tensor(y_train.reshape(-1, 1), dtype=tf.float32)

    for _ in range(epochs):
        with tf.GradientTape() as tape:
            logits = head(x_feat_train)
            loss = tf.reduce_mean(
                tf.nn.sigmoid_cross_entropy_with_logits(labels=y_train_t, logits=logits)
            )
        grads = tape.gradient(loss, head.trainable_variables)
        optimizer.apply_gradients(zip(grads, head.trainable_variables))

    return head


def evaluate_binary_classifier(
    x_feat: tf.Tensor,
    y_true: np.ndarray,
    head: tf.keras.layers.Dense,
) -> dict[str, object]:
    logits = head(x_feat)
    probs = tf.math.sigmoid(logits)
    preds = tf.cast(probs >= 0.5, tf.int64).numpy().reshape(-1)
    accuracy = float((preds == y_true).mean())
    return {"accuracy": accuracy}


def run_pipeline() -> dict[str, object]:
    exp_cfg = ExperimentConfig()
    prep_cfg = PreprocessingConfig(num_samples=256, seq_len=24)
    np.random.seed(exp_cfg.seed)

    runtime_device = configure_runtime(exp_cfg.seed)
    data = prepare_text_data(prep_cfg, seed=exp_cfg.seed)

    x_train = build_embeddings(
        data.train_token_ids,
        len(data.vocab),
        exp_cfg.d_model,
        seed=exp_cfg.seed,
    )
    x_test = build_embeddings(
        data.test_token_ids,
        len(data.vocab),
        exp_cfg.d_model,
        seed=exp_cfg.seed + 1,
    )

    q_train, k_train, v_train = project_qkv(x_train, exp_cfg.d_model, exp_cfg.seed)
    q_test, k_test, v_test = project_qkv(x_test, exp_cfg.d_model, exp_cfg.seed)

    attn_train, _ = multi_head_attention(q_train, k_train, v_train, exp_cfg.num_heads)
    attn_test, _ = multi_head_attention(q_test, k_test, v_test, exp_cfg.num_heads)

    x_feat_train = pooled_features(attn_train)
    x_feat_test = pooled_features(attn_test)

    head = train_binary_head(
        x_feat_train,
        data.y_train,
        exp_cfg.learning_rate,
        exp_cfg.epochs,
    )
    metrics = evaluate_binary_classifier(x_feat_test, data.y_test, head)
    return {"runtime_device": runtime_device, **metrics}


def main() -> None:
    metrics = run_pipeline()
    print({"library": "tensorflow", **metrics})


if __name__ == "__main__":
    main()
