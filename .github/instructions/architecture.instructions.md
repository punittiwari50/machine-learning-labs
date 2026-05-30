---
description: "Use when designing Python libraries, APIs, ML pipelines, or any system component. Enforces loose coupling, SOLID principles, enterprise design patterns, and layered architecture. Applies to all Python and notebook files."
applyTo: ["**/*.py", "**/*.ipynb"]
---

# Architecture & Design Patterns

## SOLID Principles — Apply to Every Class (Non-Negotiable)

### S — Single Responsibility Principle
One class has exactly one reason to change. If a class does two things, split it.

```python
# BAD — one class handles two concerns
class ModelManager:
    def train(self, X, y): ...
    def save_to_disk(self, path): ...  # storage is a separate concern

# GOOD — each class has one job
class ModelTrainer:
    def train(self, X: np.ndarray, y: np.ndarray) -> tf.keras.Model: ...

class ModelRepository:
    def save(self, model: tf.keras.Model, path: pathlib.Path) -> None: ...
    def load(self, path: pathlib.Path) -> tf.keras.Model: ...
```

### O — Open/Closed Principle
Classes are open for extension, closed for modification. Add behaviour by creating new classes, not editing existing ones.

```python
# BAD — adding a new format requires modifying the class
class ReportExporter:
    def export(self, data: dict, format: str) -> None:
        if format == "csv": ...
        elif format == "json": ...  # every new format mutates this method

# GOOD — extend by adding a new class
from abc import ABC, abstractmethod

class ReportExporter(ABC):
    @abstractmethod
    def export(self, data: dict, output_path: pathlib.Path) -> None: ...

class CsvExporter(ReportExporter):
    def export(self, data: dict, output_path: pathlib.Path) -> None: ...

class JsonExporter(ReportExporter):
    def export(self, data: dict, output_path: pathlib.Path) -> None: ...
```

### L — Liskov Substitution Principle
A subclass must be usable wherever its parent is used, without breaking behaviour. Never override a method to raise `NotImplementedError` — use a separate interface instead.

```python
# BAD — subclass breaks the contract of the parent
class BaseTokenizer(ABC):
    @abstractmethod
    def encode(self, text: str) -> list[int]: ...
    @abstractmethod
    def batch_encode(self, texts: list[str]) -> list[list[int]]: ...

class SimpleTokenizer(BaseTokenizer):
    def encode(self, text: str) -> list[int]: ...
    def batch_encode(self, texts: list[str]) -> list[list[int]]:
        raise NotImplementedError("not supported")  # LSP violation

# GOOD — only promise what you can deliver
class Tokenizer(ABC):
    @abstractmethod
    def encode(self, text: str) -> list[int]: ...

class BatchCapableTokenizer(Tokenizer):
    @abstractmethod
    def batch_encode(self, texts: list[str]) -> list[list[int]]: ...
```

### I — Interface Segregation Principle
Clients must not be forced to depend on methods they do not use. Prefer many small, focused abstract classes over one large base class.

```python
# BAD — a read-only consumer is forced to carry write methods
class DataStore(ABC):
    @abstractmethod
    def read(self, key: str) -> bytes: ...
    @abstractmethod
    def write(self, key: str, value: bytes) -> None: ...
    @abstractmethod
    def delete(self, key: str) -> None: ...

# GOOD — split by capability
class ReadableStore(ABC):
    @abstractmethod
    def read(self, key: str) -> bytes: ...

class WritableStore(ABC):
    @abstractmethod
    def write(self, key: str, value: bytes) -> None: ...

class DeletableStore(ABC):
    @abstractmethod
    def delete(self, key: str) -> None: ...

# A full store composes all three; a cache only needs ReadableStore
class RedisStore(ReadableStore, WritableStore, DeletableStore): ...
class InMemoryReadCache(ReadableStore): ...
```

### D — Dependency Inversion Principle
High-level classes depend on abstractions. Abstractions must not depend on details. Wire concrete classes together only at the composition root (entry point / factory).

```python
# BAD — high-level Trainer knows about a concrete PostgresLogger
class Trainer:
    def __init__(self) -> None:
        self._logger = PostgresLogger()  # hardwired detail

# GOOD — inject the abstraction
class ExperimentLogger(ABC):
    @abstractmethod
    def log_metric(self, name: str, value: float, step: int) -> None: ...

class Trainer:
    def __init__(self, logger: ExperimentLogger) -> None:
        self._logger = logger  # receives abstraction, owns nothing concrete

# Composition root (main.py / factory) wires it together:
# trainer = Trainer(logger=PostgresLogger(dsn=...))
```

