"""Career Compass SG - page 2: Career Explorer (the drill-down)."""

from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

from utils import (
    apply_filters,
    category_summary,
    filter_signature,
    filter_summary,
    finding,
    load_jobs,
    money,
    page_setup,
    reliable_subset,
    show,
    sidebar_filters,
    unique_jobs,
)

from config import COLORS, SENIORITY_ORDER, SEQUENTIAL_SCALE  # noqa: E402

page_setup("Career Explorer")

jobs = load_jobs()
filters = sidebar_filters(jobs)
sig = filter_signature(filters)
view = apply_filters(jobs, filters)
reliable = reliable_subset(jobs, filters)
cats = category_summary(view, reliable, sig)
market = unique_jobs(view, sig)

st.title("🔍 Career Explorer")
st.markdown(
    "Pick a category and see what a career in it actually looks like: what it pays at "
    "each level, which job titles are really being advertised, and who is doing the hiring."
)
filter_summary(filters, len(market), len(unique_jobs(jobs, ("unfiltered",))))

# ---------------------------------------------------------------------------
# Category picker
# ---------------------------------------------------------------------------
options = cats["category"].tolist()
default = "Information Technology" if "Information Technology" in options else options[0]
chosen = st.selectbox(
    "Career category",
    options=options,
    index=options.index(default),
    format_func=lambda c: f"{c}  ({cats.loc[cats['category'] == c, 'postings'].iloc[0]:,} postings)",
)

sub = view[view["category"] == chosen]
sub_jobs = unique_jobs(sub, sig + (chosen,))
row = cats[cats["category"] == chosen].iloc[0]

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Postings", f"{int(row['postings']):,}")
c2.metric("Median salary", money(row["median_salary"]))
c3.metric("Top-quartile pay", money(row["p75_salary"]), help="75th percentile of the salary band")
c4.metric("Entry-friendly", f"{row['entry_friendly_share']:.0f}%", help="≤ 1 year experience")
c5.metric(
    "Applicants per seat",
    "n/a" if row["apps_per_vacancy"] != row["apps_per_vacancy"] else f"{row['apps_per_vacancy']:.1f}",
    help="Measured on postings up to Jun 2023",
)

# ---------------------------------------------------------------------------
# Chart 1 - box plot: pay by seniority inside this category
# ---------------------------------------------------------------------------
st.markdown("## What it pays at each level")

present = [s for s in SENIORITY_ORDER if s in sub_jobs["seniority"].unique()]
entry_med = sub_jobs.loc[sub_jobs["seniority"] == present[0], "avg_salary"].median() if present else None
top_med = sub_jobs.loc[sub_jobs["seniority"] == present[-1], "avg_salary"].median() if present else None

if entry_med and top_med:
    finding(
        f"In <b>{chosen}</b>, moving from {present[0]} to {present[-1]} is worth "
        f"<b>{money(top_med - entry_med)} a month</b> "
        f"({top_med / entry_med:.1f}× the entry median). The boxes also widen as you go up: "
        "at senior levels the same job title can pay very different money, so negotiation "
        "matters more than it does at entry level."
    )

fig = go.Figure()
for level in present:
    values = sub_jobs.loc[sub_jobs["seniority"] == level, "avg_salary"].dropna()
    fig.add_trace(
        go.Box(
            y=values,
            name=level,
            marker=dict(color=COLORS["primary"], size=3),
            line=dict(width=1.5),
            fillcolor="rgba(42,120,214,0.18)",
            boxpoints=False,
            hovertemplate=(
                f"<b>{level}</b><br>median $%{{median:,.0f}}<br>"
                "q1 $%{q1:,.0f} · q3 $%{q3:,.0f}<extra></extra>"
            ),
        )
    )
fig.update_layout(
    title=f"Salary distribution by seniority — {chosen}",
    yaxis_title="Average monthly salary (SGD)",
    xaxis_title=None,
    showlegend=False,
)
fig.update_yaxes(rangemode="tozero")
show(fig, height=420)

# ---------------------------------------------------------------------------
# Chart 2 - heatmap: every category x seniority, with this one highlighted
# ---------------------------------------------------------------------------
st.markdown("## How this category compares with the rest of the market")

