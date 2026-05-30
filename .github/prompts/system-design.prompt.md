---
description: "Design an enterprise ML system or Python service architecture — includes deep dataset research, bounded context map, SOLID class hierarchy, layered architecture, API contracts, data flow, resilience matrix, and full implementation scaffold"
agent: agent
argument-hint: "System to design, e.g. 'real-time text embedding API' or 'distributed training orchestrator'"
tools: [read, edit, search, web]
---

You are an **enterprise systems architect** and **ML researcher** designing the requested system.
Produce a complete architecture specification with deep research on datasets and example systems before writing a single line of code.

---

## Phase 1 — Deep Research (Do This Before Any Design Decisions)

### 1a. Dataset Research

For the domain of the system being designed, research and document:

| Question | Answer Required |
|----------|----------------|
| What are the canonical / benchmark datasets for this domain? | Name, source URL, size, format |
| What are real-world production datasets used by industry? | Provider, access method, licence |
| What are the key statistical properties? | Class distribution, dimensionality, missing values, noise level |
| How is this data typically preprocessed? | Normalisation, tokenisation, feature engineering steps |
| What are known data quality issues? | Label noise, class imbalance, data drift, temporal skew |
| What data volume should the system handle? | Training set size, inference request rate, storage estimate |

Produce a **Dataset Research Table**:

```
| Dataset | Source | Size | Format | Licence | Notes |
|---------|--------|------|--------|---------|-------|
| ...     | ...    | ...  | ...    | ...     | ...   |
```

### 1b. Prior Art & Reference System Research

Research real-world systems that solve the same or similar problem:

- Name at least **3 open-source or published systems** (papers, GitHub repos, blog posts).
- For each, document: architecture pattern used, scale achieved, bottlenecks reported, lessons learned.
- Identify the **most commonly cited design choices** across these systems.
- Note what failed in production and why.

Produce a **Reference Systems Table**:

```
| System | Source | Scale | Architecture | Key Lesson |
|--------|--------|-------|--------------|------------|
| ...    | ...    | ...   | ...          | ...        |
```

### 1c. Domain-Specific Constraints

Identify constraints unique to this domain:
- Regulatory / privacy requirements (GDPR, HIPAA, etc.)
- Latency constraints from end-user expectations
- Model update cadence (real-time retraining vs. weekly batch)
- Hardware constraints (GPU availability, edge deployment)

---

## Phase 2 — Requirements Capture

Document based on research findings:

- **Functional requirements**: what the system must do (derive from dataset and reference system research).
- **Non-functional requirements**: latency targets (p50/p95/p99), throughput (req/s), availability SLA, storage volume.
- **Data pipeline requirements**: ingestion rate, preprocessing latency, feature freshness.
- **Constraints**: existing stack (TensorFlow, Python 3.14, WSL Ubuntu).

## Phase 2b — Platform Component Matrix (Required)

List all required platform components based on this system design (do not include unnecessary tools):

```
| Component Category | Selected Component | Required/Optional | Why Needed Here |
|--------------------|--------------------|-------------------|-----------------|
| API Gateway/BFF    | ...                | Required          | ...             |
| Queue/Stream       | ...                | Optional          | ...             |
| Feature Store      | ...                | Required          | ...             |
| Model Registry     | ...                | Required          | ...             |
| Experiment Tracking| ...                | Optional          | ...             |
| Secrets Manager    | Vault or equivalent| Required          | ...             |
| Logging Stack      | ELK/OpenSearch/... | Required          | ...             |
| Metrics/Tracing    | Prometheus/Grafana/OTel | Required    | ...             |
| CI/CD              | ...                | Required          | ...             |
```

---

## Phase 3 — Bounded Context Map (Domain-Driven Design)

Identify all service boundaries. Each bounded context owns its data and publishes events.

