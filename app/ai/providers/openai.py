from typing import Any

import httpx

from app.ai.providers.base import AIProvider, ChatRequest, ChatResponse, EmbeddingResponse, ModelInfo


class OpenAICompatibleProvider(AIProvider):
    """Adapter for OpenAI and APIs exposing OpenAI-compatible endpoints."""

    provider_type = "openai_compatible"

    def __init__(
        self,
        base_url: str = "https://api.openai.com/v1",
        api_key: str | None = None,
        timeout: float = 120.0,
    ):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout

    def _client(self) -> httpx.AsyncClient:
        headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
        return httpx.AsyncClient(
            base_url=self.base_url,
            headers=headers,
            timeout=self.timeout,
        )

    async def chat(self, request: ChatRequest) -> ChatResponse:
        payload: dict[str, Any] = {
            "model": request.model,
            "messages": [
                {"role": message.role, "content": message.content}
                for message in request.messages
            ],
        }
        if request.temperature is not None:
            payload["temperature"] = request.temperature
        if request.max_tokens is not None:
            payload["max_tokens"] = request.max_tokens

        async with self._client() as client:
            response = await client.post("/chat/completions", json=payload)
            response.raise_for_status()
            data = response.json()

        choice = (data.get("choices") or [{}])[0]
        message = choice.get("message") or {}
        usage = data.get("usage") or {}

        return ChatResponse(
            content=message.get("content", ""),
            model=data.get("model", request.model),
            provider=self.provider_type,
            prompt_tokens=usage.get("prompt_tokens"),
            completion_tokens=usage.get("completion_tokens"),
            total_tokens=usage.get("total_tokens"),
        )

    async def embeddings(self, texts: list[str], model: str) -> EmbeddingResponse:
        async with self._client() as client:
            response = await client.post(
                "/embeddings",
                json={"model": model, "input": texts},
            )
            response.raise_for_status()
            data = response.json()

        vectors = [item["embedding"] for item in data.get("data", [])]
        return EmbeddingResponse(
            embeddings=vectors,
            model=model,
            provider=self.provider_type,
        )

    async def list_models(self) -> list[ModelInfo]:
        async with self._client() as client:
            response = await client.get("/models")
            response.raise_for_status()
            data = response.json()

        return [
            ModelInfo(id=model["id"], provider=self.provider_type)
            for model in data.get("data", [])
            if model.get("id")
        ]