heat = (
    view.pivot_table(
        index="category", columns="seniority", values="avg_salary", aggfunc="median", observed=True
    )
    .reindex(columns=[s for s in SENIORITY_ORDER if s in view["seniority"].unique()])
)
order = cats.set_index("category").loc[heat.index, "postings"].sort_values(ascending=False)
heat = heat.loc[order.index].head(20).iloc[::-1]

finding(
    "Read this as a career map: rows are categories, columns are levels, colour is median pay. "
    "The pay ladder is far steeper in some categories than others — a Management role in one "
    "category can pay less than a Mid-level role in another."
)

fig = go.Figure(
    go.Heatmap(
        z=heat.values,
        x=heat.columns.astype(str),
        y=heat.index.astype(str),
        colorscale=SEQUENTIAL_SCALE,
        hovertemplate="<b>%{y}</b><br>%{x}: $%{z:,.0f}<extra></extra>",
        colorbar=dict(title=dict(text="Median<br>salary", side="top"), tickprefix="$", thickness=14),
        xgap=2,
        ygap=2,
    )
)
fig.update_layout(
    title="Median salary by category and seniority (top 20 categories by volume)",
    xaxis_title=None,
    yaxis_title=None,
    margin=dict(l=10, t=64, b=30),
)
show(fig, height=640)

# ---------------------------------------------------------------------------
# Charts 3 & 4 - the real job titles, and who is posting them
# ---------------------------------------------------------------------------
left, right = st.columns(2)

with left:
    st.markdown("## The jobs behind the category")
    titles = (
        sub_jobs.dropna(subset=["title_clean"])
        .groupby("title_clean", observed=True)
        .agg(postings=("avg_salary", "size"), median_salary=("avg_salary", "median"))
        .sort_values("postings", ascending=False)
        .head(15)
        .iloc[::-1]
        .reset_index()
    )
    if len(titles):
        finding(
            f"The single most advertised title in {chosen} is "
            f"<b>{titles.iloc[-1]['title_clean']}</b> "
            f"({int(titles.iloc[-1]['postings']):,} postings, median "
            f"{money(titles.iloc[-1]['median_salary'])})."
        )
        fig = go.Figure(
            go.Bar(
                x=titles["postings"],
                y=titles["title_clean"],
                orientation="h",
                marker=dict(color=COLORS["primary"], cornerradius=4),
                customdata=titles[["median_salary"]],
                hovertemplate="<b>%{y}</b><br>%{x:,} postings<br>"
                "Median: $%{customdata[0]:,.0f}<extra></extra>",
            )
        )
        fig.update_layout(
            title=f"Most advertised job titles — {chosen}",
            xaxis_title="Postings",
            yaxis_title=None,
            showlegend=False,
        )
        show(fig, height=460)
        st.caption(
            "Titles are standardised: marketing noise, bracketed skill lists and embedded "
            "salaries are stripped, so these count roles rather than adverts."
        )

with right:
    st.markdown("## Who is posting these jobs")
    companies = (
        sub_jobs.groupby("company", observed=True)
        .agg(
            postings=("avg_salary", "size"),
            median_salary=("avg_salary", "median"),
            seats=("vacancies", "sum"),
        )
        .sort_values("postings", ascending=False)
        .head(15)
        .reset_index()
    )
    finding(
        "Most high-volume posters are <b>recruitment agencies</b>, not the employer you would "
        "actually work for. Treat this as a map of where to send a CV, not a ranking of the "
        "best companies."
    )
    display = companies.copy()
    display.columns = ["Poster", "Postings", "Median salary", "Seats"]
    display["Median salary"] = display["Median salary"].map(money)
    display["Seats"] = display["Seats"].fillna(0).astype(int)
    st.dataframe(
        display,
        use_container_width=True,
        hide_index=True,
        height=460,
        column_config={
            "Postings": st.column_config.ProgressColumn(
                "Postings",
                format="%d",
                min_value=0,
                max_value=int(companies["postings"].max()) if len(companies) else 1,
            )
        },
    )
