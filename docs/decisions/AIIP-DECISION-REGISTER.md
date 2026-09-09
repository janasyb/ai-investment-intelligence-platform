# AIIP DECISION REGISTER

**Company:** AIIP Technologies  
**Product:** AI Investment Intelligence Platform  
**Version:** 1.0  
**Status:** Authoritative  
**Last Updated:** 2026-09-09

---

# PURPOSE

The Decision Register records material company, product, commercial, architecture, and engineering decisions.

Its purpose is to preserve institutional reasoning.

AIIP should not repeatedly revisit decisions without reviewing the evidence that produced them.

---

# DECISION FORMAT

Each material decision should record:

- ID
- Date
- Decision
- Context
- Evidence
- Alternatives
- Rationale
- Consequences
- Status

---

# AIIP-D001

## Decision

AIIP will initially focus on digital-asset investment intelligence.

## Context

The company requires a defined initial market rather than attempting to solve investment intelligence across every asset class.

## Evidence

AIIP's initial customer-discovery and product work has centered on digital-asset investors and their research/decision problems.

## Alternatives

- all investment assets
- equities first
- institutional finance first
- digital assets first

## Rationale

Digital assets provide a sufficiently defined initial domain for building and validating an investment-intelligence methodology.

## Consequence

Initial product, research, data, and customer-validation workflows should prioritize digital assets.

## Status

ACTIVE

---

# AIIP-D002

## Decision

AIIP is being built as a company, not merely as a software project.

## Context

Engineering decisions must support commercial validation and eventual business operations.

## Rationale

A technically impressive product without validated customer demand does not establish a sustainable company.

## Consequence

Commercial evidence is a first-class development input.

## Status

ACTIVE

---

# AIIP-D003

## Decision

AIIP will use validation-first development.

## Decision Rule

When uncertainty exists, prefer:

Research
→ Interview
→ Prototype
→ Manual service
→ Paid experiment
→ Automation

over immediately building a large automated system.

## Rationale

This reduces wasted engineering effort and exposes false assumptions earlier.

## Status

ACTIVE

---

# AIIP-D004

## Decision

The initial commercial-validation product is the Investment Decision Report.

## Context

AIIP needs evidence that customers value structured investment intelligence.

## Rationale

A paid report tests actual willingness to pay before extensive platform automation.

## Consequence

Early product development must support learning from real investment decisions.

## Status

ACTIVE

---

# AIIP-D005

## Decision

The AIIP website will initially function as a validation and positioning surface rather than a complete investment platform.

## Rationale

The company should not build a full customer-facing platform before validating the underlying value proposition.

## Consequence

Website scope remains intentionally lean until customer evidence justifies expansion.

## Status

ACTIVE

---

# AIIP-D006

## Decision

AIIP-016 productionized the early-access request pipeline before building operational administration.

## Context

The system needed reliable persistence and validation before internal operations could depend on it.

## Rationale

Operational tooling should be built on a reliable underlying workflow.

## Status

COMPLETE

---

# AIIP-D007

## Decision

AIIP-017 will be defined as Early Access Operations rather than automatically as an Admin Dashboard.

## Context

"Admin dashboard" describes an implementation, not the business problem.

## Rationale

The company first needs the capability to review, qualify, track, and act on early-access prospects.

## Consequence

AIIP-017 must implement only the minimum operational capabilities required for that objective.

## Status

ACTIVE

---

# AIIP-D008

## Decision

New development ideas do not automatically become roadmap items.

## Rule

A new idea must first be evaluated as a proposal.

## Required questions

1. What problem does it solve?
2. Who has the problem?
3. What evidence supports it?
4. How important is it?
5. Why now?
6. What is the smallest test?
7. What existing priority would move if this is approved?

## Status

ACTIVE

---

# AIIP-D009

## Decision

AIIP will prefer simple architecture until validated requirements justify additional complexity.

## Rationale

Premature infrastructure complexity increases cost and slows learning.

## Consequence

Microservices, distributed infrastructure, advanced ML infrastructure, and similar systems require explicit justification.

## Status

ACTIVE

---

# AIIP-D010

## Decision

Investment intelligence must distinguish evidence from interpretation and uncertainty.

## Rationale

AIIP operates in a high-uncertainty financial domain.

## Consequence

The product must avoid presenting uncertain analysis as guaranteed outcomes.

## Status

ACTIVE

---

# DECISION CHANGE RULE

A decision may be changed.

However, material changes require:

1. New evidence
2. Explicit review
3. Updated decision record
4. Updated affected PRDs/roadmap
5. Implementation changes only after the decision

---

# END
