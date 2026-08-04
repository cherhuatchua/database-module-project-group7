# Speaker 1 of 5 — Dashboard Overview

**Career Compass SG · Module 1 Assignment · Group 7**

**Your time: up to 3 minutes · You open the presentation**

---

## Your job in one sentence

**Make the room care about the problem, then give them a tour of what we built.** You set
the stage. Everyone after you explains one part in detail — you explain the whole picture.

## Where you sit in the flow

| | Speaker | Topic |
|---|---|---|
| **→ YOU** | **1** | **Dashboard overview** |
| | 2 | Project technology stack |
| | 3 | Data cleaning |
| | 4 | Data analysis 1 — Demand vs Competition |
| | 5 | Data analysis 2 — Career Recommender |

**Your handover line to Speaker 2:** *"That's what the product looks like. Now my teammate
will show you the technology that makes it run."*

---

## Before you start

- Dashboard already running at `http://localhost:8501` — never start it in front of the room
- Browser on the **Market Overview** page, filters at their defaults
- Browser zoom around 80% so charts fit the projector
- Screenshot backup slides ready, in case the live demo fails

---

## Script

### Part 1 — The problem *(0:00 – 0:45)*

> Have you ever opened a job website and thought: "So many jobs — but which one is
> actually right for me?"
>
> That is the problem. A job website shows you **what jobs exist**. It never tells you
> **which job is worth going after** — and that question decides your next few years.
>
> Our user is a **job seeker or career switcher in Singapore**. Before they pick a career
> track, they need four answers:
>
> - **Demand** — are there enough openings?
> - **Pay** — how much does it pay?
> - **Competition** — how many people want the same seat?
> - **Accessibility** — can I get in with my current experience?
>
> No website shows all four together. So we built one.

### Part 2 — What we built *(0:45 – 1:30)*

*(Slide: the seven pages)*

> This is **Career Compass SG**, built from **1,044,597 real Singapore job postings**,
> October 2022 to May 2024.
>
> We split the market into **215 career tracks** — a job category plus a seniority level,
> like "IT at mid level". Every track gets a score on those four things.
>
> The dashboard has **seven pages**. Think of them as six pages of **evidence** and one page
> that is the **product** — the Career Recommender, which my teammate will demo at the end.
> We designed it this way on purpose: the tool gives you advice, and every other page lets
> you check where that advice came from.

### Part 3 — Quick live tour *(1:30 – 2:30)*

> Let me show you two screens. *(Click 1 — Market Overview)*
>
> The front page: one million postings, **median salary $3,850 a month**, and **36% of
> jobs open to people with one year of experience or less**.
>
> One detail we are proud of: every chart has its **main finding written in a sentence
> above it**. We tell you the point first, then show the proof.
>
> *(Click 2 — Career Explorer)*
>
> And this page lets you dig into any category. Pick IT: you see what it pays at every
> level, the actual job titles being advertised, and who posts them. Notice we say
> **"Poster"**, not "Employer" — because the biggest posters are recruitment agencies, and
> we would rather be honest about that than look impressive.

### Part 4 — Handover *(2:30 – 2:50)*

> One honest admission before I pass on: this was **not our first idea**. We started with a
> simple "top-paying jobs" ranking. The data itself killed that idea — you will hear why
> from my teammates.
>
> **That's what the product looks like. Now — the technology that makes it run.**

---

## Numbers you must know cold

| Figure | Value |
|---|---|
| Postings analysed | **1,044,597** |
| Date range | Oct 2022 – May 2024 |
| Career tracks scored | **215** (43 categories × 5 seniority levels) |
| Median monthly salary | **$3,850** |
| Entry-friendly postings (≤ 1 yr experience) | **36%** |
| Pages in the dashboard | 7 |

## Questions you own

**"Why not just use LinkedIn or MyCareersFuture?"**
> Those sites show you job posts. They never show how many applicants compete for each seat,
> and they never compare career tracks against each other. That comparison is our whole product.

**"Who is this really for?"**
> Job seekers and career switchers first; career coaches second. It runs locally today — the
> analytics are ready, and hosting it as a public website is the natural next step.

**"Can a dashboard really answer 'which career should I pick'?"**
> Not alone — and we say so inside the app. Our score ranks *market conditions*. Whether you
> would enjoy the work is your part of the decision.

**If the live demo fails:** switch to the screenshot slides and narrate the same two
screens. **Never debug in front of the room.**

---

## Rehearsal checklist

- [ ] Timed at **3:00 or under**, including both clicks
- [ ] Demo path rehearsed on the actual presentation machine
- [ ] You can say the four dimensions without looking at the slide
- [ ] Handover line practised out loud
- [ ] Backup screenshots on your own slides
