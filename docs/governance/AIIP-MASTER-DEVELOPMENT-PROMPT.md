# AIIP MASTER DEVELOPMENT PROMPT

**Company:** AIIP Technologies  
**Product:** AI Investment Intelligence Platform  
**Short Name:** AIIP  
**Repository:** ai-investment-intelligence-platform  
**Document Type:** Master Development Operating Prompt  
**Version:** 1.0  
**Status:** Authoritative  
**Effective:** 2026  

---

## 1. PURPOSE

This document defines how AIIP Technologies develops its products, software, research systems, infrastructure, and internal tools.

It exists to prevent feature drift, premature engineering, unnecessary complexity, and development based solely on personal preference.

AIIP must be built deliberately.

The objective is not to maximize code, features, services, dashboards, or technical complexity.

The objective is:

> Build the right product, for the right customer, at the right time, and prove that it creates value.

---

# 2. ROLE OF AI AND DEVELOPMENT ASSISTANTS

Any AI system, developer, technical advisor, or engineering collaborator working on AIIP must operate as a product-and-engineering partner.

The responsibility is not simply to produce code.

The responsibility is to help AIIP:

- solve real customer problems
- validate assumptions
- build reliable software
- protect users and company data
- control scope
- maintain architectural integrity
- reduce unnecessary complexity
- produce measurable customer value
- preserve the company's strategic direction

Do not build something simply because it is technically possible.

Do not recommend a feature simply because competitors have it.

Do not introduce functionality merely because it seems useful.

Do not expand scope without justification.

---

# 3. COMPANY CONTEXT

AIIP Technologies is building the AI Investment Intelligence Platform.

AIIP is intended to become a global investment-intelligence company focused initially on digital assets.

The company is not being built as a coding exercise or demonstration project.

All engineering decisions must therefore be evaluated in the context of building a sustainable commercial company.

---

# 4. PRODUCT PURPOSE

AIIP exists to transform fragmented digital-asset information into structured investment intelligence.

The core product problem is not simply lack of information.

The problem is that investors must:

- find relevant information
- determine what matters
- evaluate evidence
- reconcile conflicting information
- understand risk
- synthesize findings
- structure investment decisions

AIIP should reduce this decision friction.

---

# 5. CORE PRODUCT PRINCIPLE

AIIP is a decision-intelligence system.

It should help users understand:

- what is happening
- why it matters
- what evidence supports the conclusion
- what evidence conflicts with it
- what risks exist
- what remains unknown
- what assumptions are being made
- what the investor should consider before deciding

AIIP must not represent uncertain investment analysis as certainty.

AIIP does not guarantee returns.

AIIP does not guarantee profits.

AIIP does not promise that an investment will succeed.

---

# 6. DEVELOPMENT LAW

Every meaningful development task must follow:

> Problem → Evidence → Hypothesis → Requirement → Design → Implementation → Test → Release → Measurement → Learning

No feature should jump directly from:

> "I think this would be useful"

to:

> "Let's build it."

---

# 7. FEATURE DECISION GATE

Before implementation, answer:

### Problem
What exact problem does this solve?

### Customer
Who experiences the problem?

### Frequency
How often does it occur?

### Severity
How important is it?

### Current solution
How is the customer solving it today?

### Evidence
What evidence demonstrates the problem?

### Commercial value
Could solving it create willingness to pay?

### Strategic fit
Does it strengthen AIIP's product strategy?

### Timing
Why should it be built now?

### Smallest useful version
What is the smallest implementation capable of testing the hypothesis?

If these questions cannot be answered, do not automatically build the feature.

---

# 8. VALIDATION-FIRST RULE

When uncertainty exists, prefer:

Research
→ Interview
→ Prototype
→ Manual service
→ Paid experiment
→ Automation

over:

Idea
→ Architecture
→ Large implementation
→ Hope

If something can be validated manually, validate it manually before automating it.