---

## Guiding Principles Summary

| Principle | Rule |
|-----------|------|
| **Loose Coupling** | Classes depend on ABCs, never on concrete implementations |
| **High Cohesion** | One class = one responsibility; split when a second reason to change appears |
| **Open/Closed** | New behaviour → new class; never edit stable code |
| **Dependency Inversion** | Inject abstractions; compose concrete objects only at the entry point |
| **Interface Segregation** | Many small ABCs over one large base class |

### Cycle-Free Design Rules (Required)

- Keep dependency graphs acyclic at every level: package, module, class, and service.
- Keep call graphs acyclic for normal control flow; avoid chains like `A.call() -> B.call() -> C.call() -> A.call()`.
- Avoid hidden cyclic logic through callbacks/events that feed into the same path without a terminal condition.
- Recursion is allowed only when explicitly required by the algorithm and must have a strict termination condition and depth bounds.
- If two modules depend on each other, extract the shared abstraction into a third module in the Domain layer.

---

## Layered Architecture (Apply to Every Non-Trivial Module)

```
┌─────────────────────────────────┐
│         Presentation Layer       │  notebooks, CLI, REST endpoints
├─────────────────────────────────┤
│         Application Layer        │  use-case classes, orchestrators
├─────────────────────────────────┤
│           Domain Layer           │  entities, value objects, domain services
├─────────────────────────────────┤
│       Infrastructure Layer       │  data loading, storage, external APIs
└─────────────────────────────────┘
```

- **No cross-layer imports** that skip levels.
- Infrastructure never imports from Application or Domain.
- Domain has zero infrastructure dependencies — it is plain Python classes with no I/O.
- Dependencies must flow one way only: Presentation -> Application -> Domain; Infrastructure implements Domain abstractions.
- Avoid god-modules/god-packages: split by responsibility and ownership.
- Keep package layout explicit (`domain/`, `application/`, `infra/`, `api/`) rather than mixing all code in one folder.

## Dual-Stack Architecture Rule (Python + Node.js)

When both Python and Node.js are present, treat both as enterprise services with explicit, non-overlapping responsibilities:

- Python owns ML/data/model-heavy logic (training, feature engineering, inference internals).
- Node.js owns API gateway/BFF/orchestration/realtime edge concerns where applicable.
- Keep shared business rules in one owning service only; other services consume via contracts.
- Enforce SOLID in both stacks independently.
- Define explicit inter-service contracts (REST/gRPC/events), versioned and documented.
- Never duplicate domain/business logic across Python and Node.js modules.

---

## Abstractions First — ABC Classes, Not Standalone Functions

Define the abstract contract before writing any concrete class. Every abstraction lives in the Domain layer and is expressed as an `ABC` class.

```python
from abc import ABC, abstractmethod
import numpy as np

class Tokenizer(ABC):
    """Abstract contract for all tokenizer implementations."""

    @abstractmethod
    def encode(self, text: str) -> list[int]: ...

    @abstractmethod
    def decode(self, ids: list[int]) -> str: ...


class VectorStore(ABC):
    """Abstract contract for all vector storage backends."""

    @abstractmethod
    def add(self, key: str, vector: np.ndarray) -> None: ...

    @abstractmethod
    def search(self, query: np.ndarray, top_k: int) -> list[str]: ...


# Application layer depends only on the ABC, never on BertTokenizer or FaissStore
class EmbeddingPipeline:
    def __init__(self, tokenizer: Tokenizer, store: VectorStore) -> None:
        self._tokenizer = tokenizer
        self._store = store

    def index(self, key: str, text: str) -> None:
        ids = self._tokenizer.encode(text)
        vector = np.array(ids, dtype=np.float32)
        self._store.add(key, vector)
```

---

## Core Design Patterns — When to Use Each

### Creational

| Pattern | When | Example |
|---------|------|---------|
| **Factory Method** | Object creation depends on config/type | `ModelFactory.create("bert-base")` |
| **Builder** | Complex object with many optional parts | `PipelineBuilder().with_tokenizer(...).with_encoder(...).build()` |
| **Singleton** | Exactly one instance needed (e.g., config, logger) | `ConfigRegistry.instance()` |
| **Registry** | Dynamic lookup of named implementations | `ModelRegistry.register("transformer", TransformerModel)` |

