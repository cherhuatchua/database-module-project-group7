"""
Career Compass SG - cleaning and feature engineering.

Two groups of functions:

* ``clean_chunk``      - row-level rules that can be applied one chunk at a time
* ``add_features``     - derived columns a job seeker can act on
* ``explode_*``        - the long tables (job x category, job x skill)

Everything here is deliberately side-effect free so the notebook can import the
same functions the ETL uses and show the before/after on a small sample.
"""

from __future__ import annotations

import json
import re

import numpy as np
import pandas as pd

from config import (
    EXPERIENCE_BAND_EDGES,
    EXPERIENCE_BAND_LABELS,
    HARD_TO_FILL_REPOSTS,
    MAX_VACANCIES,
    MAX_YEARS_EXPERIENCE,
    SALARY_BAND_EDGES,
    SALARY_BAND_LABELS,
    SALARY_CEILING,
    SALARY_FLOOR,
    SENIORITY_MAP,
    SKILL_PATTERNS,
)

DATE_COLUMNS = [
    "metadata_originalPostingDate",
    "metadata_newPostingDate",
    "metadata_expiryDate",
]

RENAME_MAP = {
    "metadata_jobPostId": "job_id",
    "metadata_originalPostingDate": "original_posting_date",
    "metadata_newPostingDate": "new_posting_date",
    "metadata_expiryDate": "expiry_date",
    "metadata_repostCount": "repost_count",
    "metadata_totalNumberJobApplication": "applications",
    "metadata_totalNumberOfView": "views",
    "metadata_isPostedOnBehalf": "posted_on_behalf",
    "minimumYearsExperience": "min_years_experience",
    "numberOfVacancies": "vacancies",
    "positionLevels": "position_level",
    "postedCompany_name": "company",
    "employmentTypes": "employment_type",
    "salary_minimum": "salary_min",
    "salary_maximum": "salary_max",
    "salary_type": "salary_type",
    "status_jobStatus": "job_status",
}


