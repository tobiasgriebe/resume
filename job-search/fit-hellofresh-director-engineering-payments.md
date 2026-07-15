# Fit Assessment — Director of Engineering, Payments
**Company:** HelloFresh SE  
**Location:** Berlin (+ Warsaw distributed team)  
**Team:** 3 squads, 20–25 engineers (EMs + Staff Engineers)  
**Date assessed:** 2026-06-30  
**Source:** careers.hellofresh.com (job 8034967)

---

## Role Summary

Director of Engineering for the Global Payments Tribe at HelloFresh — responsible for payment processing, gateway services, batch transactions, and customer profitability at 8.5M+ active customers. Leads 3 squads across Berlin and Warsaw with Engineering Managers and Staff Engineers reporting in. Core mandate: technical architecture ownership for payments, GenAI transformation of the tribe, SRE/reliability practices, and cross-functional alignment with Product, Finance, and payment service providers. Compensation is "heavily weighted toward equity" (VSO + RSU).

---

## Overall Fit: MEDIUM-HIGH (~65%)

Strong match on leadership model, org design, and most of the technical stack. Two meaningful gaps: payments domain depth and Golang. GenAI transformation mandate is a genuine strength. Equity-heavy comp structure needs scrutiny against the €150k base floor.

---

## Dimension-by-Dimension Analysis

### Role Scope & Leadership Model — STRONG MATCH ✓

| Requirement | Evidence |
|---|---|
| 4+ years managing Engineering Managers (not just ICs) | sevDesk: 6 EMs directly; Würth: team lead layer |
| 10+ years software engineering | Yes — exceeds |
| Distributed teams across multiple offices | sevDesk (distributed squads); Würth (remote + onsite) |
| Coach and develop EMs, hold them accountable | Career framework + performance management at sevDesk |
| Navigate org change, keep teams focused | GitLab→GitHub migration, modernisation programmes under concurrent business pressure |

This is the same leadership model as sevDesk — manager-of-managers, owning delivery, standards, and team health across squads. The scale (20–25 people, 3 squads) is smaller than sevDesk's 40+ indirect but the structure is identical.

### Technical Stack — GOOD MATCH WITH ONE GAP

| Stack item | Assessment |
|---|---|
| Kotlin | ✓ Core stack at sevDesk (Spring Boot/Kotlin) |
| AWS | ✓ Primary cloud at sevDesk |
| Kafka | ✓ Familiarity — not a listed CV strength but present in distributed systems work |
| PostgreSQL | ✓ Relational DB experience throughout |
| React / React Native | ✓ Frontend stack at Würth and sevDesk |
| **Golang** | ✗ Not in background — gap |
| Observability (Datadog/Grafana/PagerDuty) | ✓ Datadog, New Relic, PagerDuty at sevDesk |
| SRE / SLOs / on-call | ✓ On-call programmes and incident management established at sevDesk |

Golang is the only hard stack gap. For a Director role it matters less than for a Staff Engineer, but the posting calls for "hands-on familiarity" — something to address transparently or acquire quickly.

### Payments Domain — PARTIAL GAP ⚠️

No prior direct payments engineering experience. The posting requires "deep technical expertise" in payment processing, gateway services, batch transaction processing, and regulated multi-market environments.

What maps across:
- GoBD-compliant cloud infrastructure at sevDesk (financial software, compliance-grade infrastructure) — closest analogue
- High-throughput, reliability-critical systems (SLOs, incident management, PagerDuty) at sevDesk
- Financial services client work at adesso (Finanz- und Versicherungssektor)

What doesn't: no PSP integration work, no payment gateway architecture, no direct PCI-DSS or financial transaction system ownership. This is a meaningful gap but not an absolute disqualifier at Director level — the architecture thinking and reliability engineering transfer; the domain specifics are learnable.

### GenAI Transformation — STRONG MATCH ✓

"Own the GenAI transformation of the Payments Tribe" is the first listed responsibility. The mandate is concrete: AI-assisted development, automated incident response, agentic workflows, LLM-powered tooling.

Directly evidenced:
- GitHub Actions as AI-tooling foundation at sevDesk
- AI developer platform strategy at Cloudfactory (50Hertz mandate)
- Active practitioner of AI-assisted engineering workflows

This is a differentiator, not just a checkbox. Most candidates at this level will have opinions on GenAI; fewer have shipped the infrastructure that enables it.

### Compensation — REQUIRES SCRUTINY ⚠️

"Heavily weighted toward equity" (VSO + RSU) is explicitly stated. This means base salary is likely below what a purely cash-compensated role would offer at this level. HelloFresh is publicly listed (FRE on XETRA) — RSUs have real value but also volatility and vesting schedules.

Glassdoor data suggests Director of Engineering total comp at HelloFresh averages ~€150k, but the equity-heavy framing suggests base may be in the €120–130k range with the balance in stock. Must confirm base before proceeding — it likely falls short of the €150k base floor.

### Company Context — GOOD FIT

HelloFresh is a large-scale, publicly listed B2C product company with genuine engineering complexity at scale (8.5M customers, multi-market payments infrastructure). Not a classic SaaS B2B setup but product engineering at real scale. Fits the preference for companies where software is the core product.

---

## Key Risks

1. **Compensation structure** — equity-heavy framing is a yellow flag; confirm base salary explicitly before investing in full application
2. **Payments domain gap** — real, but manageable at Director level; needs to be addressed proactively in cover letter
3. **Golang** — minor for this level; worth a brief mention of willingness/speed to close it
4. **HelloFresh's business context** — the company has gone through significant restructuring (sold US operations, cut headcount); stability and mandate clarity worth exploring in interview

---

## CV Tailoring Proposals (if compensation clears)

1. **Lead with manager-of-managers track record** — the 6 EM / 40+ developer structure at sevDesk is a direct match to 3 squads / 20–25 people
2. **GoBD compliance infrastructure → payments framing** — sevDesk is financial software; compliance-grade, high-reliability infrastructure is the closest analogue to payments infrastructure
3. **SRE practices** — make the on-call programme, PagerDuty, incident management, and SLO work at sevDesk explicit and prominent
4. **GenAI as a lead differentiator** — GitHub Actions AI-tooling foundation + Cloudfactory AI developer platform; this is their #1 listed responsibility, make it a centrepiece
5. **Payments gap: address directly in cover letter** — acknowledge no PSP work, but anchor on: financial software domain (sevDesk), reliability engineering at scale, and fast domain acquisition track record
6. **Profile base:** `greenfusion-vp-engineering-de.yaml` is close; swap subtitle to "Director of Engineering · Payments & Platform · Engineering at Scale"; replace adesso with durstexpress-lead-pm for cross-functional product/eng collaboration angle

---

## Recommendation

**Worth pursuing — gated on salary confirmation.** The leadership profile, GenAI mandate, SRE background and Kotlin/AWS stack are strong matches. The payments domain gap is real but not disqualifying at Director level if framed well. The equity-heavy comp is the primary gate — confirm base before building full materials.

Outreach priority: **medium-high** if base ≥ €140k (equity upside from RSUs could bridge to €150k+ total); **pass** if base is below €130k.
