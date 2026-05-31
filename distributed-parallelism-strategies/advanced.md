# Advanced Distributed Parallelism Strategies

## 1. Fully Sharded Data Parallel (FSDP / ZeRO-3 style)

- Shard parameters, gradients, and optimizer states.
- Gather shards only when needed.

Best for:
- Very large model training under tight memory budgets.

Trade-offs:
- High communication volume.
- Requires careful tuning for overlap and bucket sizing.

## 2. 3D Parallelism (DP + TP + PP)

- Combines data, tensor, and pipeline parallelism in one topology.

Best for:
- Frontier-scale LLM training.

Trade-offs:
- Strong performance potential, but high system complexity.

## 3. Sequence or Context Parallelism

- Split sequence dimension across devices.

Best for:
- Long-context transformer training/inference.

Trade-offs:
- Additional synchronization in attention/residual paths.

## 4. Expert Parallelism (MoE)

- Experts distributed across devices.
- Router sends tokens to selected experts.

Best for:
- Sparse scaling with very high parameter count.

Trade-offs:
- Router load balancing and communication are hard optimization problems.

## 5. Parameter Server Architectures

- Workers pull parameters and push updates to parameter servers.

Best for:
- Heterogeneous or elastic cluster setups.

Trade-offs:
- Potential staleness and central bottlenecks without robust design.

## 6. Elastic Distributed Training

- Workers can join/leave dynamically.

Best for:
- Spot/preemptible cloud infrastructure.

Trade-offs:
- Additional checkpointing and rendezvous complexity.

## 7. Hierarchical Topology-Aware Parallelism

- Communication optimized per hardware topology.
- Intra-node (for example NVLink) and inter-node (for example InfiniBand) handled differently.

Best for:
- Multi-node training at scale.

Trade-offs:
- Requires hardware-aware process placement and scheduling.
