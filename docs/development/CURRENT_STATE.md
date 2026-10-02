# AIIP Current Development State

> This file is the primary session-to-session handoff snapshot.
> It must describe the repository as it actually exists, not as intended.

## 1. Project Identity

- **Company:** AIIP Technologies
- **Product:** AI Investment Intelligence Platform for Digital Assets
- **Repository:** `ai-investment-intelligence-platform`
- **Local path:** `C:\Development\AI-Investment-Intelligence-Platform`

## 2. Current Git State

- **Branch:** `main`
- **Latest commit:** `d8dd21c`
- **Latest commit message:** `fix(aiip-017): harden internal operations security`
- **Previous major merge:** `e68a57b`
- **Working tree at handoff:** clean
- **Remote:** `https://github.com/janasyb/ai-investment-intelligence-platform.git`
- **GitHub Actions:** successful for `d8dd21c` (`AIIP CI` run #64)

> Verify all Git fields at the beginning of a new session. These values are a starting snapshot, not permanent truth.

## 3. Current Workstream

**AIIP-017 — Early Access Operations**

Status: **Implemented, Security-Hardened, Validated, and Merged**

AIIP-017 established the minimum internal operational capability required to manage early-access requests and support customer validation.

The implementation remains intentionally limited to internal early-access operations and does not introduce a general CRM, customer-account platform, trading system, portfolio-management system, or broad administration platform.

## 4. Delivered AIIP-017 Capability

### Internal operations

- Operations UI at `/operations`
- Access-request list
- Access-request detail view
- Operational status updates
- Logout flow
- Backend-enforced operator authorization

### Authentication and session security

- Auth0 OIDC authentication
- OIDC state validation
- OIDC nonce validation
- PKCE
- ID-token signature/issuer/audience validation
- Explicit `AUTH0_OPERATOR_SUBJECT` authorization boundary
- Server-side Redis-backed operator sessions
- Opaque session identifiers
- Absolute session expiration
- Idle session expiration
- HttpOnly session cookie
- SameSite cookie policy
- Secure-cookie requirement in production
- Server-side session invalidation on logout

### CSRF and CORS

- Independently generated session-bound CSRF token
- `X-CSRF-Token` validation for state-changing operator operations
- CSRF protection on access-request status updates
- CSRF protection on logout
- Explicit CORS configuration
- Configured frontend origin only
- Credentialed browser requests supported
- `X-CSRF-Token` permitted for preflight requests

### Production configuration safeguards

Production configuration rejects:

- default development `SECRET_KEY`
- non-secure operator cookies
- non-HTTPS frontend URLs
- non-HTTPS Auth0 callback URLs
- incomplete required Auth0 operator configuration

## 5. Validation Status

### Local validation

- **Pytest:** PASS — 55 passed
- **Ruff:** PASS
- **Black:** PASS
- **Mypy:** PASS — 82 source files
- **Frontend production build:** PASS
- **`git diff --check`:** PASS
- **Working tree:** CLEAN

### CI validation

- **Workflow:** `AIIP CI`
- **Run:** `#64`
- **Commit:** `d8dd21c`
- **Branch:** `main`
- **Status:** SUCCESS
- **API Quality:** PASS
- **API Docker:** PASS

### Known test warnings

Two existing Python 3.16 deprecation warnings remain from:

`apps/api/tests/conftest.py`

They concern `asyncio.WindowsSelectorEventLoopPolicy` and are not part of the AIIP-017 security implementation.

## 6. Customer Discovery Context

AIIP's broader commercial-validation strategy remains:

`X + Reddit + LinkedIn`
→ `AIIP Research & Insights`
→ `FREE intelligence`
→ `AIIP website`
→ `Email / free account`
→ `AIIP V1`
→ `PAID CUSTOMER`

Current product-validation concept:

**Decision Intelligence Report**

Evidence progression:

`Signal → Qualification → Outreach → Conversation → Interview → Product Test → Payment`

The current objective is still to validate a sufficiently important digital-asset investment decision problem through real customer evidence rather than hypothetical interest.

## 7. Current Objective

AIIP-017 is complete.

The next development objective must be established from an approved specification rather than inferred from implementation momentum.

No new product module is currently authorized for implementation until the next initiative's requirements, scope, architecture, acceptance criteria, and security boundary are explicitly established and approved.

## 8. Explicit Next Task

- **Task:** Define and obtain approval for the next AIIP development initiative before implementation.
- **Specification:** The next approved initiative specification in `docs/product/initiatives/` and any related ADRs.
- **Expected outcome:** A bounded, implementation-ready initiative with explicit acceptance criteria and authorized scope.
- **Acceptance criteria:** Requirements, scope, architecture/security boundary, testing strategy, and Definition of Done documented and approved.
- **Blocked by:** Next initiative specification/approval.

## 9. Active Files

The next session should inspect these first:

1. `docs/development/CHATGPT_DEVELOPMENT_HANDOFF.md`
2. `docs/development/CURRENT_STATE.md`
3. The next approved initiative specification in `docs/product/initiatives/`
4. Relevant ADRs in `docs/adr/`
5. Actual Git/source state before making changes

## 10. Known Issues / Blockers

- Python 3.16 `WindowsSelectorEventLoopPolicy` deprecation warnings remain in the test configuration.
- Auth0 client secret previously exposed during development must be rotated before production use.
- Real production deployment credentials and infrastructure configuration are not represented by `.env.example`.

## 11. Decisions Requiring Attention

- Do not begin the next implementation initiative until its specification and security/architecture boundaries are explicitly approved.
- Do not mark AIIP production-ready solely from development/CI validation.
- Treat the repository and current Git state as authoritative over older conversation context.

## 12. Last Session Summary

### Completed

- Completed AIIP-017 Early Access Operations.
- Added session-bound CSRF protection.
- Added CSRF protection to status updates and logout.
- Added explicit CORS configuration.
- Added production configuration security validation.
- Added authentication, security, and settings tests.
- Updated frontend operations flow to send the CSRF token.
- Updated AIIP-017 PRD and technical design to implemented/validated status.
- Passed 55 automated tests.
- Passed Ruff, Black, Mypy, frontend production build, and `git diff --check`.
- Committed as `d8dd21c`.
- Pushed to `main`.
- Confirmed GitHub Actions CI run #64 succeeded.

### Not completed

- Next AIIP initiative has not yet been authorized for implementation.

### Important observations

- AIIP-017 is complete and should not be expanded with unrelated functionality.
- The existing Python 3.16 warnings are separate maintenance work.
- Production use requires rotation of the previously exposed Auth0 client secret.

## 13. Next Session Instruction

The next ChatGPT session must:

1. Read `docs/development/CHATGPT_DEVELOPMENT_HANDOFF.md`.
2. Read this file.
3. Verify the actual Git state against this snapshot.
4. Inspect the next approved initiative specification.
5. Verify relevant ADRs and source files.
6. Confirm the exact authorized task.
7. Implement only the approved scope.
8. Validate the implementation.
9. Update this file before handoff.