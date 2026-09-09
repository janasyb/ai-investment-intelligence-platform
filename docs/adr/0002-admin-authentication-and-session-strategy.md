@'
# ADR-0002: Admin Authentication and Session Strategy

- Status: Accepted
- Date: 2026-09-09
- Decision: Use managed OIDC authentication with secure server-side sessions for AIIP internal operations.

## Context

AIIP-017 requires an internal operational interface for managing early-access requests.

Early-access records contain personally identifiable information and customer-discovery information, including:

- name
- email address
- investor profile
- research challenge
- operational status
- future internal notes

The operations interface must therefore never be publicly accessible without authentication and authorization.

AIIP already contains security-related foundations, including JWT and password-hashing dependencies, but AIIP-017 does not require building a custom authentication system.

## Decision

AIIP-017 will use a managed OpenID Connect (OIDC) identity provider for operator authentication.

The application will establish an authenticated server-side session after successful identity-provider authentication.

The initial authorization model will contain one operational role:

`operator`

The API will enforce authorization for every protected operations endpoint.

The browser will not store long-lived authentication tokens in localStorage or sessionStorage.

Authentication credentials will not be stored in the AIIP database.

## Initial Access Model

The initial production model is:

1. Operator visits the AIIP internal operations interface.
2. Application redirects the operator to the configured OIDC identity provider.
3. Identity provider authenticates the operator.
4. MFA is enforced by the identity provider where supported/configured.
5. AIIP validates the OIDC response.
6. AIIP establishes a secure authenticated session.
7. AIIP associates the authenticated identity with the `operator` role.
8. Protected API endpoints require an authenticated operator session.
9. Unauthorized requests are rejected server-side.

## Authorization

Authorization is enforced by the FastAPI backend.

The frontend is not considered a security boundary.

The initial policy is deny-by-default:

- unauthenticated users cannot access operations endpoints
- authenticated non-operators cannot access operations endpoints
- operators may access only capabilities explicitly granted to the operator role

## Session Security

The implementation must use secure session practices.

Required controls include:

- HTTPS in production
- Secure cookies in production
- HttpOnly cookies
- appropriate SameSite policy
- session expiration
- logout/session invalidation
- protection against session fixation
- no sensitive information encoded into the session identifier
- no credentials or session secrets committed to source control

## MFA

Administrative/operator access should use MFA through the identity provider.

AIIP should prefer phishing-resistant authentication mechanisms where the selected identity provider supports them.

## Alternatives Considered

### Custom username/password authentication

Rejected for AIIP-017.

Reasons:

- increases security implementation scope
- requires password reset flows
- requires credential lifecycle management
- requires brute-force protections
- requires MFA implementation or integration
- creates additional security-sensitive code
- distracts from commercial validation

### JWT stored in browser localStorage

Rejected.

Reasons:

- increases exposure to client-side token theft
- unnecessary for the internal browser application
- creates avoidable token lifecycle complexity

### Unauthenticated internal admin route

Rejected.

The fact that a route is named `/admin` or is not linked from the public website does not constitute access control.

### Static admin API key

Rejected as the primary production authentication mechanism.

A static shared credential does not provide an appropriate operator identity, session lifecycle, or scalable authorization model.

## Consequences

### Positive

- smaller custom security surface
- MFA can be delegated to the identity provider
- clear separation between authentication and application authorization
- easier future operator expansion
- protected API boundary
- reduced authentication implementation scope

### Negative

- introduces an identity-provider dependency
- requires OIDC configuration
- requires production domain and callback configuration
- introduces provider-specific operational setup

## Scope Control

This decision does not authorize:

- customer authentication
- public user accounts
- social login for customers
- enterprise SSO
- multi-tenant authorization
- advanced role-management systems
- customer identity management
- password management UI

Those require separate product requirements and decisions.

## Implementation Principle

AIIP-017 should implement the smallest secure operator-access boundary necessary to manage early-access requests.

Authentication must serve the operational workflow rather than becoming a standalone product subsystem.

## Review Trigger

This decision should be revisited if:

- AIIP gains multiple internal teams
- customer accounts are introduced
- enterprise customers require SSO
- multiple authorization roles become necessary
- compliance requirements materially change
- the selected identity provider becomes unsuitable
'@ | Set-Content .\docs\adr\0002-admin-authentication-and-session-strategy.md