```python
# Registry — OOP class that maps names to concrete classes
class ModelRegistry:
    """Central registry for all model implementations. Open/Closed: add new
    models by calling register(); never edit this class."""

    def __init__(self) -> None:
        self._registry: dict[str, type] = {}

    def register(self, name: str, model_class: type) -> None:
        if name in self._registry:
            raise ValueError(f"Model '{name}' is already registered.")
        self._registry[name] = model_class

    def create(self, name: str, **kwargs) -> object:
        if name not in self._registry:
            raise KeyError(
                f"Model '{name}' not found. Registered: {sorted(self._registry)}"
            )
        return self._registry[name](**kwargs)

    def available(self) -> list[str]:
        return sorted(self._registry.keys())


# Factory Method — delegates construction logic to a class method
class ModelFactory:
    """Creates model instances from a config object. SRP: only responsible
    for construction, not training or serving."""

    def __init__(self, registry: ModelRegistry) -> None:
        self._registry = registry

    def create_from_config(self, config: "ModelConfig") -> object:
        return self._registry.create(config.model_name, config=config)


# Builder — constructs a complex pipeline step by step
class PipelineBuilder:
    def __init__(self) -> None:
        self._tokenizer: Tokenizer | None = None
        self._store: VectorStore | None = None

    def with_tokenizer(self, tokenizer: Tokenizer) -> "PipelineBuilder":
        self._tokenizer = tokenizer
        return self

    def with_store(self, store: VectorStore) -> "PipelineBuilder":
        self._store = store
        return self

    def build(self) -> EmbeddingPipeline:
        if self._tokenizer is None or self._store is None:
            raise ValueError("Both tokenizer and store must be set before build().")
        return EmbeddingPipeline(self._tokenizer, self._store)
```

### Structural

| Pattern | When | Example |
|---------|------|---------|
| **Adapter** | Wrap an incompatible interface | Adapt HuggingFace tokenizer to internal `Tokenizer` ABC |
| **Decorator** | Add behaviour without subclassing | `TimedTokenizer` wraps any `Tokenizer` with logging |
| **Facade** | Simplify a complex subsystem | `MLPipeline` hides tokenizer + encoder + indexer internals |
| **Composite** | Tree of uniform objects | `SequentialPipeline` containing a list of `PipelineStage` instances |

```python
import time
import logging
import pathlib

# Adapter — wraps a third-party class behind the internal ABC
class HuggingFaceTokenizerAdapter(Tokenizer):
    def __init__(self, hf_tokenizer) -> None:
        self._hf = hf_tokenizer

    def encode(self, text: str) -> list[int]:
        return self._hf(text)["input_ids"]

    def decode(self, ids: list[int]) -> str:
        return self._hf.decode(ids)


# Decorator — wraps another Tokenizer to add latency logging (OOP, not a function decorator)
class TimedTokenizer(Tokenizer):
    def __init__(self, inner: Tokenizer) -> None:
        self._inner = inner
        self._log = logging.getLogger(self.__class__.__name__)

    def encode(self, text: str) -> list[int]:
        start = time.perf_counter()
        result = self._inner.encode(text)
        self._log.info("encode completed in %.3fs", time.perf_counter() - start)
        return result

    def decode(self, ids: list[int]) -> str:
        return self._inner.decode(ids)


# Facade — hides the complexity of multiple subsystems behind one entry point
class MLPipeline:
    def __init__(
        self,
        tokenizer: Tokenizer,
        store: VectorStore,
        exporter: ReportExporter,
    ) -> None:
        self._tokenizer = tokenizer
        self._store = store
        self._exporter = exporter

    def run(self, key: str, text: str, report_path: pathlib.Path) -> None:
        ids = self._tokenizer.encode(text)
        vector = np.array(ids, dtype=np.float32)
        self._store.add(key, vector)
        self._exporter.export({"key": key, "dims": len(ids)}, report_path)
```

### Behavioural

| Pattern | When | Example |
|---------|------|---------|
| **Strategy** | Interchangeable algorithms | `LossStrategy` swapped between `CrossEntropyLoss` / `FocalLoss` |
| **Observer** | Decouple event producers from consumers | `TrainingCallback` system |
| **Command** | Encapsulate a request as an object | `TrainCommand`, `EvaluateCommand` each implement `execute()` |
| **Template Method** | Fixed skeleton, variable steps | `BaseTrainer.fit()` calls `self._train_step()` defined by subclass |
| **Pipeline / Chain of Responsibility** | Sequential processing stages | `list[PipelineStage]` each implementing `process()` |

