"""Career Compass SG - page 3: Pay & Progression."""

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

from config import COLORS, EMPLOYMENT_ORDER  # noqa: E402

page_setup("Pay & Progression")

jobs = load_jobs()
filters = sidebar_filters(jobs)
sig = filter_signature(filters)
view = apply_filters(jobs, filters)
reliable = reliable_subset(jobs, filters)
cats = category_summary(view, reliable, sig)
market = unique_jobs(view, sig)

st.title("💰 Pay & Progression")
st.markdown(
    "Two questions this page answers: **where is the money**, and **what does another "
    "year of experience actually buy you** in each field?"
)
filter_summary(filters, len(market), len(unique_jobs(jobs, ("unfiltered",))))

MIN_POSTINGS = 2000
ranked = cats[cats["postings"] >= MIN_POSTINGS].sort_values("median_salary", ascending=False)

# ---------------------------------------------------------------------------
# Chart 1 - lollipop: category pay ranking against the market median
# ---------------------------------------------------------------------------
st.markdown("## The pay ranking")

market_median = market["avg_salary"].median()
top15 = ranked.head(15).iloc[::-1]

finding(
    f"<b>{ranked.iloc[0]['category']}</b> pays the highest median in Singapore at "
    f"{money(ranked.iloc[0]['median_salary'])} — "
    f"{ranked.iloc[0]['median_salary'] / ranked.iloc[-1]['median_salary']:.1f}× the "
    f"lowest-paying sizeable category ({ranked.iloc[-1]['category']}, "
    f"{money(ranked.iloc[-1]['median_salary'])}). The dashed line is the market median of "
    f"{money(market_median)}."
)

fig = go.Figure()
for _, r in top15.iterrows():
    fig.add_trace(
        go.Scatter(
            x=[market_median, r["median_salary"]],
            y=[r["category"], r["category"]],
            mode="lines",
            line=dict(color=COLORS["grid"], width=2),
            hoverinfo="skip",
            showlegend=False,
        )
    )
fig.add_trace(
    go.Scatter(
        x=top15["median_salary"],
        y=top15["category"],
        mode="markers",
        marker=dict(size=13, color=COLORS["primary"], line=dict(color=COLORS["surface"], width=2)),
        customdata=top15[["postings", "p75_salary"]],
        hovertemplate="<b>%{y}</b><br>Median: $%{x:,.0f}<br>"
        "Top quartile: $%{customdata[1]:,.0f}<br>%{customdata[0]:,} postings<extra></extra>",
        name="Median salary",
        showlegend=False,
    )
)
fig.add_vline(x=market_median, line=dict(color=COLORS["accent"], width=2, dash="dash"))
fig.add_annotation(
    x=market_median, y=1.04, yref="paper", text=f"market median {money(market_median)}",
    showarrow=False, font=dict(color=COLORS["accent"], size=12), xanchor="center",
)
fig.update_layout(
    title=f"Best-paying categories (at least {MIN_POSTINGS:,} postings)",
    xaxis_title="Median monthly salary (SGD)",
    yaxis_title=None,
    margin=dict(t=86),
)
show(fig, height=520)

# ---------------------------------------------------------------------------
# Chart 2 - dumbbell: the salary RANGE, not just the midpoint
# ---------------------------------------------------------------------------
st.markdown("## Floor, ceiling, and the gap between them")

spread = ranked.copy()
spread["spread"] = spread["p90_salary"] - spread["p25_salary"]
widest = spread.sort_values("spread", ascending=False).head(15).iloc[::-1]

finding(
    f"A median hides the range you could actually land in. <b>{widest.iloc[-1]['category']}</b> "
    f"has the widest spread of any large category: {money(widest.iloc[-1]['p25_salary'])} at the "
    f"25th percentile against {money(widest.iloc[-1]['p90_salary'])} at the 90th — "
    f"a {money(widest.iloc[-1]['spread'])} gap between a weak and a strong offer."
)

fig = go.Figure()
for _, r in widest.iterrows():
    fig.add_trace(
        go.Scatter(
            x=[r["p25_salary"], r["p90_salary"]],
            y=[r["category"], r["category"]],
            mode="lines",
            line=dict(color=COLORS["grid"], width=6),
            hoverinfo="skip",
            showlegend=False,
        )
    )
fig.add_trace(
    go.Scatter(
        x=widest["p25_salary"], y=widest["category"], mode="markers",
        marker=dict(size=12, color=COLORS["primary"], line=dict(color=COLORS["surface"], width=2)),
        name="25th percentile (a weak offer)",
        hovertemplate="<b>%{y}</b><br>25th percentile: $%{x:,.0f}<extra></extra>",
    )
)
fig.add_trace(
    go.Scatter(
        x=widest["p90_salary"], y=widest["category"], mode="markers",
        marker=dict(size=12, color=COLORS["accent"], line=dict(color=COLORS["surface"], width=2)),
        name="90th percentile (a strong offer)",
        hovertemplate="<b>%{y}</b><br>90th percentile: $%{x:,.0f}<extra></extra>",
    )
)
fig.update_layout(
    title="Where the negotiating room is: 25th to 90th percentile salary",
    xaxis_title="Monthly salary (SGD)",
    yaxis_title=None,
)
show(fig, height=540)