# ---------------------------------------------------------------------------
# 1. Cleaning
# ---------------------------------------------------------------------------
def clean_chunk(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Apply every row-level cleaning rule to one chunk.

    Returns the cleaned chunk plus a dict of counters, so the ETL can build an
    audit trail of exactly how many rows each rule touched.
    """
    stats = {"rows_in": len(df)}

    # -- 1. Structurally empty rows -----------------------------------------
    # ~0.14% of rows have every text field blank (a broken export line).
    # They cannot describe a job, so they go.
    before = len(df)
    df = df.dropna(subset=["metadata_jobPostId", "title"]).copy()
    stats["dropped_empty_rows"] = before - len(df)

    # -- 2. Tidy column names ----------------------------------------------
    df = df.rename(columns=RENAME_MAP)

    # -- 3. Dates -----------------------------------------------------------
    for col in ["original_posting_date", "new_posting_date", "expiry_date"]:
        df[col] = pd.to_datetime(df[col], errors="coerce")
    stats["unparseable_dates"] = int(df["original_posting_date"].isna().sum())

    # A posting that expires before it opens is a data error; blank the expiry
    # rather than the whole row, because the rest of the row is still usable.
    bad_expiry = df["expiry_date"] < df["new_posting_date"]
    stats["expiry_before_posting"] = int(bad_expiry.sum())
    df.loc[bad_expiry, "expiry_date"] = pd.NaT

    # -- 4. Salary governance ----------------------------------------------
    # 4a. Zero is "not disclosed", not "this job pays nothing".
    zero_salary = (df["salary_min"] <= 0) | (df["salary_max"] <= 0)
    stats["salary_zero_to_na"] = int(zero_salary.sum())
    df.loc[zero_salary, ["salary_min", "salary_max"]] = np.nan

    # 4b. min > max means the two fields were swapped on entry - fix, don't drop.
    swapped = df["salary_min"] > df["salary_max"]
    stats["salary_swapped"] = int(swapped.sum())
    df.loc[swapped, ["salary_min", "salary_max"]] = df.loc[
        swapped, ["salary_max", "salary_min"]
    ].values

    # 4c. Impossible monthly values (a $180,000 "monthly" salary is an annual
    #     figure in the wrong box). Blank the salary, keep the row: the posting
    #     still counts as demand even when we cannot trust its pay.
    impossible = (
        (df["salary_min"] < SALARY_FLOOR)
        | (df["salary_max"] > SALARY_CEILING)
    )
    stats["salary_impossible_to_na"] = int((impossible & df["salary_min"].notna()).sum())
    df.loc[impossible, ["salary_min", "salary_max"]] = np.nan

    # 4d. Recompute the average from the cleaned band - the shipped
    #     average_salary column was computed from the dirty values.
    df["avg_salary"] = df[["salary_min", "salary_max"]].mean(axis=1)
    df = df.drop(columns=["average_salary"], errors="ignore")

    # -- 5. Impossible experience / vacancy counts --------------------------
    bad_exp = df["min_years_experience"] > MAX_YEARS_EXPERIENCE
    stats["experience_capped"] = int(bad_exp.sum())
    df.loc[bad_exp, "min_years_experience"] = np.nan

    bad_vac = (df["vacancies"] < 1) | (df["vacancies"] > MAX_VACANCIES)
    stats["vacancies_fixed"] = int(bad_vac.sum())
    df.loc[df["vacancies"] < 1, "vacancies"] = 1          # a posting is at least 1 seat
    df.loc[df["vacancies"] > MAX_VACANCIES, "vacancies"] = np.nan

    # -- 6. Text standardisation -------------------------------------------
    df["company"] = (
        df["company"].astype("string").str.strip().str.upper().str.replace(r"\s+", " ", regex=True)
    )
    df["title"] = df["title"].astype("string").str.strip()
    df["title_clean"] = _standardise_title(df["title"])

    stats["rows_out"] = len(df)
    return df, stats


_TITLE_NOISE = re.compile(
    r"""
    \([^)]*\)            # anything in round brackets: (Java, CIM, Up to $5.5K)
    | \[[^\]]*\]         # anything in square brackets
    | \{[^}]*\}
    | \|.*$              # everything after a pipe: "... | Entry Level | Up to $2,800"
    | \b(up\ to|from)\s*\$?\s*[\d,.]+\s*k?\b   # embedded salary promises
    | \$\s*[\d,.]+\s*k?
    | \b(urgent(ly)?|immediate|hiring|apply\ now|wanted|no\ experience\ needed)\b
    | [\d,.]+\s*k\b
    | [!*@#~]+
    """,
    re.IGNORECASE | re.VERBOSE,
)


def _standardise_title(titles: pd.Series) -> pd.Series:
    """Strip the marketing noise Singapore job titles are famous for.

    'Urgent Hiring!!! Business Development Manager (MES, Pre-sales) - Up to $9K'
    becomes 'Business Development Manager', so that counting titles counts
    *roles* instead of counting adverts.
    """
    cleaned = (
        titles.astype("string")
        .str.replace(_TITLE_NOISE, " ", regex=True)
        .str.replace(r"[-–—/,:]+\s*$", " ", regex=True)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
        .str.title()
    )
    return cleaned.replace("", pd.NA)


# ---------------------------------------------------------------------------
# 2. Feature engineering
# ---------------------------------------------------------------------------
def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """Derived columns that turn raw fields into things a job seeker can act on."""
    df = df.copy()

    # Seniority: 9 official levels are too many to reason about -> 5 bands.
    df["seniority"] = df["position_level"].map(SENIORITY_MAP).astype("category")

    # Bands for grouping and filtering
    df["salary_band"] = pd.cut(
        df["avg_salary"], bins=SALARY_BAND_EDGES, labels=SALARY_BAND_LABELS, right=False
    )
    df["experience_band"] = pd.cut(
        df["min_years_experience"],
        bins=EXPERIENCE_BAND_EDGES,
        labels=EXPERIENCE_BAND_LABELS,
    )

    # Time features
    df["posting_month"] = df["original_posting_date"].dt.to_period("M").dt.to_timestamp()
    df["posting_quarter"] = df["original_posting_date"].dt.to_period("Q").astype("string")
    df["days_live"] = (df["expiry_date"] - df["new_posting_date"]).dt.days

    # --- The three metrics the whole product rests on ---------------------
    # 1. Competition: how many people you are up against for each seat.
    vac = df["vacancies"].fillna(1).clip(lower=1)
    df["applications_per_vacancy"] = (df["applications"] / vac).round(2)

    # 2. Visibility -> action: what share of viewers actually applied.
    df["apply_rate"] = np.where(
        df["views"] > 0, (df["applications"] / df["views"]).round(4), np.nan
    )

    # 3. Hard-to-fill: an employer that reposts twice or more could not fill the
    #    role. For a job seeker that is not a warning - it is an opening.
    df["is_hard_to_fill"] = df["repost_count"] >= HARD_TO_FILL_REPOSTS

    # Convenience flags
    df["is_open"] = df["job_status"].isin(["Open", "Re-open"])
    df["is_entry_friendly"] = df["min_years_experience"].fillna(0) <= 1

    # Memory: repeated strings become categories (1M rows x 8 text columns)
    for col in ["employment_type", "position_level", "job_status", "salary_type"]:
        df[col] = df[col].astype("category")

    return df


# ---------------------------------------------------------------------------
# 3. Long tables
# ---------------------------------------------------------------------------
def parse_categories(raw: str) -> list[str]:
    """`[{"id":21,"category":"Information Technology"}]` -> `['Information Technology']`."""
    if not isinstance(raw, str) or not raw.startswith("["):
        return []
    try:
        return [item["category"] for item in json.loads(raw) if "category" in item]
    except (json.JSONDecodeError, TypeError):
        return []


def explode_categories(df: pd.DataFrame, keep_columns: list[str]) -> pd.DataFrame:
    """One row per (job, category).

    A job can sit in up to 3 categories (1.66 on average), so the wide table
    cannot answer "how many IT jobs are there?" without double counting or
    under counting. The long table can.
    """
    work = df[keep_columns + ["categories"]].copy()
    work["category"] = work["categories"].map(parse_categories)
    work = work.drop(columns=["categories"])
    long = work.explode("category", ignore_index=True)
    long = long[long["category"].notna()]
    long["category"] = long["category"].astype("category")
    return long


def explode_skills(df: pd.DataFrame, keep_columns: list[str]) -> pd.DataFrame:
    """One row per (job, skill), matched from the job title.

    Titles are de-duplicated first: ~1M postings contain far fewer distinct
    titles, so we run the 50 regexes once per distinct title and map back.
    """
    titles = df["title"].astype(object).str.lower()
    unique_titles = pd.Index(pd.unique(titles.dropna()), name="title_lower")

    # One boolean column per skill, evaluated once per DISTINCT title.
    matches = {
        skill: pd.Series(pattern_hits(unique_titles, pattern), index=unique_titles)
        for skill, pattern in SKILL_PATTERNS.items()
    }
    match_frame = pd.DataFrame(matches, index=unique_titles)

    # Wide booleans -> a tidy (title, skill) lookup of only the True cells.
    pairs = match_frame.stack()
    pairs = pairs[pairs].index.to_frame(index=False)
    pairs.columns = ["title_lower", "skill"]

    work = df[keep_columns].copy()
    work["title_lower"] = titles.values
    long = work.merge(pairs, on="title_lower", how="inner").drop(columns=["title_lower"])
    long["skill"] = long["skill"].astype("category")
    return long


def pattern_hits(titles: pd.Index, pattern: str) -> np.ndarray:
    """Vectorised regex test over an Index of titles."""
    return pd.Series(titles, dtype=object).str.contains(pattern, regex=True, na=False).to_numpy()


# ---------------------------------------------------------------------------
# 4. Global (whole-file) rules - applied after every chunk is concatenated
# ---------------------------------------------------------------------------
def deduplicate(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Keep one row per job posting id.

    The file contains the same posting more than once (a re-post writes a new
    row with the same id). We keep the LAST occurrence, which carries the most
    recent view/application counts - the same logic as Lesson 1.8's
    "corrected re-submission" rule.
    """
    before = len(df)
    df = df.sort_values("new_posting_date").drop_duplicates(subset="job_id", keep="last")
    return df.reset_index(drop=True), {"duplicate_job_ids_removed": before - len(df)}


def winsorise_salary(df: pd.DataFrame, lower_q: float, upper_q: float) -> tuple[pd.DataFrame, dict]:
    """Cap, do not delete.

    Even after the impossible-value rules, the top of the salary distribution
    has a thin tail of genuine-but-extreme executive packages that drag every
    mean upwards. Capping at the 1st/99th percentile keeps the row (so demand
    counts stay right) while stopping a handful of rows from steering the
    averages.
    """
    lo = df["avg_salary"].quantile(lower_q)
    hi = df["avg_salary"].quantile(upper_q)
    capped = ((df["avg_salary"] < lo) | (df["avg_salary"] > hi)).sum()
    df = df.copy()
    for col in ["salary_min", "salary_max", "avg_salary"]:
        df[col] = df[col].clip(lower=lo, upper=hi)
    return df, {
        "salary_cap_lower": float(lo),
        "salary_cap_upper": float(hi),
        "salary_rows_capped": int(capped),
    }
