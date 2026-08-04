# Career Compass SG — Team Presentation Plan

**Module 1 Assignment · Group 7 · 5 speakers · up to 3 minutes each**

> **This document is the team's coordination sheet.** Each speaker has their **own script**
> in `reports/speakers/` — that is what you rehearse from. This page is what you agree on
> together: who speaks when, the handovers, and who takes which question.

---

## Running order

| # | Topic | Speaker | Time cap | Script | Measured length |
|---|---|---|---|---|---|
| 1 | **Dashboard overview** | | 3:00 | `speakers/01_dashboard_overview.pdf` | ~2:50 |
| 2 | **Project technology stack** | | 3:00 | `speakers/02_technology_stack.pdf` | ~2:40 |
| 3 | **Data cleaning** | | 3:00 | `speakers/03_data_cleaning.pdf` | ~2:50 |
| 4 | **Data analysis 1 — Demand vs Competition** | | 3:00 | `speakers/04_data_analysis_1_demand_vs_competition.pdf` | ~2:55 |
| 5 | **Data analysis 2 — Career Recommender** | | 3:00 | `speakers/05_data_analysis_2_career_recommender.pdf` | ~2:50 |

Total speaking time ≈ **14 minutes** plus handovers. **Write your names in the blank column
and keep a printed copy on the desk.**

---

## The arc — what the room should feel

| Speaker | The one thing they must land |
|---|---|
| 1 | *A job website can't tell you which job is worth taking. We built the thing that can.* |
| 2 | *The architecture was a choice — a million rows filter in 0.06 seconds.* |
| 3 | *We found a hidden trap in the data that would have flipped our conclusions.* |
| 4 | *"Lots of jobs" and "easy to get a job" are completely different things — we measured both.* |
| 5 | *Same data, different person, different advice — and every step of it visible.* |

Read down that column: it is one argument, and each speaker is one step. If a sentence in
your section doesn't advance it, cut the sentence.

---

## Handovers — rehearse these out loud

| From → To | The line |
|---|---|
| 1 → 2 | *"That's what the product looks like. Now — the technology that makes it run."* |
| 2 → 3 | *"But fast technology means nothing if the data going in is wrong — and this dataset had a trap hidden inside it."* |
| 3 → 4 | *"So that's the data we can trust. Now — what it tells us about demand and competition."* |
| 4 → 5 | *"A map shows everyone the same picture. How do you turn it into advice for one person? That's the Career Recommender."* |
| 5 → close | *"Career Compass shows you both — and lets you decide which one you need this year."* |

---

## Live demo split

Two speakers touch the dashboard. **Nobody else opens it.**

| Speaker | Screens | Discipline |
|---|---|---|
| **1** | Market Overview → Career Explorer | **Two clicks.** Shows what the product is. |
| **5** | Career Recommender + weight sliders | **One interaction.** The payoff — the ranking changes live. |

**Setup before you walk up:**

- Dashboard already running at `http://localhost:8501` — never start it in front of the room
- Browser zoom ~80% so charts fit the projector
- Speaker 5's inputs pre-set: 3 years' experience, $4,000 minimum
- **Screenshot fallback slides for every demo screen.** If it fails, switch and narrate.
  **Nobody debugs in front of the room.**

---

## Time discipline

- Every script is measured at **~2:40–2:55** at a normal presenting pace — if you rehearse
  it once against a clock, you will fit.
- **Speaker 3's cut rule:** if running late, drop Part 2 (the two traps) and protect Part 3
  (the June 2023 story).
- **Speaker 4's cut rule:** if running late, drop Part 3 (hard-to-fill) and keep the map.
- Whoever is not speaking watches the clock and gives a visible 30-second signal.

---

## Question ownership

When a question comes, **the owner answers** — do not all start talking.

| Topic | Owner |
|---|---|
| Business case, target user, "why not LinkedIn" | 1 |
| Architecture, Parquet, Streamlit vs BI tools, scaling | 2 |
| Any cleaning rule, the June 2023 break, duplicates | 3 |
| The opportunity map, applicants per seat, hard-to-fill | 4 |
| The score, the weights, the demo, "isn't it arbitrary" | 5 |

**If a question lands outside everyone's section:** Speaker 1 takes it. It is completely
fine to say *"we didn't test that — here's what we'd need to do to answer it."*

### The three most likely questions

1. **"Why is competition only measured up to June 2023?"** → Speaker 3. The counters freeze
   after that date; 79% of later postings show zero applications. ~200,000 postings remain,
   which is plenty.
2. **"Isn't IT the obvious answer anyway?"** → Speaker 4 or 5. IT is biggest and best-paid —
   and its postings **fell 11.7%** in six months, and it has ~5 applicants per seat. The
   obvious answer is the cooling, contested one.
3. **"Aren't your score weights arbitrary?"** → Speaker 5. Deliberately — that's why they're
   sliders the user controls, not constants we chose for them.

---

## Rehearsal checklist

- [ ] One full run-through against a clock, all five speakers, each **under 3:00**
- [ ] Every speaker has read *their own* script in `reports/speakers/`
- [ ] Handover lines rehearsed — the joins are where teams lose time
- [ ] Speakers 1 and 5 have run their demo paths on the actual presentation machine
- [ ] Screenshot fallbacks exist for every demo screen
- [ ] Question ownership agreed and printed
- [ ] Everyone can answer the June 2023 question, not just Speaker 3

---

## Supporting documents

| Document | What it is |
|---|---|
| `reports/speakers/0*.pdf` | the five individual speaker scripts — **rehearse from these** |
| `reports/PROJECT_REPORT.pdf` | the full written report (assignment sections 1–4) |
| `notebooks/01_eda.ipynb` | the EDA behind every claim made on stage |
| `SETUP.md` | how to run the dashboard and rebuild the data |
