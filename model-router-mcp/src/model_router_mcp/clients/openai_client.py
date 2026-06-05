from __future__ import annotations

from base64 import b64encode
from collections.abc import Sequence
from mimetypes import guess_type
from pathlib import Path

import httpx

from model_router_mcp.models import RoutedResponse
from model_router_mcp.models import TokenUsage


class OpenAICompatibleClient:
    """HTTP client for OpenAI-compatible chat-completions endpoints."""

    def __init__(self, base_url: str, model_name: str, timeout_seconds: float) -> None:
        self._base_url = base_url.rstrip("/")
        self._model_name = model_name
        self._client = httpx.Client(base_url=self._base_url, timeout=timeout_seconds)

    def chat(
        self,
        prompt: str,
        system_prompt: str | None = None,
        image_urls: Sequence[str] | None = None,
        image_paths: Sequence[str] | None = None,
    ) -> RoutedResponse:
        """Send a chat request and return the assistant message text."""

        messages: list[dict[str, object]] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        user_content: list[dict[str, object]] = [{"type": "text", "text": prompt}]
        for image_url in image_urls or []:
            user_content.append({"type": "image_url", "image_url": {"url": image_url}})
        for image_path in image_paths or []:
            user_content.append(
                {
                    "type": "image_url",
                    "image_url": {
                        "url": self._image_path_to_data_url(Path(image_path)),
                    },
                }
            )

        messages.append({"role": "user", "content": user_content})

        response = self._client.post(
            "/v1/chat/completions",
            json={
                "model": self._model_name,
                "messages": messages,
                "temperature": 0.2,
            },
        )
        response.raise_for_status()
        body = response.json()
        choices = body.get("choices")
        if not isinstance(choices, list) or not choices:
            raise RuntimeError("OpenAI-compatible response did not include choices.")
        message = choices[0].get("message", {})
        if not isinstance(message, dict):
            raise RuntimeError(
                "OpenAI-compatible response did not include a message object."
            )
        content = message.get("content")
        if not isinstance(content, str):
            raise RuntimeError(
                "OpenAI-compatible response did not include text content."
            )

        model_name = body.get("model")
        if not isinstance(model_name, str):
            model_name = self._model_name

        usage_payload = body.get("usage")
        usage = self._extract_usage(usage_payload)

        return RoutedResponse(
            selected_model_family="openai-compatible",
            selected_model_name=model_name,
            response_text=content.strip(),
            token_usage=usage,
        )

    def health_check(self) -> dict[str, object]:
        """Return the models list payload if the endpoint is reachable."""

        response = self._client.get("/v1/models")
        response.raise_for_status()
        return response.json()

    def close(self) -> None:
        """Close the underlying HTTP session."""

        self._client.close()

    @staticmethod
    def _image_path_to_data_url(path: Path) -> str:
        """Convert a local image path to a data URL for multimodal requests."""

        if not path.exists():
            raise FileNotFoundError(f"Image file not found: {path}")

        mime_type = guess_type(path.name)[0] or "image/png"
        encoded = b64encode(path.read_bytes()).decode("ascii")
        return f"data:{mime_type};base64,{encoded}"

    @staticmethod
    def _extract_usage(payload: object) -> TokenUsage:
        if not isinstance(payload, dict):
            return TokenUsage(
                prompt_tokens=None,
                completion_tokens=None,
                total_tokens=None,
            )

        prompt_tokens = payload.get("prompt_tokens")
        completion_tokens = payload.get("completion_tokens")
        total_tokens = payload.get("total_tokens")

        return TokenUsage(
            prompt_tokens=prompt_tokens if isinstance(prompt_tokens, int) else None,
            completion_tokens=(
                completion_tokens if isinstance(completion_tokens, int) else None
            ),
            total_tokens=total_tokens if isinstance(total_tokens, int) else None,
        )
