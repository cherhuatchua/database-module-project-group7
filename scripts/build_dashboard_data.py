"""
build_dashboard_data.py — pre-aggregates the cleaned Parquet into the JSON the
dashboard needs, then injects it into scripts/dashboard_template.html to produce
a self-contained dashboard.html.

Run prepare_data.py first, then this script.
"""
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
TEMPLATE = ROOT / "scripts" / "dashboard_template.html"
OUT_HTML = ROOT / "dashboard.html"

EXP_ORDER = ["0 yrs (none)", "1-2 yrs", "3-5 yrs", "6-10 yrs", "10+ yrs"]
BAND_ORDER = ["<3K", "3-5K", "5-8K", "8-12K", "12K+"]
LEVEL_ORDER = ["Fresh/entry level", "Non-executive", "Junior Executive",
               "Executive", "Senior Executive", "Professional", "Manager",
               "Middle Management", "Senior Management"]


def agg_block(dd: pd.DataFrame) -> dict:
    """Compute every aggregate the dashboard needs for one subset of postings."""
    titles = dd.loc[dd["title_clean"].str.len() > 1, "title_clean"] \
               .value_counts().head(15)
    companies = dd["company"].value_counts().head(15)
    exp = dd.groupby("experience_band", observed=True).agg(
        n=("metadata_jobPostId", "count"), sal=("average_salary", "median"))
    exp = exp.reindex([e for e in EXP_ORDER if e in exp.index])
    bands = dd["salary_band"].value_counts()
    levels = dd.groupby("positionLevels", observed=True)["average_salary"].median()
    monthly = dd.groupby("posting_month", observed=True).agg(
        n=("metadata_jobPostId", "count"), sal=("average_salary", "median"))
    return {
        "kpi": {
            "postings": int(len(dd)),
            "vacancies": int(dd["numberOfVacancies"].sum()),
            "medSalary": round(float(dd["average_salary"].median()), 0),
            "companies": int(dd["company"].nunique()),
            "avgApps": round(float(dd["metadata_totalNumberJobApplication"].mean()), 1),
        },
        "topTitles": [[t, int(n)] for t, n in titles.items()],
        "topCompanies": [[t.title(), int(n)] for t, n in companies.items()],
        "expBands": [[i, int(r["n"]), None if pd.isna(r["sal"]) else round(float(r["sal"]))]
                     for i, r in exp.iterrows()],
        "salBands": [[b, int(bands.get(b, 0))] for b in BAND_ORDER],
        "levelSalary": [[l, round(float(levels[l]))]
                        for l in LEVEL_ORDER if l in levels.index and pd.notna(levels[l])],
        "monthly": [[m, int(r["n"]), None if pd.isna(r["sal"]) else round(float(r["sal"]))]
                    for m, r in monthly.iterrows()],
    }


def main() -> None:
    df = pd.read_parquet(DATA / "jobs_clean.parquet")
    cat_long = pd.read_parquet(DATA / "jobs_categories.parquet")

    # 2023-02 has a single posting; keeping it would distort the trend start, so drop it
    df = df[df["posting_month"] != "2023-02"]
    cat_long = cat_long[cat_long["posting_month"] != "2023-02"]

    months = sorted(df["posting_month"].unique().tolist())

    # Category summary: postings / median salary / average applications
    apps = df.set_index("metadata_jobPostId")["metadata_totalNumberJobApplication"]
    cl = cat_long.assign(apps=cat_long["metadata_jobPostId"].map(apps))
    cat_summary = cl.groupby("category").agg(
        n=("metadata_jobPostId", "count"),
        sal=("average_salary", "median"),
        avgApps=("apps", "mean")).sort_values("n", ascending=False)

    result = {
        "months": months,
        "catSummary": [[c, int(r["n"]),
                        None if pd.isna(r["sal"]) else round(float(r["sal"])),
                        round(float(r["avgApps"]), 1)]
                       for c, r in cat_summary.iterrows()],
        "catMonthly": {},   # category -> [count per month]
        "blocks": {"(All)": agg_block(df)},
    }

    cm = cl.groupby(["category", "posting_month"], observed=True).size()
    for c in cat_summary.index:
        s = cm.loc[c].reindex(months).fillna(0).astype(int)
        result["catMonthly"][c] = s.tolist()

    post_ids = cat_long.groupby("category")["metadata_jobPostId"].apply(set)
    for c in cat_summary.index:
        result["blocks"][c] = agg_block(df[df["metadata_jobPostId"].isin(post_ids[c])])

    payload = json.dumps(result, ensure_ascii=False, separators=(",", ":"))
    html = TEMPLATE.read_text(encoding="utf-8").replace("/*__DATA__*/null", payload)
    OUT_HTML.write_text(html, encoding="utf-8")
    print(f"dashboard.html written ({OUT_HTML.stat().st_size/1e6:.2f} MB), "
          f"categories: {len(cat_summary)}")


if __name__ == "__main__":
    main()
