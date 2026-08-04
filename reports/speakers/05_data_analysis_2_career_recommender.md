# Speaker 5 of 5 — Data Analysis 2: Career Recommender

**Career Compass SG · Module 1 Assignment · Group 7**

**Your time: up to 3 minutes · You close the presentation with the live demo**

---

## Your job in one sentence

**Deliver the payoff.** Your teammates showed the data and the map — you show the product
that turns all of it into personal advice, and you make the ranking change **live, in front
of the room**. The last thing the audience hears is yours.

## Where you sit in the flow

| | Speaker | Topic |
|---|---|---|
| | 1 | Dashboard overview |
| | 2 | Project technology stack |
| | 3 | Data cleaning |
| | 4 | Data analysis 1 — Demand vs Competition |
| **→ YOU** | **5** | **Data analysis 2 — Career Recommender** |

**Speaker 4 hands you:** *"…how do you turn a map into advice for one person? That's the
Career Recommender."*
**You close the whole presentation.** Nobody follows you — end strong.

---

## Before you start

- Dashboard already on the **Career Recommender** page
- Inputs pre-set: **3 years of experience, $4,000 minimum salary**, all seniority levels
- Weight sliders at their defaults (30 / 30 / 25 / 15)
- Screenshot backup of the "before and after" rankings, in case the demo fails

---

## Script

### Part 1 — How the score works *(0:00 – 0:50)*

*(Slide: the four components)*

> The Career Recommender scores every one of our 215 career tracks on **four things**:
>
> - **Openings** — how many jobs exist in this track
> - **Pay** — the median salary
> - **Low competition** — few applicants per seat, from the reliable data window
> - **Easy to enter** — what share of its jobs accept *your* years of experience
>
> Here's the problem: these four come in different units — counts, dollars, ratios,
> percentages. You can't just add them up.
>
> So we convert each one to a **rank from 0 to 100** across all tracks. Now they're on the
> same scale, and we combine them with **weights**. The default is roughly balanced. But —
> and this is the key idea — **the weights are sliders. The user controls them.** Because
> nobody but you knows whether money matters more than getting hired fast.

### Part 2 — Live demo *(0:50 – 2:10)*

> Let me be a real person. **I'm a career switcher: three years of experience, and I need at
> least $4,000 a month.** *(point at the pre-set inputs)*
>
> The tool says my best track is **Information Technology, mid level**. Around 69,000
> postings, median pay $6,500, about four applicants per seat — and **57% of those jobs
> accept my three years of experience**.
>
> And look at these bars: they show **exactly why** it ranked first — how much each of the
> four parts contributed. Nothing is a black box. If you disagree with the advice, you can
> see precisely where it came from.
>
> Now watch what happens when my priorities change. Suppose I don't want the best-paying
> career in five years — **I need a job in six weeks.**
>
> *(drag "Easy for me to enter" to maximum, drop "High pay" to minimum)*
>
> **The entire top five changes.** Now it's Human Resources, Sales, Education — at entry
> level. **Not a single track from the old list survives.** And that's correct! For someone
> who needs work quickly, those genuinely are the better answer.
>
> **The score is a set of sliders, not a verdict.** Same data, different person, different
> advice — and every step of it visible.

### Part 3 — Close *(2:10 – 2:50)*

*(Slide: the closing line)*

> Let me close with the one sentence this whole project comes down to.
>
> **The best-paying career track and the easiest-to-enter career track are almost never the
> same track.** Every job website makes you guess which one you're looking at.
>
> **Career Compass shows you both — and lets you decide which one you need this year.**
>
> Thank you. We're happy to take questions.

---

## Numbers you must know cold

| Figure | Value |
|---|---|
| Tracks scored | **215** (minimum 200 postings each) |
| The four components | openings · pay · low competition · easy to enter |
| Default weights | 30 / 30 / 25 / 15 |
| Demo persona | 3 years' experience, $4,000 minimum |
| Top result (default) | **IT – Mid**: ~69,000 postings, $6,500, ~4 applicants/seat, 57% open to 3 yrs |
| After slider change | HR / Sales / Education at Entry — **zero overlap** with the old top five |

**The before/after table — your backup if the demo fails:**

| Rank | Balanced (default) | "Easiest to enter" |
|---|---|---|
| 1 | Information Technology – Mid | Human Resources – Entry |
| 2 | Information Technology – Senior | Sales / Retail – Junior |
| 3 | Sales / Retail – Junior | Sales / Retail – Entry |
| 4 | Healthcare / Pharma – Mid | Education & Training – Entry |
| 5 | Sales / Retail – Entry | Events / Promotions – Entry |

## Questions you own

**"Aren't the weights arbitrary? You could get any answer you want."**
> Exactly — and that's why they're sliders the user controls, not numbers we buried in the
> code. There is no objectively correct trade-off between money and speed of hiring. What we
> guarantee is that the four inputs are measured honestly, and every contribution is visible.

**"Why ranks instead of raw numbers?"**
> Because you can't add dollars to a ratio. Ranks put everything on one 0-to-100 scale. The
> cost: the score is relative — "better than other tracks here", not "good in absolute terms".

**"Why a minimum of 200 postings per track?"**
> Below that, the medians get too noisy to responsibly recommend anyone into. It's a
> judgement call, and it's written as a named constant in our config file.

**"Does it know anything about me personally?"**
> Only your years of experience and your salary floor. It ranks market conditions — it
> doesn't know what you'd enjoy. We say that inside the app, in plain words.

**If the live demo fails:** switch to the before/after table above and read it out.
**Never debug in front of the room.**

---

## Rehearsal checklist

- [ ] Timed at **3:00 or under**, including the slider drag
- [ ] You have dragged those sliders on the presentation machine at least three times
- [ ] You can name the four components and the default weights from memory
- [ ] The closing two sentences delivered **without notes**
- [ ] Backup before/after table on your own slides
