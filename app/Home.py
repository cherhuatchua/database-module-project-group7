"""Career Compass SG - page 1: Market Overview."""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from utils import (
    apply_filters,
    caveat,
    category_summary,
    filter_signature,
    filter_summary,
    finding,
    load_jobs,
    load_kpis,
    money,
    page_setup,
    reliable_subset,
    show,
    sidebar_filters,
    unique_jobs,
)

from config import COLORS, VOLUME_RELIABLE_START  # noqa: E402

page_setup("Market Overview")

jobs = load_jobs()
kpis = load_kpis()
filters = sidebar_filters(jobs)
sig = filter_signature(filters)
view = apply_filters(jobs, filters)              # one row per (job, category)
reliable = reliable_subset(jobs, filters)        # the trustworthy-engagement window
cats = category_summary(view, reliable, sig)     # category questions: use the repeats
market = unique_jobs(view, sig)                  # market questions: one row per job
market_reliable = unique_jobs(reliable, sig + ("reliable",))
all_jobs = unique_jobs(jobs, ("unfiltered",))

st.title("🧭 Career Compass SG")
st.markdown(
    "#### Which Singapore career track should you aim at next?\n"
    "Built for job seekers and career switchers from **1,044,597 MyCareersFuture job "
    "postings** (Oct 2022 – May 2024). Every track is scored on the four things that "
    "decide whether it is worth entering: **demand, pay, competition and how hard it "
    "is to get in.**"
)
filter_summary(filters, len(market), len(all_jobs))

# ---------------------------------------------------------------------------
# KPI row - the hero numbers. No chart needed: these are single values.
# ---------------------------------------------------------------------------
st.markdown("## The market at a glance")

postings = len(market)
vacancies = int(market["vacancies"].sum())
median_salary = market["avg_salary"].median()
entry_share = market["is_entry_friendly"].mean() * 100
market_competition = (
    market_reliable["applications"].sum()
    / market_reliable["vacancies"].fillna(1).clip(lower=1).sum()
    if len(market_reliable)
    else float("nan")
)

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Job postings", f"{postings:,}")
c2.metric("Open seats", f"{vacancies:,}")
c3.metric("Median salary", money(median_salary), help="Average of the advertised band, per month")
c4.metric("Entry-friendly", f"{entry_share:.0f}%", help="Ask for 1 year of experience or less")
c5.metric(
    "Applicants per seat",
    f"{market_competition:.1f}",
    help="Market-wide competition, measured on postings up to Jun 2023",
)

# ---------------------------------------------------------------------------
# Chart 1 - horizontal bar: where the jobs are
# ---------------------------------------------------------------------------
st.markdown("## Where the openings are")

top = cats.head(15).sort_values("postings")
highlight = top["postings"].idxmax()
colours = [
    COLORS["accent"] if idx == highlight else COLORS["primary"] for idx in top.index
]

top3 = cats.head(3)
finding(
    f"<b>{top3.iloc[0]['category']}</b> and <b>{top3.iloc[1]['category']}</b> are neck and neck "
    f"at the top ({top3.iloc[0]['postings']:,} and {top3.iloc[1]['postings']:,} postings). "
    f"The three largest categories together account for "
    f"{top3['postings'].sum() / postings:.0%} of all postings — but they pay very differently: "
    f"{money(top3.iloc[0]['median_salary'])} vs {money(top3.iloc[2]['median_salary'])} median. "
    "<i>Shares overlap because a job can sit in up to three categories.</i>"
)

fig = go.Figure(
    go.Bar(
        x=top["postings"],
        y=top["category"],
        orientation="h",
        marker=dict(color=colours, cornerradius=4),
        customdata=top[["median_salary", "vacancies"]],
        hovertemplate=(
            "<b>%{y}</b><br>Postings: %{x:,}<br>"
            "Seats: %{customdata[1]:,.0f}<br>"
            "Median salary: $%{customdata[0]:,.0f}<extra></extra>"
        ),
        text=[f"{v:,}" for v in top["postings"]],
        textposition="outside",
        textfont=dict(color=COLORS["text_secondary"], size=11),
    )
)
fig.update_layout(
    title="Top 15 categories by number of postings",
    xaxis_title="Job postings",
    yaxis_title=None,
    showlegend=False,
)
fig.update_xaxes(range=[0, top["postings"].max() * 1.15])
show(fig, height=520)

# ---------------------------------------------------------------------------
# Charts 2 & 3 - salary distribution, employment mix
# ---------------------------------------------------------------------------
left, right = st.columns([3, 2])

