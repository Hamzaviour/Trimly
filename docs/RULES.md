# Trimly — Development Rules & Principles

**Version:** 1.0  
**Status:** Active  
**Applies to:** All engineers, all codebases

> These rules are non-negotiable. Every PR must comply. These exist to protect code quality, security, performance, and the customer experience.

---

## 1. Architecture Rules

### 1.1 Multi-Tenancy is Sacred
- Every query touching business data **MUST** be scoped to `salon_id`
- Never trust client-provided `salon_id` — always extract from JWT
- Row Level Security (RLS) is the last line of defense, not the first
- Cross-salon data access requires `SUPER_ADMIN` role + audit log entry
- Never return data from a salon the user doesn't belong to — ever

### 1.2 Monolith First, Microservices Later
- Start with a structured monolith inside `services/api/`
- Split into microservices only when a service has clear scaling or ownership boundaries
- The voice agent (`voice-agent/`) is the only standalone service from day one

### 1.3 Async by Default (Python)
- All database operations must use async SQLAlchemy
- No blocking calls in request handlers
- Long-running tasks go to Celery — never in the request/response cycle
- WebSocket connections managed via dedicated async handler

---

## 2. API Rules

### 2.1 Consistency
- All responses follow the standard envelope: `{ success, data, meta }` or `{ success, error }`
- HTTP methods must be semantically correct (GET=read, POST=create, PUT=replace, PATCH=partial, DELETE=remove)
- Use plural nouns for collection endpoints: `/customers`, not `/customer`
- Include pagination meta for all list endpoints

### 2.2 Validation
- Pydantic schemas required for all request bodies — no raw dict access
- Validate phone numbers to E.164 Pakistani format (`+923XXXXXXXXX`)
- Sanitize all string inputs — strip HTML, trim whitespace
- Never pass unvalidated user input to database queries

### 2.3 Error Handling
- Use custom exception classes, never raise generic `Exception`
- All errors must return machine-readable error codes (e.g., `APPOINTMENT_CONFLICT`)
- Never expose stack traces, internal paths, or SQL errors to clients
- Log all 5xx errors with full context (request ID, user ID, salon ID)

### 2.4 Rate Limiting
- Unauthenticated: 60 req/min per IP
- Authenticated: 600 req/min per user
- OTP endpoints: 5 req/hour per phone number
- AI voice call trigger: 10 calls/hour per salon

---

## 3. Database Rules

### 3.1 Schema Rules
- All tables must have: `id` (UUID), `created_at`, `updated_at`
- All deletions must be soft (use `deleted_at`) for auditable data
- No nullable foreign keys without clear justification
- All migrations via Alembic — no manual DDL changes on production

### 3.2 Query Rules
- Never write raw SQL unless absolutely necessary — use SQLAlchemy ORM
- All queries must use parameterized inputs — no f-string SQL
- Add `EXPLAIN ANALYZE` for any query touching > 10k rows
- All queries returning lists must be paginated (max 100/page)
- Use database-level indexes — don't filter in Python if DB can do it

### 3.3 Performance
- Denormalize stats (total_visits, average_rating) via triggers — never compute in real-time for dashboards
- Redis cache for: queue state, salon config, barber availability (TTL: 30s–5min)
- Never run analytics queries on the primary DB — use read replica or materialized views

---

## 4. Security Rules

### 4.1 Authentication
- OTP-only authentication — no passwords stored, ever
- JWT access tokens: 15 minute expiry
- JWT refresh tokens: 30 day expiry, stored in httpOnly cookie only
- Never return tokens in JSON response body for production
- Invalidate all refresh tokens on logout

### 4.2 Authorization
- Check role AND salon membership on every protected endpoint
- RBAC enforced in middleware — never rely on frontend to hide features
- Barbers can only access their own data, never other barbers' data
- Customer data access requires active salon relationship

### 4.3 Data Protection
- PII (name, phone, birthday) encrypted at rest using PostgreSQL pgcrypto where possible
- Phone numbers never logged in plaintext in application logs
- File uploads: validate MIME type server-side, never trust Content-Type header
- All external webhook calls must verify HMAC signatures