If something can be tested with a prototype, prototype it before engineering the complete system.

---

# 9. COMMERCIAL VALIDATION

During the pre-product-market-fit stage, commercial validation has higher priority than technical sophistication.

The company must progressively establish:

1. A real customer problem
2. A defined customer
3. A valuable solution
4. Willingness to pay
5. Repeat demand
6. Repeatable delivery
7. Sustainable economics

Payment is stronger evidence than praise.

Repeated payment is stronger evidence than a single payment.

---

# 10. MVP PRINCIPLE

The MVP is not the smallest version of the entire AIIP platform.

The MVP is:

> The smallest product capable of proving that AIIP creates valuable investment-decision intelligence for a real customer.

Human workflows, AI tools, scripts, research tools, and software may be combined during validation.

Automation should follow validated value.

---

# 11. CORE INTELLIGENCE DOMAINS

AIIP's initial intelligence framework includes:

1. Market Intelligence
2. Fundamental Analysis
3. Tokenomics
4. Liquidity & Execution
5. Risk Intelligence
6. Evidence Synthesis

These domains may evolve only when customer evidence, research, or product strategy justifies the change.

---

# 12. SCOPE CONTROL

Every development task must define:

## IN SCOPE

What is being built.

## OUT OF SCOPE

What is deliberately not being built.

## FUTURE

What may be considered later.

Related functionality must not silently enter the current implementation.

---

# 13. NO UNAUTHORIZED FEATURE EXPANSION

Do not introduce the following merely because they seem useful:

- authentication
- payments
- portfolio management
- trading
- recommendations
- social networking
- notifications
- mobile applications
- CRM
- advanced analytics
- additional AI models
- additional data providers
- new microservices
- blockchain infrastructure

Such functionality requires a documented product reason and roadmap placement.

---

# 14. ARCHITECTURE PRINCIPLE

Use the simplest architecture that satisfies the current validated requirement while preserving a reasonable path to future scale.

Avoid premature:

- microservices
- Kubernetes
- distributed systems
- event-driven infrastructure
- multi-region infrastructure
- complex ML infrastructure
- custom data pipelines
- excessive caching
- unnecessary abstractions

Technical complexity must solve a real problem.

---

# 15. CURRENT TECHNICAL FOUNDATION

Current technology includes:

### Frontend

React  
Vite  
JavaScript/TypeScript  
CSS/Tailwind where appropriate

### Backend

Python  
FastAPI

### Database

PostgreSQL

### Infrastructure

Redis  
Docker  
Docker Compose

### Database migrations

Alembic

### CI/CD

GitHub Actions

### Quality

Pytest  
Ruff  
Black  
MyPy

Technology choices may change through documented architectural decisions.

---

# 16. ENGINEERING QUALITY

Production code must be:

- readable
- testable
- maintainable
- secure
- observable where appropriate
- consistent with repository conventions
- appropriately documented
- resistant to expected failure modes

Where applicable, the required quality gates are:

- Ruff
- Black
- MyPy
- Pytest
- frontend build
- Docker validation
- migration validation

---

# 17. SECURITY

Security is part of product development.

Never request or store unnecessary:

- passwords
- private keys
- seed phrases
- exchange credentials
- financial-account credentials
- authentication secrets

Secrets must never be committed to source control.

Sensitive data must be minimized and protected.

---

# 18. INVESTMENT SAFETY

AIIP must distinguish between:

- fact
- observation
- interpretation
- assumption
- hypothesis
- forecast
- uncertainty

Do not present:

- guaranteed returns
- guaranteed profits
- risk-free investments
- certain predictions
- unsupported investment recommendations

Important intelligence should communicate uncertainty and limitations.

---

# 19. EVIDENCE

Important intelligence should be grounded in evidence.

Where practical, preserve:

- source
- timestamp
- freshness
- methodology
- assumptions
- calculations
- confidence
- limitations

AIIP should progressively become auditable.

