from app.ai.providers.ollama import OllamaProvider
from app.ai.providers.openai import OpenAICompatibleProvider
from app.ai.registry import ProviderRegistry


def test_default_registry_exposes_supported_provider_types() -> None:
    registry = ProviderRegistry()

    assert registry.supported_types() == (
        "ollama",
        "openai_compatible",
    )


def test_registry_creates_ollama_provider() -> None:
    provider = ProviderRegistry().create(
        "ollama",
        base_url="http://127.0.0.1:11434",
    )

    assert isinstance(provider, OllamaProvider)


def test_registry_creates_openai_compatible_provider() -> None:
    provider = ProviderRegistry().create(
        "openai_compatible",
        base_url="https://api.openai.com/v1",
        api_key="test-key",
    )

    assert isinstance(provider, OpenAICompatibleProvider)


def test_registry_rejects_unknown_provider() -> None:
    try:
        ProviderRegistry().create("does-not-exist")
    except ValueError as exc:
        assert "Unsupported AI provider type" in str(exc)
    else:
        raise AssertionError("Unknown provider type should fail")
