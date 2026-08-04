# Speaker 3 of 5 — Data Cleaning

**Career Compass SG · Module 1 Assignment · Group 7**

**Your time: up to 3 minutes · You have the strongest story in the presentation**

---

## Your job in one sentence

**Prove we understood this data instead of just loading it.** Data handling carries the
biggest weight in the marking (25%), and you own the best story in the whole talk — the
discovery that the dataset was secretly two files stitched together.

## Where you sit in the flow

| | Speaker | Topic |
|---|---|---|
| | 1 | Dashboard overview |
| | 2 | Project technology stack |
| **→ YOU** | **3** | **Data cleaning** |
| | 4 | Data analysis 1 — Demand vs Competition |
| | 5 | Data analysis 2 — Career Recommender |

**Speaker 2 hands you:** *"…this dataset had a trap hidden inside it."*
**Your handover to Speaker 4:** *"So that's the data we can trust. Now let's see what it
tells us about demand and competition."*

> **Time rule:** if you are running late, cut Part 2. **Part 3 is the story that must be
> told** — protect it.

---

## Script

### Part 1 — Our cleaning principle *(0:00 – 0:50)*

*(Slide: cleaning examples — show 3, not all 11)*

> We wrote eleven cleaning rules. The one principle behind all of them:
>
> **If a value is broken, blank the value — but keep the row.**
>
> A posting with a broken salary still proves **a job existed** — deleting the whole row
> would break our job counts just to make salaries look clean. Three examples:
>
> - One column was **completely empty** in all 1.05 million rows — dropped.
> - About **10,000 postings claimed salaries like $180,000 a month** — yearly figures in a
>   monthly field. We blanked the salary, kept the posting.
> - The most extreme 1% of salaries were **capped, not deleted**.
>
> After all the cleaning, **99.6% of the rows survive**.

### Part 2 — Two traps that nearly caught us *(0:50 – 1:30)*

*(Slide: the two traps)*

> Two traps worth sharing, because they could catch anyone in this room.
>
> **Trap one: the duplicate check lied.** pandas reported 289 duplicate job IDs — all 289
> were **empty cells compared with each other**. Real duplicates: **zero**.
>
> **Trap two: one job can belong to up to three categories** — 1.69 on average. Count rows
> after splitting by category and you double-count. We made this mistake ourselves: for an
> hour our front page said **1.66 million postings instead of 1.04 million** — and it
> looked completely believable.

### Part 3 — The discovery that changed everything *(1:30 – 2:50)*

*(Slide: the two-line engagement chart — speak slowly here)*

> Now the big one.
>
> As a routine check, we plotted views and applications **over time**. We were not looking
> for a problem. Look at what happens at **June 2023**.
>
> Average views per posting **fall from about 111 to about 5**. The share of postings with
> **zero applications jumps from 18% to 79%**.
>
> Did Singaporeans stop applying for jobs? Of course not. **This dataset is two separate
> downloads stitched together.** Postings after June 2023 were captured the moment they
> were posted — their counters **never had time to grow**. They're frozen at zero.
>
> So our design decision: **job counts and salaries use all 1.04 million rows, but
> competition uses only postings up to June 2023** — about 200,000 — and every page says
> so on screen.
>
> If we had missed this, every track would have looked like it had **no competition at
> all** — and our recommender would have sent people into the most crowded markets in
> Singapore.
>
> **That is the difference between a dashboard and a wrong dashboard.**
>
> **So that's the data we can trust. Now — what it tells us about demand and competition.**

---

## Numbers you must know cold

| Figure | Value |
|---|---|
| Rows read → kept | **1,048,585 → 1,044,597 (99.6%)** |
| Impossible salaries blanked | ~10,000 |
| Salary rows capped (top/bottom 1%) | 19,647 |
| Real duplicate job IDs | **0** (the "289" were blanks) |
| Categories per job | **1.69 average**, max 3 |
| **The break** | **views 111 → 5, zero-application 18% → 79%, at June 2023** |
| Competition window | postings up to **30 June 2023** (~203,702) |

## Questions you own

**"Why cap outliers instead of deleting them?"**
> Deleting the row also deletes the job from our demand counts. Capping keeps the counts
> honest while stopping extreme values from distorting averages.

**"How do you know the June 2023 break is a data problem and not real?"**
> Because only the engagement counters break — posting volume, salaries, and categories all
> continue smoothly across that date. A real market collapse would show up everywhere.

**"Isn't using only 200,000 postings for competition too few?"**
> It's still two hundred thousand postings — plenty. And the alternative was using numbers
> we *know* are frozen at zero. Better a smaller honest number than a bigger wrong one.

**"Why drop rows with missing values instead of filling them in?"**
> We checked first: the missing values were all on the *same* rows — completely empty lines
> with no ID, no title, no dates. There was nothing left to fill in from.

---

## Rehearsal checklist

- [ ] Timed at **3:00 or under** — and you know Part 2 is the part to cut if late
- [ ] You can tell the June 2023 story from memory, without the slide
- [ ] You can explain in one sentence why the counters are frozen, not wrong
- [ ] You are comfortable admitting our own 1.66-million bug — owning it reads as competence
- [ ] Handover line practised
