# Speaker 3 of 5 — Data Cleaning

**Career Compass SG · Module 1 Assignment · Group 7**

**Your slot: 3:45 – 6:00 (2 minutes 15 seconds) · You have the strongest material**

---

## Your job in one sentence

**Prove that we understood this data rather than just loading it.** You own the single best
story in the whole presentation — the engagement break — and the assessment gives 25% to
data handling, the largest single weighting. Spend your time on the *reasoning*, not the
inventory of rules.

## Where you sit in the flow

| | Speaker | Topic |
|---|---|---|
| | 1 | Dashboard overview |
| | 2 | Technology stack |
| **→ YOU** | **3** | **Data cleaning** |
| | 4 | Data analysis 1 — market & pay |
| | 5 | Data analysis 2 — competition, skills & scoring |

**Speaker 2 hands you:** *"…none of it matters if the numbers going in are wrong — and this
dataset had a trap in it."*
**You hand to Speaker 4** with: *"So that's the data we trust. Here's what it actually says."*

> **Discipline rule:** you are the most likely person to overrun. **If the clock passes 5:00
> and you haven't started Part C, skip straight to it.** Part C is the part that must land.

---

## Script

### Part A — The principle, not the inventory *(3:45 – 4:25)*

*(Slide: cleaning decisions — you will walk 3 rows, not 11)*

> Eleven cleaning rules. I'll give you the **principle** instead: **blank the untrustworthy
> field, keep the trustworthy row.** A posting with a broken salary still proves a job exists.
>
> - **`occupationId` was 100% empty** across all 1.05 million rows — dropped.
> - **10,016 postings claimed a monthly salary above $60,000 or below $500** — annual figures
>   in a monthly field. We blanked the salary and kept the posting.
> - **We capped the top and bottom 1%** rather than deleting, because deleting would have
>   biased our demand counts.
>
> **99.6% of rows survive.**

### Part B — Two traps worth naming *(4:25 – 4:55)*

*(Slide: the duplicates trap + the two-table diagram)*

> Two traps.
>
> **`.duplicated()` lied to us** — it reported 289 duplicate job IDs; all 289 were repeated
> **blanks**. There are **zero real duplicates**.
>
> **And one job belongs to up to three categories** — 1.69 on average — so counting rows and
> counting category-rows answer different questions. We shipped that bug to ourselves: for an
> hour our overview said **1.66 million postings instead of 1.04.**

### Part C — The finding that changed the product *(4:55 – 6:00)*

*(Slide: the two-line engagement chart — this is your centrepiece, do not rush it)*

> **Now the finding that changed everything.**
>
> We plotted views and applications over time as a sanity check. Look at **June 2023**: mean
> views per posting falls **from about 111 to about 5.** Zero-application postings jump **from
> 18% to 79%.**
>
> That's not Singapore losing interest. **This dataset is two extracts stitched together** —
> everything after July 2023 was captured at posting time, so those counters never accumulated.
>
> **So demand and salary use all 1.04 million rows, but every competition metric uses only
> postings up to 30 June 2023** — 203,702 of them — and it says so on screen every time.
>
> **If we'd missed this, every track would have looked uncontested, and our recommender would
> have pointed people at the most crowded markets in Singapore.**
>
> Same story, smaller: **volume ramps until May 2023**, so every trend figure starts there.
>
> **That's the data we trust. Here's what it says.**

---

## Numbers you must know cold

| Figure | Value |
|---|---|
| Rows read → rows kept | **1,048,585 → 1,044,597 (99.6%)** |
| Wholly empty rows dropped | 3,988 (0.38%) |
| Impossible salaries blanked | **10,016** |
| Rows capped at 1st/99th percentile | **19,647** (band $1,150 – $16,500) |
| Genuine duplicate job IDs | **0** (the 289 were repeated blanks) |
| Categories per posting | **1.69 average**, max 3 → 1,767,829 long rows |
| **Engagement break** | **views 111 → 5; zero-application 18% → 79%, at Jun/Jul 2023** |
| Competition window | postings ≤ **2023-06-30**, **203,702** of them |
| Volume reliable from | **May 2023** (~75,000 postings/month) |
| Salary disclosed after cleaning | 99.0% |

## The eleven rules, if anyone asks for the full list

| Issue | Decision |
|---|---|
| `occupationId` 100% null | drop column |
| `status_id` duplicates `status_jobStatus` | drop column |
| 3,988 wholly empty rows | drop rows |
| `salary == 0` | set to missing — zero means "not disclosed" |
| salary < $500 or > $60,000/month | blank the salary, keep the row |
| `salary_min > salary_max` | swap the values — fields entered backwards |
| long right tail | cap at 1st/99th percentile |
| experience > 40 years | set to missing |
| vacancies 0 or > 500 | floor at 1 / blank above 500 |
| duplicate job IDs | de-duplicate `keep="last"` (no-op here) |
| `categories` JSON array | parse and explode to a long table |

## Questions you own

**"Why cap outliers instead of dropping them?"**
> Dropping the row removes the posting from the demand count too. Capping keeps the demand
> signal honest while stopping 19,647 extreme values from steering every average.

**"How do you know the June 2023 break is a collection artefact and not real?"**
> Three things move together at exactly one boundary: mean views, zero-application share, and
> nothing else — posting volume, salaries and categories are all continuous across it. A real
> collapse in jobseeker interest would show up in the postings too. It doesn't.

**"Isn't throwing away 80% of your data for competition metrics a problem?"**
> We're not throwing it away — demand and salary still use all of it. For competition we use
> 203,702 postings, which is an ample base. The alternative was using numbers we know are wrong.

**"Why `repost_count >= 1` for hard-to-fill and not `>= 2`?"**
> Because the field is capped at 2 in this extract — the only values are 0, 1 and 2. At `>= 2`
> we'd flag 1.4% of postings; at `>= 1`, 4.1%. Any repost at all is the meaningful signal here.

**"What about the 0.14% of missing values — why drop rows rather than impute?"**
> We checked first whether the gaps were the *same* rows. They were: wholly empty export lines
> with no ID, no title, no company and no dates. There's nothing to impute from.

---

## Rehearsal checklist

- [ ] Timed at **2:15** — and you know which part to cut if you're over (Part A drops to one example)
- [ ] You can deliver the engagement-break story **without the slide**, from memory
- [ ] You can say why it's an artefact, not a real signal, in two sentences
- [ ] You are comfortable saying "we shipped that bug to ourselves" — owning a mistake reads
      as competence, not weakness
- [ ] Handover line to Speaker 4 practised
