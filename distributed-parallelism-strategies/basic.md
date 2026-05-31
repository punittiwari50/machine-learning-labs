# Basic Distributed Parallelism Strategies

## 1. Data Parallelism (DP)

- Full model replica on each device.
- Each device processes a different mini-batch shard.
- Gradients are synchronized (usually All-Reduce).

When to use:
- Model fits on a single GPU.
- Goal is higher throughput.

Pros:
- Simple and widely supported.
- Strong scaling on multi-GPU for many workloads.

Cons:
- Communication overhead increases with model size and device count.

## 2. Model Parallelism (Layer/Vertical Split)

- Different model parts are placed on different devices.

When to use:
- Model cannot fit in one GPU memory.

Pros:
- Enables training larger models.

Cons:
- Cross-device dependencies can reduce utilization.

## 3. Pipeline Parallelism (PP)

- Model is split into ordered stages.
- Micro-batches flow stage by stage.

When to use:
- Deep networks with clear stage boundaries.

Pros:
- Better memory distribution across devices.

Cons:
- Pipeline bubbles and stage imbalance may lower efficiency.

## 4. Tensor Parallelism (TP)

- Intra-layer operations (for example matrix multiplications) are partitioned across devices.

When to use:
- Large transformer blocks that are too expensive for one GPU.

Pros:
- Scales large layers directly.

Cons:
- Frequent collective communication inside forward/backward passes.

## 5. Sharded Data Parallel (ZeRO Stage 1/2 concept)

- Shard optimizer states and/or gradients across workers.

When to use:
- Need more memory efficiency than classic DP.

Pros:
- Lower per-device memory footprint.

Cons:
- More communication and orchestration complexity.
