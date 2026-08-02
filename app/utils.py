"""
Career Compass SG - shared dashboard plumbing.

Data loading (cached), the global filter sidebar, and the chart styling that
keeps every page looking like one product.

The heavy analytical functions are imported from ``src/`` rather than re-written
here, so the numbers in the dashboard are produced by exactly the same code that
produced the numbers in the report.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st

SRC = Path(__file__).resolve().parents[1] / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from build_aggregates import build_career_tracks, competition_ratio  # noqa: E402
from config import (  # noqa: E402
    AGG_COMPANY,
    AGG_TITLE,
    CATEGORICAL_SEQUENCE,
    COLORS,
    DEFAULT_SCORE_WEIGHTS,
    EMPLOYMENT_ORDER,
    ENGAGEMENT_RELIABLE_END,
    JOBS_CATEGORY_PARQUET,
    PROCESSED_DIR,
    SENIORITY_ORDER,
    SKILLS_PARQUET,
    VOLUME_RELIABLE_START,
)

KPI_JSON = PROCESSED_DIR / "headline_kpis.json"

APP_COLUMNS = [
    "job_key",
    "category",
    "seniority",
    "employment_type",
    "job_status",
    "is_open",
    "avg_salary",
    "salary_band",
    "min_years_experience",
    "experience_band",
    "is_entry_friendly",
    "vacancies",
    "applications",
    "views",
    "applications_per_vacancy",
    "repost_count",
    "is_hard_to_fill",
    "posting_month",
    "original_posting_date",
    "title_clean",
    "company",
]


# ---------------------------------------------------------------------------
# Page setup
# ---------------------------------------------------------------------------
def page_setup(title: str, icon: str = "compass") -> None:
    st.set_page_config(page_title=f"{title} | Career Compass SG", page_icon="🧭", layout="wide")
    register_template()
    st.markdown(
        """
        <style>
          .block-container {padding-top: 2.2rem; max-width: 1500px;}
          h1 {font-size: 1.9rem !important;}
          h2 {font-size: 1.25rem !important; margin-top: 1.6rem !important;}
          .finding {
              background: #f4f7fb; border-left: 4px solid #2a78d6;
              padding: 0.75rem 1rem; border-radius: 4px; margin: 0.4rem 0 1rem 0;
              font-size: 0.95rem; color: #22282f;
          }
          .caveat {
              background: #fdf5ef; border-left: 4px solid #eb6834;
              padding: 0.7rem 1rem; border-radius: 4px; margin: 0.4rem 0 1rem 0;
              font-size: 0.88rem; color: #3a2f27;
          }
          div[data-testid="stMetricValue"] {font-size: 1.6rem;}
        </style>
        """,
        unsafe_allow_html=True,
    )


def register_template() -> None:
    """One Plotly template for the whole app - recessive grid, quiet axes."""
    template = go.layout.Template()
    template.layout = go.Layout(
        colorway=CATEGORICAL_SEQUENCE,
        font=dict(family="Inter, Helvetica Neue, Arial, sans-serif", size=13, color=COLORS["text"]),
        paper_bgcolor=COLORS["surface"],
        plot_bgcolor=COLORS["surface"],
        title=dict(font=dict(size=16, color=COLORS["text"]), x=0, xanchor="left", pad=dict(b=12)),
        margin=dict(l=10, r=20, t=64, b=40),
        xaxis=dict(
            gridcolor=COLORS["grid"],
            zerolinecolor=COLORS["grid"],
            linecolor=COLORS["grid"],
            tickfont=dict(color=COLORS["text_secondary"], size=12),
            title=dict(font=dict(color=COLORS["text_secondary"], size=12)),
        ),
        yaxis=dict(
            gridcolor=COLORS["grid"],
            zerolinecolor=COLORS["grid"],
            linecolor=COLORS["grid"],
            tickfont=dict(color=COLORS["text_secondary"], size=12),
            title=dict(font=dict(color=COLORS["text_secondary"], size=12)),
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            x=0,
            font=dict(size=12, color=COLORS["text_secondary"]),
            title=dict(text=""),
            traceorder="normal",  # legend order matches the order series are drawn
        ),
        hoverlabel=dict(bgcolor="white", font_size=12, bordercolor=COLORS["grid"]),
    )
    pio.templates["compass"] = template
    pio.templates.default = "plotly_white+compass"


def finding(text: str) -> None:
    """The sentence the chart exists to deliver. Always above the chart."""
    st.markdown(f'<div class="finding">{text}</div>', unsafe_allow_html=True)


def caveat(text: str) -> None:
    """A limitation the reader must know about before trusting the chart above."""
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    st.markdown(f'<div class="caveat">⚠️ {text}</div>', unsafe_allow_html=True)


def show(fig: go.Figure, height: int | None = None) -> None:
    if height:
        fig.update_layout(height=height)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------
@st.cache_data(show_spinner="Loading 1.77M job-category records ...")
def load_jobs() -> pd.DataFrame:
    df = pd.read_parquet(JOBS_CATEGORY_PARQUET, columns=APP_COLUMNS)
    for col in ["title_clean", "company"]:
        df[col] = df[col].astype("category")
    return df


@st.cache_data(show_spinner=False)
def load_skills() -> pd.DataFrame:
    cols = [
        "skill",
        "seniority",
        "employment_type",
        "avg_salary",
        "min_years_experience",
        "is_entry_friendly",
        "is_hard_to_fill",
        "posting_month",
        "vacancies",
    ]
    return pd.read_parquet(SKILLS_PARQUET, columns=cols)


@st.cache_data(show_spinner=False)
def load_kpis() -> dict:
    return json.loads(KPI_JSON.read_text())


@st.cache_data(show_spinner=False)
def load_titles() -> pd.DataFrame:
    return pd.read_parquet(AGG_TITLE)


@st.cache_data(show_spinner=False)
def load_companies() -> pd.DataFrame:
    return pd.read_parquet(AGG_COMPANY)


# ---------------------------------------------------------------------------
# Global filters - one sidebar, shared across every page via session_state keys
# ---------------------------------------------------------------------------
def sidebar_filters(df: pd.DataFrame) -> dict:
    st.sidebar.markdown("### 🧭 Career Compass SG")
    st.sidebar.caption(
        "Singapore job postings, Oct 2022 - May 2024. Filters apply to every page."
    )
    st.sidebar.divider()

    months = sorted(df["posting_month"].dropna().unique())
    month_labels = [pd.Timestamp(m).strftime("%b %Y") for m in months]
    default_start = month_labels.index(pd.Timestamp(VOLUME_RELIABLE_START).strftime("%b %Y"))

    start_label, end_label = st.sidebar.select_slider(
        "Posting period",
        options=month_labels,
        value=(month_labels[default_start], month_labels[-1]),
        key="f_period",
        help="Defaults to the full-coverage window. Months before May 2023 are "
        "partially collected and are excluded by default.",
    )
    start = months[month_labels.index(start_label)]
    end = months[month_labels.index(end_label)]

    employment = st.sidebar.multiselect(
        "Employment type",
        options=[e for e in EMPLOYMENT_ORDER if e in set(df["employment_type"].cat.categories)],
        default=[],
        key="f_employment",
        placeholder="All employment types",
    )

    seniority = st.sidebar.multiselect(
        "Seniority",
        options=SENIORITY_ORDER,
        default=[],
        key="f_seniority",
        placeholder="All seniority levels",
    )

    salary_min, salary_max = st.sidebar.slider(
        "Average monthly salary (SGD)",
        min_value=1000,
        max_value=17000,
        value=(1000, 17000),
        step=250,
        key="f_salary",
    )

    open_only = st.sidebar.checkbox(
        "Currently open postings only", value=False, key="f_open"
    )

    st.sidebar.divider()
    st.sidebar.caption(
        f"Competition metrics are always computed on postings up to "
        f"**{ENGAGEMENT_RELIABLE_END}** - see the caveat on the Competition page."
    )

    return {
        "start": pd.Timestamp(start),
        "end": pd.Timestamp(end),
        "employment": employment,
        "seniority": seniority,
        "salary": (salary_min, salary_max),
        "open_only": open_only,
    }


def apply_filters(df: pd.DataFrame, f: dict, ignore_period: bool = False) -> pd.DataFrame:
    if ignore_period:
        mask = pd.Series(True, index=df.index)
    else:
        mask = (df["posting_month"] >= f["start"]) & (df["posting_month"] <= f["end"])
    if f["employment"]:
        mask &= df["employment_type"].isin(f["employment"])
    if f["seniority"]:
        mask &= df["seniority"].isin(f["seniority"])
    if f["open_only"]:
        mask &= df["is_open"]
    lo, hi = f["salary"]
    if (lo, hi) != (1000, 17000):
        mask &= df["avg_salary"].between(lo, hi)
    return df[mask]


@st.cache_data(show_spinner=False)
def unique_jobs(_df: pd.DataFrame, sig: tuple) -> pd.DataFrame:
    """One row per posting again.

    The working table repeats a posting once per category it belongs to (1.69
    on average). Category-level questions want those repeats; market-level
    questions - "how many jobs are there", "what is the median salary" - must
    not double-count, so they go through here first.
    """
    return _df.drop_duplicates(subset="job_key")


@st.cache_data(show_spinner=False)
def reliable_subset(_df: pd.DataFrame, f: dict) -> pd.DataFrame:
    """The window where views and applications can be trusted.

    Deliberately ignores the sidebar's period filter. Competition is a property
    of a career track, not of the months a user happens to be looking at, and
    the counters simply do not exist after 2023-06 - so a user browsing 2024
    postings should still see real competition figures rather than zeros.
    """
    window = _df[_df["original_posting_date"] <= pd.Timestamp(ENGAGEMENT_RELIABLE_END)]
    return apply_filters(window, f, ignore_period=True)


def filter_signature(f: dict) -> tuple:
    """A hashable key so cached computations know when the filters changed."""
    return (
        f["start"],
        f["end"],
        tuple(f["employment"]),
        tuple(f["seniority"]),
        f["salary"],
        f["open_only"],
    )


def filter_summary(f: dict, rows: int, total: int) -> None:
    bits = [f"{f['start']:%b %Y} - {f['end']:%b %Y}"]
    if f["employment"]:
        bits.append(", ".join(f["employment"]))
    if f["seniority"]:
        bits.append(", ".join(f["seniority"]))
    if f["salary"] != (1000, 17000):
        bits.append(f"${f['salary'][0]:,}-${f['salary'][1]:,}")
    if f["open_only"]:
        bits.append("open only")
    st.caption(
        f"**{rows:,}** job postings in view "
        f"({rows / total:.0%} of the dataset) — filters: {' · '.join(bits)}"
    )


# ---------------------------------------------------------------------------
# Shared computations
# ---------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def category_summary(_df: pd.DataFrame, _reliable: pd.DataFrame, sig: tuple) -> pd.DataFrame:
    """Per-category metrics on the CURRENT filter selection."""
    base = _df.groupby("category", observed=True).agg(
        postings=("avg_salary", "size"),
        vacancies=("vacancies", "sum"),
        median_salary=("avg_salary", "median"),
        p25_salary=("avg_salary", lambda s: s.quantile(0.25)),
        p75_salary=("avg_salary", lambda s: s.quantile(0.75)),
        p90_salary=("avg_salary", lambda s: s.quantile(0.90)),
        median_min_years=("min_years_experience", "median"),
        entry_friendly_share=("is_entry_friendly", "mean"),
        hard_to_fill_share=("is_hard_to_fill", "mean"),
        open_share=("is_open", "mean"),
        companies=("company", "nunique"),
    )
    comp = (
        _reliable.groupby("category", observed=True)[["applications", "vacancies"]]
        .apply(competition_ratio)
        .rename("apps_per_vacancy")
    )
    out = base.join(comp).reset_index()
    for col in ["entry_friendly_share", "hard_to_fill_share", "open_share"]:
        out[col] = (out[col] * 100).round(1)
    return out.sort_values("postings", ascending=False)


@st.cache_data(show_spinner="Scoring career tracks ...")
def scored_tracks(_df: pd.DataFrame, _reliable: pd.DataFrame, sig: tuple) -> pd.DataFrame:
    """Re-run the exact scoring routine from src/ on the filtered data.

    Nothing is re-implemented here: ``build_career_tracks`` is the same function
    the batch job calls, so a track's score in the app and in the report can
    never drift apart.
    """
    work = _df.copy()
    work["job_id"] = 1  # build_career_tracks counts rows via this column
    reliable = _reliable.copy()
    reliable["job_id"] = 1
    return build_career_tracks(work, reliable)


def money(value: float) -> str:
    return "n/a" if pd.isna(value) else f"${value:,.0f}"


DEFAULT_WEIGHTS = DEFAULT_SCORE_WEIGHTS
