# Inference Performance Metrics - Basic

## 1. Latency

- Measures how long a single request takes from input to output.
- Common reporting levels: p50, p95, and p99.
- Lower is better, but only when quality stays acceptable.

Enterprise usage example:
- Customer support classification service with a p95 latency SLO.

## 2. Throughput

- Measures how many requests or tokens a system can process per second.
- Useful for understanding capacity under load.
- Usually improves with batching, but batching can increase latency.

Enterprise usage example:
- Batch document processing pipeline for weekly compliance review.

## 3. Memory Footprint

- Measures CPU RAM or GPU VRAM consumed during inference.
- Includes model weights, activations, and temporary buffers.
- Important for edge devices and multi-tenant serving.

Enterprise usage example:
- On-device document summarization where VRAM is limited.

## 4. Accuracy or Quality

- Measures whether the model output is correct, relevant, or useful.
- Must be tracked alongside latency and throughput.
- A faster model is not useful if quality drops too much.

Enterprise usage example:
- Search ranking service that balances precision with response time.

## 5. Simple Trade-Off Rule

- Optimize latency, throughput, memory, and quality together.
- Do not select a variant based on only one metric.
- Use the application SLO to decide which metric matters most.

Enterprise usage example:
- Fraud scoring service where tail latency and accuracy both affect customer experience.
