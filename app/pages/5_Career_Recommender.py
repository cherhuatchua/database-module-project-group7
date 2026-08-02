"""
Career Compass SG - page 6: the Career Recommender.

This is the product. Everything else on the site is evidence for what this page
outputs: a ranked shortlist of career tracks for one specific person, with the
reasoning shown rather than hidden.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from utils import (
    apply_filters,
    filter_signature,
    finding,
    load_jobs,
    money,
    page_setup,
    reliable_subset,
    scored_tracks,
    show,
    sidebar_filters,
)

from config import COLORS, DEFAULT_SCORE_WEIGHTS, SENIORITY_ORDER  # noqa: E402

ACCESS_THRESHOLDS = [0, 1, 2, 3, 5, 8, 10, 15]

page_setup("Career Recommender")

jobs = load_jobs()
filters = sidebar_filters(jobs)
sig = filter_signature(filters)
view = apply_filters(jobs, filters)
reliable = reliable_subset(jobs, filters)
tracks = scored_tracks(view, reliable, sig)

st.title("⭐ Career Recommender")
st.markdown(
    "Tell us where you are and what you care about. We score all "
    f"**{len(tracks)} career tracks** (category × seniority) on four dimensions and rank them "
    "for *you* — with every component of the score shown, so you can disagree with it."
)

# ---------------------------------------------------------------------------
# The user's inputs
# ---------------------------------------------------------------------------
st.markdown("## 1. Your situation")

c1, c2, c3 = st.columns([1, 1, 2])
with c1:
    years = st.number_input(
        "Years of relevant experience", min_value=0, max_value=25, value=3, step=1
    )
with c2:
    target_salary = st.number_input(
        "Minimum monthly salary you need (SGD)",
        min_value=1000,
        max_value=20000,
        value=4000,
        step=250,
    )
with c3:
    levels = st.multiselect(
        "Seniority levels you would consider",
        options=SENIORITY_ORDER,
        default=SENIORITY_ORDER,
        help="Leave all selected if you are open to anything.",
    )

interests = st.multiselect(
    "Restrict to these fields (optional)",
    options=sorted(tracks["category"].astype(str).unique()),
    default=[],
    placeholder="All fields — leave empty if you are exploring",
)

# ---------------------------------------------------------------------------
# The weights
# ---------------------------------------------------------------------------
st.markdown("## 2. What matters to you")
st.caption(
    "The four sliders are the whole model. Move them and the ranking changes in front of you — "
    "there is no hidden black box here."
)

w1, w2, w3, w4 = st.columns(4)
with w1:
    w_demand = st.slider("Plenty of openings", 0, 100, int(DEFAULT_SCORE_WEIGHTS["demand"] * 100))
with w2:
    w_pay = st.slider("High pay", 0, 100, int(DEFAULT_SCORE_WEIGHTS["pay"] * 100))
with w3:
    w_comp = st.slider(
        "Low competition", 0, 100, int(DEFAULT_SCORE_WEIGHTS["low_competition"] * 100)
    )
with w4:
    w_access = st.slider(
        "Easy for me to enter", 0, 100, int(DEFAULT_SCORE_WEIGHTS["accessibility"] * 100)
    )

total_weight = w_demand + w_pay + w_comp + w_access
if total_weight == 0:
    st.warning("Give at least one priority some weight.")
    st.stop()

# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------
threshold = min(ACCESS_THRESHOLDS, key=lambda t: abs(t - years))
access_col = f"access_le_{threshold}"

work = tracks.copy()
if levels:
    work = work[work["seniority"].astype(str).isin(levels)]
if interests:
    work = work[work["category"].astype(str).isin(interests)]
work = work[work["median_salary"] >= target_salary]

if work.empty:
    st.error(
        "No career track matches those constraints. Try lowering the salary floor, "
        "widening the seniority levels, or clearing the field restriction."
    )
    st.stop()

# Accessibility is re-ranked within the surviving set, so it answers "of the
# tracks still on the table, which ones actually take someone with my years?"
work["accessibility_score"] = (work[access_col].rank(pct=True) * 100).round(1)
work["fit_score"] = (
    w_demand * work["demand_score"]
    + w_pay * work["pay_score"]
    + w_comp * work["low_competition_score"].fillna(50)
    + w_access * work["accessibility_score"]
) / total_weight
work = work.sort_values("fit_score", ascending=False).reset_index(drop=True)

st.markdown("## 3. Your shortlist")

best = work.iloc[0]
competition_phrase = (
    "competition data unavailable"
    if pd.isna(best["apps_per_vacancy"])
    else f"{best['apps_per_vacancy']:.1f} applicants per seat"
)
finding(
    f"Your best-fit track is <b>{best['track']}</b> — {int(best['postings']):,} postings, "
    f"a median of {money(best['median_salary'])}, {competition_phrase}, "
    f"and {best[access_col]:.0%} of its postings are open to someone with {years} "
    f"year{'s' if years != 1 else ''} of experience."
)

top_n = work.head(8)

# ---------------------------------------------------------------------------
# Chart 1 - stacked contribution bars: WHY each track ranks where it does
# ---------------------------------------------------------------------------
components = [
    ("Openings", "demand_score", w_demand, "#2a78d6"),
    ("Pay", "pay_score", w_pay, "#eb6834"),
    ("Low competition", "low_competition_score", w_comp, "#1baf7a"),
    ("Easy to enter", "accessibility_score", w_access, "#eda100"),
]

fig = go.Figure()
plot_order = top_n.iloc[::-1]
for label, col, weight, colour in components:
    contribution = plot_order[col].fillna(50) * weight / total_weight
    fig.add_trace(
        go.Bar(
            x=contribution,
            y=plot_order["track"],
            orientation="h",
            name=label,
            marker=dict(color=colour, line=dict(color=COLORS["surface"], width=2)),
            customdata=np.stack([plot_order[col].fillna(50)], axis=-1),
            hovertemplate=f"<b>%{{y}}</b><br>{label}: %{{customdata[0]:.0f}}/100"
            f" × {weight / total_weight:.0%} weight = %{{x:.1f}} points<extra></extra>",
        )
    )
fig.update_layout(
    barmode="stack",
    title="Why these tracks ranked: each bar is the weighted contribution of the four components",
    xaxis_title="Career Fit Score (0–100)",
    yaxis_title=None,
)
show(fig, height=460)

# ---------------------------------------------------------------------------
# Chart 2 - radar: the shape of the top three
# ---------------------------------------------------------------------------
st.markdown("## How the top three compare, shape by shape")

finding(
    "A radar shows the <i>trade-off</i> a track asks you to make. A track that bulges towards "
    "'Pay' but collapses on 'Easy to enter' is a long-term target, not a next move."
)

axes = ["Openings", "Pay", "Low competition", "Easy to enter"]
cols = ["demand_score", "pay_score", "low_competition_score", "accessibility_score"]
palette = ["#2a78d6", "#eb6834", "#1baf7a"]

fig = go.Figure()
for i, (_, r) in enumerate(work.head(3).iterrows()):
    values = [float(r[c]) if pd.notna(r[c]) else 50.0 for c in cols]
    rgb = tuple(int(palette[i][j:j + 2], 16) for j in (1, 3, 5))
    fig.add_trace(
        go.Scatterpolar(
            r=values + [values[0]],
            theta=axes + [axes[0]],
            fill="toself",
            fillcolor=f"rgba({rgb[0]},{rgb[1]},{rgb[2]},0.18)",
            line=dict(color=palette[i], width=2.5),
            name=r["track"],
            hovertemplate="<b>" + r["track"] + "</b><br>%{theta}: %{r:.0f}/100<extra></extra>",
        )
    )
fig.update_layout(
    polar=dict(
        radialaxis=dict(visible=True, range=[0, 100], gridcolor=COLORS["grid"], tickfont=dict(size=10)),
        angularaxis=dict(gridcolor=COLORS["grid"]),
        bgcolor=COLORS["surface"],
    ),
    title="Score profile of your top three tracks",
    showlegend=True,
)
show(fig, height=520)

# ---------------------------------------------------------------------------
# The evidence table
# ---------------------------------------------------------------------------
st.markdown("## The numbers behind the ranking")

table = work.head(15)[
    [
        "track",
        "fit_score",
        "postings",
        "median_salary",
        "p75_salary",
        "apps_per_vacancy",
        access_col,
        "hard_to_fill_share",
        "growth_pct_6m",
    ]
].copy()
table[access_col] = (table[access_col] * 100).round(0)
table["fit_score"] = table["fit_score"].round(1)
table["median_salary"] = table["median_salary"].map(money)
table["p75_salary"] = table["p75_salary"].map(money)
table["apps_per_vacancy"] = table["apps_per_vacancy"].round(1)
table.columns = [
    "Career track",
    "Fit score",
    "Postings",
    "Median pay",
    "Top-quartile pay",
    "Applicants per seat",
    f"% open to {years} yrs exp",
    "% reposted",
    "6-month growth %",
]
st.dataframe(
    table,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Fit score": st.column_config.ProgressColumn(
            "Fit score", format="%.1f", min_value=0, max_value=100
        )
    },
)

with st.expander("How the Career Fit Score is calculated"):
    st.markdown(
        f"""
