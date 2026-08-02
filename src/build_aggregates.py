"""
Career Compass SG - stage 2: aggregates and the Career Fit Score.

The dashboard must stay responsive on a 1M-row dataset, so every summary the
app draws is pre-computed here once and written to parquet. The app then reads
small tables (tens of KB to a few MB) instead of grinding through a million
rows per interaction.

The one thing NOT pre-computed is the final Career Fit Score, because its
weights are a user control. What we pre-compute are the four component scores
and an accessibility curve per track; the app combines them in milliseconds.

Run:  python src/build_aggregates.py   (after etl_clean.py)
"""

from __future__ import annotations

import json
import time

import numpy as np
import pandas as pd

from config import (
    AGG_CATEGORY,
    AGG_CATEGORY_SENIORITY,
    AGG_COMPANY,
    AGG_EXPERIENCE,
    AGG_MONTHLY,
    AGG_SKILL,
    AGG_TITLE,
    CAREER_TRACKS,
    DEFAULT_SCORE_WEIGHTS,
    ENGAGEMENT_RELIABLE_END,
    JOBS_CATEGORY_PARQUET,
    JOBS_PARQUET,
    MIN_POSTINGS_FOR_TRACK,
    PROCESSED_DIR,
    SENIORITY_ORDER,
    SKILLS_PARQUET,
    VOLUME_RELIABLE_START,
)

KPI_JSON = PROCESSED_DIR / "headline_kpis.json"

# Years-of-experience thresholds the recommender can answer "can I get in?" for
ACCESS_THRESHOLDS = [0, 1, 2, 3, 5, 8, 10, 15]


def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def competition_ratio(group: pd.DataFrame) -> float:
    """Applications per vacancy as a ratio of sums, not a mean of ratios.

    A mean of per-posting ratios is dominated by tiny postings with one seat and
    one applicant. Total applications / total vacancies answers the question a
    job seeker is actually asking: for every seat in this track, how many people
    are in the queue?
    """
    vacancies = group["vacancies"].fillna(1).clip(lower=1).sum()
    return float(group["applications"].sum() / vacancies) if vacancies else np.nan


def pct_rank(series: pd.Series, higher_is_better: bool = True) -> pd.Series:
    """Percentile rank on a 0-100 scale, so four different units become comparable."""
    ranked = series.rank(pct=True, na_option="keep")
    if not higher_is_better:
        ranked = 1 - ranked
    return (ranked * 100).round(1)


def salary_stats(group: pd.DataFrame) -> pd.Series:
    salaries = group["avg_salary"].dropna()
    return pd.Series(
        {
            "median_salary": salaries.median(),
            "p25_salary": salaries.quantile(0.25),
            "p75_salary": salaries.quantile(0.75),
            "p90_salary": salaries.quantile(0.90),
        }
    )


# ---------------------------------------------------------------------------
# Aggregate builders
# ---------------------------------------------------------------------------
def build_category(cat: pd.DataFrame, cat_reliable: pd.DataFrame) -> pd.DataFrame:
    """One row per job category - the backbone of the overview page."""
    base = cat.groupby("category", observed=True).agg(
        postings=("job_id", "size"),
        vacancies=("vacancies", "sum"),
        median_salary=("avg_salary", "median"),
        p25_salary=("avg_salary", lambda s: s.quantile(0.25)),
        p75_salary=("avg_salary", lambda s: s.quantile(0.75)),
        p90_salary=("avg_salary", lambda s: s.quantile(0.90)),
        median_min_years=("min_years_experience", "median"),
        entry_friendly_share=("is_entry_friendly", "mean"),
        hard_to_fill_share=("is_hard_to_fill", "mean"),
        open_share=("is_open", "mean"),
        avg_repost=("repost_count", "mean"),
        companies=("company", "nunique"),
    )

    comp = (
        cat_reliable.groupby("category", observed=True)[["applications", "vacancies"]]
        .apply(competition_ratio)
        .rename("apps_per_vacancy")
    )
    comp_n = cat_reliable.groupby("category", observed=True).size().rename("competition_sample")

    growth = build_growth(cat)

    out = base.join([comp, comp_n, growth]).reset_index()
    out["entry_friendly_share"] = (out["entry_friendly_share"] * 100).round(1)
    out["hard_to_fill_share"] = (out["hard_to_fill_share"] * 100).round(1)
    out["open_share"] = (out["open_share"] * 100).round(1)
    return out.sort_values("postings", ascending=False)


