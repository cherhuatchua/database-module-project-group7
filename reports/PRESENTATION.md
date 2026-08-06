# Career Compass SG — Team Presentation Plan

**Module 1 Assignment · Group 7 · 10 minutes · the assignment's official 4-section flow**

> **This document is the team's coordination sheet.** Each section has its **own script** in
> `reports/speakers/` — that is what you rehearse from. This page is what you agree on
> together: who speaks when, the handovers, and who takes which question.

---

## Running order — matches the assignment brief exactly

| # | Section (official name) | Official guide | Ours | Speaker | Script |
|---|---|---|---|---|---|
| 1 | **Business case & objective** | 2–3 mins | **2:15** | | `speakers/01_business_case_and_objective.pdf` |
| 2 | **Process & data handling** | 3–4 mins | **3:30** | | `speakers/02_process_and_data_handling.pdf` |
| 3 | **Dashboard / app walkthrough** | 3–4 mins | **3:00** | | `speakers/03_dashboard_walkthrough.pdf` |
| 4 | **Challenges & learnings** | 1–2 mins | **1:15** | | `speakers/04_challenges_and_learnings.pdf` |

Total = **10:00**. Every measured script runs 5–10 seconds under its slot, which is your
handover allowance. **Write names in the blank column and keep a printed copy on the desk.**

**Five members, four sections:** the natural split is one section each plus a dedicated
**demo driver** — the fifth member sits at the laptop and drives the mouse during Section 3
while the speaker narrates. That keeps the walkthrough smooth and gives everyone a live
role. (Alternatively the fifth member leads Q&A.)

---

## The arc — what the room should feel

| Section | The one thing it must land |
|---|---|
| 1 | *A specific user, a specific decision: which career track should I target next?* |
| 2 | *We found a hidden trap in the data that would have flipped our conclusions.* |
| 3 | *Three screens answer the question — and the ranking changes live when priorities change.* |
| 4 | *The best-paying track and the easiest-to-enter track are almost never the same track.* |

Read down that column: one argument, four steps.

---

## Handovers — rehearse these out loud

| From → To | The line |
|---|---|
| 1 → 2 | *"So that's the question we set out to answer. Now — how we turned one million messy rows into data we could trust."* |
| 2 → 3 | *"That's the data. Now — the dashboard we built on top of it."* |
| 3 → 4 | *"That's the product. My teammate will close with what this project taught us."* |
| 4 → end | *"…and lets you decide which one you need this year. Thank you."* |

---

## Live demo (Section 3 only)

**Three screens, one interaction. Nobody else opens the dashboard.**

1. **Market Overview** — the market at a glance, medians, honesty marks
2. **Demand vs Competition** — the opportunity map, 0.7 → 11.3 applicants per seat
3. **Career Recommender** — pre-set persona, then drag the sliders: top five changes live

**Setup before you walk up:**

- Dashboard already running at `http://localhost:8501` — never start it in front of the room
- Browser zoom ~80%; Recommender inputs pre-set (3 years, $4,000)
- **Screenshot fallback slides for all three screens.** If the demo fails, switch and
  narrate. **Nobody debugs in front of the room.**

---

## Time discipline

- Section 2 is the longest and richest. **Its cut rule: drop the "two traps" part, protect
  the June 2023 story.**
- Section 3's cut rule: shorten Screen 1 to one sentence; **the slider moment must happen.**
- Whoever is not speaking watches the clock and gives a visible 30-second signal.

---

## Question ownership

When a question comes, **the owner answers** — do not all start talking.

| Topic | Owner |
|---|---|
| Business case, target user, "why not LinkedIn", success criteria | 1 |
| Cleaning rules, the June 2023 break, duplicates, Parquet/pipeline | 2 |
| Any dashboard page, filters, the score, the weights, the demo | 3 |
| Lessons, limitations, next steps, "what would you do differently" | 4 |
| Anything else | 1 (and it's fine to say "we didn't test that") |

### The three most likely questions

1. **"Why is competition only measured up to June 2023?"** → Owner 2. The counters freeze
   after that date; 79% of later postings show zero applications. ~200,000 postings remain.
2. **"Isn't IT the obvious answer anyway?"** → Owner 3. IT is biggest and best-paid — with
   ~5 applicants per seat, and postings **down 11.7%** in six months. The obvious answer is
   the crowded, cooling one.
3. **"Aren't your score weights arbitrary?"** → Owner 3. Deliberately — that's why they're
   sliders the user controls, not constants we chose for them.

---

## Rehearsal checklist

- [ ] One full run-through against a clock — **under 10:00 including handovers**
- [ ] Every speaker has read *their own* script in `reports/speakers/`
- [ ] Handover lines rehearsed — the joins are where teams lose time
- [ ] Demo path (3 screens + slider drag) run on the actual presentation machine
- [ ] Screenshot fallbacks exist for all three demo screens
- [ ] Question ownership agreed and printed
- [ ] Everyone can answer the June 2023 question, not just Owner 2

---

## Supporting documents

| Document | What it is |
|---|---|
| `reports/speakers/0*.pdf` | the four section scripts — **rehearse from these** |
| `reports/PROJECT_REPORT.pdf` | the full written report (assignment sections 1–4) |
| `notebooks/01_eda.ipynb` | the EDA behind every claim made on stage |
| `SETUP.md` | how to run the dashboard and rebuild the data |
