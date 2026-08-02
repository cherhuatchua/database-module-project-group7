"""Career Compass SG - page 7: Trends over time."""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from utils import (
    apply_filters,
    caveat,
    category_summary,
    filter_signature,
    finding,
    load_jobs,
    money,
    page_setup,
    reliable_subset,
    show,
    sidebar_filters,
    unique_jobs,
)

from config import COLORS, SENIORITY_ORDER, VOLUME_RELIABLE_START  # noqa: E402

page_setup("Trends")

jobs = load_jobs()
filters = sidebar_filters(jobs)
sig = filter_signature(filters)
view = apply_filters(jobs, filters)
reliable = reliable_subset(jobs, filters)
cats = category_summary(view, reliable, sig)
market = unique_jobs(view, sig)

st.title("📈 Trends")
st.markdown(
    "A career decision is a bet on the next few years, not on last month. This page asks "
    "which fields are **growing**, which are **shrinking**, and whether pay is moving with them."
)

cutoff = pd.Timestamp(VOLUME_RELIABLE_START)
trend_view = view[view["posting_month"] >= cutoff]

# ---------------------------------------------------------------------------
# Chart 1 - growth ranking
# ---------------------------------------------------------------------------
st.markdown("## Who is hiring more, and who is hiring less")

last_month = trend_view["posting_month"].max()
recent_start = last_month - pd.DateOffset(months=5)
prior_start = last_month - pd.DateOffset(months=11)

recent = trend_view[trend_view["posting_month"] >= recent_start]
prior = trend_view[
    (trend_view["posting_month"] >= prior_start) & (trend_view["posting_month"] < recent_start)
]

growth = pd.DataFrame(
    {
        "recent": recent.groupby("category", observed=True).size(),
        "prior": prior.groupby("category", observed=True).size(),
    }
).dropna()
growth = growth[growth["prior"] >= 500]
growth["growth_pct"] = (growth["recent"] / growth["prior"] - 1) * 100
growth = growth.sort_values("growth_pct", ascending=False).reset_index()

ends = pd.concat([growth.head(10), growth.tail(10)]).sort_values("growth_pct")
colours = [COLORS["positive"] if v > 0 else COLORS["negative"] for v in ends["growth_pct"]]

finding(
    f"<b>{growth.iloc[0]['category']}</b> grew fastest — postings up "
    f"{growth.iloc[0]['growth_pct']:+.0f}% in the last six months against the six before. "
    f"<b>{growth.iloc[-1]['category']}</b> fell the most at "
    f"{growth.iloc[-1]['growth_pct']:+.0f}%. Comparing two six-month blocks rather than "
    "month-on-month keeps seasonal noise out of the answer."
)

fig = go.Figure(
    go.Bar(
        x=ends["growth_pct"],
        y=ends["category"],
        orientation="h",
        marker=dict(color=colours, cornerradius=4),
        customdata=ends[["recent", "prior"]],
        hovertemplate="<b>%{y}</b><br>%{x:+.1f}%<br>"
        "%{customdata[1]:,.0f} → %{customdata[0]:,.0f} postings<extra></extra>",
        text=[f"{v:+.0f}%" for v in ends["growth_pct"]],
        textposition="outside",
        textfont=dict(color=COLORS["text_secondary"], size=11),
    )
)
fig.add_vline(x=0, line=dict(color=COLORS["text_secondary"], width=1.5))
fig.update_layout(
    title="Six-month posting growth: the 10 fastest risers and 10 steepest fallers",
    xaxis_title="Change in postings vs the previous six months (%)",
    yaxis_title=None,
    showlegend=False,
)
span = max(abs(ends["growth_pct"].min()), abs(ends["growth_pct"].max())) * 1.3
fig.update_xaxes(range=[-span, span])
show(fig, height=620)

# ---------------------------------------------------------------------------
# Chart 2 - multi-line comparison
# ---------------------------------------------------------------------------
st.markdown("## Follow a category month by month")

options = cats["category"].tolist()
default = [c for c in [growth.iloc[0]["category"], growth.iloc[-1]["category"]] if c in options]
pick = st.multiselect(
    "Compare up to 3 categories",
    options=options,
    default=default[:3],
    max_selections=3,
    help="Three at most — beyond that the lines cross too often to read, and the palette "
    "only guarantees separability for three overlapping series.",
)

