# Project Report — Singapore Job Market Dashboard

> Module 1 assignment submission, following Sections 1–4 of the assignment README.
> Data: MyCareersFuture Singapore job postings, 1,048,864 rows × 22 columns (Mar 2023 – May 2024).

---

## 1. Business Case

- **Business scenario**: Talent acquisition (TA) teams and recruitment agencies that need a factual view of supply, demand and salary levels across the Singapore job market.
- **Objective (the decisions we help with)**:
  1. **Prioritisation** — which job categories and roles have the highest (and fastest-growing) demand, so hiring resources go where they matter most?
  2. **Salary benchmarking** — what monthly salary is competitive for a given category, position level and experience band?
  3. **Sourcing strategy** — which categories attract many applicants (easy to fill) versus almost none (require proactive sourcing)?
- **Target users & value**: A hiring lead opens the dashboard and can answer "what to hire, what to pay, and how hard it will be" — turning judgement calls that used to rely on anecdotes into decisions backed by 1.04M real job postings.

## 2. Data Handling & Process

- **Toolchain**: Python 3 + Pandas (chunked loading & cleaning) → Parquet (intermediate storage) → pre-aggregated JSON → self-contained HTML with native SVG charts (zero external dependencies; opens with a double-click).
- **Loading (~1.05M rows, 286 MB CSV)**:
  - First-pass EDA on a sample via `nrows=50000` (`df.shape` → (50000, 22); `df.info()`; `df['average_salary'].describe()`);
  - Full processing with `chunksize=250_000` streaming reads + `usecols` limited to the 18 columns we need, keeping peak memory modest;
  - Cleaned output stored as Parquet (columnar + categorical dtypes) — an order of magnitude faster to re-read than CSV.
- **Key cleaning decisions (and why)**:
  | Decision | Rationale |
  |---|---|
  | Keep `salary_type == 'Monthly'` only (99.6%; drop 3,988 rows with missing basis) | Mixed salary bases (hourly/annual/monthly) are not comparable |
  | Salaries outside **[800, 60000]** set to NaN but the **row is kept** (13,768 rows, 1.3%) | Placeholder values (e.g. 1) and likely annual-salary typos (200K+) exist; ~800 is a reasonable local monthly floor; the posting itself is real — only the salary field is dirty |
  | Drop the `occupationId` column entirely | 100% missing across the full file — zero information |
  | Drop Feb 2023 (a single posting) | One sample would create a misleading start to every trend chart |
  | De-duplicate on `metadata_jobPostId` | Guards against double-counted reposts (none found in practice — kept as insurance) |
  | Company names stripped + upper-cased | Case/whitespace variants of the same company would otherwise split its counts |
- **Feature engineering**:
  - `categories` (JSON array; one posting can have several) → parsed and **exploded into a posting–category long table**, with the first item kept as primary category;
  - `posting_month`, `salary_band` (<3K / 3-5K / 5-8K / 8-12K / 12K+), `experience_band` (0 / 1-2 / 3-5 / 6-10 / 10+ yrs);
  - `apps_per_vacancy` (applications ÷ vacancies) and average applications per posting — proxy metrics for **candidate competition / hiring difficulty**;
  - `title_clean` — strips "Up to $5.5K / Urgent / (location)"-style noise from titles so similar roles aggregate together.
- **EDA highlights (which shaped the dashboard design)**:
  1. IT (141K) and Engineering (136K) are the two largest categories → the overview leads with a "Top 12 by demand" chart;
  2. Salaries are heavily right-skewed (mean 4,716 > median 3,850) → the whole dashboard reports **medians**, never means;
  3. IT's median salary of S$6,500 is the market's highest; General Work sits at S$2,700 — a 2.4× gap → a category-salary comparison chart is essential;
  4. The biggest "companies" by postings are all recruitment agencies (The Supreme HR Advisory alone: 62K) → the chart carries an explicit caveat;
  5. Applications are extremely zero-inflated (median 0, mean 2.1) → the competition metric uses the mean, with the limitation documented;
  6. Mar/Apr 2023 and May 2024 are partial months → the trends view labels this to prevent a false "market cooling" read.

