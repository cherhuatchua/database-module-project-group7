# Speaker 4 of 5 — Data Analysis 1: Market & Pay

**Career Compass SG · Module 1 Assignment · Group 7**

**Your slot: 6:00 – 8:00 (2 minutes) · You deliver the first half of the findings**

---

## Your job in one sentence

**Answer "where are the jobs and what do they pay" — and then break the assumption that
those are the same question.** Your section is what forced the whole product design, so
land the independence point clearly; Speaker 5 builds directly on it.

## Where you sit in the flow

| | Speaker | Topic |
|---|---|---|
| | 1 | Dashboard overview |
| | 2 | Technology stack |
| | 3 | Data cleaning |
| **→ YOU** | **4** | **Data analysis 1 — market & pay** |
| | 5 | Data analysis 2 — competition, skills & scoring |

**Speaker 3 hands you:** *"…so that's the data we trust. Here's what it actually says."*
**You hand to Speaker 5** with: *"Volume and pay are two of the four dimensions. The other
two are where it gets interesting."*

> **Framing rule:** every finding is a **sentence**, not a chart. Say the sentence, then point
> at the evidence. Never say "as you can see here".

---

## Script

### Part A — Where the jobs are is not where the money is *(6:00 – 6:45)*

*(Slide: the two-panel chart — postings on the left, median pay on the right, same row order)*

> Two panels, same twelve categories, same order. Left: **how many postings**. Right: **what
> they pay**. If size and pay moved together these would be the same shape. **They're not.**
>
> - **Admin / Secretarial is the third-largest category** — 117,854 postings — and among the
>   worst paid at **$2,900**, against a market median of $3,850.
> - **IT is the only large category that's both biggest and best paid** — 140,866 postings at
>   **$6,500**. The exception, not the rule.
>
> **Where the jobs are and where the money is are different questions.** That's why we score
> four dimensions instead of one.

### Part B — What an average hides *(6:45 – 7:10)*

*(Slide: the salary histogram with both lines marked)*

> One note on how we report pay. The distribution is **right-skewed — skew 1.95.** The **mean
> is $4,674; the median is $3,850.** That $800 gap means the mean describes almost nobody.
>
> **So every headline figure we publish is a median**, and this chart shows both lines so you
> can see why.

### Part C — What experience is actually worth *(7:10 – 7:50)*

*(Slide: the seniority ladder + the IT experience curve)*

> Now the question a switcher actually asks: **what does moving up buy me?**
>
> | Level | Median |
> |---|---|
> | Entry | $2,675 |
> | Junior | $3,150 |
> | Mid | $4,000 |
> | Senior | $5,000 |
> | Management | $6,500 |
>
> **Entry to Management is a 2.4× multiple** — but the rate of climb varies hugely by field. In
> **IT, each extra year of required experience is worth about $908 a month** — $3,100 at zero
> years, **$14,000 at twelve.**
>
> One surprise: **part-time pays a 36% discount**, $2,500 against $3,900 permanent. But
> **contract pays more than permanent, at $4,250.** A contract isn't automatically a pay cut.

### Part D — Handover *(7:50 – 8:00)*

> Volume and pay are two of our four dimensions, and they already disagree. **The other two are
> where it gets interesting.**

---

## Numbers you must know cold

| Figure | Value |
|---|---|
| Market median / mean / skew | **$3,850 / $4,674 / 1.95** |
| Quartiles | $2,950 (p25) – $5,500 (p75) |
| Best-paid sizeable category | **Information Technology, $6,500** (140,866 postings) |
| Worst-paid sizeable category | General Work, **$2,650** (30,140 postings) |
| Third-largest category | Admin / Secretarial, 117,854 postings, **$2,900** |
| Seniority ladder | 2,675 → 3,150 → 4,000 → 5,000 → **6,500** |
| IT return on experience | **~$908/month per year**; $3,100 at 0 yrs → $14,000 at 12 |
| Part-time vs permanent | $2,500 vs $3,900 — a **36% discount** |
| Contract | **$4,250 — above permanent** |

## Backup figures

**Top 5 best-paying categories (≥ 2,000 postings)**

| Category | Postings | Median |
|---|---|---|
| Information Technology | 140,866 | $6,500 |
| Risk Management | 9,390 | $6,000 |
| Banking and Finance | 62,000 | $5,500 |
| Consulting | 38,961 | $4,750 |
| Insurance | 7,994 | $4,750 |

**Five largest categories**

| Category | Postings | Median |
|---|---|---|
| Information Technology | 140,866 | $6,500 |
| Engineering | 136,372 | $4,250 |
| Admin / Secretarial | 117,854 | $2,900 |
| Customer Service | 111,785 | $3,100 |
| Sales / Retail | 105,067 | $3,600 |

## Questions you own

**"Are these salaries reliable? Employers exaggerate."**
> These are advertised bands, not offers — we say that explicitly. What makes them usable is
> volume and consistency: 99% of a million postings disclose a band, and we're comparing
> categories against each other on the same measure, so any systematic advertising bias
> largely cancels out.

**"Why medians everywhere?"**
> Skew of 1.95. The mean is $4,674 against a $3,850 median — the mean sits above what most
> people would actually be offered.

**"Isn't the experience curve just seniority relabelled?"**
> They're different fields — `minimumYearsExperience` is a number in the posting,
> `positionLevels` is a category. They correlate, but the curve lets us price a *year*, which
> the seniority band can't.

**"Category shares don't add to 100% — why?"**
> A posting can belong to up to three categories; the average is 1.69. Shares overlap by
> design, and we say so on the dashboard.

**"Why is Admin so big and so badly paid — is that not just Singapore?"**
> It's a large, low-barrier category: 57.5% of its postings are open to someone with a year of
> experience or less. High accessibility and low pay travel together, which is exactly the
> trade-off our recommender makes visible.

---

## Rehearsal checklist

- [ ] Timed at **2:00 or under**
- [ ] You can say the independence finding — "where the jobs are is not where the money is" —
      as a clean one-liner
- [ ] You know the seniority ladder from memory (2,675 / 3,150 / 4,000 / 5,000 / 6,500)
- [ ] You never say "as you can see" — you say the finding first, then point
- [ ] Handover line to Speaker 5 practised
