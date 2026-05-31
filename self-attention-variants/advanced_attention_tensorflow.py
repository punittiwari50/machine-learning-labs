from __future__ import annotations

import math
import os
import time
from dataclasses import dataclass

import numpy as np
import tensorflow as tf

from shared_text_preprocessing import PreprocessingConfig, prepare_text_data


@dataclass(frozen=True)
class ExperimentConfig:
    num_samples: int = 64
    seq_len: int = 128
    d_model: int = 48
    local_window: int = 8
    temperature_grid_size: int = 31
    seed: int = 42


def parse_use_gpu_flag(raw_value: str) -> bool:
    normalized = raw_value.strip().lower()
    return normalized not in {"0", "false", "no", "off"}


def resolve_runtime_device() -> str:
    use_gpu = parse_use_gpu_flag(os.getenv("USE_GPU", "1"))
    has_gpu = bool(tf.config.list_physical_devices("GPU"))
    return "cuda" if use_gpu and has_gpu else "cpu"


def init_projection_weights(
    d_model: int, seed: int
) -> tuple[tf.Tensor, tf.Tensor, tf.Tensor]:
    w_q = tf.random.normal((d_model, d_model), stddev=0.2, seed=seed)
    w_k = tf.random.normal((d_model, d_model), stddev=0.2, seed=seed + 1)
    w_v = tf.random.normal((d_model, d_model), stddev=0.2, seed=seed + 2)
    return w_q, w_k, w_v


def apply_qkv_projection(
    x: tf.Tensor,
    w_q: tf.Tensor,
    w_k: tf.Tensor,
    w_v: tf.Tensor,
) -> tuple[tf.Tensor, tf.Tensor, tf.Tensor]:
    return tf.linalg.matmul(x, w_q), tf.linalg.matmul(x, w_k), tf.linalg.matmul(x, w_v)


def dense_attention(q: tf.Tensor, k: tf.Tensor, v: tf.Tensor) -> tf.Tensor:
    scores = tf.linalg.matmul(q, k, transpose_b=True) / math.sqrt(float(q.shape[-1]))
    weights = tf.nn.softmax(scores, axis=-1)
    return tf.linalg.matmul(weights, v)


def sparse_with_temperature(
    q: tf.Tensor,
    k: tf.Tensor,
    v: tf.Tensor,
    window: int,
    temperature: float,
) -> tf.Tensor:
    seq_len = tf.shape(q)[1]
    raw = tf.linalg.matmul(q, k, transpose_b=True) / (
        math.sqrt(float(q.shape[-1])) * temperature
    )
    idx = tf.range(seq_len)
    distance = tf.abs(tf.expand_dims(idx, 0) - tf.expand_dims(idx, 1))
    local_mask = tf.expand_dims(distance <= window, axis=0)
    scores = tf.where(
        local_mask, raw, tf.fill(tf.shape(raw), tf.constant(-1e9, dtype=raw.dtype))
    )
    weights = tf.nn.softmax(scores, axis=-1)
    return tf.linalg.matmul(weights, v)


def linear_attention(q: tf.Tensor, k: tf.Tensor, v: tf.Tensor) -> tf.Tensor:
    q_phi = tf.nn.relu(q) + 1e-3
    k_phi = tf.nn.relu(k) + 1e-3
    kv = tf.einsum("bnd,bne->bde", k_phi, v)
    z = 1.0 / (tf.einsum("bnd,bd->bn", q_phi, tf.reduce_sum(k_phi, axis=1)) + 1e-6)
    return tf.einsum("bnd,bde,bn->bne", q_phi, kv, z)