if pick:
    finding(
        "Absolute posting counts, not indexed. A category that starts small stays small here — "
        "which is the point: it shows how many jobs you could actually apply to each month."
    )
    fig = go.Figure()
    palette = [COLORS["primary"], "#eb6834", "#1baf7a"]
    for i, category in enumerate(pick):
        series = (
            trend_view[trend_view["category"] == category]
            .groupby("posting_month", observed=True)
            .size()
            .reset_index(name="postings")
            .sort_values("posting_month")
        )
        fig.add_trace(
            go.Scatter(
                x=series["posting_month"],
                y=series["postings"],
                mode="lines+markers",
                name=category,
                line=dict(color=palette[i], width=2.5),
                marker=dict(size=7),
                hovertemplate=f"<b>{category}</b><br>%{{x|%b %Y}}<br>"
                "%{y:,} postings<extra></extra>",
            )
        )
    fig.update_layout(
        title="Monthly postings by category",
        xaxis_title=None,
        yaxis_title="Postings",
        hovermode="x unified",
    )
    fig.update_yaxes(rangemode="tozero")
    show(fig, height=440)

# ---------------------------------------------------------------------------
# Chart 3 - seniority mix over time (stacked area, 100%)
# ---------------------------------------------------------------------------
st.markdown("## Is the market shifting towards junior or senior hiring?")

mix = (
    unique_jobs(trend_view, sig + ("trend",))
    .groupby(["posting_month", "seniority"], observed=True)
    .size()
    .unstack(fill_value=0)
)
mix = mix[[s for s in SENIORITY_ORDER if s in mix.columns]]
share = mix.div(mix.sum(axis=1), axis=0) * 100

first, last = share.iloc[0], share.iloc[-1]
mover = (last - first).abs().idxmax()
direction = "up" if last[mover] > first[mover] else "down"

finding(
    f"The seniority mix is broadly stable — the biggest move is <b>{mover}</b>, "
    f"{direction} from {first[mover]:.0f}% to {last[mover]:.0f}% of postings. "
    "A stable mix is good news for a career switcher: the ladder is not being pulled up."
)

fig = go.Figure()
for i, level in enumerate(share.columns):
    fig.add_trace(
        go.Scatter(
            x=share.index,
            y=share[level],
            mode="lines",
            stackgroup="one",
            name=level,
            line=dict(width=0.5, color=COLORS["surface"]),
            fillcolor=["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"][i],
            hovertemplate=f"<b>{level}</b><br>%{{x|%b %Y}}<br>%{{y:.1f}}% of postings<extra></extra>",
        )
    )
fig.update_layout(
    title="Share of postings by seniority level, month by month",
    xaxis_title=None,
    yaxis_title="% of postings",
)
fig.update_yaxes(range=[0, 100], ticksuffix="%")
show(fig, height=420)

# ---------------------------------------------------------------------------
# Chart 4 - is pay moving?
# ---------------------------------------------------------------------------
st.markdown("## Is pay moving?")

pay = (
    unique_jobs(trend_view, sig + ("trend",))
    .groupby("posting_month", observed=True)["avg_salary"]
    .median()
    .reset_index()
    .sort_values("posting_month")
)
change = pay["avg_salary"].iloc[-1] - pay["avg_salary"].iloc[0]

finding(
    f"The median advertised salary moved from {money(pay['avg_salary'].iloc[0])} to "
    f"{money(pay['avg_salary'].iloc[-1])} over the window — a change of "
    f"<b>{money(abs(change))}</b> ({change / pay['avg_salary'].iloc[0]:+.1%}). "
    "The y-axis starts at zero so the size of that move is not exaggerated."
)

fig = go.Figure(
    go.Scatter(
        x=pay["posting_month"],
        y=pay["avg_salary"],
        mode="lines+markers",
        line=dict(color=COLORS["primary"], width=2.5),
        marker=dict(size=7),
        name="Median advertised salary",
        hovertemplate="%{x|%b %Y}<br>Median: $%{y:,.0f}<extra></extra>",
    )
)
fig.update_layout(
    title="Median advertised monthly salary over time",
    xaxis_title=None,
    yaxis_title="Median monthly salary (SGD)",
    showlegend=False,
)
fig.update_yaxes(rangemode="tozero", tickprefix="$")
show(fig, height=380)

caveat(
    "**Trends start at May 2023 on this page regardless of the sidebar**, because months before "
    "that are only partially collected. A 'growth' figure that includes them would be measuring "
    "the data collection ramping up, not the job market."
)
