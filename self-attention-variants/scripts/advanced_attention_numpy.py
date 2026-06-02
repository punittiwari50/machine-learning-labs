from __future__ import annotations

import math
import time
from dataclasses import dataclass

import numpy as np

from shared_text_preprocessing import PreprocessingConfig, prepare_text_data


@dataclass(frozen=True)
class ExperimentConfig:
    num_samples: int = 64
    seq_len: int = 128
    d_model: int = 48
    local_window: int = 8
    temperature_grid_size: int = 31
    seed: int = 42


def softmax(x: np.ndarray, axis: int = -1) -> np.ndarray:
    z = x - x.max(axis=axis, keepdims=True)
    exp_z = np.exp(z)
    return exp_z / exp_z.sum(axis=axis, keepdims=True)


def init_projection_weights(
    d_model: int,
    rng: np.random.Generator,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    w_q = rng.normal(0.0, 0.2, (d_model, d_model)).astype(np.float32)
    w_k = rng.normal(0.0, 0.2, (d_model, d_model)).astype(np.float32)
    w_v = rng.normal(0.0, 0.2, (d_model, d_model)).astype(np.float32)
    return w_q, w_k, w_v


def apply_qkv_projection(
    x: np.ndarray,
    w_q: np.ndarray,
    w_k: np.ndarray,
    w_v: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    return x @ w_q, x @ w_k, x @ w_v


def dense_attention(q: np.ndarray, k: np.ndarray, v: np.ndarray) -> np.ndarray:
    scores = (q @ np.swapaxes(k, -1, -2)) / math.sqrt(q.shape[-1])
    return softmax(scores, axis=-1) @ v


def sparse_with_temperature(
    q: np.ndarray,
    k: np.ndarray,
    v: np.ndarray,
    window: int,
    temperature: float,
) -> np.ndarray:
    batch, seq_len, _ = q.shape
    scores = np.full((batch, seq_len, seq_len), -1e9, dtype=np.float32)
    raw = (q @ np.swapaxes(k, -1, -2)) / (math.sqrt(q.shape[-1]) * temperature)
    for i in range(seq_len):
        lo = max(0, i - window)
        hi = min(seq_len, i + window + 1)
        scores[:, i, lo:hi] = raw[:, i, lo:hi]
    return softmax(scores, axis=-1) @ v


def linear_attention(q: np.ndarray, k: np.ndarray, v: np.ndarray) -> np.ndarray:
    q_phi = np.maximum(q, 0.0) + 1e-3
    k_phi = np.maximum(k, 0.0) + 1e-3
    kv = np.einsum("bnd,bne->bde", k_phi, v)
    z = 1.0 / (np.einsum("bnd,bd->bn", q_phi, k_phi.sum(axis=1)) + 1e-6)
    return np.einsum("bnd,bde,bn->bne", q_phi, kv, z).astype(np.float32)


def grouped_query_attention(
    q: np.ndarray,
    k: np.ndarray,
    v: np.ndarray,
    num_groups: int = 4,
) -> np.ndarray:
    batch, seq_len, d_model = q.shape
    if d_model % num_groups != 0:
        raise ValueError(
            f"d_model ({d_model}) must be divisible by num_groups ({num_groups})."
        )

    group_dim = d_model // num_groups
    qg = q.reshape(batch, seq_len, num_groups, group_dim).transpose(0, 2, 1, 3)
    k_shared = k.reshape(batch, seq_len, num_groups, group_dim).mean(axis=2)
    v_shared = v.reshape(batch, seq_len, num_groups, group_dim).mean(axis=2)

    outputs: list[np.ndarray] = []
    for g in range(num_groups):
        scores = (qg[:, g] @ np.swapaxes(k_shared, -1, -2)) / math.sqrt(group_dim)
        outputs.append(softmax(scores, axis=-1) @ v_shared)

    out = np.stack(outputs, axis=1).transpose(0, 2, 1, 3)
    return out.reshape(batch, seq_len, d_model)


def timed_run(fn, *args):
    start = time.perf_counter()
    out = fn(*args)
    return out, (time.perf_counter() - start) * 1000.0


def run_pipeline() -> dict[str, float]:
    exp_cfg = ExperimentConfig()
    rng = np.random.default_rng(exp_cfg.seed)

    prep_cfg = PreprocessingConfig(
        num_samples=exp_cfg.num_samples,
        seq_len=exp_cfg.seq_len,
        max_vocab_size=4096,
        train_ratio=0.8,
    )
    data = prepare_text_data(prep_cfg, seed=exp_cfg.seed)

    emb_table = rng.normal(0.0, 0.2, (len(data.vocab), exp_cfg.d_model)).astype(
        np.float32
    )
    x_train = emb_table[data.train_token_ids]
    x_test = emb_table[data.test_token_ids]

    w_q, w_k, w_v = init_projection_weights(exp_cfg.d_model, rng)
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
        mse = float(np.mean((student - teacher_train) ** 2))
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
        "best_temperature": best_temp,
        "dense_ms": float(t_dense),
        "sparse_ms": float(t_sparse),
        "linear_ms": float(t_linear),
        "gqa_ms": float(t_gqa),
        "sparse_mse_vs_dense": float(np.mean((sparse_test - teacher_test) ** 2)),
        "linear_mse_vs_dense": float(np.mean((linear_test - teacher_test) ** 2)),
        "gqa_mse_vs_dense": float(np.mean((gqa_test - teacher_test) ** 2)),
    }


def main() -> None:
    metrics = run_pipeline()
    print({"library": "numpy", "variant": "advanced", **metrics})


if __name__ == "__main__":
    main()
