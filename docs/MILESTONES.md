# PAssist Milestone / Completion Tracker

Last updated: 2026-08-15

Status legend:

- `[x]` Complete and committed
- `[~]` In progress / partially complete
- `[ ]` Planned

## Phase 0 — Architecture and foundation

### M0.1 Architecture

- [x] Provider-agnostic architecture defined
- [x] Domain/bounded-context structure defined
- [x] Dependency inversion principle established
- [x] Stateless JWT authentication direction established
- [x] Async-first application direction established
- [x] Configuration-over-code principle established
- [x] PostgreSQL production / SQLite development strategy established
- [x] Alembic migration strategy established

### M0.2 Application foundation

- [x] `pyproject.toml`
- [x] pydantic-settings configuration
- [x] async SQLAlchemy engine/session factory
- [x] application lifespan
- [x] structured logging
- [x] timezone-aware UTC datetime handling
- [x] Alembic async environment
- [x] database migrations from day one

## Phase 1 — Identity

### M1.1 Identity schema

- [x] users
- [x] roles
- [x] permissions
- [x] user_roles
- [x] role_permissions
- [x] sessions / refresh-token persistence
- [x] API key persistence foundation
- [x] OAuth account persistence foundation
- [x] default `user` role migration

### M1.2 Authentication

- [x] Argon2 password hashing
- [x] registration
- [x] login
- [x] JWT access tokens
- [x] refresh tokens
- [x] refresh-token hashing
- [x] refresh-token rotation
- [x] refresh-token revocation
- [x] logout
- [x] authenticated `/me`
- [x] inactive-account rejection
- [x] async-safe relationship loading
- [x] UTC-aware refresh-token expiry checks
- [ ] authentication integration test suite

### M1.3 Authorization

- [~] role/permission data model
- [ ] permission constants / naming convention
- [ ] `require_permission(...)` dependency
- [ ] role management service
- [ ] API-key authentication
- [ ] API-key lifecycle endpoints
- [ ] authorization integration tests

## Phase 2 — AI runtime

### M2.1 Provider abstraction

- [x] provider-neutral message contract
- [x] provider-neutral chat response
- [x] embeddings contract
- [x] model discovery contract
- [~] streaming contract defined
- [x] no provider SDK dependency in application services

### M2.2 Provider adapters

- [x] Ollama adapter
- [x] OpenAI-compatible adapter
- [ ] Anthropic adapter
- [ ] Gemini adapter
- [ ] generic custom HTTP provider adapter
- [ ] provider capability negotiation
- [ ] provider error normalization
- [ ] provider retry/backoff policy
- [ ] provider health checks

### M2.3 Provider registry/configuration

- [x] persisted provider configuration model
- [x] owner-scoped provider repository
- [x] provider registry
- [x] provider type discovery endpoint
- [x] encrypted provider API-key persistence
- [x] provider creation endpoint
- [x] provider listing endpoint
- [ ] provider update endpoint
- [ ] provider delete endpoint
- [ ] provider test-connection endpoint
- [ ] default provider/model selection
- [ ] provider-level permissions

## Phase 3 — Conversations

- [ ] conversation entity
- [ ] message entity
- [ ] message roles
- [ ] conversation ownership
- [ ] model/provider selection metadata
- [ ] token/usage accounting
- [ ] conversation service
- [ ] conversation repository
- [ ] conversation API
- [ ] context-window management
- [ ] message pagination
- [ ] soft deletion / archival

## Phase 4 — Streaming and runtime execution

- [ ] streaming provider contract
- [ ] SSE response layer
- [ ] cancellation handling
- [ ] timeout policy
- [ ] partial-response persistence strategy
- [ ] provider error mapping
- [ ] request correlation IDs
- [ ] runtime telemetry

## Phase 5 — Tool Runtime

- [ ] tool interface
- [ ] tool schema / JSON Schema contract
- [ ] tool registry
- [ ] tool permissions
- [ ] tool execution sandbox boundary
- [ ] tool invocation audit events
- [ ] email tool
- [ ] calendar tool
- [ ] filesystem/document tool
- [ ] database tool
- [ ] custom tool/plugin interface
- [ ] tool result normalization

## Phase 6 — Documents and RAG

- [ ] document entity
- [ ] document versions
- [ ] ingestion pipeline
- [ ] text extraction
- [ ] chunking strategy
- [ ] embedding pipeline
- [ ] ChromaDB integration
- [ ] retrieval service
- [ ] citation metadata
- [ ] access-control-aware retrieval
- [ ] background ingestion jobs

## Phase 7 — Memory and personalization

- [ ] memory model
- [ ] explicit user memories
- [ ] inferred memory policy
- [ ] memory retrieval
- [ ] memory write/update/delete
- [ ] privacy controls
- [ ] memory expiration / lifecycle
- [ ] personalization context builder

## Phase 8 — Agents and plugins

- [ ] agent model
- [ ] agent configuration
- [ ] system prompts
- [ ] agent tool permissions
- [ ] agent/provider selection
- [ ] agent execution runtime
- [ ] plugin manifest
- [ ] plugin registry
- [ ] plugin permissions/capabilities
- [ ] plugin lifecycle/versioning

## Phase 9 — Multi-user / multi-tenant deployment

- [ ] workspace model
- [ ] organization model
- [ ] memberships
- [ ] workspace roles
- [ ] resource ownership boundaries
- [ ] tenant-aware repositories
- [ ] tenant-aware authorization
- [ ] per-tenant provider configuration
- [ ] per-tenant rate limits
- [ ] isolation tests

## Phase 10 — Production hardening

- [ ] Redis cache
- [ ] distributed rate limiting
- [ ] background workers (Celery or Dramatiq)
- [ ] audit event pipeline
- [ ] structured application metrics
- [ ] tracing / OpenTelemetry
- [ ] database connection-pool tuning
- [ ] health/readiness probes
- [ ] graceful shutdown under load
- [ ] secrets manager/KMS integration
- [ ] containerization
- [ ] CI/CD
- [ ] automated migration deployment
- [ ] backup/restore procedures
- [ ] security review
- [ ] load testing
- [ ] failure-mode testing

## Current checkpoint

**Completed:** Foundation + core identity + initial AI abstraction/registry.

**Current active work:** Finish Identity authorization/API-key lifecycle and then build Conversations.

**Architectural rule:** A milestone is not considered complete merely because the endpoint works. It is complete when its domain model, service boundary, persistence behavior, failure modes, security implications, tests, and migration path are sufficiently defined for the next layer to depend on it.
