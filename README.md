# PAssist — AI Operating Platform

PAssist is a provider-agnostic **AI Operating Platform**, not a single chatbot. It is being built as a durable backend capable of hosting multiple AI providers, agents, tools, retrieval systems, plugins, authenticated users, and eventually multi-user/workspace deployments.

> The project is also a reference implementation of a reusable Python backend foundation. The framework is not the architecture: FastAPI supplies the HTTP layer, while the application owns the domain, security, persistence, provider abstractions, and runtime boundaries.

## Vision

```text
Browser / Desktop / Mobile
            |
       API Gateway
            |
   +--------+---------+
   |                  |
Authentication     Cross-cutting
Authorization       Rate limits
   |               Audit / observability
   +--------+---------+
            |
      FastAPI Application
            |
  +---------+---------+---------+---------+
  |         |         |         |         |
Identity Conversations AI Runtime Tool Runtime Documents
  |         |         +-- providers         +-- RAG
  |         |            +-- Ollama        +-- vector store
  |         |            +-- OpenAI        +-- ingestion
  |         |            +-- future
  |         |
  +---------+------------------------------------+
                    |
             SQLAlchemy 2.x
                    |
                 Alembic
                    |
                PostgreSQL
```

## Core principles

### Provider agnostic
No conversation, tool, memory, or API layer should know whether the model is Ollama, OpenAI, Gemini, Anthropic, or another provider. Provider-specific behavior belongs behind the `AIProvider` interface and registry.

### Stateless API
Access authentication uses signed JWTs. Refresh tokens are stored only as hashes and are rotated/revoked through persisted authentication sessions. The API does not require server-side HTTP sessions.

### Domain-driven modules
Bounded contexts own their models, repositories, services, schemas, and routers. The current structure includes Identity and AI configuration and reserves boundaries for Conversations, Documents, Tools, Plugins, Memory, and Settings.

### Dependency inversion
Application logic depends on contracts and services rather than concrete HTTP SDKs or provider libraries. Infrastructure adapters implement those contracts.

### Configuration over code
Providers, models, endpoints, and enabled capabilities are persisted as configuration. Adding a provider should not require modifying conversation logic.

### Migrations from day one
Alembic is part of the application foundation. Schema changes are versioned and reproducible.

### Async first
The API, SQLAlchemy database layer, and provider adapters use asynchronous I/O where appropriate. This is important for concurrent model calls, database operations, and external tool execution.

### UTC everywhere
Application timestamps are UTC-aware. The custom `UTCDateTime` type normalizes SQLite's timezone limitations while preserving PostgreSQL `TIMESTAMP WITH TIME ZONE` semantics.

## Technology stack

| Layer | Technology |
|---|---|
| API | FastAPI |
| ORM | SQLAlchemy 2.x async |
| Validation | Pydantic v2 |
| Configuration | pydantic-settings |
| Authentication | JWT / OAuth2 bearer semantics |
| Password hashing | Argon2 |
| Database | PostgreSQL production / SQLite development |
| Migrations | Alembic |
| Logging | structlog |
| HTTP client | httpx |
| Secret encryption | cryptography / Fernet |
| AI runtime | Provider interface + registry |
| Local model | Ollama |
| Cloud-compatible model APIs | OpenAI-compatible adapter |
| Vector store | ChromaDB planned |
| Cache | Redis planned |
| Background work | Celery or Dramatiq planned |
| Frontend | Astro / React / Flutter — decision pending |

## Current project structure

```text
Passist/
├── app/
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── exceptions.py
│   │   ├── lifespan.py
│   │   ├── logging.py
│   │   ├── secrets.py
│   │   └── security.py
│   │
│   ├── identity/
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── repository.py
│   │   ├── service.py
│   │   ├── router.py
│   │   └── security.py
│   │
│   ├── ai/
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── repository.py
│   │   ├── service.py
│   │   ├── registry.py
│   │   ├── router.py
│   │   └── providers/
│   │       ├── base.py
│   │       ├── ollama.py
│   │       └── openai.py
│   │
│   ├── conversations/
│   ├── documents/
│   ├── memory/
│   ├── tools/
│   ├── plugins/
│   ├── settings/
│   └── main.py
│
├── alembic/
├── tests/
├── scripts/
├── docker/
├── frontend/
├── .env
└── pyproject.toml
```

## Identity foundation