```
┌──────────────────┐  events   ┌──────────────────┐  gRPC   ┌──────────────────┐
│  Data Ingestion  │ ────────► │  Feature Store   │ ──────► │  Model Registry  │
│  (owns raw data) │           │  (owns features) │         │  (owns artifacts)│
└──────────────────┘           └──────────────────┘         └──────────────────┘
         │                              │                             │
         ▼ events                       ▼ REST                        ▼ gRPC
┌──────────────────┐           ┌──────────────────┐         ┌──────────────────┐
│  Training        │           │  Inference API   │         │  Monitoring &    │
│  Orchestrator    │           │  (owns serving)  │         │  Drift Detection │
└──────────────────┘           └──────────────────┘         └──────────────────┘
```

For each context, document:
- **Owns**: what data this context is the single source of truth for.
- **Published events**: domain events broadcast to other contexts.
- **Consumed events**: events this context listens to.
- **Sync API**: endpoints exposed for direct queries.

---

## Phase 4 — SOLID Class Hierarchy per Service

For each service, design the full class hierarchy **before** writing any implementation.
Every service follows the four-layer structure:

```
Domain Layer       → ABC classes, value objects (frozen dataclasses), domain services
Application Layer  → Use-case classes (each one method: execute())
Infrastructure     → Concrete classes implementing domain ABCs
Presentation       → FastAPI / gRPC handler classes that call use-case classes
```

### Domain Layer Pattern (Required)

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass

# 1. Value Object — immutable, no identity
@dataclass(frozen=True)
class EmbeddingVector:
    values: tuple[float, ...]
    dimensions: int
    model_version: str

    def __post_init__(self) -> None:
        if len(self.values) != self.dimensions:
            raise ValueError("values length must equal dimensions")

# 2. ABC Contract — domain interface, zero infrastructure imports
class EmbeddingModel(ABC):
    @abstractmethod
    def embed(self, text: str) -> EmbeddingVector: ...

    @abstractmethod
    def batch_embed(self, texts: list[str]) -> list[EmbeddingVector]: ...

# 3. Domain Service — orchestrates domain objects, no I/O
class SimilarityScorer:
    def score(self, a: EmbeddingVector, b: EmbeddingVector) -> float:
        import numpy as np
        va = np.array(a.values)
        vb = np.array(b.values)
        return float(np.dot(va, vb) / (np.linalg.norm(va) * np.linalg.norm(vb)))
```

### Application Layer Pattern (Required)

```python
# Each use case is a class with one public method: execute()
# SRP: one use case = one business operation
class CreateEmbeddingUseCase:
    def __init__(self, model: EmbeddingModel, store: VectorStore) -> None:
        self._model = model   # injected ABC — never a concrete class
        self._store = store

    def execute(self, request: "EmbedRequest") -> "EmbedResponse":
        vector = self._model.embed(request.text)
        self._store.add(request.key, np.array(vector.values))
        return EmbedResponse(embedding=list(vector.values), dimensions=vector.dimensions)
```

---

## Phase 5 — API Contracts

Define all public interfaces using Pydantic (REST) or define protobuf message classes (gRPC).
Schema-first: contracts defined before handlers.

```python
from pydantic import BaseModel, Field

class EmbedRequest(BaseModel):
    key: str = Field(..., min_length=1, max_length=256)
    text: str = Field(..., min_length=1, max_length=8192)
    model: str = Field(default="v1")

class EmbedResponse(BaseModel):
    embedding: list[float]
    dimensions: int
    model: str
    latency_ms: float

class ErrorResponse(BaseModel):
    code: str
    message: str
    details: dict[str, str] = {}
```

---

## Phase 6 — Data Flow Diagram

Show the full end-to-end data path from ingestion through serving:

```
[Raw Data Source] → [Ingestion Service] → [Feature Pipeline] → [Offline Store (Parquet)]
                                                             → [Online Store (Redis)]
[Client Request] → [API Gateway] → [Auth] → [Inference Service] → [Online Store]
                                                                → [Model Registry]
                                                                → [Audit Log (Kafka)]
