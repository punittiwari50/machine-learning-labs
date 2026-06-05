from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ModelFamily(StrEnum):
    """Supported model families."""

    GEMMA = "gemma"
    DEEPSEEK = "deepseek"
    QWEN = "qwen"


@dataclass(frozen=True, slots=True)
class BackendStatus:
    """Simple reachability status payload."""

    name: str
    base_url: str
    reachable: bool
    detail: str


@dataclass(frozen=True, slots=True)
class TokenUsage:
    """Normalized token accounting for model responses."""

    prompt_tokens: int | None
    completion_tokens: int | None
    total_tokens: int | None


@dataclass(frozen=True, slots=True)
class RoutedResponse:
    """Standard response payload returned by MCP ask tools."""

    selected_model_family: str
    selected_model_name: str
    response_text: str
    token_usage: TokenUsage
