# Speaker 5 of 5 — Data Analysis 2: Competition, Skills & Scoring

**Career Compass SG · Module 1 Assignment · Group 7**

**Your slot: 8:00 – 10:00 (2 minutes) · You close the presentation — and you do the live demo**

---

## Your job in one sentence

**Deliver the payoff.** Speaker 4 showed that volume and pay disagree; you show the two
dimensions nobody else measures, then put all four together on screen and make the ranking
change in front of the room. **The last thing the room hears is yours** — end on the message,
not on a chart.

## Where you sit in the flow

| | Speaker | Topic |
|---|---|---|
| | 1 | Dashboard overview |
| | 2 | Technology stack |
| | 3 | Data cleaning |
| | 4 | Data analysis 1 — market & pay |
| **→ YOU** | **5** | **Data analysis 2 — competition, skills & scoring** |

**Speaker 4 hands you:** *"…the other two dimensions are where it gets interesting."*
**You close the presentation.** Nobody follows you.

---

## Before you start

- The dashboard is already on the **Career Recommender** page — set up during Speaker 4's slot
  if you can do it without noise, otherwise click through during your first sentence
- Inputs pre-set: **3 years of experience, $4,000 minimum salary**, all seniority levels
- Weight sliders at their defaults (30 / 30 / 25 / 15)

---

## Script

### Part A — Competition, the dimension nobody measures *(8:00 – 8:35)*

*(Slide: the opportunity map — the four-quadrant bubble chart)*

> Every dot is a category. **Across is competition — applicants per seat. Up is volume.**
> Size is seats, colour is pay.
>
> **Competition varies 16-fold:** Personal Care **0.7 applicants per seat**, F&B **1.0**,
> Social Services **11.3**.
>
> **Top left is where you want to be — volume without the queue.** Top right is the trap. And
> this caveat is permanent: **these come from postings up to June 2023 only.**

### Part B — Two findings that invert an assumption *(8:35 – 9:05)*

*(Slide: hard-to-fill pay gap + the skill premium bar chart)*

> Two findings that reverse expectations.
>
> **Hard-to-fill means underpaid, not elite:** reposted jobs pay **$3,700 against $3,850**.
> They're not elite roles — they're underpaid. That's your leverage.
>
> **And the skill premium is 4.6×** — an **AI title pays $8,750, 127% above market**; cleaning
> pays $1,900, 51% below.
>
> And keeping us honest: **IT postings fell 11.7% in six months** — the safest-looking track is
> cooling.

### Part C — Live demo: putting the four together *(9:05 – 9:45)*

> Four dimensions, four different units. We convert each to a **0-to-100 percentile rank**
> across 215 tracks, then weight them. That's the **Career Fit Score**.
>
> I'm a **switcher with three years' experience who needs $4,000 a month.**
>
> *(the page is already set — point at the result)*
>
> Top result: **IT at Mid level** — 69,000 postings, **$6,500** median, four applicants per
> seat, **57% open to my three years.** These bars show why.
>
> But watch. *(drag "Easy for me to enter" to maximum, drop "High pay")*
>
> **The entire top five changes** — HR, Sales and Education at entry level. **Not one was in
> the previous list.** For someone who needs a job in six weeks, that's better advice.
>
> **The score is a set of sliders, not a verdict.**

### Part D — Close *(9:45 – 10:00)*

*(Slide: the closing line)*

> **The best-paying track and the easiest-to-enter track are almost never the same track.**
> Every job board makes you guess which one you're looking at.
>
> **Now you can see both — and decide which one you need this year.**
>
> Thank you.

---

## Numbers you must know cold

| Figure | Value |
|---|---|
| Competition spread | **0.7 to 11.3 applicants per seat — a factor of 16** |
| Market-wide competition | 3.77 applicants per seat |
| Hard-to-fill share / pay gap | **4.1% of postings; $3,700 vs $3,850** |
| Top skill premium | **AI / Machine Learning, $8,750, +127%** |
| Bottom skill premium | Cleaning / Housekeeping, $1,900, **−51%** |
| Premium ratio | **4.6×** |
| IT six-month growth | **−11.7%** |
| Fastest-growing categories | General Work +7%, Sciences / Lab +6%, Wholesale +5% |
| Steepest decline | Purchasing / Merchandising −23% |
| Tracks scored | **215**, minimum 200 postings each |
| Default weights | demand 30 · pay 30 · low competition 25 · accessibility 15 |

## The Career Fit Score, if you're asked to explain it

| Component | Measure |
|---|---|
| **Openings** | percentile of log₁₀(postings) — log, because 40,000 postings isn't twice as good a bet as 20,000 |
| **Pay** | percentile of median advertised salary |
| **Low competition** | percentile of the *inverse* of applications ÷ vacancies, reliable window only |
| **Accessibility** | share of the track's postings open to your years of experience, re-ranked across surviving tracks |

**Weight sensitivity — the proof it isn't cosmetic**

| Rank | Balanced (default) | Money first | Easiest to enter |
|---|---|---|---|
| 1 | Information Technology – Mid | Information Technology – Senior | Human Resources – Entry |
| 2 | Information Technology – Senior | Information Technology – Mid | Sales / Retail – Junior |
| 3 | Sales / Retail – Junior | Information Technology – Management | Sales / Retail – Entry |

*Easiest to enter* shares **no entries at all** with the default ranking.

## Questions you own

**"Aren't the weights arbitrary? You could get any answer you want."**
> That's the point, and it's why they're exposed rather than buried. There is no objectively
> correct weighting of money against speed-to-hire — that depends on the person. What we
> guarantee is that the four *inputs* are measured consistently and that you can see exactly
> how each one contributed.

**"Why percentile ranks instead of the raw numbers?"**
> Because you can't add dollars to a ratio. Percentile ranks put all four on one 0-to-100
> scale. The cost is that the score is relative — it tells you a track is better than others
> here, not that it's good in absolute terms.

**"Your skill list is just keywords from job titles."**
> Correct, and it's labelled that way in the app. The dataset has no skills field, so we match
> titles against a 50-term dictionary spanning tech, business, trades, healthcare and services.
> It measures *what employers advertise for*, which is what a job seeker has to match — but it
> is not a skills census. A Python developer whose advert says "Software Engineer" isn't
> counted under Python.

**"Isn't recommending F&B because it's uncontested bad advice?"**
> The tool never recommends on one dimension. F&B scores well on competition and volume and
> poorly on pay, and the user sees all four bars. If they weight pay highly, F&B drops out.

**"Why a minimum of 200 postings per track?"**
> Below that the medians are too noisy to recommend anyone into. It's a judgement call, and
> it's in `config.py` as a named constant rather than buried in the code.

**If the live demo fails:** switch to the screenshot slides and narrate the same before/after
ranking. **Do not debug.** The weight-sensitivity table above is your fallback — read it out.

---

## Rehearsal checklist

- [ ] Timed at **2:00 or under**, including the slider drag
- [ ] You have dragged those sliders **on the presentation machine** at least three times
- [ ] You can name the four score components and why each is measured that way
- [ ] You can deliver the closing two sentences **without notes** — this is the last thing the
      room hears
- [ ] Screenshot fallback for the before/after ranking is on your slides
- [ ] You know who takes which question if the panel asks something outside your section
