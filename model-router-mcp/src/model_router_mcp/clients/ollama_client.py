from __future__ import annotations

from collections.abc import Mapping

import httpx

from model_router_mcp.models import RoutedResponse
from model_router_mcp.models import TokenUsage


class OllamaClient:
    """Thin HTTP client for an Ollama text-generation backend."""

    def __init__(self, base_url: str, model_name: str, timeout_seconds: float) -> None:
        self._base_url = base_url.rstrip("/")
        self._model_name = model_name
        self._client = httpx.Client(base_url=self._base_url, timeout=timeout_seconds)

    def generate(self, prompt: str, system_prompt: str | None = None) -> RoutedResponse:
        """Generate a text response from Ollama."""

        payload: dict[str, object] = {
            "model": self._model_name,
            "prompt": prompt,
            "stream": False,
        }
        if system_prompt:
            payload["system"] = system_prompt

        response = self._client.post("/api/generate", json=payload)
        response.raise_for_status()
        body = response.json()
        text = body.get("response")
        if not isinstance(text, str):
            raise RuntimeError("Ollama response payload did not include text content.")

        model_name = body.get("model")
        if not isinstance(model_name, str):
            model_name = self._model_name

        prompt_tokens = self._as_int_or_none(body.get("prompt_eval_count"))
        completion_tokens = self._as_int_or_none(body.get("eval_count"))
        total_tokens = None
        if prompt_tokens is not None and completion_tokens is not None:
            total_tokens = prompt_tokens + completion_tokens

        return RoutedResponse(
            selected_model_family="ollama",
            selected_model_name=model_name,
            response_text=text.strip(),
            token_usage=TokenUsage(
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=total_tokens,
            ),
        )

    def health_check(self) -> Mapping[str, object]:
        """Return a lightweight health payload."""

        response = self._client.get("/api/tags")
        response.raise_for_status()
        return response.json()

    def close(self) -> None:
        """Close the underlying HTTP session."""

        self._client.close()

    @staticmethod
    def _as_int_or_none(value: object) -> int | None:
        if isinstance(value, int):
            return value
        return None
