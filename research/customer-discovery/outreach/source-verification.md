# AIIP-012 Source Verification

## Purpose

This document defines the verification process required before an AIIP customer-discovery lead becomes eligible for outreach.

The purpose is to ensure that every outreach attempt is based on a real, publicly accessible source and that the lead genuinely matches the customer-discovery criteria.

AIIP must not contact people based solely on inferred, copied, summarized, or unverified signals.

---

## Core Principle

A customer signal is not automatically a qualified lead.

Before outreach:

```text
Customer Signal
      |
      v
Source Verification
      |
      v
Lead Qualification
      |
      v
Contact Eligibility
      |
      v
Personalized Outreach
```

The source must be verified before the lead is contacted.

---

# Verification Requirements

Every outreach candidate should have the following information where publicly available:

- Lead ID
- Signal ID
- Platform
- Original post URL
- Public username
- Date observed
- Original post text or relevant excerpt
- Digital-asset relevance
- Decision type
- Decision urgency
- Evidence of actual investment behavior
- Contact eligibility
- Verification status
- Verification date
- Verification notes

Do not invent missing information.

If a required source detail cannot be established, the lead remains blocked.

---

# Verification Status

Use one of the following statuses.

## UNVERIFIED

The source has not yet been checked.

No outreach is permitted.

---

## VERIFIED

The original public source has been located and the signal matches the recorded customer-discovery information.

The lead may proceed to qualification.

---

## VERIFIED — QUALIFICATION REQUIRED

The source is genuine, but additional information is required to determine whether the person fits the AIIP target customer.

No outreach until qualification is complete.

---

## BLOCKED

The source cannot be verified, the information is insufficient, or the lead cannot currently be contacted appropriately.

No outreach is permitted.

---

## EXCLUDED

The signal is not relevant to AIIP customer discovery.

Do not contact the lead.

---

# Source Verification Checklist

For every lead, verify the following.

### 1. Platform

Confirm that the signal actually originated from the recorded platform.

Examples:

- X
- Reddit
- Public forum
- Public community

---

### 2. Original Post

Locate the actual public post.

Do not rely on:

- screenshots without source information
- search-result snippets
- reposts when the original can be located
- summaries
- AI-generated descriptions
- second-hand references

Record the original public URL when available.

---

### 3. Username

Confirm the public username associated with the post.

Do not infer identity from unrelated accounts.

Do not attempt to uncover private identity information.

Use only information publicly associated with the relevant account.

---

### 4. Problem Match

Compare the actual post with the customer signal recorded in:

`../customer-signals.csv`

Confirm that the recorded problem accurately represents what the person publicly described.

Do not exaggerate the problem.

Do not convert a general statement into a stronger investment claim than the source supports.

---

### 5. Decision Match

Determine whether the post actually demonstrates a decision such as:

- BUY
- HOLD
- SELL
- WAIT
- EVALUATE
- CAPITAL ALLOCATION
- RISK EVALUATION

If the decision type is unclear, record:

`UNKNOWN`

Do not force a classification.

---

### 6. Digital-Asset Relevance

Determine whether the person is actually discussing digital assets.

Strong evidence includes explicit references to:

- cryptocurrency
- Bitcoin
- Ethereum
- altcoins
- memecoins
- stablecoins
- tokens
- exchanges
- crypto portfolios
- blockchain assets

A general investment question is not automatically a digital-asset signal.

---

### 7. Current or Recent Behavior

Determine whether the source indicates actual or recent behavior rather than purely hypothetical interest.

Examples of stronger evidence:

- currently holding an asset
- recently bought an asset
- recently sold an asset
- considering a current purchase
- evaluating an exchange before depositing funds
- currently researching an investment

Hypothetical statements should receive weaker qualification.

---

### 8. Decision Proximity

Determine how close the person appears to be to an actual decision.

Use:

### 1 — Low

General discussion or education.

### 2 — Moderate

General interest in a category or asset.

### 3 — Active Research

Person is actively evaluating an investment.

### 4 — Near Decision

Person appears to be deciding what to buy, hold, sell, or evaluate.

### 5 — Immediate Decision

Person explicitly indicates an imminent investment decision or capital deployment.

Do not infer urgency that is not supported by the source.

---

# Contact Eligibility

A lead may be considered eligible for outreach when:

1. The original public source is verified.
2. The username is publicly identifiable.
3. The problem matches the recorded signal.
4. The lead is relevant to AIIP.
5. The person appears to be discussing their own situation or decision.
6. The outreach can be personalized to the actual post.
7. Contacting the person is consistent with the platform's rules and norms.
8. No sensitive information is required for the outreach.

---

# Contact Eligibility States

Use one of:

- Eligible
- Qualification Required
- Blocked
- Excluded

### Eligible

Source and relevance are sufficiently verified.

The lead may be contacted.

### Qualification Required

Source is verified, but additional customer qualification is required.

Do not contact yet.

### Blocked

Source or eligibility cannot be established.

Do not contact.

### Excluded

The lead does not fit AIIP customer discovery.

Do not contact.

---

# Verification Evidence

For each verified lead, record concise evidence.

Example:

