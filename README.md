# Module 1 Assignment Project – Singapore Jobs Analytics

Design a simple data product (dashboard or web app) using a real-world CSV of Singapore job postings (~1M+ rows). Your goal is to solve a clear business problem for a specific user group using insights from the data.

> **This looks big. It isn't** — it's every small skill from Module 1, chained together: loading data, cleaning it, exploring it, and showing what you found. Follow the milestones below and you'll be fine.

---

## 🚀 Getting Started (do this first)

**Step 0 — Load a sample, not the whole file.** The full file has ~1M rows; taste a spoonful before cooking the whole pot. Build everything on the fast subset, and scale up once it works:

```python
import pandas as pd
df = pd.read_csv('sg_jobs.csv', nrows=50000)   # first 50,000 rows only
```

**Then take your first three EDA steps** (adjust column names to what's actually in the file):

```python
df.shape                    # 1. How big is your sample? (rows, columns)
df.info()                   # 2. What columns do you have, and what types are they?
df['salary'].describe()     # 3. Pick one numeric column — what's typical, what's extreme?
```

That's it — you've started. Everything else in this brief builds on these first looks.

**Where to get the dataset:** [Dataset link — provided by your instructor]

---

## 🗓️ Suggested Milestones

A gentle ramp so you're never cramming at the end:

| Week | You should have... |
|------|--------------------|
| **Week 1** | Business case chosen + data loaded (sample first!) + first EDA done |
| **Week 2** | Cleaning + feature engineering + your key charts drafted |
| **Week 3** | Dashboard assembled + story polished + presentation rehearsed |

---

## 1. Business Case (2–3 bullets)

Briefly describe:

- Business scenario (e.g. talent acquisition, policy analyst, career coach).
- **Objective**: What decision/problem are you helping to address?
- Target users and value: How will this dashboard/app help them?

> Example: “Help a talent acquisition team identify which roles and skills are most in demand so they can prioritise hiring and sourcing.”

---

## 2. Data Handling & Process (5–8 bullets)

Summarise your end-to-end process:

- Tools used (e.g. Python + Pandas / DuckDB / SQL).
- How you loaded the CSV (~1M+ rows).
- Key cleaning steps (missing values, standardising categories, parsing dates, handling salary formats).
- Important feature engineering (e.g. seniority, salary bands, demand metrics, skill tags).
- EDA highlights: key patterns or anomalies you discovered that shaped your dashboard design.

You do not need to show all code, but the logic and key decisions should be clear.

---

## 3. Dashboard / App (6–10 bullets)

Describe and demonstrate your solution:

- Type of solution: dashboard (e.g. Streamlit, Power BI, Tableau) or simple web app.
- Main views:
  - Overview metrics (e.g. total postings, top roles/industries, salary ranges).
  - Drill-down view (by role, industry, location, skills, etc.).
  - Time trend view (e.g. postings over time, salary trends).
- Interactivity: filters, sorting, drill-downs, tooltips where relevant.
- Design choices: layout, chart types, colour scheme, readability.
- How each view directly supports your business objective and target users.

Include 2–4 key screenshots in your written submission (or show live in the presentation).

---

## 4. Presentation (10 mins per team)

Suggested flow:

1. **Business case & objective** (2–3 mins)  
   - Scenario, users, objective, success criteria.
2. **Process & data handling** (3–4 mins)  
   - How you cleaned, transformed, and explored the data.
3. **Dashboard / app walkthrough** (3–4 mins)  
   - Main views, interactions, and how they answer the business question.
4. **Challenges & learnings** (1–2 mins)  
   - Technical/analytical challenges, what you learned, and possible next steps.

---

## 5. Deliverables

- Brief written report (Markdown/PDF) following Sections 1–4 above.
- Working dashboard / app (deployed link or clear run instructions).
- Code repo with:
  - Data handling notebook(s) / scripts,
  - Dashboard/app code,
  - README with setup steps.

Focus on a **coherent story** from business question → data process → dashboard → insights, rather than advanced techniques.

---

## 📊 How You'll Be Assessed

| Criterion | Weight | What excellent looks like |
|-----------|--------|---------------------------|
| Business case clarity | 20% | A specific user, a specific decision, and a clear reason your dashboard helps them make it. |
| Data handling & cleaning | 25% | Cleaning choices are explained and justified — we can see *why* you handled missing values or salary formats the way you did. |
| Dashboard functionality | 25% | Views load, filters work, and each element answers part of the business question. |
| Insight & story | 20% | Findings are framed as answers ("Roles X and Y are surging in the East"), not just charts. |
| Presentation | 10% | Clear, within time, everyone contributes, and the demo lands. |

**To pass:** a working dashboard with at least one overview view and one drill-down, tied to a stated business question.

**Working in teams:** [Team size: X — confirm with your instructor]. The presentation is assessed as a team; your commit history is assessed individually — so push your own work under your own GitHub account.

---

# Our Implementation & How to Run

> Full report (business case / cleaning decisions / dashboard design / presentation outline) in **[docs/REPORT.md](docs/REPORT.md)**.

## Project structure

```
├── SGJobData.csv                     # raw data (~1.05M rows, 286 MB, not committed)
├── scripts/
│   ├── prepare_data.py               # chunked cleaning + feature engineering → data/*.parquet
│   ├── build_dashboard_data.py       # pre-aggregation + template injection → dashboard.html
│   └── dashboard_template.html       # dashboard front-end template (native SVG, zero deps)
├── data/                             # generated Parquet intermediates
├── dashboard.html                    # ✅ final dashboard (double-click to open)
├── docs/REPORT.md                    # written report (answers to Sections 1–4)
└── requirements.txt
```

## Run steps

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python scripts/prepare_data.py          # ~2 min: cleans 1.05M rows → Parquet
python scripts/build_dashboard_data.py  # ~1 min: aggregates → generates dashboard.html
open dashboard.html                     # no server needed — opens straight in the browser
```

The dashboard is a **single self-contained HTML file** (pre-aggregated data embedded, ~0.1 MB) — send it to reviewers as-is or deploy to any static host.

## Key findings (TL;DR)

1. **IT and Engineering lead on both demand and pay**: ~277K postings combined (~26% of the market), and IT's S$6,500 median monthly salary is the highest of any category.
2. **Salaries are heavily right-skewed**: market median S$3,850 (mean 4,716); 44% of postings fall in the 3–5K band.
3. **A steep seniority ladder**: entry level S$2,600 → senior management S$9,500 (3.7×).
4. **Agencies dominate posting volume**: the top 8 posters are all recruitment agencies — the top 2 alone exceed 110K postings — so company-level analysis must separate agencies from direct employers.
5. **Low candidate competition**: just 2.1 applications per posting on average — most categories require proactive sourcing.

# database-module1-project-group7