# ---------------------------------------------------------------------------
# Chart 3 - experience curve with an interquartile band
# ---------------------------------------------------------------------------
st.markdown("## What a year of experience is worth")

pick = st.multiselect(
    "Compare up to 3 categories",
    options=cats["category"].tolist(),
    default=[c for c in ["Information Technology", "Healthcare / Pharmaceutical", "F&B"]
             if c in set(cats["category"])][:3],
    max_selections=3,
    help="Capped at three: a line chart with more than three series stops being readable, "
         "and the colour palette only guarantees separability for three overlapping series.",
)

curves = (
    view[view["min_years_experience"].notna()]
    .assign(years=lambda d: d["min_years_experience"].clip(upper=12).astype(int))
    .groupby(["category", "years"], observed=True)
    .agg(
        median_salary=("avg_salary", "median"),
        p25=("avg_salary", lambda s: s.quantile(0.25)),
        p75=("avg_salary", lambda s: s.quantile(0.75)),
        postings=("avg_salary", "size"),
    )
    .reset_index()
)
curves = curves[curves["postings"] >= 30]

if pick:
    lead = curves[curves["category"] == pick[0]].sort_values("years")
    if len(lead) > 1:
        gain = (lead["median_salary"].iloc[-1] - lead["median_salary"].iloc[0]) / max(
            lead["years"].iloc[-1] - lead["years"].iloc[0], 1
        )
        finding(
            f"In <b>{pick[0]}</b>, each additional year of required experience is worth about "
            f"<b>{money(gain)} a month</b> on the median — from "
            f"{money(lead['median_salary'].iloc[0])} at {int(lead['years'].iloc[0])} years to "
            f"{money(lead['median_salary'].iloc[-1])} at {int(lead['years'].iloc[-1])} years. "
            "The shaded band is the middle 50% of offers at each level of experience."
        )

    fig = go.Figure()
    palette = [COLORS["primary"], "#eb6834", "#1baf7a"]
    for i, category in enumerate(pick):
        c = curves[curves["category"] == category].sort_values("years")
        if c.empty:
            continue
        colour = palette[i]
        rgb = tuple(int(colour[j:j + 2], 16) for j in (1, 3, 5))
        fig.add_trace(
            go.Scatter(
                x=list(c["years"]) + list(c["years"])[::-1],
                y=list(c["p75"]) + list(c["p25"])[::-1],
                fill="toself",
                fillcolor=f"rgba({rgb[0]},{rgb[1]},{rgb[2]},0.13)",
                line=dict(width=0),
                hoverinfo="skip",
                showlegend=False,
            )
        )
        fig.add_trace(
            go.Scatter(
                x=c["years"],
                y=c["median_salary"],
                mode="lines+markers",
                name=category,
                line=dict(color=colour, width=2.5),
                marker=dict(size=8),
                hovertemplate=f"<b>{category}</b><br>%{{x}} yrs experience<br>"
                "Median: $%{y:,.0f}<extra></extra>",
            )
        )
    fig.update_layout(
        title="Median salary by years of experience required",
        xaxis_title="Minimum years of experience asked for",
        yaxis_title="Median monthly salary (SGD)",
        hovermode="x unified",
    )
    fig.update_yaxes(rangemode="tozero")
    show(fig, height=460)

# ---------------------------------------------------------------------------
# Chart 4 - violin: what employment type costs you
# ---------------------------------------------------------------------------
st.markdown("## The price of flexibility")

types = [t for t in EMPLOYMENT_ORDER if (market["employment_type"] == t).sum() >= 500]
perm = market.loc[market["employment_type"] == "Permanent", "avg_salary"].median()
part = market.loc[market["employment_type"] == "Part Time", "avg_salary"].median()

finding(
    f"Permanent roles pay a median of {money(perm)}; part-time roles "
    f"{money(part)} — a <b>{(1 - part / perm):.0%} discount</b> for flexibility. "
    "The shapes matter as much as the medians: contract roles have a long upper tail, "
    "so a contract is not automatically a pay cut."
)

fig = go.Figure()
for t in types:
    values = market.loc[market["employment_type"] == t, "avg_salary"].dropna()
    fig.add_trace(
        go.Violin(
            y=values,
            name=t,
            box_visible=True,
            meanline_visible=False,
            line=dict(color=COLORS["primary"], width=1.4),
            fillcolor="rgba(42,120,214,0.16)",
            points=False,
            hovertemplate=f"<b>{t}</b><br>median $%{{median:,.0f}}<extra></extra>",
        )
    )
fig.update_layout(
    title="Salary distribution by employment type",
    yaxis_title="Average monthly salary (SGD)",
    showlegend=False,
)
fig.update_yaxes(rangemode="tozero")
show(fig, height=440)
