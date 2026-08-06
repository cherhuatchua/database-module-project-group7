# Section 3 of 4 — Dashboard / App Walkthrough

**Career Compass SG · Module 1 Assignment · Group 7**

**Your time: 3:00 (official range 3–4 min) · You run the live demo**

---

## Your job in one sentence

**Show the main views, the interactions, and how each one answers the business question.**
The rubric's words exactly. Three screens, three interactions, and the ranking changing
live in front of the room — that is your whole section.

## Where you sit in the flow

| | Section | Time | Official guide |
|---|---|---|---|
| | 1 · Business case & objective | 2:15 | 2–3 mins |
| | 2 · Process & data handling | 3:30 | 3–4 mins |
| **→ YOU** | **3 · Dashboard / app walkthrough** | **3:00** | 3–4 mins |
| | 4 · Challenges & learnings | 1:15 | 1–2 mins |

**Section 2 hands you:** *"…the dashboard we built on top of it."*
**Your handover to Section 4:** *"That's the product. My teammate will close with what this
project taught us."*

---

## Before you start

- Dashboard already running at `http://localhost:8501` — never start it live
- Browser zoom ~80% so charts fit the projector
- Recommender inputs pre-set: **3 years' experience, $4,000 minimum salary**
- Screenshot backup slides for all three screens
- **Discipline: three screens, not seven. Do not free-roam.**

---

## Script

### Screen 1 — Market Overview *(0:00 – 0:40)*

> The dashboard has seven pages — six pages of evidence and one product page. Let me show
> you the three that matter most.
>
> *(Screen 1: Market Overview)*
>
> The front page answers "how big is this market?" One million postings, **median salary
> $3,850 a month**, and **36% of jobs open to people with one year of experience or less**.
>
> Two design choices you'll see everywhere. First, **every chart states its finding in a
> sentence above it** — we tell you the point, then show the proof. Second, honesty marks:
> this grey band flags months where data collection was incomplete, so nobody misreads it
> as a market crash.

### Screen 2 — Demand vs Competition *(0:40 – 1:40)*

> *(Screen 2: the opportunity map)*
>
> This page answers the first half of our business question: **where are the good odds?**
>
> Every bubble is a job category. **Up means more jobs. Right means more applicants per
> seat.** Size is open seats; colour is pay.
>
> **Top-left is the sweet spot — many jobs, almost no queue.** F&B sits there with just
> **1.0 applicants per seat**. Top-right is the trap. And the spread is enormous: from
> **0.7** applicants per seat in Personal Care to **11.3** in Social Services — a
> **sixteen-fold difference** that no job website will ever show you.
>
> Notice the orange note: competition figures come from the reliable data window my
> teammate explained. We'd rather show a caveat than a confident wrong number.

### Screen 3 — Career Recommender *(1:40 – 2:45)*

> *(Screen 3: the Recommender — the product)*
>
> And this page answers the question itself: **which track should *I* target?**
>
> I'm a career switcher: **three years of experience, need at least $4,000 a month.** The
> tool scores all 215 tracks on four things — openings, pay, competition, and how easy each
> is to enter for *my* experience — and ranks them.
>
> Top answer: **IT at mid level** — 69,000 postings, $6,500 median, and 57% of its jobs
> accept my three years. These bars show **exactly why** it ranked first. Nothing is a
> black box.
>
> Now watch. Suppose I don't want the best pay in five years — **I need a job in six
> weeks.** *(drag "Easy for me to enter" up, "High pay" down)*
>
> **The entire top five changes** — HR, Sales, Education at entry level. Not one survivor
> from the old list. Same data, different person, different advice — **the score is a set
> of sliders, not a verdict.**

### Handover *(2:45 – 3:00)*

> Six evidence pages, one product page, every number auditable. That's how the dashboard
> answers the business question.
>
> **That's the product. My teammate will close with what this project taught us.**

---

## Numbers you must know cold

| Figure | Value |
|---|---|
| Front page | 1M postings · **$3,850 median** · 36% entry-friendly |
| Competition spread | **0.7 → 11.3 applicants per seat (16×)** · F&B 1.0 |
| Demo persona | 3 years' experience · $4,000 minimum |
| Top result (default) | **IT – Mid**: ~69k postings · $6,500 · 57% open to 3 yrs |
| After slider change | HR / Sales / Education at Entry — **zero overlap** |
| Tracks scored | 215 · four components · weights 30/30/25/15 |

**Backup if the demo fails — read this table out:**

| Rank | Balanced (default) | "Easiest to enter" |
|---|---|---|
| 1 | Information Technology – Mid | Human Resources – Entry |
| 2 | Information Technology – Senior | Sales / Retail – Junior |
| 3 | Sales / Retail – Junior | Sales / Retail – Entry |

## Questions you own

**"Aren't the score weights arbitrary?"**
> Deliberately — that's why they're sliders the user controls, not constants we buried in
> code. There's no objectively right trade-off between money and speed of hiring. What we
> guarantee is that the four inputs are measured honestly and every contribution is visible.

**"What filters does it have?"**
> A global sidebar on every page: time period, employment type, seniority, salary range,
> open-postings-only. Filters recompute everything live from 1.77 million rows in about
> 0.06 seconds — not from frozen summaries.

**"Why does the map use a log axis?"**
> Category sizes span a few hundred to 140,000 postings. On a normal axis the small half of
> the market would be squashed flat. The axis is labelled as logarithmic.

**"Does the recommender know anything about me?"**
> Only your years of experience and salary floor. It ranks market conditions — it doesn't
> know what you'd enjoy, and the app says so in plain words.

**If the live demo fails:** switch to the screenshots and the backup table. **Never debug
in front of the room.**

---

## Rehearsal checklist

- [ ] Timed at **3:00 or under**, including the slider drag
- [ ] The three-screen path rehearsed on the presentation machine, three times
- [ ] Sliders dragged on that machine — you know exactly where they are
- [ ] "0.7 to 11.3, sixteen-fold" said from memory
- [ ] Backup screenshots on your own slides
