---
description: "Use when designing or implementing microservices, distributed ML systems, event-driven pipelines, service meshes, or any multi-service architecture. Covers service boundaries, communication patterns, resilience, observability, and enterprise deployment."
applyTo: ["**/*.py", "**/*.ipynb"]
---

# Microservices & Distributed Systems

## Service Design Principles

| Principle | Rule |
|-----------|------|
| **Single Responsibility** | One service = one bounded context. A tokenizer service does not store models. |
| **Autonomy** | Each service owns its data store. No shared databases between services. |
| **Decentralised Data** | Polyglot persistence — each service picks the right storage (Postgres, Redis, object store). |
| **Design for Failure** | Every network call may fail. Always apply timeout + retry + circuit-breaker. |
| **Observable by Default** | Every service emits structured logs, metrics, and traces from day one. |

---

## Service Boundary Identification (Domain-Driven Design)

Before writing code, identify bounded contexts:

```
ML Platform — Bounded Contexts
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│  Data Ingestion  │  │  Feature Store   │  │  Model Registry  │
│  Service         │  │  Service         │  │  Service         │
└────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘
         │ events               │ feature queries      │ model artifacts
         ▼                      ▼                      ▼
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│  Training        │  │  Serving /       │  │  Monitoring &    │
│  Orchestrator    │  │  Inference API   │  │  Drift Detection │
└──────────────────┘  └──────────────────┘  └──────────────────┘
```

Rules:
- A service that needs data from another service **requests it via API**, never via direct DB access.
- Cross-service communication uses **async events** (Kafka/RabbitMQ) for write operations and **sync REST/gRPC** for queries.

### Polyglot Boundary Rule (Python + Node.js)

If the architecture uses both Python and Node.js services:
- Assign clear service ownership per bounded context; no overlapping ownership.
- Keep ML/data/model internals in Python services.
- Keep API edge/BFF/orchestration/realtime interface in Node.js services where needed.
- Share behavior via contracts and events, not copied code.
- Avoid duplicating business logic between Python and Node.js services.
- Apply SOLID principles within each service codebase.

### Enterprise Security and Observability Baseline

For enterprise-grade local projects:
- Use an enterprise secret manager for secret delivery and rotation (HashiCorp Vault preferred; equivalent solutions allowed).
- Use centralized observability stack across logs, metrics, and traces (ELK/OpenSearch + Prometheus/Grafana + OpenTelemetry as applicable).
- Emit structured JSON logs with stable fields (`event`, `service`, `trace_id`, `env`, `severity`).
- Define local runtime (Docker Compose) and production-like runtime (Kubernetes) with explicit environment overlays.
- Keep infrastructure assets organized by responsibility (`ops/docker`, `ops/k8s`, `ops/secrets`, `ops/observability`).
- Include only components required by the current system design and justify each selected component.

---

## Communication Patterns

### Synchronous (Request/Response)
Use for: real-time inference, feature queries, model metadata.

```python
# gRPC stub — preferred for internal services (typed, efficient)
import grpc
from generated import inference_pb2, inference_pb2_grpc

def get_embedding(text: str, stub: inference_pb2_grpc.InferenceStub) -> list[float]:
    request = inference_pb2.EmbedRequest(text=text)
    response = stub.Embed(request, timeout=2.0)  # always set timeout
    return list(response.embedding)
```

### Asynchronous (Event-Driven)
Use for: training triggers, data pipeline stages, notifications, audit logs.

```python
# Producer — publish domain event
from dataclasses import dataclass, asdict
import json, time

@dataclass
class ModelTrainedEvent:
    model_id: str
    version: str
    accuracy: float
    timestamp: float = time.time()
    event_type: str = "model.trained"

def publish_event(producer, topic: str, event: ModelTrainedEvent) -> None:
    producer.send(topic, value=json.dumps(asdict(event)).encode())
    producer.flush()
```

---

## Resilience Patterns (Required for Every Service-to-Service Call)

### Circuit Breaker + Retry

```python
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import httpx

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    retry=retry_if_exception_type((httpx.TimeoutException, httpx.ConnectError)),
    reraise=True,
)
def fetch_features(feature_ids: list[str], client: httpx.Client) -> dict:
    response = client.post(
        "/v1/features/batch",
        json={"ids": feature_ids},
        timeout=5.0,
    )
    response.raise_for_status()
    return response.json()
```

### Bulkhead — Isolate resource pools

```python
from concurrent.futures import ThreadPoolExecutor

# Separate pools prevent one slow service from blocking all threads
inference_pool = ThreadPoolExecutor(max_workers=4, thread_name_prefix="inference")
feature_pool   = ThreadPoolExecutor(max_workers=8, thread_name_prefix="features")
```