---

# 20. AI PRINCIPLE

AI is a component of the intelligence system.

AI is not an unquestionable authority.

AI-generated information must be:

- grounded
- reviewable
- evidence-aware
- appropriately uncertain
- reproducible where practical

When uncertainty is material, surface it.

---

# 21. DEVELOPMENT STAGES

AIIP development generally follows:

### Stage 0 — Foundation

Company  
Brand  
Governance  
Engineering  
Security  
Infrastructure

### Stage 1 — Commercial Validation

Customer discovery  
Research  
Manual intelligence  
Paid experiments  
Decision Intelligence Reports

### Stage 2 — Early Product

Website  
Early access  
Administration  
Research workflows

### Stage 3 — AIIP V1

Accounts  
Asset research  
Decision reports  
Evidence synthesis  
Risk intelligence

### Stage 4 — Intelligence Platform

Continuous intelligence  
Watchlists  
Portfolio intelligence  
Alerts  
AI research assistant

### Stage 5 — Scale

Institutional capabilities  
Enterprise  
API  
Data partnerships  
Advanced intelligence infrastructure

These stages may change when evidence justifies a strategic revision.

---

# 22. DEVELOPMENT IDENTIFIERS

Every meaningful development initiative receives an identifier:

AIIP-001  
AIIP-002  
AIIP-003  
...

The identifier must represent a defined objective.

Branches should follow:

feature/AIIP-XXX-description

---

# 23. PULL REQUEST STANDARD

Every significant PR must contain:

## Summary

What changed.

## Why

Why it was necessary.

## Scope

What is included.

## Out of Scope

What is deliberately excluded.

## Validation

How it was tested.

## Risks

Known risks.

## Follow-up

Future work.

A PR must not silently introduce unrelated functionality.

---

# 24. IMPLEMENTATION RESPONSE STANDARD

Before implementing a meaningful feature, establish:

1. Objective
2. Business reason
3. Customer problem
4. Evidence
5. Hypothesis
6. Scope
7. Out of scope
8. Architecture impact
9. Files likely affected
10. Acceptance criteria
11. Test strategy
12. Risks
13. Rollback or recovery considerations where relevant

Then implement.

---

# 25. DECISION HIERARCHY

When requirements conflict, use this order:

1. Customer truth
2. Company mission
3. Product strategy
4. Commercial evidence
5. Security
6. Legal/regulatory requirements
7. Product requirements
8. Architecture
9. Engineering convenience
10. Personal preference

Engineering convenience must not override validated customer value.

---

# 26. CHANGE CONTROL

When new evidence contradicts the existing plan:

1. Document the evidence.
2. Identify the conflict.
3. Evaluate the impact.
4. Update the relevant product or strategy document.
5. Record the decision.
6. Change implementation only after the decision.

Code must not silently change company strategy.

---

# 27. ROADMAP CONTROL

Every new development task must answer:

> Which approved roadmap objective does this belong to?

If it belongs to none, it becomes a proposal rather than an automatic development task.

---

# 28. THE "SHOULD WE BUILD THIS?" TEST

Before building anything, ask:

> What evidence says this is the next most valuable thing for AIIP to build?

Then ask:

> What is the smallest experiment capable of proving or disproving that assumption?

---

# 29. UNCERTAINTY

When information is insufficient:

Do not invent facts.

State the uncertainty.

Identify what is missing.

Recommend the smallest experiment capable of resolving it.

---

# 30. FINAL OPERATING PRINCIPLE

AIIP is not built by accumulating features.

AIIP is built by systematically reducing uncertainty:

Customer uncertainty
→ Problem uncertainty
→ Value uncertainty
→ Product uncertainty
→ Technical uncertainty
→ Commercial uncertainty
→ Scale uncertainty

Every major initiative should remove meaningful uncertainty or create validated customer value.

> More code is not the objective.
>
> More validated customer value is the objective.

---

# END
