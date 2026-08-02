"""
Career Compass SG - stage 1 ETL.

Reads the full 1,048,864-row SGJobData.csv in chunks, applies every cleaning
and feature rule, and writes three parquet files plus a JSON audit trail:

    data/processed/jobs_clean.parquet        one row per job posting
    data/processed/jobs_by_category.parquet  one row per (job, category)
    data/processed/jobs_by_skill.parquet     one row per (job, skill)
    data/processed/data_quality_report.json  what the cleaning actually did

Run:  python src/etl_clean.py
"""

from __future__ import annotations

import json
import sys
import time
from collections import defaultdict

import numpy as np
import pandas as pd

from config import (
    CHUNK_SIZE,
    DROP_COLUMNS,
    JOBS_CATEGORY_PARQUET,
    JOBS_PARQUET,
    PROCESSED_DIR,
    QUALITY_REPORT,
    RAW_CSV,
    SKILLS_PARQUET,
    USE_COLUMNS,
    WINSOR_LOWER_Q,
    WINSOR_UPPER_Q,
)
from features import (
    add_features,
    clean_chunk,
    deduplicate,
    explode_categories,
    explode_skills,
    winsorise_salary,
)

# Columns carried into the long tables. Anything the dashboard groups or
# filters by has to be here; anything else is left in the wide table.
LONG_TABLE_COLUMNS = [
    "job_key",
    "job_id",
    "title_clean",
    "company",
    "employment_type",
    "seniority",
    "position_level",
    "job_status",
    "is_open",
    "salary_min",
    "salary_max",
    "avg_salary",
    "salary_band",
    "min_years_experience",
    "experience_band",
    "is_entry_friendly",
    "vacancies",
    "applications",
    "views",
    "applications_per_vacancy",
    "apply_rate",
    "repost_count",
    "is_hard_to_fill",
    "days_live",
    "posting_month",
    "original_posting_date",
]


def log(message: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


def run(nrows: int | None = None) -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    started = time.time()

    if not RAW_CSV.exists():
        sys.exit(f"Raw file not found: {RAW_CSV}")

    log(f"Reading {RAW_CSV.name} in chunks of {CHUNK_SIZE:,} rows ...")

    totals: dict[str, float] = defaultdict(float)
    cleaned_chunks: list[pd.DataFrame] = []

    reader = pd.read_csv(
        RAW_CSV,
        usecols=USE_COLUMNS + ["average_salary"],
        chunksize=CHUNK_SIZE,
        nrows=nrows,
        low_memory=False,
    )

    for i, chunk in enumerate(reader, start=1):
        cleaned, stats = clean_chunk(chunk)
        for key, value in stats.items():
            totals[key] += value
        cleaned_chunks.append(cleaned)
        log(f"  chunk {i}: {stats['rows_in']:,} in -> {stats['rows_out']:,} kept")

    df = pd.concat(cleaned_chunks, ignore_index=True)
    del cleaned_chunks
    log(f"Concatenated: {len(df):,} rows")

    # ---- whole-file rules -------------------------------------------------
    df, dedupe_stats = deduplicate(df)
    totals.update(dedupe_stats)
    log(f"De-duplicated on job_id: removed {dedupe_stats['duplicate_job_ids_removed']:,}")

    df, cap_stats = winsorise_salary(df, WINSOR_LOWER_Q, WINSOR_UPPER_Q)
    totals.update(cap_stats)
    log(
        f"Salary capped to [{cap_stats['salary_cap_lower']:,.0f}, "
        f"{cap_stats['salary_cap_upper']:,.0f}] "
        f"({cap_stats['salary_rows_capped']:,} rows touched)"
    )

    df = add_features(df)
    # A compact integer key for the posting. The long tables repeat a posting
    # once per category, so anything measured at MARKET level (totals, salary
    # distribution, monthly volume) must de-duplicate on this first - counting
    # rows there would inflate the market by the 1.69 categories a job carries.
    df["job_key"] = np.arange(len(df), dtype="int32")
    log("Feature engineering done")

    # ---- long tables ------------------------------------------------------
    categories_long = explode_categories(df, LONG_TABLE_COLUMNS)
    log(f"Category long table: {len(categories_long):,} rows "
        f"({categories_long['category'].nunique()} distinct categories)")

    skills_long = explode_skills(df, LONG_TABLE_COLUMNS)
    log(f"Skill long table: {len(skills_long):,} rows "
        f"({skills_long['skill'].nunique()} distinct skills)")

    # ---- write ------------------------------------------------------------
    wide = df.drop(columns=["categories"], errors="ignore")
    wide.to_parquet(JOBS_PARQUET, index=False)
    categories_long.to_parquet(JOBS_CATEGORY_PARQUET, index=False)
    skills_long.to_parquet(SKILLS_PARQUET, index=False)

    # ---- audit trail ------------------------------------------------------
    quality = {
        "source_file": RAW_CSV.name,
        "rows_read": int(totals["rows_in"]),
        "rows_after_cleaning": int(len(df)),
        "columns_dropped": DROP_COLUMNS,
        "cleaning_counters": {k: int(v) for k, v in totals.items()},
        "date_range": {
            "first_posting": str(df["original_posting_date"].min().date()),
            "last_posting": str(df["original_posting_date"].max().date()),
        },
        "salary_coverage_pct": round(float(df["avg_salary"].notna().mean() * 100), 2),
        "distinct_categories": int(categories_long["category"].nunique()),
        "distinct_companies": int(df["company"].nunique()),
        "runtime_seconds": round(time.time() - started, 1),
    }
    QUALITY_REPORT.write_text(json.dumps(quality, indent=2))

    log(f"Wrote {JOBS_PARQUET.name} ({len(wide):,} rows), "
        f"{JOBS_CATEGORY_PARQUET.name}, {SKILLS_PARQUET.name}")
    log(f"Done in {quality['runtime_seconds']}s")
    print(json.dumps(quality, indent=2))


if __name__ == "__main__":
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else None
    run(nrows=limit)
