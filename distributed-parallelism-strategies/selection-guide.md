# Selection Guide: From Basic to Advanced

## Quick Strategy Picker

1. If the model fits on one GPU and you want speed:
- Start with Data Parallelism.

2. If the model does not fit on one GPU:
- Use FSDP/ZeRO-style sharding or Tensor Parallelism.

3. If the model is very deep:
- Add Pipeline Parallelism.

4. If you run at very large scale:
- Combine DP + TP + PP (3D parallelism).

5. If context length is very large:
- Add Sequence/Context Parallelism.

6. If using sparse Mixture-of-Experts:
- Add Expert Parallelism with careful load balancing.

## Communication Primitives You Must Tune

- All-Reduce: common for gradient sync.
- Reduce-Scatter: memory and bandwidth efficient reductions.
- All-Gather: collect parameter shards in sharded training.
- Point-to-Point: pipeline stage hand-offs.

## Practical Maturity Path

1. Single-node Data Parallel baseline.
2. Multi-node Data Parallel.
3. FSDP/ZeRO memory scaling.
4. Add TP or PP based on bottleneck.
5. Move to 3D parallelism for frontier-scale workloads.
6. Add topology-aware scheduling and communication overlap.

## Common Failure Modes

- Communication-bound training (too many collectives).
- Pipeline bubbles (poor micro-batch scheduling).
- Imbalanced MoE experts (router skew).
- CPU input pipeline bottleneck starving GPUs.
- Checkpoint and restart instability in elastic clusters.

## Minimal Operational Checklist

- Profile end-to-end step time before changing strategy.
- Measure compute/communication overlap.
- Validate memory headroom per device.
- Test fault recovery and checkpoint restore.
- Track throughput, latency, and convergence quality together.