def build_growth(cat: pd.DataFrame) -> pd.Series:
    """Momentum: postings in the most recent 6 months vs the 6 months before.

    Restricted to the reliable-volume window so the collection ramp-up in late
    2022 cannot masquerade as explosive growth.
    """
    reliable = cat[cat["posting_month"] >= pd.Timestamp(VOLUME_RELIABLE_START)]
    last_month = reliable["posting_month"].max()
    recent_start = last_month - pd.DateOffset(months=5)
    prior_start = last_month - pd.DateOffset(months=11)

    recent = reliable[reliable["posting_month"] >= recent_start]
    prior = reliable[
        (reliable["posting_month"] >= prior_start) & (reliable["posting_month"] < recent_start)
    ]

    recent_counts = recent.groupby("category", observed=True).size()
    prior_counts = prior.groupby("category", observed=True).size()
    growth = ((recent_counts / prior_counts - 1) * 100).round(1)
    return growth.rename("growth_pct_6m")


def build_category_seniority(cat: pd.DataFrame, cat_reliable: pd.DataFrame) -> pd.DataFrame:
    """Category x seniority - powers the heatmap and the drill-down."""
    grouped = cat.groupby(["category", "seniority"], observed=True).agg(
        postings=("job_id", "size"),
        vacancies=("vacancies", "sum"),
        median_salary=("avg_salary", "median"),
        p25_salary=("avg_salary", lambda s: s.quantile(0.25)),
        p75_salary=("avg_salary", lambda s: s.quantile(0.75)),
        median_min_years=("min_years_experience", "median"),
        hard_to_fill_share=("is_hard_to_fill", "mean"),
    )
    comp = (
        cat_reliable.groupby(["category", "seniority"], observed=True)[["applications", "vacancies"]]
        .apply(competition_ratio)
        .rename("apps_per_vacancy")
    )
    out = grouped.join(comp).reset_index()
    out["hard_to_fill_share"] = (out["hard_to_fill_share"] * 100).round(1)
    return out


def build_monthly(cat: pd.DataFrame) -> pd.DataFrame:
    """Month x category postings and pay - the time-trend page."""
    out = (
        cat.groupby(["posting_month", "category"], observed=True)
        .agg(
            postings=("job_id", "size"),
            vacancies=("vacancies", "sum"),
            median_salary=("avg_salary", "median"),
        )
        .reset_index()
    )
    out["is_partial_coverage"] = out["posting_month"] < pd.Timestamp(VOLUME_RELIABLE_START)
    return out


def build_skill(skills: pd.DataFrame, market_median: float) -> pd.DataFrame:
    """Skill demand and the pay premium it carries over the market median."""
    out = (
        skills.groupby("skill", observed=True)
        .agg(
            postings=("job_id", "size"),
            median_salary=("avg_salary", "median"),
            p75_salary=("avg_salary", lambda s: s.quantile(0.75)),
            median_min_years=("min_years_experience", "median"),
            entry_friendly_share=("is_entry_friendly", "mean"),
            hard_to_fill_share=("is_hard_to_fill", "mean"),
        )
        .reset_index()
    )
    out["salary_premium_pct"] = ((out["median_salary"] / market_median - 1) * 100).round(1)
    out["entry_friendly_share"] = (out["entry_friendly_share"] * 100).round(1)
    out["hard_to_fill_share"] = (out["hard_to_fill_share"] * 100).round(1)
    return out.sort_values("postings", ascending=False)


def build_titles(cat: pd.DataFrame, top_n: int = 40) -> pd.DataFrame:
    """The top job titles inside each category, after title standardisation."""
    grouped = (
        cat.dropna(subset=["title_clean"])
        .groupby(["category", "title_clean"], observed=True)
        .agg(
            postings=("job_id", "size"),
            median_salary=("avg_salary", "median"),
            median_min_years=("min_years_experience", "median"),
        )
        .reset_index()
    )
    grouped = grouped[grouped["postings"] >= 5]
    return (
        grouped.sort_values(["category", "postings"], ascending=[True, False])
        .groupby("category", observed=True)
        .head(top_n)
        .reset_index(drop=True)
    )


def build_companies(cat: pd.DataFrame, top_n: int = 25) -> pd.DataFrame:
    """Top posting organisations per category.

    Named 'poster', not 'employer', on purpose: the raw column is the account
    that posted the advert, and in Singapore that is very often a recruitment
    agency rather than the hiring company.
    """
    grouped = (
        cat.groupby(["category", "company"], observed=True)
        .agg(
            postings=("job_id", "size"),
            median_salary=("avg_salary", "median"),
            vacancies=("vacancies", "sum"),
        )
        .reset_index()
    )
    grouped = grouped[grouped["postings"] >= 5]
    return (
        grouped.sort_values(["category", "postings"], ascending=[True, False])
        .groupby("category", observed=True)
        .head(top_n)
        .reset_index(drop=True)
    )


