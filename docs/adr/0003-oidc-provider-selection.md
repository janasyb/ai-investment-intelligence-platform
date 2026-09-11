# ADR-0003: OIDC Provider Selection for Internal Operations

- **Status:** Accepted
- **Date:** 2026-09-09
- **Decision Owners:** AIIP Technologies
- **Initiative:** AIIP-017 — Early Access Operations

---

## 1. Decision

AIIP will use **Auth0 as the managed OpenID Connect (OIDC) identity provider for internal operator authentication**.

Auth0 will provide identity authentication.

AIIP will retain ownership of:

- application authorization;
- operator roles;
- access-control decisions;
- application sessions;
- protected operations endpoints;
- business-level permissions.

Auth0 is therefore an identity provider, not AIIP's authorization system.

The initial AIIP internal role is:

```text
operator

---

# 2. Context

AIIP-017 introduces internal operations functionality for managing early-access requests.

This functionality may expose information including:

- prospect names;
- email addresses;
- customer-discovery information;
- internal notes;
- relationship status;
- product-validation information;
- operational follow-up information.

Unauthenticated access to these operations would therefore create an unacceptable security and privacy boundary.

AIIP needs a reliable authentication mechanism without introducing unnecessary custom security-sensitive infrastructure.

The selected solution must support:

OpenID Connect;
Authorization Code Flow;
managed authentication;
MFA through the identity provider;
secure integration with the FastAPI backend;
server-side application sessions;
separation between authentication and application authorization;
future growth without requiring a custom identity system.

---

# 3. Considered Options

The following providers were evaluated for the AIIP-017 internal-operations use case:

Auth0
Clerk
Google Identity Platform
Supabase Auth
Custom username/password authentication

The evaluation was limited to the requirements of AIIP-017.

It does not constitute a general evaluation of the providers for future customer authentication.

---

# 4. Evaluation Criteria

Providers were evaluated against:

```text
| Criterion                                      | Importance |
| ---------------------------------------------- | ---------- |
| OIDC support                                   | Required   |
| Authorization Code Flow support                | Required   |
| MFA capability                                 | Required   |
| Secure web-application integration             | Required   |
| Session architecture compatibility             | Required   |
| Mature security model                          | High       |
| Separation of authentication and authorization | High       |
| Operational simplicity                         | High       |
| Startup suitability                            | Medium     |
| Future extensibility                           | Medium     |
| Avoidance of unnecessary custom security code  | High       |

---

# 5. Decision Matrix

```text
| Capability                             |    Auth0 |                                    Clerk | Google Identity Platform |              Supabase Auth | Custom Auth |
| -------------------------------------- | -------: | ---------------------------------------: | -----------------------: | -------------------------: | ----------: |
| OIDC                                   |   Strong |                                   Strong |                   Strong |                     Strong |      Custom |
| Authorization Code Flow                |   Strong | Supported through managed authentication |                Supported |                  Supported |      Custom |
| Managed MFA                            |   Strong |                                   Strong |                Supported |                  Supported |      Custom |
| Mature identity platform               |   Strong |                                   Strong |                   Strong |                     Strong |        None |
| Security maintenance burden for AIIP   |      Low |                                      Low |                      Low |                        Low |        High |
| AIIP retains application authorization |      Yes |                                      Yes |                      Yes |                        Yes |         Yes |
| Custom credential handling required    |       No |                                       No |                       No | Yes/No depending on design |         Yes |
| Fit for AIIP-017                       | **High** |                                     High |              Medium/High |                     Medium |         Low |

---

# 6. Selected Provider: Auth0

Auth0 is selected for AIIP-017 because it provides a mature managed identity boundary while allowing AIIP to retain application-level authorization and session ownership.

The architecture is:

```text
Operator
   |
   v
AIIP Login
   |
   v
Auth0
   |
   | OIDC Authorization Code Flow
   v
AIIP FastAPI
   |
   +--> Validate identity
   |
   +--> Establish server-side session
   |
   +--> Resolve operator authorization
   |
   +--> Enforce protected operations access
   |
   v
Operations API

---

# 7. Authentication Boundary

Auth0 is responsible for establishing the authenticated identity.

AIIP is responsible for determining whether that authenticated identity is allowed to access a particular AIIP operation.

This creates a deliberate separation:

```text
Authentication
    =
"Who is this operator?"

Authorization
    =
"Is this operator allowed to perform this AIIP operation?"

Auth0 answers the first question.

AIIP answers the second.
---

# 8. OIDC Flow

AIIP will use the OIDC Authorization Code Flow appropriate for a server-backed web application.

The logical flow is:

```text
1. Operator requests AIIP internal login.

2. AIIP redirects the operator to Auth0.