```python
# Strategy — swap loss functions at runtime via injection
class LossStrategy(ABC):
    @abstractmethod
    def compute(self, y_true: np.ndarray, y_pred: np.ndarray) -> float: ...


class CrossEntropyLoss(LossStrategy):
    def compute(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        clipped = np.clip(y_pred, 1e-7, 1.0)
        return float(-np.mean(y_true * np.log(clipped)))


class FocalLoss(LossStrategy):
    def __init__(self, gamma: float = 2.0) -> None:
        self._gamma = gamma

    def compute(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        ce = CrossEntropyLoss().compute(y_true, y_pred)
        pt = np.exp(-ce)
        return float((1 - pt) ** self._gamma * ce)


# Template Method — base class owns the training loop skeleton
class BaseTrainer(ABC):
    def fit(self, X: np.ndarray, y: np.ndarray, epochs: int) -> None:
        for epoch in range(epochs):
            loss = self._train_step(X, y)
            self._log_epoch(epoch, loss)

    @abstractmethod
    def _train_step(self, X: np.ndarray, y: np.ndarray) -> float: ...

    def _log_epoch(self, epoch: int, loss: float) -> None:
        logging.getLogger(self.__class__.__name__).info(
            "epoch=%d loss=%.4f", epoch, loss
        )


class GradientDescentTrainer(BaseTrainer):
    def __init__(self, loss: LossStrategy, learning_rate: float = 0.01) -> None:
        self._loss = loss
        self._lr = learning_rate
        self._weights: np.ndarray = np.array([])

    def _train_step(self, X: np.ndarray, y: np.ndarray) -> float:
        y_pred = X @ self._weights
        return self._loss.compute(y, y_pred)


# Command — encapsulate each action as a class with execute()
class Command(ABC):
    @abstractmethod
    def execute(self) -> None: ...


class TrainCommand(Command):
    def __init__(self, trainer: BaseTrainer, X: np.ndarray, y: np.ndarray) -> None:
        self._trainer = trainer
        self._X = X
        self._y = y

    def execute(self) -> None:
        self._trainer.fit(self._X, self._y, epochs=10)
```

---

## Library Design Rules

When building a reusable Python library (anything in `foundation/`):

1. **Public API contract first** — define the public interface (protocols/abstract classes) before implementations.
2. **Semantic versioning** — `MAJOR.MINOR.PATCH`; breaking changes bump MAJOR.
3. **No internal state leakage** — never expose mutable internal data structures directly.
4. **Configuration as value objects** — use `dataclass(frozen=True)` for all config objects.
5. **Fail fast and loud** — validate inputs at public API boundaries; raise `ValueError` / `TypeError` with clear messages.

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class TokenizerConfig:
    vocab_size: int
    max_length: int
    lowercase: bool = True
    oov_token: str = "<OOV>"

    def __post_init__(self) -> None:
        if self.vocab_size < 1:
            raise ValueError(f"vocab_size must be >= 1, got {self.vocab_size}")
        if self.max_length < 1:
            raise ValueError(f"max_length must be >= 1, got {self.max_length}")
```

---

## API Design Rules (REST / gRPC / Python API)

1. **Resource-oriented**: nouns, not verbs — `/embeddings`, not `/getEmbedding`.
2. **Consistent error contracts**: always return structured errors with `code`, `message`, `details`.
3. **Idempotency**: GET and PUT must be idempotent; POST creates, PATCH updates.
4. **Versioning**: prefix all routes with `/v1/`, `/v2/` — never break existing consumers.
5. **Schema-first**: define request/response with Pydantic models before writing handlers.

```python
from pydantic import BaseModel, Field

class EmbedRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=8192)
    model: str = Field(default="text-embedding-v1")

class EmbedResponse(BaseModel):
    embedding: list[float]
    token_count: int
    model: str
    latency_ms: float
```

---

## Quality Gates

- [ ] No concrete class imported directly by a higher-level module (use Protocol/ABC injection).
- [ ] No `isinstance` checks on domain objects — use polymorphism.
- [ ] Config objects are immutable `dataclass(frozen=True)`.
- [ ] Every public API function validates its inputs at the boundary.
- [ ] No circular imports — verify with `pydeps` or import graph check.
