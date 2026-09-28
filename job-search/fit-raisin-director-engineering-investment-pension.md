# Fit Assessment — Director Engineering, Investment & Pension Domain
**Company:** Raisin GmbH — world's leading savings and investment platform (Series D+, 800+ employees, €80B+ AuM)
**Location:** Berlin
**Team:** 25+ engineers in the Investment & Pension (IPP) domain
**Model:** "Binary-star" co-leadership with a Director of Product counterpart
**Salary:** Not stated
**Date assessed:** 2026-09-28
**Source:** job-boards.eu.greenhouse.io/raisin/jobs/4922825101

**Note:** Raisin appeared in the history once before — March 2019, "Chapter Lead Backend", rejected. Different role, 7 years ago; not a meaningful signal either way.

---

## Overall Fit: MEDIUM (40–45%)

Strong structural and leadership match — the IPP team at 25+ engineers is smaller than the sevDesk scope but the pattern (domain-owning engineering director in a binary-star model with product) is familiar territory. The problem is the hard requirement: **4+ years in FinTech**. sevDesk is the only plausible candidate, and (a) it runs to ~2.75 years and (b) whether accounting SaaS counts as FinTech depends on Raisin's definition. If they read FinTech strictly (investment, banking, payments, lending), Tobias has zero. If broadly (financial software), he has under three years. Either way it's a named screen, not boilerplate. The investment/pension domain gap is secondary but real.

---

## Dimension-by-Dimension Analysis

### Engineering Leadership at Director Level — STRONG MATCH ✓

| Requirement | Evidence |
|---|---|
| 10+ years leadership experience | Engineering leadership from adesso (2016), through Würth, sevDesk — 9+ years in senior roles |
| Track record developing high-performing teams | Career frameworks + EM coaching at sevDesk; built team from scratch at Würth |
| OKR/KPI-based management | Introduced OKRs at sevDesk as binding steering system; DORA metrics as delivery KPIs |
| Binary-star co-leadership with Product | Exactly the sevDesk model — Engineering Director alongside a Product Director per pillar |
| Attract and retain top talent globally | Full hiring ownership at sevDesk (including hiring a peer Engineering Director); Würth built from zero |
| Hands-on technical mentality | Architecture ownership at Würth; ADRs and technical debt governance at sevDesk |

### FinTech Experience — GAP ⚠️ (hard requirement)

The posting states: *"At least 4y experience in FinTech."*

Honest accounting of the background:

- **sevDesk GmbH** (Feb 2023 – Nov 2025, ~2.75 years): cloud accounting/invoicing SaaS for German SMEs. Finance-adjacent — handles tax compliance (GoBD), invoicing, payroll. Arguable FinTech depending on definition.
- **Würth Cloud Services** (Apr 2021 – Jan 2023): B2B platform for craftsmen. Not FinTech.
- **adesso SE** (2016–2019): IT consulting, including finance and insurance sector clients. Not FinTech in the product sense, though relevant exposure.
- **Cloudfactory / 50Hertz** (2025–present): energy infrastructure. Not FinTech.

Best case: sevDesk is counted as FinTech → ~2.75 years, still below the 4-year bar.
Worst case (Raisin's likely view): FinTech = investment, banking, payments, lending → zero qualifying years.

This is the single biggest risk. Raisin explicitly builds investment and pension products under BaFin/MiFID II regulation. Their FinTech requirement almost certainly means the financial services industry, not accounting software.

### Technology Stack — PARTIAL MATCH

| Stack item | Tobias |
|---|---|
| AWS | Strong — sevDesk ran on Kubernetes/Docker on AWS |
| Java | Strong — Spring Boot/Kotlin at sevDesk, Java at adesso |
| SQL | Implied, not explicitly highlighted |
| **Kafka** | **Not mentioned anywhere in the background — gap** |

Kafka is listed as a core skill requirement alongside AWS, Java, and SQL. It is common in event-driven financial platforms (exactly what Raisin would use for savings/investment event streams). Absence of Kafka from the CV is a visible technical gap at Director level where stack credibility matters.

### Domain: Investment & Pension — GAP (advantageous, not required)

The posting lists investment products domain knowledge as "advantageous" rather than required, which is honest — a Director can lead domain engineers without prior domain depth. However, at Raisin the domain (pension schemes, investment products, fund administration, regulatory reporting) is complex and highly regulated. The team would expect their Director to build domain knowledge quickly and engage credibly on regulatory topics. No financial product background exists to draw on.

### Company Stage & Profile — MATCH ✓

Raisin is Series D+ with 800+ employees and €80B+ AuM — established, scaled, sustainable. Not a pre-product-market-fit startup. Berlin-based. Not an excluded sector.

### Salary — Unknown

Not stated. Raisin Director Engineering in Berlin: likely €140k–€170k. Needs early confirmation.

---

## Key Risks

1. **FinTech experience requirement** — explicitly stated at 4 years; sevDesk is the only candidate and it is both too short (~2.75y) and arguably outside the definition
2. **Kafka gap** — named in the required stack; absence is visible
3. **Investment/pension domain depth** — listed as advantageous but Raisin's core business is exactly this; interviewers will probe it
4. **Prior rejection** — 2019 rejection for Chapter Lead Backend was at a much lower level and is unlikely to be a factor, but worth noting

---

## Recommendation

**Low priority — do not pursue unless FinTech gap can be argued.** The leadership and structural match is genuinely good: binary-star model, team size, OKR discipline, career framework, AWS/Java/K8s delivery. But the FinTech requirement is both named and under-met. If the application passes screening at all, the FinTech question will come in the first call and the honest answer is "sevDesk is accounting software, which is finance-adjacent but not FinTech in the way you mean it." That is a weak position to open from.

If Tobias believes sevDesk's financial software context is sufficient to make the argument, and if salary clears €150k, it is worth a speculative application — the leadership match means there is something real to talk about. But it should be ranked below positions where the domain gap does not exist.