### Timeout Hierarchy

| Call Type | Timeout |
|-----------|---------|
| Internal microservice (LAN) | 500 ms |
| Cross-region service | 2 s |
| External API | 5 s |
| Background batch job | 300 s |

---

## Data Consistency Patterns

### Saga Pattern (distributed transactions without 2PC)

```
Training Saga:
  1. ReserveGPU command  → GPU Service
  2. LoadDataset command → Data Service
  3. RunTraining command → Trainer Service
  4. RegisterModel command → Registry Service
  
Compensations (on failure):
  4 fails → RollbackRegistration
  3 fails → ReleaseGPU
  2 fails → ReleaseGPU
```

### Event Sourcing for Audit Trails

```python
@dataclass
class ExperimentEvent:
    experiment_id: str
    event_type: str   # "started" | "step_logged" | "completed" | "failed"
    payload: dict
    timestamp: float

# Rebuild state by replaying events — never mutate history
def rebuild_experiment(events: list[ExperimentEvent]) -> dict:
    state: dict = {}
    for event in sorted(events, key=lambda e: e.timestamp):
        state = apply_event(state, event)
    return state
```

---

## Observability Triad (Mandatory in Every Service)

### Structured Logging

```python
import structlog

log = structlog.get_logger()

def process_batch(batch_id: str, size: int) -> None:
    log.info("batch.started", batch_id=batch_id, size=size)
    try:
        result = _run_batch(batch_id)
        log.info("batch.completed", batch_id=batch_id, items_processed=result.count)
    except Exception as exc:
        log.error("batch.failed", batch_id=batch_id, error=str(exc), exc_info=True)
        raise
```

### Metrics (Prometheus-compatible)

```python
from prometheus_client import Counter, Histogram, start_http_server

REQUEST_COUNT   = Counter("inference_requests_total", "Total inference requests", ["model", "status"])
REQUEST_LATENCY = Histogram("inference_latency_seconds", "Inference latency", ["model"])

def serve(request: dict) -> dict:
    model_name = request["model"]
    with REQUEST_LATENCY.labels(model=model_name).time():
        result = model.predict(request["input"])
    REQUEST_COUNT.labels(model=model_name, status="success").inc()
    return result
```

### Distributed Tracing

```python
from opentelemetry import trace
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

tracer = trace.get_tracer(__name__)

def embed_text(text: str) -> list[float]:
    with tracer.start_as_current_span("embed_text") as span:
        span.set_attribute("input.length", len(text))
        result = _model.encode(text)
        span.set_attribute("output.dimensions", len(result))
        return result
```

---

## ML-Specific Distributed Patterns

### Feature Store Integration

```
Online Feature Store  (Redis)  ← low latency serving
Offline Feature Store (Parquet/Delta Lake) ← training
Feature Pipeline → writes to both stores
Model Server → reads from Online store only
```

### Model Serving Tiers

| Tier | Latency Target | Pattern |
|------|----------------|---------|
| Real-time (<10ms) | Single-model, in-process | Direct TF/ONNX inference |
| Near-real-time (<100ms) | Batch micro-requests | Dynamic batching server |
| Async (<1s) | Queue-backed worker | Celery / Ray worker |
| Batch (minutes) | Distributed compute | Spark / Ray Data |

### Blue-Green & Canary Deployments

```yaml
# Conceptual — traffic split config
routing:
  - model: "text-embed-v2"
    weight: 90
  - model: "text-embed-v3-canary"
    weight: 10
    shadow: false
```

---

## Quality Gates

- [ ] No direct database access across service boundaries.
- [ ] Every service-to-service call has an explicit timeout.
- [ ] Retry logic present with exponential backoff on all network calls.
- [ ] Structured JSON logging with `event`, `service`, `trace_id` fields.
- [ ] No synchronous calls in the hot path for non-latency-critical operations — use async events.
- [ ] All public service APIs versioned (`/v1/`, `/v2/`).
- [ ] In Python+Node systems, service boundaries and ownership are explicit and non-overlapping.
- [ ] In Python+Node systems, shared business logic is not duplicated across stacks.
- [ ] Local/integration runtime is defined (Docker Compose or equivalent).
- [ ] Staging/production orchestration is defined (Kubernetes or equivalent).
- [ ] Secrets are delivered via secret manager (Vault preferred or equivalent), not plaintext config.
- [ ] Centralized observability path is defined for logs, metrics, and traces.
- [ ] Platform components are justified by architecture needs (no unnecessary stack bloat).