## 3. Dashboard / App

- **Format**: a single file, [dashboard.html](../dashboard.html) — data pre-aggregated in Python and embedded in the HTML, charts drawn in native SVG, no external dependencies (no CDN, no server). Double-click to open, or host on any static site.
- **Three main views**:
  1. **Market Overview**: 5 KPIs (1.04M postings, 2.81M vacancies, S$3,850 median salary, 53K companies, 2.1 avg applications) + Top 12 categories by demand, Top 12 by salary, salary-band distribution, and the position-level salary ladder;
  2. **Role Drill-down**: Top 15 job titles, Top 15 posting companies, experience-requirement distribution (hover shows the matching median salary), and the most competitive categories;
  3. **Time Trends**: postings per month, median salary per month, and a comparison of **up to 4 categories** over time (toggled via chips).
- **Interactivity**:
  - A **category drill-down filter** at the top — any of 43 categories; every KPI and chart updates together;
  - **Hover tooltips** on every bar and data point (with secondary detail, e.g. median salary per experience band);
  - Trend-comparison chips, tab switching, responsive re-render on resize, automatic dark mode.
- **Design choices**:
  - A single blue encodes "magnitude" (no rainbow bars); the category-comparison lines use a fixed-order 4-colour set (blue/orange/aqua/yellow from a colourblind-validated palette);
  - Horizontal bars with rounded ends and direct value labels, so long category names stay readable;
  - Medians used consistently; data pitfalls (partial months, agency-dominated posting counts) are **annotated directly beneath the charts**.
- **How each view serves the objective**: the overview answers *what to hire* (demand ranking); the level/experience/category salary charts answer *what to pay*; the competition chart and the applications KPI answer *how hard it will be*; the trends view supports timing decisions (when to post, whether demand is heating up).

### Suggested screenshots for the written submission
1. Overview page (KPIs + demand/salary Top 12);
2. Drill-down page with Information Technology selected (top titles & companies);
3. Trends page with the 4-category comparison lines.

## 4. Presentation (10-minute outline)

1. **Business case & objective (2 min)**: the TA team's three decisions (what to hire / what to pay / how hard to fill); success = replacing gut feel with data.
2. **Process & data handling (3 min)**: chunked loading of 1.05M rows → salary-basis standardisation and the outlier policy (explain the [800, 60000] reasoning) → exploding the category JSON → the competition feature.
3. **Dashboard walkthrough (3–4 min)**: live demo of the three views + category drill-down, closing on two insights —
   - "IT and Engineering account for ~26% of all postings, and IT's S$6,500 median salary is also the market's highest — high demand stacked on high pay makes it the battleground for hiring resources";
   - "The median salary ladder runs S$2,600 (entry) to S$9,500 (senior management) — 3.7×, and the per-level premium steepens sharply past Senior Executive (S$5,000)".
4. **Challenges & learnings (1–2 min)**: see below.

### Challenges & Learnings
- **Scale**: a 286 MB CSV rules out trial-and-error on the full file — we adopted the standard "sample first, process in chunks, prune columns, cache as Parquet" workflow;
- **The cost of judging dirty data**: there is no textbook answer for salary outliers; we combined quantiles (p01 = 0, p99 = 18,000) with domain sense (the local monthly-wage floor) and wrote the decision down;
- **Multi-category postings**: categories arrive as a JSON array — a naive value_counts undercounts; after exploding to a long table, "posting–category" counts and "posting" counts are different denominators, and chart titles must say which one they use;
- **Possible next steps**: extract skill tags from job titles, build salary-band role recommendations, connect a live data source for automatic monthly refreshes.

## 5. Deliverables Checklist

| Deliverable | Location |
|---|---|
| Written report | this file, `docs/REPORT.md` |
| Working dashboard | `dashboard.html` (double-click to open; no server needed) |
| Data-handling scripts | `scripts/prepare_data.py` (cleaning + features), `scripts/build_dashboard_data.py` (aggregation + HTML build) |
| Setup steps | "Our Implementation" section at the end of the project `README.md` |
