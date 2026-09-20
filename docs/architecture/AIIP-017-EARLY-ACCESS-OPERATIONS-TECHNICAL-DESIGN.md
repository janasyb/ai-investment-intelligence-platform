# AIIP-017 — EARLY ACCESS OPERATIONS

# Technical Design

- **Initiative:** AIIP-017
- **Title:** Early Access Operations
- **Status:** Proposed for Implementation
- **Related PRD:** `docs/product/initiatives/AIIP-017-EARLY-ACCESS-OPERATIONS-PRD.md`
- **Related ADR:** `docs/adr/0002-admin-authentication-and-session-strategy.md`
- **Related Decision:** `AIIP-D011`
- **OIDC Provider:** Auth0
- **Date:** 2026-09-10

---

## 1. Purpose

This document translates the approved AIIP-017 product requirements and authentication decision into an implementation-level technical design.

AIIP-017 provides the minimum internal operational capability required to manage early-access requests and support customer discovery.

The design deliberately avoids building a general-purpose administration platform.

The implementation must remain:

- small
- secure
- testable
- production-ready
- deployable
- consistent with the existing AIIP architecture

---

# 2. Design Principles

AIIP-017 follows these principles:

1. Reuse existing AIIP architecture.
2. Reuse the existing `access_requests` data model wherever possible.
3. Keep authentication separate from application authorization.
4. Keep authorization server-side.
5. Deny access by default.
6. Do not expose operational data publicly.
7. Do not introduce custom password authentication.
8. Do not store long-lived authentication tokens in browser storage.
9. Avoid unnecessary database entities.
10. Avoid unnecessary infrastructure.
11. Do not introduce a full CRM.
12. Do not introduce customer accounts.
13. Do not introduce payments or billing.
14. Every protected capability must have automated tests.
15. Existing AIIP-016 behavior must remain regression-safe.
16. Do not allow the frontend to become the security boundary.
17. Do not expand authentication into a customer identity platform.
18. Prefer the smallest secure implementation that satisfies the operational requirement.

---

# 3. Existing Architecture

The existing public early-access flow is:

```text
Public Website
      |
      v
FastAPI Access Request API
      |
      v
Access Request Service
      |
      v
Access Request Repository
      |
      v
PostgreSQL

---

 # 4. Target Architecture

AIIP-017 introduces a separate internal operations boundary.

The target architecture is:

```text
                         PUBLIC SYSTEM
                              |
                              v
                      AIIP Website
                              |
                              v
                 Public Access Request API
                              |
                              v
                    Access Request Service
                              |
                              v
                   Access Request Repository
                              |
                              v
                         PostgreSQL


                         INTERNAL SYSTEM
                              |
                              v
                     Operations Web UI
                              |
                              v
                    FastAPI Operations API
                              |
                    +---------+---------+
                    |                   |
                    v                   v
              Authorization        Data Access
                    |                   |
                    v                   v
             Operator Session    Access Request
                    |                   |
                    v                   v
                 Auth0              PostgreSQL

Authentication flow:

```text
Operator
   |
   v
AIIP Operations Login
   |
   v
Auth0
   |
   | OIDC Authorization Code Flow
   v
AIIP Callback
   |
   v
OIDC Validation
   |
   v
Server-Side Session
   |
   v
Secure Session Cookie
   |
   v
Protected Operations API
   |
   v
Operator Authorization

# 5. Authentication Architecture

## 5.1 Decision

AIIP-017 uses a managed OpenID Connect identity provider.

The selected provider is:

Auth0

The application uses OIDC Authorization Code Flow for the internal operator authentication flow.

AIIP does not implement:

password authentication
password reset
password hashing
account recovery
MFA implementation
credential storage
customer identity management

## 5.2 Authentication Responsibility Boundary

Auth0 is responsible for:

authenticating the operator
managing operator credentials
enforcing configured MFA
issuing OIDC authentication responses
maintaining the upstream identity-provider session where applicable

AIIP is responsible for:

validating the OIDC response
establishing its own application session
determining whether the authenticated identity is an authorized operator
enforcing application-level authorization
protecting operations endpoints
invalidating the application session during logout

## 5.3 Authentication Flow

The expected flow is:

1. Operator requests protected operations page.

2. AIIP determines that no valid application session exists.

3. AIIP redirects the operator to Auth0.

4. Auth0 authenticates the operator.

5. Auth0 applies configured MFA requirements.

6. Auth0 returns the operator through the OIDC callback.

7. AIIP validates the OIDC response.

8. AIIP identifies the operator.

9. AIIP verifies that the identity is authorized for AIIP internal operations.

10. AIIP creates a server-side application session.

11. AIIP sends a secure session cookie to the browser.

12. Browser requests protected operations resources.

13. AIIP validates the server-side session.

14. AIIP performs authorization checks.

15. Authorized operations are executed.

# 6. Authorization Architecture

## 6.1 Authorization Model

AIIP-017 begins with one application role:

operator

The initial authorization rule is:

Authenticated + Authorized Operator
            |
            v
       Operations Access

# 6.2 Deny-by-Default

Protected operations must follow deny-by-default behavior.

Expected behavior:

No session
    -> HTTP 401

Valid session
but unauthorized identity
    -> HTTP 403

Valid authenticated operator
    -> operation permitted

# 6.3 Operator Allowlisting

The initial implementation should use a configured operator identity rather than creating an operator-management database.

The authorization mechanism may use a provider claim or explicitly configured identity value.

The exact claim and configuration must be finalized during implementation based on the selected Auth0 application configuration.

The implementation must not introduce:

user-management UI
role-management UI
organization-management infrastructure
multi-tenant authorization
customer roles

# 7. Session Architecture

## 7.1 Application Session

AIIP uses a server-side application session.

The browser receives an opaque session identifier rather than a long-lived authentication token.

Conceptually:

Browser
   |
   | Secure session cookie
   v
AIIP API
   |
   | session lookup
   v
Server-Side Session Store

## 7.2 Cookie Requirements

The application session cookie must use:

Secure
HttpOnly
appropriate SameSite policy
explicit expiration
server-side invalidation on logout

## 7.3 Session Security

The implementation must protect against session fixation.

A new application session must be established after successful authentication.

The implementation must not:

reuse attacker-controlled session identifiers
place access tokens in localStorage
place refresh tokens in localStorage
expose session secrets to frontend JavaScript
log session identifiers
log OIDC tokens
commit session secrets to source control

## 7.4 Session Expiration

Sessions must have a bounded lifetime.

The implementation should support:

idle expiration
absolute expiration
explicit logout
server-side invalidation

# 8. Operator Identity

AIIP-017 does not require a new database table for operators.

The initial operator identity model is:

Auth0 Identity
      |
      v
OIDC Claims
      |
      v
AIIP Authorization Check
      |
      v
operator

The minimum identity information required by the application should be limited to what is necessary for:

authentication
authorization
operational identification
auditability where justified

# 9. Authentication Endpoints

The authentication boundary should expose the following logical endpoints:

GET  /api/v1/auth/login
GET  /api/v1/auth/callback
GET  /api/v1/auth/session
POST /api/v1/auth/logout

## 9.1 Login

GET /api/v1/auth/login

Responsibilities:

initiate OIDC authentication
generate required OIDC state
generate nonce where required
redirect the operator to Auth0

## 9.2 Callback

GET /api/v1/auth/callback

Responsibilities:

receive the OIDC authorization response
validate the response
validate state
validate nonce where applicable
validate issuer
validate audience
validate token claims
establish the AIIP application session
redirect the operator to the protected operations interface

## 9.3 Session

GET /api/v1/auth/session

Responsibilities:

determine whether an application session exists
return minimal authenticated operator information
avoid exposing tokens or sensitive identity-provider data

## 9.4 Logout

POST /api/v1/auth/logout

Responsibilities:

invalidate the AIIP application session
clear the application session cookie
optionally initiate provider logout where required by the final authentication flow

# 10. Operations API

The initial operations API is intentionally small.

Required endpoints:

GET /api/v1/operations/access-requests
GET /api/v1/operations/access-requests/{id}
PATCH /api/v1/operations/access-requests/{id}/status

## 10.1 List Access Requests

GET /api/v1/operations/access-requests

Purpose:

Allow an authorized operator to review early-access requests.

Initial response information may include:

request identifier
email
creation timestamp
current operational status
relevant submitted information required for discovery

## 10.2 Access Request Detail

GET /api/v1/operations/access-requests/{id}

Purpose:

Allow an authorized operator to inspect an individual request.

The endpoint must:

require authentication
require operator authorization
return 404 when the request does not exist
avoid exposing internal database implementation details

## 10.3 Update Status

PATCH /api/v1/operations/access-requests/{id}/status

Purpose:

Allow an authorized operator to update the operational status of a request.

The update must:

validate the requested status
persist the change
return the updated representation
reject invalid status values
require operator authorization

# 11. Access Request Operations

The existing access_requests model should remain the source of truth for the original public submission.

AIIP-017 should not duplicate the access request into a second operational database.

The operational layer should build on the existing model.

Where a new operational field is genuinely required, the field must be justified against:

customer-discovery value
operational necessity
data minimization
implementation cost
privacy implications

# 12. Status Model

The initial operational status vocabulary should remain small.

Candidate statuses:

pending
reviewed
contacted
interview
qualified
report
paid
converted
rejected

# 13. Notes

Internal notes may be introduced only if customer-discovery evidence demonstrates that they are necessary.

If notes are implemented, they must:

be internal-only
never be returned through public APIs
require operator authorization
be subject to data minimization
not contain passwords, private keys, seed phrases, financial credentials, or other unnecessary sensitive information
not be unnecessarily logged

# 14. Backend Structure

The logical backend structure is:

apps/api/app/

├── api/
│   ├── routes/
│   │   ├── access_requests.py
│   │   ├── auth.py
│   │   └── operations_access_requests.py
│   │
│   └── v1/
│       └── router.py
│
├── auth/
│   ├── oidc.py
│   ├── session.py
│   └── authorization.py
│
├── models/
│   └── access_request.py
│
├── repositories/
│   └── access_request.py
│
├── schemas/
│   └── access_request.py
│
└── services/
    └── access_request.py

# 15. Service and Repository Boundaries

Existing access-request responsibilities remain separated:

Route
  |
  v
Service
  |
  v
Repository
  |
  v
Database

The operations API should reuse these boundaries.

The route must not contain:

direct SQL
database transaction logic
authentication-provider business logic
authorization policy logic

# 16. Frontend Structure

The internal operations interface should be separated from the public website.

Conceptually:

apps/web/src/

├── components/
│   ├── access/
│   └── operations/
│
├── pages/
│   ├── public/
│   └── operations/
│
└── auth/

The exact structure may be simplified if the existing application does not justify additional routing abstractions.

The operations interface should initially provide only:

authentication state
access-request list
access-request detail
status update
logout

# 17. Frontend Security Boundary

The frontend is not a security boundary.

The frontend may:

hide protected UI from unauthenticated users
redirect to login
display authenticated state
display authorization errors

The frontend must not be trusted to enforce:

operator authorization
access-request visibility
status-update permissions
data-access permissions

# 18. Security Controls

AIIP-017 must implement the following controls.

## 18.1 Authentication
managed OIDC
Auth0
Authorization Code Flow
state validation
nonce validation where applicable
issuer validation
audience validation
secure callback handling

## 18.2 Authorization
deny by default
server-side authorization
operator role
explicit identity allowlisting/configuration
401 for unauthenticated requests
403 for unauthorized authenticated requests

## 18.3 Session
server-side session
opaque session identifier
Secure cookie
HttpOnly cookie
appropriate SameSite policy
bounded expiration
logout invalidation
session fixation protection

## 18.4 Secrets

Secrets must not be:

committed to Git
embedded in frontend source
returned by APIs
written to logs
stored in browser local storage

# 19. CSRF and CORS

Because the application uses cookie-based authentication, CSRF protection must be considered explicitly.

State-changing operations include:

POST /api/v1/auth/logout
PATCH /api/v1/operations/access-requests/{id}/status

# 20. HTTP Error Contract

Protected operations should use predictable HTTP behavior.

Minimum expectations:

401 Unauthorized

Returned when authentication is required but no valid application session exists.

403 Forbidden

Returned when the caller is authenticated but is not authorized for the requested operation.

404 Not Found

Returned when a requested access request does not exist.

422 Unprocessable Entity

Returned for invalid request data according to the application's existing validation conventions.

500 Internal Server Error

Returned for unexpected server failures without exposing implementation details.

Errors must not expose:

database stack traces
SQL statements
tokens
secrets
session identifiers
internal credentials

21. Testing Strategy

AIIP-017 is not complete without automated security and behavior tests.

Testing must cover:

## 21.1 Authentication Tests

Test cases should include:

unauthenticated access to protected endpoint
successful authentication flow using a test seam
invalid OIDC state
invalid authentication response
rejected identity
successful operator authentication
session creation
session expiration
logout
session invalidation

Normal CI must not depend on a real external Auth0 login.

## 21.2 Authorization Tests

Test cases should include:

No session
    -> 401

Authenticated non-operator
    -> 403

Authenticated operator
    -> allowed

## 21.3 Operations API Tests

Test:

list access requests
retrieve access request
nonexistent request
valid status update
invalid status update
persistence of status update
unauthorized status update
duplicate handling remains regression-safe

## 21.4 Regression Tests

Existing AIIP-016 tests must continue passing.

At minimum:

valid public access request
invalid email
missing consent
duplicate email
PostgreSQL persistence
API integration behavior

---

# 22. Test Seam for Auth0

Automated tests should not require live interaction with Auth0.

The authentication implementation should provide a controlled test seam at the application boundary.

The test environment should be able to simulate:

authenticated operator
authenticated non-operator
unauthenticated request
expired session
invalid authentication response

---

# 23. Configuration and Environment Variables

Authentication configuration must be supplied through environment configuration.

Conceptual configuration includes:

AUTH0_DOMAIN
AUTH0_CLIENT_ID
AUTH0_CLIENT_SECRET
AUTH0_AUDIENCE
AUTH0_ISSUER
AUTH0_CALLBACK_URL
AUTH0_LOGOUT_URL
SESSION_SECRET
SESSION_COOKIE_NAME
SESSION_COOKIE_SECURE
SESSION_COOKIE_SAMESITE
SESSION_TTL
AUTHORIZED_OPERATOR

# 24. Auth0 Provider Configuration

The Auth0 implementation must be configured as an application suitable for a server-side web application.

The final configuration must establish:

application type appropriate for the AIIP backend architecture
allowed callback URL
allowed logout URL
allowed web origins where required
issuer
audience where an API resource is used
required MFA policy
appropriate session/security settings

# 25. MFA

MFA is an identity-provider responsibility.

AIIP-017 should rely on Auth0 for MFA enforcement.

The production configuration should require MFA for authorized internal operators.

Where supported and practical, phishing-resistant authentication should be preferred.

AIIP must not implement its own MFA subsystem.

# 26. Database Strategy

AIIP-017 should reuse the existing PostgreSQL database.

The initial design does not require:

a separate operations database
an operator database
an authentication database
a CRM database
a second access-request table

The database remains:

PostgreSQL
    |
    +-- access_requests

# 27. Data Privacy and Minimization

The operations interface contains prospect information.

The implementation must therefore minimize exposure.

Requirements:

do not expose access-request data publicly
do not include unnecessary PII in API responses
do not log full request bodies unnecessarily
do not log authentication tokens
do not log session identifiers
do not expose database credentials
restrict internal data to authorized operators
retain only information required for the business purpose

# 28. Auditability

AIIP-017 should provide sufficient operational visibility to determine:

who accessed protected operations
when protected operations occurred
what operational action occurred

The initial implementation should avoid building a full audit platform.

If audit logging is introduced, it should record security-relevant events such as:

operator_login_success
operator_login_failure
operator_logout
unauthorized_operation_attempt
access_request_status_changed

Logs must not contain:

passwords
OIDC tokens
session identifiers
private keys
seed phrases
financial-account credentials

# 29. Observability

AIIP-017 must integrate with the existing AIIP observability approach.

Operational monitoring should cover:

authentication failures
authorization failures
operations API errors
status-update failures
unexpected server errors
database errors

# 30. Performance

AIIP-017 is an internal operational workflow.

The initial design should optimize for:

correctness
security
simplicity
maintainability

rather than premature high-scale optimization.

# 31. Availability and Failure Handling

If Auth0 is unavailable:

New operator authentication
        |
        v
       FAIL

Existing application sessions may continue according to the configured session policy, provided their validity can be safely established without depending on an unavailable external call.

If PostgreSQL is unavailable:

Operations API
      |
      v
Database failure
      |
      v
Controlled server error

32. Deployment Architecture

The production architecture remains:

Browser
   |
   v
HTTPS
   |
   v
AIIP Web Application
   |
   v
FastAPI
   |
   +-------> Auth0
   |
   +-------> PostgreSQL
   |
   +-------> Redis where required by the existing architecture

   Production requirements include:

HTTPS
secure cookies
production secrets
restricted CORS
protected operations routes
production Auth0 configuration
database migrations
health checks
logging
monitoring

# 33. Local Development

Local development must provide a way to test the operations architecture without requiring production credentials.

Development should support:

AIIP Web
    |
    v
FastAPI
    |
    +--> Test authentication seam
    |
    +--> PostgreSQL
    |
    +--> Redis where required

# 34. Implementation Sequence

Implementation must proceed in controlled slices.

Step 1 — Provider Decision

Complete and commit:

docs/adr/0003-oidc-provider-selection.md

Decision:

Auth0

Step 2 — Auth0 Application Configuration

Configure the Auth0 application and verify:

callback URL
logout URL
issuer
client configuration
MFA policy
required claims

Do not begin operations UI implementation before the authentication boundary is understood.

Step 3 — Environment Contract

Define the required environment configuration.

Update configuration validation.

Add safe development/test defaults where appropriate.

Never add production secrets to the repository.

Step 4 — OIDC Authentication Adapter

Implement the smallest AIIP authentication adapter required to:

start login
handle callback
validate OIDC response
establish application identity

Add automated tests.

Step 5 — Server-Side Session

Implement:

opaque session identifier
server-side session storage
secure cookie
expiration
logout
invalidation
session fixation protection

Add automated tests.

Step 6 — Authorization

Implement:

operator identity check
operator role
deny-by-default
401
403

Add automated tests.

Step 7 — Protected Operations API

Implement:

GET /api/v1/operations/access-requests
GET /api/v1/operations/access-requests/{id}
PATCH /api/v1/operations/access-requests/{id}/status

Step 8 — Operations UI

Implement only:

protected operations route
login state
request list
request detail
status update
logout

Do not build a general admin dashboard.

Step 9 — Security Hardening

Validate:

HTTPS behavior
cookie flags
CORS
CSRF
authorization
session expiration
logout
error handling
secret handling
logging
Step 10 — Full Validation

Run:

Black
Ruff
Mypy
Pytest
Frontend build
Docker validation
Database migration validation
Git diff checks
CI

# 35. Acceptance Gate

AIIP-017 must not be considered complete until all of the following are true.

Authentication
 Auth0 is configured.
 OIDC Authorization Code Flow works.
 OIDC response validation works.
 MFA policy is configured for production operators.
 Application session is server-side.
 Session cookie is Secure.
 Session cookie is HttpOnly.
 Appropriate SameSite policy is configured.
 Session expiration is enforced.
 Logout invalidates the application session.
 Session fixation protection is implemented.
Authorization
 Protected operations require authentication.
 Operator authorization is enforced server-side.
 Unauthorized authenticated identities receive 403.
 Unauthenticated requests receive 401.
 Frontend is not the authorization boundary.
Operations
 Authorized operator can list access requests.
 Authorized operator can inspect an access request.
 Authorized operator can update operational status.
 Status changes persist correctly.
 Invalid statuses are rejected.
 Public access-request behavior remains functional.
 Duplicate protection remains functional.
Security
 No custom password authentication exists.
 No long-lived authentication tokens are stored in browser local storage.
 No secrets are committed.
 Tokens are not logged.
 Session identifiers are not logged.
 CORS is explicitly configured.
 CSRF protection is implemented appropriately.
 Internal operations endpoints are not publicly accessible without authorization.
 Sensitive data exposure has been reviewed.
Testing
 Authentication tests pass.
 Authorization tests pass.
 Operations API tests pass.
 Regression tests pass.
 PostgreSQL integration tests pass.
 Frontend build passes.
 Black passes.
 Ruff passes.
 Mypy passes.
 CI passes.
Documentation
 AIIP-017 PRD is current.
 ADR-0002 is current.
 ADR-0003 is committed.
 Technical Design is current.
 Implementation decisions are documented.
 PR includes validation evidence.

# 36. Explicit Non-Goals

AIIP-017 does not authorize implementation of:

customer authentication
public user accounts
customer profiles
enterprise SSO
multi-tenant identity
advanced role management
full CRM
marketing automation
email automation
payment processing
billing
portfolio management
investment recommendations
automated trading
exchange integration
custody
wallets
social features
mobile applications
AI chatbot functionality
advanced analytics platform
notification infrastructure
general-purpose administration platform

Any of these capabilities requires separate product and engineering justification.

# 37. Architectural Constraints

AIIP-017 must remain consistent with the current AIIP stack:

Frontend:
React
Vite

Backend:
FastAPI
Python

Database:
PostgreSQL
SQLAlchemy
Alembic

Infrastructure:
Docker

Testing:
Pytest
Ruff
Black
Mypy

Authentication:
Auth0
OIDC

Application Authorization:
AIIP FastAPI backend

Application Session:
AIIP server-side session

# 38. Security Boundary Summary

The security model can be summarized as:

                    AUTHENTICATION
                         |
                         v
                       Auth0
                         |
                         v
                  OIDC Validation
                         |
                         v
                 AIIP Application
                     Session
                         |
                         v
                   Authorization
                         |
                 +-------+-------+
                 |               |
                 v               v
              Denied           Allowed
                 |               |
                401/403           |
                                 v
                         Operations API
                                 |
                                 v
                              PostgreSQL

# 39. Architectural Rationale

AIIP-017 requires an internal operational boundary because early-access requests contain information that should not be exposed through public application routes.

A managed OIDC provider reduces the need for AIIP to implement security-sensitive credential management.

A server-side application session allows AIIP to maintain control over application authentication state without placing long-lived authentication tokens in browser storage.

Server-side authorization ensures that the security boundary is enforced by the backend rather than by the user interface.

Reusing the existing access-request model prevents unnecessary duplication of customer data.

The deliberately small operator role avoids prematurely creating a role-management system.

The architecture therefore provides the minimum security and operational capability required for AIIP-017 while preserving room for future evolution if customer evidence justifies it.

# 40. Change Control

This Technical Design is subordinate to:

AIIP Master Development Prompt
AIIP Master PRD
AIIP Product Roadmap
AIIP Decision Register
Approved AIIP-017 PRD
Approved ADRs

If implementation reveals a requirement that materially changes this design, development must pause at the affected boundary and the change must be documented.

The implementation must not silently expand scope.

Changes affecting:

authentication
authorization
session architecture
data model
public API behavior
security boundary
customer accounts
payments
external integrations

require explicit review before implementation.

# 41. Definition of Done

AIIP-017 is complete when:

Requirement
    |
    v
Technical Design
    |
    v
Authentication
    |
    v
Authorization
    |
    v
Protected Operations API
    |
    v
Operations UI
    |
    v
Automated Tests
    |
    v
Security Validation
    |
    v
CI
    |
    v
Production Validation
    |
    v
Pull Request
    |
    v
Review
    |
    v
Merge

# 42. Final Architectural Decision

AIIP-017 will implement a deliberately small internal operations capability using:

Auth0
   |
   | OIDC
   v
AIIP FastAPI
   |
   +--> Server-Side Session
   |
   +--> Operator Authorization
   |
   +--> Operations API
   |
   v
PostgreSQL

# 43. Authority

This document defines the technical design for AIIP-017.

It does not replace the AIIP-017 PRD.

The PRD defines what AIIP-017 must accomplish.

This document defines how the approved requirements are intended to be implemented.

Where implementation evidence demonstrates that this design is insufficient, the appropriate response is to update the design through the AIIP change-control process rather than silently expanding implementation scope.