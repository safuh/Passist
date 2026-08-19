# PAssist Milestone / Completion Tracker

Last updated: 2026-08-19

Status legend:
- `[x]` Complete and committed
- `[~]` In progress / partially complete
- `[ ]` Planned

## Phase 0 — Architecture and foundation
- [x] Provider-agnostic architecture
- [x] Domain/bounded-context structure
- [x] Dependency inversion
- [x] Stateless JWT direction
- [x] Async-first direction
- [x] Configuration-over-code
- [x] PostgreSQL production / SQLite development strategy
- [x] Alembic migration strategy
- [x] pydantic-settings configuration
- [x] async SQLAlchemy engine/session factory
- [x] application lifespan
- [x] structured logging
- [x] UTC-aware datetime handling
- [x] async Alembic environment

## Phase 1 — Identity

### M1.1 Schema
- [x] users, roles, permissions
- [x] user_roles, role_permissions
- [x] sessions / refresh-token persistence
- [x] API key persistence
- [x] OAuth account persistence
- [x] default user role
- [x] default permission seed migration

### M1.2 Authentication
- [x] Argon2 password hashing
- [x] registration / login
- [x] JWT access tokens
- [x] refresh-token hashing and rotation
- [x] revocation / logout
- [x] authenticated `/me`
- [x] inactive-account rejection
- [x] async-safe relationship loading
- [x] UTC-aware expiry checks
- [ ] authentication integration test suite

### M1.3 Authorization and API keys
- [x] stable permission constants
- [x] `require_permission(...)`
- [x] role/permission resolution
- [x] JWT and `X-API-Key` principal authentication
- [x] one-time API-key secret issuance
- [x] API-key listing without secrets
- [x] API-key revocation
- [x] API-key expiry and last-used tracking
- [x] authorization unit tests
- [ ] role management service
- [ ] authorization integration tests
- [ ] scoped API-key capabilities

## Phase 2 — AI runtime
### M2.1 Provider abstraction
- [x] provider-neutral message contract
- [x] provider-neutral chat response
- [x] embeddings contract
- [x] model discovery contract
- [~] streaming contract
- [x] application services independent of provider SDKs

### M2.2 Provider adapters
- [x] Ollama
- [x] OpenAI-compatible
- [ ] Anthropic
- [ ] Gemini
- [ ] generic custom HTTP provider
- [ ] capability negotiation
- [ ] normalized provider errors
- [ ] retry/backoff policy
- [ ] health checks

### M2.3 Provider registry/configuration
- [x] persisted provider model
- [x] owner-scoped repository
- [x] registry
- [x] provider type discovery
- [x] encrypted provider credentials
- [x] create/list endpoints
- [ ] update/delete endpoints
- [ ] test-connection endpoint
- [ ] default provider/model selection
- [ ] provider-level permissions

## Phase 3 — Conversations
- [ ] conversation entity
- [ ] message entity and roles
- [ ] ownership
- [ ] provider/model metadata
- [ ] usage accounting
- [ ] repository/service/API
- [ ] context-window management
- [ ] pagination
- [ ] archival

## Phase 4 — Streaming
- [ ] streaming provider contract
- [ ] SSE layer
- [ ] cancellation
- [ ] timeout policy
- [ ] partial-response persistence
- [ ] provider error mapping
- [ ] correlation IDs
- [ ] runtime telemetry

## Phase 5 — Tool Runtime
- [ ] tool contract / JSON Schema
- [ ] registry
- [ ] capability authorization
- [ ] execution timeouts and cancellation
- [ ] sandbox boundary
- [ ] audit events
- [ ] email/calendar/files/database tools
- [ ] plugin bridge

## Phase 6 — Documents and RAG
- [ ] document/version model
- [ ] ingestion and extraction
- [ ] chunking
- [ ] embeddings
- [ ] ChromaDB
- [ ] retrieval service
- [ ] citations
- [ ] access-controlled retrieval
- [ ] background ingestion

## Phase 7 — Memory and personalization
- [ ] memory model and lifecycle
- [ ] explicit/inferred memory policy
- [ ] retrieval and mutation
- [ ] privacy controls
- [ ] personalization context builder

## Phase 8 — Agents and plugins
- [ ] agent model/configuration
- [ ] prompts
- [ ] tool/provider selection
- [ ] execution runtime
- [ ] plugin manifest/registry
- [ ] capability permissions
- [ ] lifecycle/versioning

## Phase 9 — Multi-user / multi-tenant deployment
- [ ] workspaces / organizations
- [ ] memberships and workspace roles
- [ ] resource ownership boundaries
- [ ] tenant-aware repositories/authorization
- [ ] per-tenant providers/rate limits
- [ ] isolation tests

## Phase 10 — Production hardening
- [ ] Redis
- [ ] distributed rate limiting
- [ ] background workers
- [ ] audit pipeline
- [ ] metrics / tracing
- [ ] database pool tuning
- [ ] readiness / graceful shutdown
- [ ] secrets manager/KMS
- [ ] containers / CI/CD
- [ ] migration deployment
- [ ] backup/restore
- [ ] security review
- [ ] load/failure testing

## Current checkpoint

**Completed:** Foundation, core authentication, initial AI abstraction/registry, and first authorization/API-key implementation.

**Active:** Harden Identity with integration tests and scoped API-key capabilities, then build Conversations.

**Completion rule:** A milestone is complete only when its domain model, service boundary, persistence behavior, failure modes, security implications, tests, and migration path are sufficiently defined for the next layer to depend on it.