3. Auth0 authenticates the operator.

4. Auth0 performs configured MFA requirements.

5. Auth0 returns an authorization response to AIIP.

6. AIIP validates the OIDC response.

7. AIIP establishes its own server-side application session.

8. AIIP resolves the authenticated operator.

9. AIIP authorizes the operator.

10. Protected operations endpoints become available.

AIIP must not treat the frontend as the security boundary.

Authorization must be enforced by the FastAPI backend.
---

# 9. Session Ownership

AIIP will own the application session.

The browser will receive a secure session cookie rather than a long-lived identity token stored in browser local storage.

The session architecture will use:

- Secure cookies in production;
- HttpOnly cookies;
- appropriate SameSite protection;
- server-side session state;
- explicit session expiration;
- logout and session invalidation;
- session fixation protection;
- no sensitive information embedded directly in the session identifier.

The exact session implementation will be defined during AIIP-017 implementation.

This ADR does not authorize a specific session library.

---

# 10. MFA

MFA will be enforced through the managed identity provider.

AIIP will not implement its own MFA mechanism for AIIP-017.

Where supported and appropriate, phishing-resistant authentication methods should be preferred over weaker authentication factors.

The exact Auth0 MFA configuration will be established during provider setup.

---

# 11. Authorization Model

AIIP-017 will begin with a deliberately small authorization model.

Initial role:

```text
operator

The backend will enforce:

```text
authenticated
    AND
authorized operator
    =
access granted

Otherwise:

```text
access denied

Authorization will follow a deny-by-default model.

The frontend may hide controls from unauthorized users for usability, but frontend behavior must never be treated as authorization.

---

# 12. Operator Allowlisting

Authentication alone must not automatically grant access to AIIP internal operations.

AIIP will maintain an application-level mechanism for determining which authenticated identities are authorized as operators.

The initial implementation should use the simplest secure mechanism consistent with the technical design.

The mechanism must not require creation of a general-purpose customer identity or role-management platform.

---

## 13. Security Requirements

The implementation must satisfy the following requirements:

# 13.1 Transport Security

Production authentication and operations traffic must use HTTPS.

# 13.2 Cookie Security

Production session cookies must use:

```text
Secure
HttpOnly
SameSite

with values appropriate to the deployed architecture.

# 13.3 Token Handling

AIIP must not place long-lived authentication tokens in:

```text
localStorage
sessionStorage

or equivalent browser-accessible persistent storage.

# 13.4 Secrets

Auth0 secrets and credentials must never be committed to source control.

Configuration must use environment variables or an appropriate production secret-management mechanism.

# 13.5 Authorization

Every protected operations endpoint must enforce authorization server-side.

# 13.6 Logging

Authentication credentials, tokens, session secrets, and other sensitive authentication material must not be written to application logs.

# 13.7 Failure Behavior

Authentication or authorization failures must fail closed.

The system must not fall back to unauthenticated operations access if the identity provider or authorization subsystem is unavailable.

---

## 14. Alternatives Rejected
# 14.1 Custom Username/Password Authentication

Rejected for AIIP-017.

A custom authentication system would require AIIP to own additional security-sensitive functionality including:

password storage;
password reset;
credential recovery;
authentication protections;
MFA;
session security;
account lockout;
credential attack defenses;
ongoing security maintenance.

This is unnecessary for the current internal-operations requirement.

---

# 14.2 Unauthenticated Operations

Rejected.

AIIP-017 handles operational and prospect information.

Exposing operations functionality without authentication would violate the intended security boundary.

---

# 14.3 Static Shared Admin API Key

Rejected as the primary production authentication mechanism.

A shared static key provides weak operator identity semantics and poor accountability.

It also creates unnecessary key-distribution and rotation concerns.

---

# 14.4 Browser-Stored Long-Lived Tokens

Rejected.

AIIP will not use browser local storage as the primary location for long-lived authentication tokens.

---

# 14.5 Building a General Identity Platform

Rejected.

AIIP-017 does not require:

customer accounts;
multi-tenancy;
enterprise SSO;
customer password management;
advanced RBAC;
organization management;
identity administration UI.

Those capabilities remain outside the initiative scope.

# 15. Why Auth0 Rather Than Building Authentication Internally

The primary reason for selecting Auth0 is not simply feature count.

The architectural objective is to reduce AIIP's security-sensitive implementation surface.

The desired division of responsibility is:

```text
Auth0
 ├── Identity authentication
 ├── Authentication flows
 └── MFA

AIIP
 ├── Application session
 ├── Operator authorization
 ├── Business permissions
 └── Operations functionality

This keeps AIIP focused on its product domain instead of becoming an identity provider.
---

# 16. Scope