def build_experience(cat: pd.DataFrame) -> pd.DataFrame:
    """What each extra year of experience is worth, per category."""
    work = cat[cat["min_years_experience"].notna()].copy()
    work["years"] = work["min_years_experience"].clip(upper=15).astype(int)
    return (
        work.groupby(["category", "years"], observed=True)
        .agg(
            postings=("job_id", "size"),
            median_salary=("avg_salary", "median"),
            p25_salary=("avg_salary", lambda s: s.quantile(0.25)),
            p75_salary=("avg_salary", lambda s: s.quantile(0.75)),
        )
        .reset_index()
    )


# ---------------------------------------------------------------------------
# The recommender's scoring table
# ---------------------------------------------------------------------------
def build_career_tracks(cat: pd.DataFrame, cat_reliable: pd.DataFrame) -> pd.DataFrame:
    """One row per career track = (category x seniority), with score components.

    Four components, each converted to a 0-100 percentile rank so that dollars,
    counts and ratios can be compared on one scale:

      demand           log postings   (log, because 40k vs 20k postings is not
                                       twice as good a bet as 200 vs 100)
      pay              median salary
      low_competition  inverse of applications per vacancy
      accessibility    share of postings you already qualify for, given your
                       years of experience - stored as a curve, applied in-app
    """
    tracks = cat.groupby(["category", "seniority"], observed=True).agg(
        postings=("job_id", "size"),
        vacancies=("vacancies", "sum"),
        median_salary=("avg_salary", "median"),
        p25_salary=("avg_salary", lambda s: s.quantile(0.25)),
        p75_salary=("avg_salary", lambda s: s.quantile(0.75)),
        median_min_years=("min_years_experience", "median"),
        hard_to_fill_share=("is_hard_to_fill", "mean"),
        open_share=("is_open", "mean"),
        companies=("company", "nunique"),
    )

    comp = (
        cat_reliable.groupby(["category", "seniority"], observed=True)[
            ["applications", "vacancies"]
        ]
        .apply(competition_ratio)
        .rename("apps_per_vacancy")
    )
    tracks = tracks.join(comp)

    # Accessibility curve: for each threshold, what share of this track's
    # postings ask for that many years or fewer?
    years = cat[["category", "seniority", "min_years_experience"]].copy()
    for threshold in ACCESS_THRESHOLDS:
        flag = (years["min_years_experience"].fillna(0) <= threshold).astype(float)
        share = (
            flag.groupby([years["category"], years["seniority"]], observed=True)
            .mean()
            .rename(f"access_le_{threshold}")
        )
        tracks = tracks.join(share)

    # Growth, reused from the category level but computed per track
    growth = build_track_growth(cat)
    tracks = tracks.join(growth)

    tracks = tracks.reset_index()
    tracks = tracks[tracks["postings"] >= MIN_POSTINGS_FOR_TRACK].copy()

    # ---- component scores ------------------------------------------------
    tracks["demand_score"] = pct_rank(np.log10(tracks["postings"]))
    tracks["pay_score"] = pct_rank(tracks["median_salary"])
    tracks["low_competition_score"] = pct_rank(tracks["apps_per_vacancy"], higher_is_better=False)
    tracks["growth_score"] = pct_rank(tracks["growth_pct_6m"])

    # A default score so the table is meaningful before anyone touches a slider
    tracks["accessibility_score_default"] = pct_rank(tracks["access_le_3"])
    tracks["fit_score_default"] = (
        DEFAULT_SCORE_WEIGHTS["demand"] * tracks["demand_score"]
        + DEFAULT_SCORE_WEIGHTS["pay"] * tracks["pay_score"]
        + DEFAULT_SCORE_WEIGHTS["low_competition"] * tracks["low_competition_score"].fillna(50)
        + DEFAULT_SCORE_WEIGHTS["accessibility"] * tracks["accessibility_score_default"]
    ).round(1)

    tracks["hard_to_fill_share"] = (tracks["hard_to_fill_share"] * 100).round(1)
    tracks["open_share"] = (tracks["open_share"] * 100).round(1)
    tracks["track"] = tracks["category"].astype(str) + " - " + tracks["seniority"].astype(str)
    return tracks.sort_values("fit_score_default", ascending=False).reset_index(drop=True)