def grouped_query_attention(
    q: tf.Tensor,
    k: tf.Tensor,
    v: tf.Tensor,
    num_groups: int = 4,
) -> tf.Tensor:
    batch = q.shape[0]
    seq_len = q.shape[1]
    d_model = q.shape[2]
    if d_model % num_groups != 0:
        raise ValueError(
            f"d_model ({d_model}) must be divisible by num_groups ({num_groups})."
        )

    group_dim = d_model // num_groups
    qg = tf.transpose(
        tf.reshape(q, (batch, seq_len, num_groups, group_dim)), perm=(0, 2, 1, 3)
    )
    k_shared = tf.reduce_mean(
        tf.reshape(k, (batch, seq_len, num_groups, group_dim)), axis=2
    )
    v_shared = tf.reduce_mean(
        tf.reshape(v, (batch, seq_len, num_groups, group_dim)), axis=2
    )

    outputs: list[tf.Tensor] = []
    for g in range(num_groups):
        scores = tf.linalg.matmul(qg[:, g], k_shared, transpose_b=True) / math.sqrt(
            float(group_dim)
        )
        weights = tf.nn.softmax(scores, axis=-1)
        outputs.append(tf.linalg.matmul(weights, v_shared))

    out = tf.stack(outputs, axis=1)
    return tf.reshape(tf.transpose(out, perm=(0, 2, 1, 3)), (batch, seq_len, d_model))


def timed_run(fn, *args):
    start = time.perf_counter()
    out = fn(*args)
    return out, (time.perf_counter() - start) * 1000.0


def run_pipeline() -> dict[str, object]:
    exp_cfg = ExperimentConfig()
    tf.random.set_seed(exp_cfg.seed)
    np.random.seed(exp_cfg.seed)

    runtime_device = resolve_runtime_device()
    prep_cfg = PreprocessingConfig(
        num_samples=exp_cfg.num_samples,
        seq_len=exp_cfg.seq_len,
        max_vocab_size=4096,
        train_ratio=0.8,
    )
    data = prepare_text_data(prep_cfg, seed=exp_cfg.seed)

    embedding = tf.keras.layers.Embedding(
        input_dim=len(data.vocab),
        output_dim=exp_cfg.d_model,
        embeddings_initializer=tf.keras.initializers.RandomNormal(
            mean=0.0,
            stddev=0.2,
            seed=exp_cfg.seed,
        ),
    )
    x_train = embedding(tf.convert_to_tensor(data.train_token_ids, dtype=tf.int32))
    x_test = embedding(tf.convert_to_tensor(data.test_token_ids, dtype=tf.int32))

    w_q, w_k, w_v = init_projection_weights(exp_cfg.d_model, exp_cfg.seed)
    q_train, k_train, v_train = apply_qkv_projection(x_train, w_q, w_k, w_v)
    q_test, k_test, v_test = apply_qkv_projection(x_test, w_q, w_k, w_v)

    teacher_train = dense_attention(q_train, k_train, v_train)
    temp_grid = np.linspace(0.5, 2.0, exp_cfg.temperature_grid_size, dtype=np.float32)

    best_temp = float(temp_grid[0])
    best_mse = float("inf")
    for temp in temp_grid:
        student = sparse_with_temperature(
            q_train,
            k_train,
            v_train,
            exp_cfg.local_window,
            float(temp),
        )
        mse = float(tf.reduce_mean((student - teacher_train) ** 2).numpy())
        if mse < best_mse:
            best_mse = mse
            best_temp = float(temp)

    teacher_test, t_dense = timed_run(dense_attention, q_test, k_test, v_test)
    sparse_test, t_sparse = timed_run(
        sparse_with_temperature,
        q_test,
        k_test,
        v_test,
        exp_cfg.local_window,
        best_temp,
    )
    linear_test, t_linear = timed_run(linear_attention, q_test, k_test, v_test)
    gqa_test, t_gqa = timed_run(grouped_query_attention, q_test, k_test, v_test)

    return {
        "runtime_device": runtime_device,
        "best_temperature": best_temp,
        "dense_ms": float(t_dense),
        "sparse_ms": float(t_sparse),
        "linear_ms": float(t_linear),
        "gqa_ms": float(t_gqa),
        "sparse_mse_vs_dense": float(
            tf.reduce_mean((sparse_test - teacher_test) ** 2).numpy()
        ),
        "linear_mse_vs_dense": float(
            tf.reduce_mean((linear_test - teacher_test) ** 2).numpy()
        ),
        "gqa_mse_vs_dense": float(
            tf.reduce_mean((gqa_test - teacher_test) ** 2).numpy()
        ),
    }


def main() -> None:
    metrics = run_pipeline()
    print({"library": "tensorflow", "variant": "advanced", **metrics})


if __name__ == "__main__":
    main()
