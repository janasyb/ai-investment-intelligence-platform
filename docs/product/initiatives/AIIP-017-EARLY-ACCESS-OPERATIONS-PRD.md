# AIIP-017 — EARLY ACCESS OPERATIONS

**Company:** AIIP Technologies  
**Product:** AI Investment Intelligence Platform  
**Initiative:** AIIP-017  
**Version:** 1.0  
**Status:** Draft for Approval  
**Type:** Internal Operations  
**Priority:** High  
**Date:** 2026-09-09

---

# 1. EXECUTIVE SUMMARY

AIIP-017 establishes the minimum internal operational capability required to manage early-access requests collected by AIIP.

AIIP-016 established the reliable technical pipeline for receiving and persisting early-access requests.

AIIP-017 determines what AIIP Technologies must be able to do with those requests.

The initiative exists to support commercial validation.

It is not an initiative to build a generic CRM, enterprise administration platform, or broad internal dashboard.

---

# 2. STRATEGIC OBJECTIVE

Support AIIP's commercial-validation stage by making early-access requests operationally usable.

The system should allow the AIIP team to:

1. Review incoming requests.
2. Understand the prospect's stated profile and investment challenge.
3. Track the current relationship status.
4. Identify which prospects require follow-up.
5. Preserve useful customer-discovery information.
6. Support progression from prospect to conversation to product validation.

---

# 3. BUSINESS PROBLEM

AIIP can currently collect access requests.

However, collecting information is insufficient.

AIIP must be able to operationally manage the information so that valuable prospects do not become lost, duplicated, or impossible to track.

Without an operational workflow:

- follow-up may be inconsistent
- prospects may be forgotten
- customer discovery may become difficult to manage
- commercial-validation evidence may be fragmented
- the company may lose visibility into its earliest customers

---

# 4. PRIMARY USER

The initial user is:

> AIIP Technologies internal operator/founder.

This is an internal system.

It is not a customer-facing product.

---

# 5. CORE HYPOTHESIS

If AIIP has a simple internal workflow for managing early-access prospects, the company will be able to conduct customer discovery and commercial validation more consistently.

---

# 6. SUCCESS CRITERIA

AIIP-017 is successful if the internal operator can:

- see submitted access requests
- understand each request
- identify request status
- update operational status
- record useful follow-up information
- identify prospects requiring action
- avoid duplicate prospect records
- continue customer-validation workflows without relying on raw database access

The system should reduce operational friction.

---

# 7. IN SCOPE

The minimum viable operational capability may include:

## 7.1 Access Request List

Display submitted access requests.

Useful fields may include:

- name
- email
- profile
- challenge
- submission date
- status

---

## 7.2 Request Detail

Allow the operator to inspect the complete request.

---

## 7.3 Operational Status

The system should support an explicitly defined status workflow.

Initial candidate statuses:

- pending
- reviewed
- contacted
- interview
- qualified
- report
- paid
- converted
- rejected

The final status model must be kept as small as possible.

---

## 7.4 Status Updates

Authorized internal operators should be able to change operational status.

---

## 7.5 Internal Notes

If justified by the customer-discovery workflow, the operator may record non-sensitive operational notes.

Notes must not contain:

- passwords
- private keys
- seed phrases
- exchange credentials
- financial-account credentials

---

## 7.6 Basic Operational Filtering

If required for usability, operators may filter requests by status.

Additional filtering requires justification.

---

# 8. OUT OF SCOPE

AIIP-017 does NOT include:

- customer accounts
- public user dashboards
- portfolio management
- investment recommendations
- trading
- payments
- subscription billing
- CRM replacement
- marketing automation
- email automation
- advanced analytics
- AI chatbot
- social features
- mobile application
- role-management platform
- enterprise identity system
- notification infrastructure
- portfolio engine
- recommendation engine
- valuation engine
- market-engine expansion

These remain separate roadmap considerations.

---

# 9. SECURITY REQUIREMENTS

Because early-access records contain personal information:

- access must be restricted to authorized internal users
- sensitive credentials must never be stored
- API endpoints must not expose records publicly
- authentication/authorization requirements must be explicitly resolved before exposing administrative data
- data access must follow least privilege
- production secrets must never be committed
- logs must not unnecessarily expose personal information

---

# 10. PRIVACY REQUIREMENTS

The system should collect and retain only information necessary for the intended operational purpose.

The company should be able to explain why information is collected and how it is used.

---

# 11. DATA MODEL REQUIREMENTS

AIIP-017 must reuse the existing access-request model where possible.

Do not create duplicate representations of the same prospect without a documented reason.

If new entities are necessary, their relationship to AccessRequest must be explicit.

---

# 12. ARCHITECTURE PRINCIPLE