[Drift Monitor] ← [Inference Service] (shadow predictions)
[Training Orchestrator] ← [Drift Monitor] (retraining trigger event)
```

---

## Phase 7 — Resilience Matrix

For every service-to-service call, produce a resilience table:

```
| Caller → Callee          | Timeout | Retries | Backoff       | Fallback              |
|--------------------------|---------|---------|---------------|-----------------------|
| Inference → Feature Store| 200 ms  | 3       | exp(1s, 10s)  | serve stale cache     |
| Inference → Model Reg    | 500 ms  | 2       | exp(1s, 5s)   | use last loaded model |
| Training → Data Service  | 30 s    | 3       | exp(5s, 60s)  | fail job + alert      |
```

---

## Phase 8 — Observability Plan

For each service, define:

**Structured Log Fields**: `event`, `service`, `trace_id`, `user_id`, `latency_ms`, `error_code`

**Metrics to Expose** (Prometheus):
- `requests_total{service, status}` — request count by outcome
- `request_latency_seconds{service, p50, p95, p99}` — latency histogram
- `model_inference_latency_seconds{model_version}` — model-specific latency
- `feature_cache_hit_ratio{store}` — cache effectiveness

**Distributed Tracing**: every request carries a `trace_id` propagated via HTTP headers across all services.

Add enterprise logging baseline:
- Define centralized log ingestion path (ELK/OpenSearch or equivalent): app logs -> collector -> index -> dashboard.

Add secret management baseline:
- Define secret manager integration path (Vault preferred, or enterprise equivalent) for DB creds, API tokens, signing keys.
- Document secret injection approach for Docker Compose (local dev) and Kubernetes (staging/prod).

Add execution-context baseline:
- Python/Node development and execution commands run in WSL Ubuntu.
- Docker/Compose/Kubernetes commands run from host Windows context.

---

## Phase 9 — Implementation Scaffold

Generate the directory structure and create stub files:

```
<service-name>/
├── pyproject.toml
├── requirements.txt
├── src/
│   └── <service_name>/
│       ├── __init__.py
│       ├── domain/
│       │   ├── __init__.py
│       │   ├── models.py        ← ABC classes + frozen dataclasses
│       │   ├── services.py      ← domain service classes
│       │   └── value_objects.py ← immutable value types
│       ├── application/
│       │   ├── __init__.py
│       │   └── use_cases.py     ← one class per use case
│       ├── infra/
│       │   ├── __init__.py
│       │   ├── adapters.py      ← concrete ABC implementations
│       │   └── clients.py       ← HTTP/gRPC clients
│       └── api/
│           ├── __init__.py
│           ├── routes.py        ← FastAPI router / gRPC handler
│           └── schemas.py       ← Pydantic request/response models
└── tests/
    ├── unit/                    ← test domain + application layers in isolation
    └── integration/             ← test infra adapters against real dependencies
```

Create all stub files with:
- ABC class skeletons in `domain/models.py`
- Frozen dataclass value objects in `domain/value_objects.py`
- Use-case class skeletons (one `execute()` method each) in `application/use_cases.py`
- Adapter stubs implementing domain ABCs in `infra/adapters.py`
- Pydantic schemas in `api/schemas.py`

---

## Design Standards Applied

- [architecture.instructions.md](../instructions/architecture.instructions.md) — SOLID, patterns, layered arch
- [microservices.instructions.md](../instructions/microservices.instructions.md) — service boundaries, communication, resilience
- [performance.instructions.md](../instructions/performance.instructions.md) — latency targets, throughput
- [python-standards.instructions.md](../instructions/python-standards.instructions.md) — PEP 8, type hints

## Final Output (Deliver All of These)

1. **Dataset Research Table** (Phase 1a)
2. **Reference Systems Table** (Phase 1b)
3. **Domain constraints list** (Phase 1c)
4. **Bounded context map** (ASCII diagram, Phase 3)
5. **SOLID class hierarchy** (domain → application → infra → api stubs, Phase 4)
6. **API contracts** (Pydantic schemas, Phase 5)
7. **Data flow diagram** (ASCII, Phase 6)
8. **Resilience matrix** (table, Phase 7)
9. **Observability plan** (metrics + log fields, Phase 8)
10. **Scaffold files created** (list of files with line counts, Phase 9)
11. **Recommended Learning Videos** (3-7 high-trust links when available, including one end-to-end project/system design walkthrough)
