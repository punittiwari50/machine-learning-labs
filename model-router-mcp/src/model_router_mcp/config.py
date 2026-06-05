from __future__ import annotations

from dataclasses import dataclass
from os import environ


@dataclass(frozen=True, slots=True)
class ModelEndpointConfig:
    """Configuration for a single model endpoint."""

    base_url: str
    model_name: str


@dataclass(frozen=True, slots=True)
class AppConfig:
    """Runtime configuration loaded from environment variables."""

    gemma: ModelEndpointConfig
    deepseek: ModelEndpointConfig
    qwen: ModelEndpointConfig
    request_timeout_seconds: float = 180.0

    @classmethod
    def from_env(cls) -> "AppConfig":
        """Build configuration from environment variables."""

        return cls(
            gemma=ModelEndpointConfig(
                base_url=environ.get(
                    "GEMMA_BASE_URL",
                    "http://host.docker.internal:11434",
                ),
                model_name=environ.get("GEMMA_MODEL", "gemma3:latest"),
            ),
            deepseek=ModelEndpointConfig(
                base_url=environ.get(
                    "DEEPSEEK_BASE_URL",
                    "http://host.docker.internal:11435",
                ),
                model_name=environ.get("DEEPSEEK_MODEL", "deepseek-r1:latest"),
            ),
            qwen=ModelEndpointConfig(
                base_url=environ.get(
                    "QWEN_BASE_URL",
                    "http://host.docker.internal:11436",
                ),
                model_name=environ.get("QWEN_MODEL", "qwen3:latest"),
            ),
            request_timeout_seconds=float(
                environ.get("REQUEST_TIMEOUT_SECONDS", "180.0")
            ),
        )
