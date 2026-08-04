# Career Compass SG — Team Presentation Plan

**Module 1 Assignment · Group 7 · 10 minutes · 5 speakers**

> **This document is the team's coordination sheet.** Each speaker has their **own script** in
> `reports/speakers/` — that is what you rehearse from. This page is what you agree on
> together: who speaks when, what the handovers are, and who takes which question.

---

## Timing plan

| # | Topic | Speaker | Time | Runs from | Script |
|---|---|---|---|---|---|
| 1 | **Dashboard overview** | | 2:15 | 0:00 | `speakers/01_dashboard_overview.pdf` |
| 2 | **Project technology stack** | | 1:30 | 2:15 | `speakers/02_technology_stack.pdf` |
| 3 | **Data cleaning** | | 2:15 | 3:45 | `speakers/03_data_cleaning.pdf` |
| 4 | **Data analysis 1 — market & pay** | | 2:00 | 6:00 | `speakers/04_data_analysis_1_market_and_pay.pdf` |
| 5 | **Data analysis 2 — competition, skills & scoring** | | 2:00 | 8:00 | `speakers/05_data_analysis_2_competition_and_scoring.pdf` |

**Write your names in the blank column and keep a printed copy on the desk.**

---

## The arc — what the room should feel

| Speaker | The one thing they must land |
|---|---|
| 1 | *A job board can't tell you which job is worth taking. Here's what we built.* |
| 2 | *The architecture was a decision — a million rows filter in 0.06 seconds.* |
| 3 | *We found a trap in this data that would have inverted our conclusions.* |
| 4 | *Where the jobs are is not where the money is.* |
| 5 | *The best-paying track and the easiest-to-enter track are almost never the same one.* |

Read down that column. It is a single argument, and each speaker is one step in it. If your
section doesn't advance it, cut the sentence.

---

## Handovers — rehearse these out loud

| From → To | The line |
|---|---|
| 1 → 2 | *"So that's what we built. Now — how do you make a million rows feel instant?"* |
| 2 → 3 | *"That's the machinery. But none of it matters if the numbers going in are wrong — and this dataset had a trap in it."* |
| 3 → 4 | *"So that's the data we trust. Here's what it actually says."* |
| 4 → 5 | *"Volume and pay are two of the four dimensions. The other two are where it gets interesting."* |
| 5 → close | *"Now you can see both — and decide for yourself which one you need this year."* |

---

## Live demo split

Two speakers touch the dashboard. **Nobody else opens it.**

| Speaker | Screens | Discipline |
|---|---|---|
| **1** | Market Overview → Career Explorer | **Two clicks.** Sets up what the product is. |
| **5** | Career Recommender + weight sliders | **One interaction.** The payoff — the ranking changes live. |

**Setup, done before you walk up:**

- Dashboard already running at `http://localhost:8501` — never start it in front of the room
- Browser zoom ~80% so charts fit the projector
- Speaker 5's inputs pre-set: 3 years' experience, $4,000 minimum
- **Screenshot fallback slides for every demo screen.** If it fails, switch and narrate.
  **Nobody debugs in front of the room.**

---

## Time discipline

**Speaker 3 has the richest material and is the most likely to overrun.** Agree this in advance:

- If the clock passes **5:00** and Speaker 3 hasn't reached the engagement-break story, they
  cut straight to it. That story is the one that must land.
- If the whole presentation passes **8:30** before Speaker 5 starts, Speaker 5 drops Part B
  (hard-to-fill and skill premium) and goes straight to the live demo and the close.

**Whoever is not speaking watches the clock** and gives a visible one-minute signal.

---

## Question ownership

Decide this before you present. When a question comes, **the owner answers** — do not all
start talking.

| Topic | Owner |
|---|---|
| Business case, target user, "why not LinkedIn" | 1 |
| Architecture, Parquet, Streamlit vs BI tools, scaling | 2 |
| Any cleaning rule, the June 2023 break, duplicates, missing values | 3 |
| Salaries, medians vs means, seniority ladder, experience curve | 4 |
| Competition metric, skill keywords, the score and its weights | 5 |

**If a question lands outside everyone's section:** Speaker 1 takes it, since they framed the
project. It is completely fine to say *"we didn't test that — here's what we'd need to do to
answer it."*

### The three most likely questions

1. **"Why is competition only measured up to Jun 2023?"** → Speaker 3. The counters stop
   accumulating; 79% of later postings show zero applications. 203,702 postings is still ample.
2. **"Isn't IT the obvious answer? Why build a tool?"** → Speaker 5. IT is the biggest *and*
   best-paying — and its postings **fell 11.7%** in six months. The obvious answer is the
   cooling one.
3. **"Aren't your score weights arbitrary?"** → Speaker 5. Yes, deliberately — which is why
   they're sliders the user controls rather than constants we chose for them.

---

## Rehearsal checklist

- [ ] **One full run-through against a clock**, all five speakers, under 10:00 including handovers
- [ ] Every speaker has read *their own* script in `reports/speakers/`
- [ ] Handover lines rehearsed — the join is where teams lose time
- [ ] Speakers 1 and 5 have run their demo paths **on the actual presentation machine**
- [ ] Screenshot fallbacks exist for every demo screen
- [ ] Question ownership table agreed and printed
- [ ] Everyone can answer the June 2023 question, not just Speaker 3 — it is the most likely one
- [ ] Notebook open in a second tab in case someone asks to see the cleaning code

---

## Supporting documents

| Document | What it is |
|---|---|
| `reports/speakers/0*.pdf` | the five individual speaker scripts — **rehearse from these** |
| `reports/PROJECT_REPORT.pdf` | the full written report (assignment sections 1–4) |
| `notebooks/01_eda.ipynb` | the EDA behind every claim made on stage |
| `SETUP.md` | how to run the dashboard and rebuild the data |