Every track is scored on four components. Each is converted to a **percentile rank from 0 to
100** before weighting, so dollars, counts and ratios can be added together honestly.

| Component | What it measures | How it is computed |
|---|---|---|
| **Openings** | is there volume to apply to? | percentile of log₁₀(postings) — 40,000 postings is not "twice as good a bet" as 20,000, so the log matters |
| **Pay** | what the track pays | percentile of median advertised salary |
| **Low competition** | how many rivals per seat | percentile of the *inverse* of applications ÷ vacancies, measured only on postings up to Jun 2023 where the counters are real |
| **Easy to enter** | can *you* get in? | share of the track's postings asking for ≤ **{threshold} years** — the threshold nearest your {years} years — re-ranked across the tracks that survived your filters |

Your current weights: **openings {w_demand / total_weight:.0%} · pay {w_pay / total_weight:.0%} ·
low competition {w_comp / total_weight:.0%} · easy to enter {w_access / total_weight:.0%}**.

A track needs at least 200 postings to be scored at all — below that the medians are too noisy
to recommend anyone into.

**What this score is not.** It knows nothing about you beyond your years of experience, and
nothing about whether you would enjoy the work. It ranks *market conditions*, and market
conditions are one input to a career decision, not the decision.
        """
    )

st.download_button(
    "⬇️ Download your shortlist (CSV)",
    data=work.head(15).to_csv(index=False).encode("utf-8"),
    file_name="career_compass_shortlist.csv",
    mime="text/csv",
)