The identity bounded context currently provides:

- users
- roles
- permissions
- user-role many-to-many relationships
- role-permission relationships
- hashed refresh-token sessions
- API-key persistence foundation
- OAuth account persistence foundation
- Argon2 password hashing
- JWT access tokens
- refresh-token rotation
- logout/revocation
- authenticated `/api/auth/me`
- async-safe eager relationship loading

Refresh tokens are never persisted in plaintext. API keys are hashed. AI provider API keys are encrypted before persistence.

## AI runtime foundation

The first AI runtime brick deliberately separates the application from providers.

```text
AIService
    |
ProviderRepository
    |
Provider configuration
    |
ProviderRegistry
    |
+--------------------------+
| AIProvider contract      |
+--------------------------+
       |             |
   Ollama       OpenAI-compatible
```

The provider contract currently covers:

- chat completions
- embeddings
- model discovery
- future streaming

The first adapters are:

- `ollama`
- `openai_compatible`

The registry is extensible: future Anthropic, Gemini, local servers, or custom providers can be registered without changing the conversation service.

## Security model

```text
Password
   |
   +--> Argon2 hash

Login
   |
   +--> short-lived JWT access token
   |
   +--> random refresh token
            |
            +--> SHA-256 hash in sessions table

Refresh
   |
   +--> validate hash / expiry / revocation
   +--> revoke old session
   +--> issue new refresh token
   +--> issue new access token

Provider API key
   |
   +--> Fernet encryption
   +--> encrypted database value
   +--> decrypt only when constructing provider runtime
```

For production, the application secret must be generated securely and injected through a secret-management system. The current encryption utility derives its Fernet key from `SECRET_KEY`; a dedicated KMS/secret provider can replace this without changing the AI domain contract.

## Local development

```bash
conda activate passist
pip install -e '.[dev]'
```

Create `.env` from your local environment and never commit secrets.

Run migrations:

```bash
alembic upgrade head
```

Start the API:

```bash
uvicorn app.main:app --reload
```

Health check:

```bash
curl http://localhost:8000/health
```

Authentication endpoints:

```text
POST /api/auth/register
POST /api/auth/login
POST /api/auth/refresh
POST /api/auth/logout
GET  /api/auth/me
```

AI configuration endpoints:

```text
GET  /api/ai/provider-types
GET  /api/ai/providers
POST /api/ai/providers
```

## Example provider configuration

Ollama:

```json
{
  "name": "local-ollama",
  "provider_type": "ollama",
  "base_url": "http://127.0.0.1:11434",
  "default_model": "qwen3",
  "enabled": true
}
```

OpenAI-compatible API:

```json
{
  "name": "cloud-models",
  "provider_type": "openai_compatible",
  "base_url": "https://api.openai.com/v1",
  "api_key": "<secret>",
  "default_model": "<model-id>",
  "enabled": true
}
```

The API never returns the encrypted provider key.

## Database strategy

Development uses SQLite for low-friction local setup. Production is PostgreSQL.

The application uses SQLAlchemy 2.x's async engine and keeps `expire_on_commit=False`. Async ORM code avoids implicit relationship I/O; relationships that are needed are eagerly loaded with `selectinload` or explicitly assigned. This prevents the `MissingGreenlet` class of failures that occurs when traditional lazy loading attempts database I/O during ordinary attribute access.

## Roadmap

See [`docs/MILESTONES.md`](docs/MILESTONES.md) for the completion tracker.

High-level sequence:

1. Foundation
2. Identity and authorization
3. AI provider abstraction
4. Provider registry/configuration
5. Conversations and messages
6. Streaming
7. Tool runtime
8. Documents and RAG
9. Memory/personalization
10. Workspaces/organizations/multi-tenancy
11. Production observability, rate limiting, background jobs, and deployment hardening

## Reusable backend foundation

The architectural foundation developed here is intentionally reusable outside AI applications. The genericized version is maintained separately as [FastApiBackbone](https://github.com/safuh/FastApiBackbone).

That repository focuses on the stable backend substrate: configuration, async database lifecycle, Alembic, structured logging, API composition, health checks, and clean extension points. PAssist demonstrates how a real domain can be layered on top of it.

## Status

PAssist is under active construction. The current objective is not to rush to a chat screen; it is to establish a foundation that remains maintainable as the system grows into multiple providers, agents, tools, knowledge stores, users, and deployments.