Use the existing architecture:

Website
→ FastAPI
→ Service
→ Repository
→ PostgreSQL

Administrative functionality should use the existing backend architecture rather than introducing a second backend.

---

# 13. AUTHENTICATION DECISION

Administrative access contains customer information.

Therefore, an administrative interface must not be exposed as a public unauthenticated surface.

Before implementation of a production administrative interface, AIIP must establish an appropriate authentication/authorization mechanism.

If full authentication is not yet justified for the validation stage, a safe internal operational alternative should be evaluated rather than exposing sensitive records publicly.

---

# 14. ACCEPTANCE CRITERIA

AIIP-017 must satisfy all applicable criteria below.

### AC-01

An authorized operator can view access requests.

### AC-02

An operator can inspect an individual request.

### AC-03

The system displays sufficient information to understand why the prospect requested access.

### AC-04

An operator can update the operational status.

### AC-05

Status changes persist to PostgreSQL.

### AC-06

Duplicate prospect records are not unintentionally created.

### AC-07

Administrative data is not publicly exposed.

### AC-08

Invalid administrative operations are rejected safely.

### AC-09

Automated tests cover the operational workflow.

### AC-10

Ruff passes.

### AC-11

Black passes.

### AC-12

Mypy passes.

### AC-13

Pytest passes.

### AC-14

Frontend production build passes.

### AC-15

CI passes.

### AC-16

No unrelated product functionality is introduced.

---

# 15. TEST STRATEGY

Tests should cover:

## Backend

- listing requests
- retrieving a request
- updating status
- invalid status
- missing request
- persistence
- access control

## Frontend

- request list rendering
- request detail
- status interaction
- loading state
- empty state
- error state

## Integration

- API → PostgreSQL
- administrative workflow persistence

---

# 16. OPERATIONAL METRICS

Potential metrics:

- number of new access requests
- pending requests
- reviewed requests
- contacted prospects
- interviews
- qualified prospects
- reports requested
- paid customers

Metrics should be added only when they support actual commercial-validation decisions.

---

# 17. RISKS

### Risk 1 — Premature CRM

The system could become a general CRM.

Mitigation:

Keep scope limited to AIIP early-access and customer-validation operations.

### Risk 2 — Security Exposure

Administrative data could be exposed publicly.

Mitigation:

Require authentication/authorization before production exposure.

### Risk 3 — Overengineering

Too much infrastructure could be created before the workflow is validated.

Mitigation:

Build the smallest operational capability.

### Risk 4 — Data Pollution

Internal notes may accumulate unnecessary or sensitive information.

Mitigation:

Define permitted information and prohibit credentials/secrets.

### Risk 5 — Losing Commercial Focus

Internal tooling could consume resources needed for customer validation.

Mitigation:

Measure AIIP-017 by whether it improves customer-validation operations.

---

# 18. DEPENDENCIES

AIIP-017 depends on:

- AIIP-016 access-request persistence
- PostgreSQL
- existing FastAPI architecture
- existing frontend architecture

Potential dependency:

- secure internal authentication/authorization

---

# 19. IMPLEMENTATION SEQUENCE

Implementation should proceed in this order:

1. Confirm business requirement.
2. Confirm data model.
3. Resolve administrative authentication boundary.
4. Define minimal API contract.
5. Define minimal UI.
6. Implement backend.
7. Implement frontend.
8. Add tests.
9. Run quality gates.
10. Validate with realistic operational workflow.
11. Open PR.
12. Review CI.
13. Merge only after acceptance criteria pass.

---

# 20. RELEASE REQUIREMENT

AIIP-017 cannot be considered complete merely because the code works locally.

Completion requires:

- requirements satisfied
- tests passing
- CI passing
- security boundary established
- documentation updated
- PR reviewed
- merged into main
- operational workflow validated

---

# 21. FUTURE CONSIDERATIONS

Future internal capabilities may include:

- customer relationship management
- communication tracking
- research workflow management
- customer analytics
- commercial pipeline
- reporting

None are part of AIIP-017 unless explicitly added through product decision.

---

# 22. PRODUCT DECISION

The purpose of AIIP-017 is not:

> Build an admin dashboard.

The purpose is:

> Enable AIIP Technologies to reliably operate the early-access and customer-validation workflow.

The implementation should remain subordinate to that objective.

---

# 23. APPROVAL

Before implementation begins:

Product objective: DEFINED

Customer problem: DEFINED

Hypothesis: DEFINED

Scope: DEFINED

Out of scope: DEFINED

Acceptance criteria: DEFINED

Security boundary: REQUIRES FINAL DESIGN DECISION

Implementation: NOT YET AUTHORIZED

---

# END
