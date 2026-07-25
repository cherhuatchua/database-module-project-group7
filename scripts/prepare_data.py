"""
prepare_data.py — data cleaning & feature engineering
Reads the raw SGJobData.csv (~1.05M rows, MyCareersFuture Singapore job postings),
cleans it in chunks and writes two Parquet files:
  data/jobs_clean.parquet      one row per job posting (with primary category)
  data/jobs_categories.parquet job-category long table (a posting can have several categories)

Cleaning decisions (see docs/REPORT.md):
  1. Keep salary_type == 'Monthly' only (99.6%; mixed salary bases are not comparable)
  2. Monthly salaries outside [800, 60000] are treated as dirty (annual-salary typos /
     placeholder values like 1) and set to NaN while the row is kept
  3. categories is a JSON array; parse all of them, first item = primary category
  4. Features: posting_month, salary_band, experience_band, apps_per_vacancy
"""
import json
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "SGJobData.csv"
OUT_DIR = ROOT / "data"
OUT_DIR.mkdir(exist_ok=True)

USECOLS = [
    "categories", "employmentTypes", "metadata_jobPostId",
    "metadata_newPostingDate", "metadata_originalPostingDate",
    "metadata_repostCount", "metadata_totalNumberJobApplication",
    "metadata_totalNumberOfView", "minimumYearsExperience",
    "numberOfVacancies", "positionLevels", "postedCompany_name",
    "salary_maximum", "salary_minimum", "salary_type",
    "status_jobStatus", "title", "average_salary",
]

SALARY_LO, SALARY_HI = 800, 60_000

_cat_cache: dict[str, tuple[str, ...]] = {}


def parse_categories(raw: str) -> tuple[str, ...]:
    if raw in _cat_cache:
        return _cat_cache[raw]
    try:
        cats = tuple(d["category"] for d in json.loads(raw))
    except (TypeError, ValueError, KeyError):
        cats = ()
    _cat_cache[raw] = cats
    return cats


def experience_band(years: float) -> str:
    if years <= 0:
        return "0 yrs (none)"
    if years <= 2:
        return "1-2 yrs"
    if years <= 5:
        return "3-5 yrs"
    if years <= 10:
        return "6-10 yrs"
    return "10+ yrs"


def salary_band(s: float) -> str:
    if pd.isna(s):
        return "Unknown"
    if s < 3000:
        return "<3K"
    if s < 5000:
        return "3-5K"
    if s < 8000:
        return "5-8K"
    if s < 12000:
        return "8-12K"
    return "12K+"


def clean_chunk(ch: pd.DataFrame) -> pd.DataFrame:
    ch = ch[ch["salary_type"] == "Monthly"].copy()

    bad = (ch["average_salary"] < SALARY_LO) | (ch["average_salary"] > SALARY_HI)
    ch.loc[bad, ["average_salary", "salary_minimum", "salary_maximum"]] = pd.NA

    ch["posting_date"] = pd.to_datetime(ch["metadata_newPostingDate"], errors="coerce")
    ch = ch.dropna(subset=["posting_date"])
    ch["posting_month"] = ch["posting_date"].dt.to_period("M").astype(str)

    ch["categories_list"] = ch["categories"].map(parse_categories)
    ch["primary_category"] = ch["categories_list"].map(lambda t: t[0] if t else "Uncategorized")

    ch["experience_band"] = ch["minimumYearsExperience"].map(experience_band)
    ch["salary_band"] = ch["average_salary"].map(salary_band)
    ch["apps_per_vacancy"] = (
        ch["metadata_totalNumberJobApplication"] / ch["numberOfVacancies"].clip(lower=1)
    ).round(2)
    ch["company"] = ch["postedCompany_name"].str.strip().str.upper()
    # Strip salary/urgency noise from titles so similar roles aggregate together
    ch["title_clean"] = (
        ch["title"].str.replace(r"[\(\[\|#!].*", "", regex=True).str.strip().str.title()
    )

    return ch.drop(columns=["categories", "salary_type", "metadata_newPostingDate",
                            "metadata_originalPostingDate", "postedCompany_name"])


def main() -> None:
    chunks = []
    for i, ch in enumerate(pd.read_csv(SRC, usecols=USECOLS, chunksize=250_000)):
        chunks.append(clean_chunk(ch))
        print(f"chunk {i + 1} done, rows kept: {len(chunks[-1]):,}")

    df = pd.concat(chunks, ignore_index=True)
    df = df.drop_duplicates(subset="metadata_jobPostId")
    print(f"total rows after cleaning: {len(df):,}")

    cat_long = (
        df[["metadata_jobPostId", "categories_list", "posting_month",
            "average_salary", "positionLevels", "numberOfVacancies"]]
        .explode("categories_list")
        .rename(columns={"categories_list": "category"})
        .dropna(subset=["category"])
    )

    df = df.drop(columns=["categories_list"])
    for col in ["employmentTypes", "positionLevels", "status_jobStatus",
                "primary_category", "experience_band", "salary_band", "posting_month"]:
        df[col] = df[col].astype("category")

    df.to_parquet(OUT_DIR / "jobs_clean.parquet", index=False)
    cat_long.to_parquet(OUT_DIR / "jobs_categories.parquet", index=False)
    print("saved:", OUT_DIR / "jobs_clean.parquet", "|", OUT_DIR / "jobs_categories.parquet")


if __name__ == "__main__":
    main()