```text
Source:
Public Reddit post

Problem:
User explicitly asks how to evaluate a smaller crypto exchange before depositing funds.

Digital-asset relevance:
Confirmed

Decision proximity:
4 — Near Decision

Behavior evidence:
User references putting real money onto the exchange.

Verification:
Original post located and matched to recorded signal.

Contact eligibility:
Eligible
```

Do not include unnecessary personal information.

---

# Handling Missing Sources

If the original URL or username is unavailable:

```text
Verification Status: BLOCKED
Contact Eligibility: Blocked - source details required
```

Do not search for private information to fill the gap.

Do not guess the username.

Do not manufacture a URL.

Do not create an outreach record.

---

# Handling Ambiguous Sources

If the source exists but the customer's actual investment behavior is unclear:

```text
Verification Status: VERIFIED — QUALIFICATION REQUIRED
Contact Eligibility: Qualification Required
```

The lead may require a conversational qualification step before being treated as an AIIP customer.

---

# Handling Irrelevant Sources

If the original post does not support an AIIP customer problem:

```text
Verification Status: EXCLUDED
Contact Eligibility: Excluded
```

The lead should not enter the outreach funnel.

---

# Batch-001 Verification Priority

Verify Batch A in this order:

1. LEAD-003
2. LEAD-002
3. LEAD-001

Do not automatically proceed to the next lead simply because the previous lead is unverified.

Each lead must be independently verified.

---

# LEAD-003 Verification

## Recorded Signal

> How do you actually vet a smaller exchange before putting real money on it?

## Current Status

BLOCKED — source details required

## Required Verification

- Locate original Reddit post.
- Confirm public username.
- Confirm original post URL.
- Confirm the post is publicly accessible.
- Confirm the user is discussing an actual or current exchange-evaluation decision.
- Confirm the question concerns a digital-asset exchange.
- Determine decision proximity.
- Determine contact eligibility.

## Outreach Rule

Do not send the proposed outreach message until verification is complete.

---

# LEAD-002 Verification

## Recorded Signal

> If a coin drops 90%, should I sell what is left or ride it to zero?

## Current Status

BLOCKED — source details required

## Required Verification

- Locate original X post.
- Confirm public username.
- Confirm original post URL.
- Confirm the post is publicly accessible.
- Confirm the person appears to be discussing an actual investment position.
- Confirm the asset is a digital asset.
- Determine whether the question reflects a current decision.
- Determine contact eligibility.

## Outreach Rule

Do not send the proposed outreach message until verification is complete.

---

# LEAD-001 Verification

## Recorded Signal

> What memecoins should I buy right now?

## Current Status

BLOCKED — source details required

## Required Verification

- Locate original X post.
- Confirm public username.
- Confirm original post URL.
- Confirm the post is publicly accessible.
- Confirm the person is discussing digital-asset investment.
- Determine whether the person is actively evaluating a purchase.
- Determine decision proximity.
- Determine contact eligibility.

## Outreach Rule

Do not send the proposed outreach message until verification is complete.

---

# Verification Record

Verification should eventually produce structured records containing:

```text
Lead ID
Signal ID
Verification Status
Verification Date
Platform
Post URL
Username
Original Post Confirmed
Problem Confirmed
Digital Asset Relevance
Decision Type
Decision Proximity
Current Behavior Evidence
Contact Eligibility
Verification Notes
Verified By
```

---

# Evidence Standard

Source verification establishes that the signal is real.

It does not establish:

- customer willingness to participate
- problem frequency
- product demand
- willingness to pay
- commercial validation

Those require later stages of AIIP-012.

The evidence chain remains:

```text
Real Source
    |
Real Person / Public Account
    |
Relevant Problem
    |
Relevant Customer Behavior
    |
Qualified Lead
    |
Outreach
    |
Conversation
    |
Interview
    |
Problem Evidence
    |
Product Test
    |
Commercial Evidence
```

---

# Anti-Bias Rules

Do not upgrade a lead because:

- the post sounds compelling
- the person appears wealthy
- the account has many followers
- the question sounds urgent
- the problem resembles the AIIP thesis
- the person expresses enthusiasm

Do not downgrade a lead because:

- the account is small
- the person has few followers
- the wording is informal
- the person disagrees with AIIP's assumptions

Qualification must be based on evidence.

---

# Privacy and Safety

Use only publicly available information necessary for customer discovery.

Do not attempt to discover:

- private addresses
- private phone numbers
- passwords
- private keys
- seed phrases
- exchange credentials
- bank credentials
- payment credentials
- private financial records

Do not collect unnecessary personal information.

The purpose of source verification is to establish whether a public customer signal is genuine and relevant, not to investigate the individual.

---

# Definition of Done

Source verification for a lead is complete when:

- [ ] Original source located.
- [ ] Public URL recorded.
- [ ] Public username confirmed.
- [ ] Problem matches the source.
- [ ] Digital-asset relevance established.
- [ ] Decision type established or explicitly marked unknown.
- [ ] Decision proximity assessed.
- [ ] Current/recent behavior assessed.
- [ ] Contact eligibility determined.
- [ ] Verification notes recorded.
- [ ] No unsupported assumptions remain.

Only then may an eligible lead proceed to personalized outreach.

---

# AIIP-012 Principle

The objective is not to find people who appear to need AIIP.

The objective is to establish, with evidence, whether real people are experiencing problems AIIP can solve.

**Verify first. Contact second. Learn third. Sell last.**