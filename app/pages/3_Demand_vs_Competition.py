"""Career Compass SG - page 4: Demand vs Competition."""

from __future__ import annotations

import numpy as np
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
    money,
    page_setup,
    reliable_subset,
    show,
    sidebar_filters,
    unique_jobs,
)

from config import COLORS, ENGAGEMENT_RELIABLE_END, SEQUENTIAL_SCALE  # noqa: E402

page_setup("Demand vs Competition")

jobs = load_jobs()
filters = sidebar_filters(jobs)
sig = filter_signature(filters)
view = apply_filters(jobs, filters)
reliable = reliable_subset(jobs, filters)
cats = category_summary(view, reliable, sig)
market = unique_jobs(view, sig)

st.title("🎯 Demand vs Competition")
st.markdown(
    "Plenty of openings is only half the story. A category with 100,000 postings and "
    "20 applicants per seat is a worse bet than one with 20,000 postings and 2. "
    "This page puts both on one map."
)
filter_summary(filters, len(market), len(unique_jobs(jobs, ("unfiltered",))))

caveat(
    f"**Competition is measured on postings up to {ENGAGEMENT_RELIABLE_END} only.** "
    "For postings after that date the source file's view and application counters were "
    "captured at posting time and never updated — 79% of them sit at exactly zero "
    "applications. Including them would make every category look uncontested. "
    f"The window still contains {len(reliable):,} job-category records, which is ample."
)

# ---------------------------------------------------------------------------
# Chart 1 - the quadrant map
# ---------------------------------------------------------------------------
st.markdown("## The opportunity map")

plot = cats[(cats["postings"] >= 2000) & cats["apps_per_vacancy"].notna()].copy()
x_split = plot["apps_per_vacancy"].median()
y_split = plot["postings"].median()

sweet = plot[(plot["apps_per_vacancy"] < x_split) & (plot["postings"] > y_split)].sort_values(
    "postings", ascending=False
)

finding(
    "The <b>top-left</b> quadrant is where you want to be: many openings (high up) and few "
    "applicants per seat (far left). "
    + (
        f"On the current filters that is <b>{', '.join(sweet['category'].head(3))}</b>."
        if len(sweet)
        else "No category currently sits there on these filters."
    )
    + " Bubble size is the number of open seats; colour is median pay."
)

fig = go.Figure(
    go.Scatter(
        x=plot["apps_per_vacancy"],
        y=plot["postings"],
        mode="markers+text",
        marker=dict(
            size=plot["vacancies"],
            sizemode="area",
            sizeref=2.0 * plot["vacancies"].max() / (55**2),
            sizemin=6,
            color=plot["median_salary"],
            colorscale=SEQUENTIAL_SCALE,
            line=dict(color=COLORS["surface"], width=2),
            colorbar=dict(
                title=dict(text="Median<br>salary", side="top"), tickprefix="$", thickness=14
            ),
        ),
        text=[
            c if p > plot["postings"].quantile(0.72) else ""
            for c, p in zip(plot["category"], plot["postings"])
        ],
        textposition="top center",
        textfont=dict(size=11, color=COLORS["text_secondary"]),
        customdata=plot[["category", "median_salary", "vacancies", "entry_friendly_share"]],
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>%{y:,} postings<br>"
            "%{x:.1f} applicants per seat<br>"
            "Median salary: $%{customdata[1]:,.0f}<br>"
            "Entry-friendly: %{customdata[3]:.0f}%<extra></extra>"
        ),
    )
)
fig.add_vline(x=x_split, line=dict(color=COLORS["grid"], width=1.5, dash="dot"))
fig.add_hline(y=y_split, line=dict(color=COLORS["grid"], width=1.5, dash="dot"))
# Quadrant labels are anchored to the plot frame, not to data values - on a log
# axis a data-space y would have to be given as an exponent and lands off-chart.
fig.add_annotation(
    xref="paper", yref="paper", x=0.01, y=0.99, xanchor="left", yanchor="top",
    text="<b>Best odds</b><br>many jobs, few rivals", showarrow=False, align="left",
    font=dict(color=COLORS["positive"], size=12),
)
fig.add_annotation(
    xref="paper", yref="paper", x=0.99, y=0.99, xanchor="right", yanchor="top",
    text="<b>Crowded</b><br>many jobs, many rivals", showarrow=False, align="right",
    font=dict(color=COLORS["negative"], size=12),
)
fig.update_layout(
    title="Where the openings are versus how contested they are",
    xaxis_title=f"Applicants per seat (postings up to {ENGAGEMENT_RELIABLE_END})",
    showlegend=False,
)
fig.update_yaxes(type="log", dtick=1, title="Job postings (log scale)")
show(fig, height=620)
st.caption(
    "The vertical axis is logarithmic: category sizes span two orders of magnitude, and on a "
    "linear axis the smaller half of the market would collapse onto the floor."
)

