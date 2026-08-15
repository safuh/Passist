from collections.abc import Callable

from app.ai.providers.base import AIProvider
from app.ai.providers.ollama import OllamaProvider
from app.ai.providers.openai import OpenAICompatibleProvider


ProviderFactory = Callable[[str | None, str | None], AIProvider]


class ProviderRegistry:
    """Maps persisted provider types to concrete adapters.

    Application services depend on this registry rather than importing a
    concrete AI SDK/provider implementation.
    """

    def __init__(self) -> None:
        self._factories: dict[str, ProviderFactory] = {}
        self.register(
            "ollama",
            lambda base_url, api_key: OllamaProvider(
                base_url=base_url or "http://127.0.0.1:11434"
            ),
        )
        self.register(
            "openai_compatible",
            lambda base_url, api_key: OpenAICompatibleProvider(
                base_url=base_url or "https://api.openai.com/v1",
                api_key=api_key,
            ),
        )

    def register(self, provider_type: str, factory: ProviderFactory) -> None:
        if not provider_type.strip():
            raise ValueError("Provider type cannot be empty.")
        self._factories[provider_type] = factory

    def create(
        self,
        provider_type: str,
        *,
        base_url: str | None = None,
        api_key: str | None = None,
    ) -> AIProvider:
        factory = self._factories.get(provider_type)
        if factory is None:
            raise ValueError(f"Unsupported AI provider type: {provider_type}")
        return factory(base_url, api_key)

    def supported_types(self) -> tuple[str, ...]:
        return tuple(sorted(self._factories))


provider_registry = ProviderRegistry()
