# Speaker 1 of 5 — Dashboard Overview

**Career Compass SG · Module 1 Assignment · Group 7**

**Your slot: 0:00 – 2:15 (2 minutes 15 seconds) · You open the presentation**

---

## Your job in one sentence

**Make the room care about the problem, then show them the thing we built.** You are the only
speaker who gets to set the frame — everyone after you is explaining *how*. You explain *what*
and *why*.

## Where you sit in the flow

| | Speaker | Topic |
|---|---|---|
| **→ YOU** | **1** | **Dashboard Overview** |
| | 2 | Technology stack |
| | 3 | Data cleaning |
| | 4 | Data analysis 1 — market & pay |
| | 5 | Data analysis 2 — competition, skills & scoring |

**You hand over to Speaker 2** with: *"…so that's what we built. Now — how do you make a
million rows feel instant?"*

---

## Before you start

- Dashboard already running at `http://localhost:8501` — **do not start it in front of the room**
- Browser on the **Market Overview** page, sidebar filters at defaults (May 2023 – May 2024)
- Browser zoom ~80% so the full chart fits on the projector
- Screenshot fallback slides ready for both demo screens

---

## Script

### Part A — The problem *(0:00 – 0:45)*

*(Slide: title + the four dimensions)*

> Everyone here has looked at a job board and asked a question it cannot answer.
>
> A job board tells you **what jobs exist**. It never tells you **which one is worth going
> after** — and that question decides your next five years.
>
> **Our user is a Singapore job seeker or career switcher**, deciding which track to aim at.
> That decision turns on four things no job board shows side by side:
>
> - **Demand** — are there enough openings?
> - **Pay** — what does it pay, at my level?
> - **Competition** — how many people am I up against per seat?
> - **Accessibility** — can I get in with what I have *today*?

### Part B — What we built *(0:45 – 1:15)*

*(Slide: the seven pages)*

> So we built **Career Compass SG**. It scores **215 career tracks** — 43 categories across
> five seniority levels — on those four dimensions, from **1,044,597 Singapore job postings**.
>
> Seven pages: six are **evidence**, and the seventh, the Recommender, is the **product**. We
> didn't want a tool that tells you what to do without letting you check its reasoning.
>
> **Our test is three minutes** — open it and you can name the three tracks you should target.

### Part C — Live demo, two screens only *(1:15 – 2:00)*

> **Discipline: two clicks, not twelve. Do not free-roam.**

**Click 1 — Market Overview** *(~25 s)*

> One million postings. **$3,850 median monthly salary.** **36% open to someone with a year of
> experience or less.**
>
> Two habits you'll see everywhere: **we quote medians, not means** — the distribution is
> skewed, and both lines are on this histogram. And this **grey band** marks months where our
> collection was still filling up.

**Click 2 — Career Explorer** *(~20 s)*

> Every number is auditable. Pick IT: the pay ladder by seniority, the real job titles, and who
> posts them — labelled **"Poster"**, not "Employer", because the top five are recruitment
> agencies.

### Part D — The honest admission *(2:00 – 2:15)*

> One admission: **this wasn't our first idea.** We started with a top-paying-jobs dashboard.
> The data killed it — pay, volume and competition are almost independent. My colleagues will
> show you the numbers.
>
> **So that's what we built. Now — how do you make a million rows feel instant?**

---

## Numbers you must know cold

| Figure | Value |
|---|---|
| Postings analysed | **1,044,597** (from 1,048,585 raw) |
| Date range | Oct 2022 – May 2024 |
| Career tracks scored | **215** (43 categories × 5 seniority bands) |
| Median monthly salary | **$3,850** |
| Entry-friendly postings (≤ 1 yr experience) | **36%** |
| Total vacancies (seats) | 2,725,717 |
| Distinct posting organisations | 53,150 |

## Questions you own

**"Why not just use LinkedIn or MyCareersFuture directly?"**
> They show you *postings*. They never show you the applicant-to-seat ratio, and they never let
> you compare a track you're in against one you're not. That comparison is the entire product.

**"Who exactly is this for — is it a real product?"**
> Primarily job seekers and career switchers; secondarily the coaches advising them. It is a
> working local dashboard, not a deployed service. The analytics scale already — the missing
> pieces are user accounts, a scheduled refresh and hosting.

**"Isn't 'which career should I pick' too big a question for a dashboard?"**
> It is, and we say so in the app. The score ranks *market conditions* — it knows nothing about
> whether you'd enjoy the work. Market conditions are one input to a career decision, not the
> decision.

**If the live demo fails:** switch to the screenshot slides and narrate the same two screens.
**Do not debug in front of the room.** Say "I'll show you the live version afterwards" and move on.

---

## Rehearsal checklist

- [ ] Timed at **2:15 or under**, including the two clicks
- [ ] The two-click path rehearsed on the actual machine you'll present from
- [ ] You can state the four dimensions without looking at the slide
- [ ] Handover line to Speaker 2 practised out loud
- [ ] Fallback screenshots on your own slides, not someone else's laptop
