from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AIMessage:
    role: str
    content: str


@dataclass(frozen=True, slots=True)
class ChatRequest:
    messages: list[AIMessage]
    model: str
    temperature: float | None = None
    max_tokens: int | None = None


@dataclass(frozen=True, slots=True)
class ChatResponse:
    content: str
    model: str
    provider: str
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None


@dataclass(frozen=True, slots=True)
class EmbeddingResponse:
    embeddings: list[list[float]]
    model: str
    provider: str


@dataclass(frozen=True, slots=True)
class ModelInfo:
    id: str
    provider: str
    capabilities: tuple[str, ...] = ()


class AIProvider(ABC):
    """Provider-neutral contract used by the AI runtime."""

    provider_type: str

    @abstractmethod
    async def chat(self, request: ChatRequest) -> ChatResponse:
        raise NotImplementedError

    @abstractmethod
    async def embeddings(self, texts: list[str], model: str) -> EmbeddingResponse:
        raise NotImplementedError

    @abstractmethod
    async def list_models(self) -> list[ModelInfo]:
        raise NotImplementedError

    async def stream_chat(self, request: ChatRequest) -> AsyncIterator[str]:
        """Optional streaming contract; providers implement when supported."""
        raise NotImplementedError(
            f"{self.provider_type} does not implement streaming yet."
        )
        yield ""