### 4.4 Secrets Management
- Zero hardcoded secrets — all secrets via environment variables
- Use `.env.example` with placeholder values — never commit real `.env`
- Rotate secrets if ever committed, even briefly
- Production secrets managed via Railway/Render secrets or HashiCorp Vault

---

## 5. Frontend Rules

### 5.1 Design System Compliance
- All UI must use the defined design tokens (CSS variables)
- No hardcoded hex colors — use `var(--color-xxx)` or Tailwind semantic classes
- All components must support dark mode via `dark:` variants
- Urdu text must use RTL-compatible layout (`dir="rtl"`)

### 5.2 Performance
- All pages must score > 85 on Lighthouse Performance (mobile)
- Images: always use `next/image` with WebP format
- Never import entire libraries — use tree-shakeable imports
- Bundle size check on every PR: flag any +50KB increase

### 5.3 State Management
- Server state: TanStack Query (fetch, cache, refetch)
- Client state: Zustand (UI state, selections, sidebar state)
- Never store sensitive data in localStorage (no tokens, no PII)
- URL state for shareable filters (e.g., `?status=active&barber=uuid`)

### 5.4 Accessibility
- All interactive elements must have `aria-label` or visible label
- Focus states must be visible (no `outline: none` without custom focus ring)
- Color must not be the only way to convey information (add text/icon)
- Keyboard navigation must work for all critical flows (booking, queue)

### 5.5 Error & Loading States
- Every data-fetching component must have:
  - Loading skeleton (not spinner alone)
  - Error state with retry option
  - Empty state with CTA
- Never show raw error messages to users — map to friendly text

---

## 6. AI & Automation Rules

### 6.1 AI Calls
- Never make AI calls without customer consent (captured at registration)
- AI call attempts maximum: 3 per customer per month per campaign type
- If customer says "stop" or "nahi" — immediately log opt-out, never call again
- All AI transcripts stored in `call_logs` for quality review

### 6.2 Message Generation
- AI-generated messages must be reviewed by templates before sending at scale
- Personalization variables (`{name}`, `{barber}`) must be validated before message send
- If variable is missing, use graceful fallback (never send "Hello {name}!")
- All messages must include opt-out instruction for SMS (per Jazz/Zong rules)

### 6.3 Reminders
- Maximum 1 reminder per customer per 7 days per salon
- Respect quiet hours: no calls/SMS between 10 PM – 8 AM PKT
- Track reminder effectiveness — disable for customers who never respond after 3 attempts

### 6.4 Credits
- Deduct AI credits before making API calls — never on failure
- Refund credits on provider-side failures (ElevenLabs error, Twilio failure)
- Alert owner when credits < 20% remaining
- Hard stop at 0 credits — no credit debt allowed

---

## 7. Mobile Rules

### 7.1 Performance
- First meaningful paint < 1.5s on mid-range Android
- Optimize all images to WebP, lazy-load below fold
- Implement React Native Hermes engine
- Enable offline-first for queue view and appointment list

### 7.2 UX
- All touch targets minimum 44×44 points (iOS HIG standard)
- Never use more than 5 items in bottom navigation
- All modals must be dismissible by swipe down
- Handle keyboard appearance — prevent form fields from being hidden

### 7.3 Notifications
- Always ask permission before requesting push access
- Group notifications — never spam with individual pings
- Notification tap must deep-link to the relevant screen
- Badge count must reflect unread items accurately

---

## 8. Communication & Notification Rules

### 8.1 SMS
- All SMS must comply with Jazz/Zong character limits (160 chars per segment)
- Always include salon name at start: "Trimly: [Salon Name] — ..."
- Include opt-out instruction in marketing SMS: "Unsubscribe: STOP ko 8900 pe bhejein"
- Log all SMS in `sms_logs` with delivery status

