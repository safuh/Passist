from typing import Any

import httpx

from app.ai.providers.base import (
    AIMessage,
    AIProvider,
    ChatRequest,
    ChatResponse,
    EmbeddingResponse,
    ModelInfo,
)


class OllamaProvider(AIProvider):
    provider_type = "ollama"

    def __init__(self, base_url: str = "http://127.0.0.1:11434", timeout: float = 120.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _client(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout)

    async def chat(self, request: ChatRequest) -> ChatResponse:
        payload: dict[str, Any] = {
            "model": request.model,
            "messages": [
                {"role": message.role, "content": message.content}
                for message in request.messages
            ],
            "stream": False,
        }

        options: dict[str, Any] = {}
        if request.temperature is not None:
            options["temperature"] = request.temperature
        if request.max_tokens is not None:
            options["num_predict"] = request.max_tokens
        if options:
            payload["options"] = options

        async with self._client() as client:
            response = await client.post("/api/chat", json=payload)
            response.raise_for_status()
            data = response.json()

        message = data.get("message") or {}
        prompt_tokens = data.get("prompt_eval_count")
        completion_tokens = data.get("eval_count")

        return ChatResponse(
            content=message.get("content", ""),
            model=data.get("model", request.model),
            provider=self.provider_type,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=(
                prompt_tokens + completion_tokens
                if prompt_tokens is not None and completion_tokens is not None
                else None
            ),
        )

    async def embeddings(self, texts: list[str], model: str) -> EmbeddingResponse:
        async with self._client() as client:
            response = await client.post(
                "/api/embed",
                json={"model": model, "input": texts},
            )
            response.raise_for_status()
            data = response.json()

        return EmbeddingResponse(
            embeddings=data.get("embeddings", []),
            model=model,
            provider=self.provider_type,
        )

    async def list_models(self) -> list[ModelInfo]:
        async with self._client() as client:
            response = await client.get("/api/tags")
            response.raise_for_status()
            data = response.json()

        return [
            ModelInfo(id=model["name"], provider=self.provider_type)
            for model in data.get("models", [])
            if model.get("name")
        ]