def build_track_growth(cat: pd.DataFrame) -> pd.Series:
    reliable = cat[cat["posting_month"] >= pd.Timestamp(VOLUME_RELIABLE_START)]
    last_month = reliable["posting_month"].max()
    recent_start = last_month - pd.DateOffset(months=5)
    prior_start = last_month - pd.DateOffset(months=11)

    recent = reliable[reliable["posting_month"] >= recent_start]
    prior = reliable[
        (reliable["posting_month"] >= prior_start) & (reliable["posting_month"] < recent_start)
    ]
    keys = ["category", "seniority"]
    recent_counts = recent.groupby(keys, observed=True).size()
    prior_counts = prior.groupby(keys, observed=True).size()
    return ((recent_counts / prior_counts - 1) * 100).round(1).rename("growth_pct_6m")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def run() -> None:
    started = time.time()
    log("Loading parquet ...")
    jobs = pd.read_parquet(JOBS_PARQUET)
    cat = pd.read_parquet(JOBS_CATEGORY_PARQUET)
    skills = pd.read_parquet(SKILLS_PARQUET)
    log(f"jobs={len(jobs):,}  job-category={len(cat):,}  job-skill={len(skills):,}")

    reliable_cutoff = pd.Timestamp(ENGAGEMENT_RELIABLE_END)
    cat_reliable = cat[cat["original_posting_date"] <= reliable_cutoff]
    log(
        f"Competition window: postings up to {ENGAGEMENT_RELIABLE_END} "
        f"({len(cat_reliable):,} of {len(cat):,} category-rows)"
    )

    market_median = float(jobs["avg_salary"].median())

    log("Building aggregates ...")
    agg_category = build_category(cat, cat_reliable)
    agg_cat_sen = build_category_seniority(cat, cat_reliable)
    agg_monthly = build_monthly(cat)
    agg_skill = build_skill(skills, market_median)
    agg_title = build_titles(cat)
    agg_company = build_companies(cat)
    agg_experience = build_experience(cat)
    tracks = build_career_tracks(cat, cat_reliable)

    for frame, path in [
        (agg_category, AGG_CATEGORY),
        (agg_cat_sen, AGG_CATEGORY_SENIORITY),
        (agg_monthly, AGG_MONTHLY),
        (agg_skill, AGG_SKILL),
        (agg_title, AGG_TITLE),
        (agg_company, AGG_COMPANY),
        (agg_experience, AGG_EXPERIENCE),
        (tracks, CAREER_TRACKS),
    ]:
        frame.to_parquet(path, index=False)
        log(f"  wrote {path.name:<32} {len(frame):>8,} rows")

    # ---- headline KPIs for the overview page -----------------------------
    jobs_reliable = jobs[jobs["original_posting_date"] <= reliable_cutoff]
    kpis = {
        "total_postings": int(len(jobs)),
        "total_vacancies": int(jobs["vacancies"].sum()),
        "distinct_categories": int(cat["category"].nunique()),
        "distinct_companies": int(jobs["company"].nunique()),
        "median_salary": round(market_median, 0),
        "p25_salary": round(float(jobs["avg_salary"].quantile(0.25)), 0),
        "p75_salary": round(float(jobs["avg_salary"].quantile(0.75)), 0),
        "salary_coverage_pct": round(float(jobs["avg_salary"].notna().mean() * 100), 1),
        "open_share_pct": round(float(jobs["is_open"].mean() * 100), 1),
        "hard_to_fill_pct": round(float(jobs["is_hard_to_fill"].mean() * 100), 1),
        "entry_friendly_pct": round(float(jobs["is_entry_friendly"].mean() * 100), 1),
        "market_apps_per_vacancy": round(competition_ratio(jobs_reliable), 2),
        "date_min": str(jobs["original_posting_date"].min().date()),
        "date_max": str(jobs["original_posting_date"].max().date()),
        "engagement_reliable_end": ENGAGEMENT_RELIABLE_END,
        "volume_reliable_start": VOLUME_RELIABLE_START,
        "tracks_scored": int(len(tracks)),
        "seniority_order": SENIORITY_ORDER,
    }
    KPI_JSON.write_text(json.dumps(kpis, indent=2))
    log(f"  wrote {KPI_JSON.name}")

    log(f"Done in {time.time() - started:.1f}s")
    print(json.dumps(kpis, indent=2))
    print("\nTop 10 career tracks by default Career Fit Score:")
    print(
        tracks.head(10)[
            ["track", "postings", "median_salary", "apps_per_vacancy", "fit_score_default"]
        ].to_string(index=False)
    )


if __name__ == "__main__":
    run()