with left:
    salaries = market["avg_salary"].dropna()
    med, mean = salaries.median(), salaries.mean()
    finding(
        f"Half of all postings pay under <b>{money(med)}</b> a month. The distribution is "
        f"right-skewed, so the mean ({money(mean)}) sits above the experience of most "
        "job seekers — always quote the median."
    )
    fig = go.Figure(
        go.Histogram(
            x=salaries,
            nbinsx=60,
            marker=dict(color=COLORS["primary"], line=dict(width=0)),
            hovertemplate="$%{x:,.0f}<br>%{y:,} postings<extra></extra>",
            name="Postings",
        )
    )
    fig.add_vline(x=med, line=dict(color=COLORS["accent"], width=2))
    fig.add_vline(x=mean, line=dict(color=COLORS["neutral"], width=2, dash="dash"))
    fig.add_annotation(
        x=med, y=1.06, yref="paper", text=f"<b>median {money(med)}</b>", showarrow=False,
        font=dict(color=COLORS["accent"], size=12), xanchor="right", xshift=-4,
    )
    fig.add_annotation(
        x=mean, y=1.06, yref="paper", text=f"mean {money(mean)}", showarrow=False,
        font=dict(color=COLORS["text_secondary"], size=12), xanchor="left", xshift=4,
    )
    fig.update_layout(
        title="What Singapore jobs actually pay",
        margin=dict(t=86),
        xaxis_title="Average monthly salary (SGD)",
        yaxis_title="Postings",
        showlegend=False,
        bargap=0.02,
    )
    show(fig, height=400)

with right:
    mix = market["employment_type"].value_counts()
    top_types = mix.head(3)
    other = mix.iloc[3:].sum()
    labels = list(top_types.index) + ["All other types"]
    values = list(top_types.values) + [other]
    finding(
        f"<b>{labels[0]}</b> and <b>{labels[1]}</b> roles are "
        f"{(values[0] + values[1]) / sum(values):.0%} of the market — "
        "part-time and freelance options are marginal here."
    )
    fig = go.Figure(
        go.Pie(
            labels=labels,
            values=values,
            hole=0.55,
            sort=False,
            marker=dict(
                colors=[COLORS["primary"], "#eb6834", "#1baf7a", COLORS["neutral"]],
                line=dict(color=COLORS["surface"], width=2),
            ),
            textinfo="label+percent",
            textposition="outside",
            hovertemplate="<b>%{label}</b><br>%{value:,} postings (%{percent})<extra></extra>",
        )
    )
    fig.update_layout(title="Employment type mix", showlegend=False)
    show(fig, height=400)

# ---------------------------------------------------------------------------
# Chart 4 - monthly volume line with the partial-coverage period shaded
# ---------------------------------------------------------------------------
st.markdown("## Hiring volume over time")

monthly = (
    all_jobs.groupby("posting_month", observed=True)
    .size()
    .rename("postings")
    .reset_index()
    .sort_values("posting_month")
)
cutoff = pd.Timestamp(VOLUME_RELIABLE_START)

finding(
    "Posting volume is stable at roughly <b>75,000 per month</b> from May 2023 onwards. "
    "The ramp before that is the dataset filling up, not the job market waking up — so "
    "every trend view in this app starts at May 2023 by default."
)

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=monthly["posting_month"],
        y=monthly["postings"],
        mode="lines+markers",
        line=dict(color=COLORS["primary"], width=2),
        marker=dict(size=6),
        name="Postings per month",
        hovertemplate="%{x|%b %Y}<br>%{y:,} postings<extra></extra>",
    )
)
fig.add_vrect(
    x0=monthly["posting_month"].min(),
    x1=cutoff,
    fillcolor=COLORS["neutral"],
    opacity=0.10,
    line_width=0,
    annotation_text="partial data collection",
    annotation_position="top left",
    annotation_font=dict(color=COLORS["text_secondary"], size=11),
)
fig.update_layout(
    title="Monthly job postings, Oct 2022 – May 2024",
    xaxis_title=None,
    yaxis_title="Postings",
    showlegend=False,
)
fig.update_yaxes(rangemode="tozero")
show(fig, height=380)

caveat(
    "**Read the data honestly.** Two collection artefacts shape everything in this app: "
    "(1) months before May 2023 are only partially collected; (2) view and application "
    "counters stop accumulating for postings after Jun 2023, so all competition metrics "
    "are computed on the Oct 2022 – Jun 2023 window (203,702 postings) and labelled as such."
)

st.markdown("---")
st.markdown(
    "#### Where to go next\n"
    "- **Career Explorer** — drill into one category: pay by seniority, real job titles, who is hiring.\n"
    "- **Pay & Progression** — what each extra year of experience is worth, and where the ceilings are.\n"
    "- **Demand vs Competition** — the four-quadrant map of easy-to-enter vs crowded tracks.\n"
    "- **Skills** — which title keywords carry a salary premium.\n"
    "- **Career Recommender** — ⭐ enter your experience and priorities, get a ranked shortlist.\n"
    "- **Trends** — how each category has moved month by month."
)