### 8.2 WhatsApp
- Use approved message templates for transactional messages
- Never send promotional WhatsApp without opt-in
- Respect WhatsApp's 24-hour window for non-template messages

### 8.3 Push Notifications
- Don't send more than 3 push notifications per day per user
- Use notification categories for better organization
- Silent push for data sync — loud push only for actionable events

---

## 9. Testing Rules

### 9.1 Backend
- Unit tests for all business logic functions
- Integration tests for all API endpoints
- Coverage target: 80% minimum
- All Celery tasks must have integration tests
- Database migrations must be tested before production deploy

### 9.2 Frontend
- Component tests with React Testing Library
- E2E tests for critical flows: signup, booking, queue view
- Visual regression tests for design system components
- Mobile: test on real Android device before release

### 9.3 CI/CD
- No PR merged without passing CI
- Failing tests = blocked deploy
- Linting + type checking in CI (ESLint, TypeScript, Ruff for Python)
- Automated security scanning (Snyk or GitHub Dependabot)

---

## 10. Code Quality Rules

### 10.1 General
- No commented-out code in production — use feature flags
- No `TODO` in production — create a ticket instead
- No `console.log` in production frontend code — use logger
- No `print()` in production backend — use Python logging

### 10.2 Python (Backend)
- Follow PEP 8; enforced via Ruff
- Type hints on all function signatures
- Docstrings on all public functions and classes
- Max function length: 50 lines (refactor if longer)

### 10.3 TypeScript (Frontend)
- `strict: true` in tsconfig — no exceptions
- No `any` type — use `unknown` + type guards if needed
- All component props typed with interfaces
- API response types auto-generated from OpenAPI schema

### 10.4 Git & PRs
- Branch naming: `feat/`, `fix/`, `chore/`, `docs/`, `refactor/`
- Commit messages: Conventional Commits format (`feat: add queue WebSocket`)
- PRs must have a description + linked ticket
- Maximum PR size: 400 lines changed (split larger work)
- At least 1 reviewer required before merge

---

## 11. Logging & Observability Rules

### 11.1 What to Log
- All API requests (method, path, status, duration, user_id, salon_id)
- All authentication events (login, logout, OTP sent, OTP failed)
- All financial transactions (invoice created, payment processed)
- All AI actions (call initiated, message sent, booking made by AI)
- All errors (with full context, never with PII in log line)

### 11.2 What NOT to Log
- Passwords (we don't use them, but still)
- OTP codes (never, under any circumstances)
- Full credit card numbers
- Plain text phone numbers in error messages

### 11.3 Log Format
```json
{
  "timestamp": "2026-08-07T10:00:00Z",
  "level": "INFO",
  "service": "api",
  "request_id": "uuid",
  "user_id": "uuid",
  "salon_id": "uuid",
  "action": "appointment.created",
  "duration_ms": 45,
  "status": 201
}
```

---

## 12. Deployment Rules

### 12.1 Production Deployments
- Backend deployments require manual approval after CI passes
- Database migrations run separately before app deploy
- Always test migration rollback before pushing forward migration
- Maintain at least 2 versions of API endpoints simultaneously during transitions

### 12.2 Environment Parity
- Development, staging, and production must use same OS and major versions
- Never test only on development — staging must mirror production
- Use feature flags (not branches) for in-progress features in production

### 12.3 Rollbacks
- Every deployment must have a documented rollback procedure
- Database migrations must be reversible (write `downgrade()` functions)
- Keep previous Docker image available for 7 days for rapid rollback

---

## Violations & Enforcement

| Severity | Examples | Action |
|---|---|---|
| **Critical** | Security vuln, data leak, multi-tenant breach | Immediate revert, incident report, post-mortem |
| **High** | No error handling, missing auth check, hardcoded secret | PR blocked, must fix before merge |
| **Medium** | Missing tests, type: any, console.log in prod | Comment on PR, fix in same sprint |
| **Low** | Style inconsistency, missing docstring | Note for author, fix at convenience |

---

*Rules enforced via automated linting, CI checks, and code review. Questions → engineering lead.*