# ---------------------------------------------------------------------------
# Chart 2 - hard-to-fill roles: the employer's problem is your opening
# ---------------------------------------------------------------------------
st.markdown("## Hard-to-fill roles — the employer's problem is your opening")

hard = cats[cats["postings"] >= 2000].sort_values("hard_to_fill_share", ascending=False).head(12)
hard = hard.iloc[::-1]
repost_median = market.loc[market["is_hard_to_fill"], "avg_salary"].median()
normal_median = market.loc[~market["is_hard_to_fill"], "avg_salary"].median()

finding(
    f"<b>{hard.iloc[-1]['category']}</b> reposts {hard.iloc[-1]['hard_to_fill_share']:.1f}% of its "
    "adverts — employers there cannot fill the seats. And the reason is visible in the pay: "
    f"reposted jobs pay a median of {money(repost_median)} against {money(normal_median)} for "
    "jobs filled first time. <b>Hard-to-fill usually means underpaid, not elite.</b> "
    "Use these as leverage in a negotiation, not as a signal of prestige."
)

fig = go.Figure(
    go.Bar(
        x=hard["hard_to_fill_share"],
        y=hard["category"],
        orientation="h",
        marker=dict(color=COLORS["primary"], cornerradius=4),
        customdata=hard[["postings", "median_salary"]],
        hovertemplate="<b>%{y}</b><br>%{x:.1f}% of adverts reposted<br>"
        "%{customdata[0]:,} postings · median $%{customdata[1]:,.0f}<extra></extra>",
        text=[f"{v:.1f}%" for v in hard["hard_to_fill_share"]],
        textposition="outside",
        textfont=dict(color=COLORS["text_secondary"], size=11),
    )
)
fig.update_layout(
    title="Share of adverts that had to be reposted",
    xaxis_title="% of postings reposted",
    yaxis_title=None,
    showlegend=False,
)
fig.update_xaxes(range=[0, hard["hard_to_fill_share"].max() * 1.18])
show(fig, height=480)

# ---------------------------------------------------------------------------
# Table - the shortlist
# ---------------------------------------------------------------------------
st.markdown("## The shortlist: sizeable, well paid, and not yet crowded")

shortlist = plot.copy()
shortlist["opportunity"] = (
    np.log10(shortlist["postings"]).rank(pct=True) * 0.4
    + shortlist["median_salary"].rank(pct=True) * 0.35
    + (1 - shortlist["apps_per_vacancy"].rank(pct=True)) * 0.25
)
shortlist = shortlist.sort_values("opportunity", ascending=False).head(12)

table = shortlist[
    ["category", "postings", "median_salary", "apps_per_vacancy", "entry_friendly_share",
     "hard_to_fill_share"]
].copy()
table.columns = [
    "Category", "Postings", "Median salary", "Applicants per seat",
    "Entry-friendly %", "Reposted %",
]
table["Median salary"] = table["Median salary"].map(money)
table["Applicants per seat"] = table["Applicants per seat"].round(1)
st.dataframe(table, use_container_width=True, hide_index=True)
st.caption(
    "Ranked on a blend of demand (40%), pay (35%) and low competition (25%). "
    "The Career Recommender applies the same idea per seniority level and lets you set the weights."
)