This decision applies only to:

```text
AIIP-017
Internal Early Access Operations

It does not authorize implementation of:

- customer authentication;
- public user accounts;
- enterprise SSO;
- multi-tenant identity;
- organization management;
- advanced RBAC;
- customer password management;
- social login for customers;
- mobile authentication;
- general identity-management infrastructure.

A future customer authentication decision must be evaluated independently.

# 17. Configuration Boundary

Auth0 configuration will be treated as deployment configuration rather than application business logic.

Expected configuration will include values such as:

```text
AUTH0_DOMAIN
AUTH0_CLIENT_ID
AUTH0_CLIENT_SECRET
AUTH0_AUDIENCE
AUTH0_REDIRECT_URI
AUTH0_LOGOUT_URI

The exact environment-variable contract will be finalized during implementation.

Secrets must be supplied through environment configuration or a production secret-management system.

No secrets may be committed to Git.

---

# 18. Local Development

Local development must support authentication without requiring production credentials to be committed to the repository.

The implementation should provide a clear development configuration path.

Production and development authentication configuration must remain explicitly distinguishable.

Local development must not weaken production security assumptions.

---

# 19. Testing Implications

Authentication must be tested independently from the Auth0 service wherever practical.

Tests should verify at minimum:

- unauthenticated access is rejected;
- authenticated non-operator access is rejected;
- authorized operator access succeeds;
- invalid authentication state is rejected;
- expired sessions are rejected;
- logout invalidates the application session;
- protected endpoints cannot bypass authorization;
- authentication failures fail closed.

Integration tests involving the actual identity provider may be added where justified.

The core application authorization logic must remain testable without requiring an external Auth0 dependency for every test.

---

# 20. Operational Considerations

AIIP must consider identity-provider failure as an external dependency failure.

If Auth0 is unavailable:

- new authentication attempts may fail;
- existing application-session behavior must follow the defined - session policy;
- protected operations must never become publicly accessible;
- the application must fail closed for authorization decisions it cannot safely establish.

Authentication failures should produce operationally useful logs without exposing sensitive authentication data.

# 21. Cost Considerations

Auth0's current commercial offering includes a free tier, while some production security capabilities such as certain MFA configurations may depend on the selected plan.

AIIP must therefore verify the applicable Auth0 plan and startup-program eligibility before production deployment.

The architecture must not depend on a pricing assumption that has not been verified.

Cost optimization must not override the security requirements established by this ADR.

---

# 22. Future Review Triggers

This decision should be reviewed if AIIP introduces materially different identity requirements, including:

customer accounts;
-  internal teams;
- materially different operator roles;
- enterprise SSO;
- multi-tenancy;
- customer-managed identity;
- significant compliance requirements;
- materially increased authentication scale.

A future review does not imply that Auth0 must be replaced.

It means the identity architecture should be reassessed against the new requirements.

---

# 23. Consequences
Positive Consequences
AIIP avoids building custom credential infrastructure.
Authentication is delegated to a mature identity provider.
MFA can be handled by the identity provider.
AIIP retains control over application authorization.
The backend remains the security boundary.
The architecture is compatible with secure server-side sessions.
Authentication logic can remain isolated from business logic.
AIIP-017 can remain intentionally small.
Negative Consequences
AIIP becomes dependent on an external identity provider.
Auth0 configuration must be maintained.
Provider availability becomes an external dependency.
Some security capabilities may require a paid plan.
Provider-specific configuration must be documented and tested.

These trade-offs are acceptable for AIIP-017.

---

# 24. Relationship to Other AIIP Decisions

This ADR implements the authentication-provider portion of:

```text
D011 — Managed OIDC Authentication for Internal Operations

It must be read together with:

```text
docs/adr/0002-admin-authentication-and-session-strategy.md

and:

```text
docs/product/initiatives/AIIP-017-EARLY-ACCESS-OPERATIONS-PRD.md

and:

```text
docs/architecture/AIIP-017-EARLY-ACCESS-OPERATIONS-TECHNICAL-DESIGN.md

The PRD defines what AIIP-017 must accomplish.

The technical design defines how the approved initiative is intended to be implemented.

This ADR records the identity-provider decision.

---

# 25. Decision Authority

This ADR establishes:

```text
Auth0
=
AIIP-017 managed OIDC identity provider

It does not authorize unrelated authentication or identity features.

Any material change to this decision must follow the AIIP change-control process and update the relevant decision register and architecture documentation.

---

# 26. Final Decision

Accepted.

AIIP-017 will use Auth0 for managed OIDC authentication of internal operators.

AIIP FastAPI will retain ownership of:

```text
application session
authorization
operator role
protected operations endpoints
business permissions
