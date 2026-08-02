"""Career Compass SG - page 5: Skills & Keywords."""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from utils import (
    apply_filters,
    caveat,
    filter_signature,
    finding,
    load_jobs,
    load_skills,
    money,
    page_setup,
    show,
    sidebar_filters,
    unique_jobs,
)

from config import COLORS, DIVERGING_SCALE, SEQUENTIAL_SCALE  # noqa: E402

page_setup("Skills")

jobs = load_jobs()
filters = sidebar_filters(jobs)
sig = filter_signature(filters)
market = unique_jobs(apply_filters(jobs, filters), sig)
skills_raw = load_skills()

st.title("🛠️ Skills & Keywords")
st.markdown(
    "Job titles advertise their own requirements. We match every title against a "
    "50-term dictionary spanning technology, business, the trades, healthcare and services, "
    "then ask: **which terms carry a pay premium, and which are just common?**"
)


# ---------------------------------------------------------------------------
# Filter the skill table with the same sidebar controls
# ---------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def filtered_skills(_raw: pd.DataFrame, f: dict) -> pd.DataFrame:
    mask = (_raw["posting_month"] >= f["start"]) & (_raw["posting_month"] <= f["end"])
    if f["employment"]:
        mask &= _raw["employment_type"].isin(f["employment"])
    if f["seniority"]:
        mask &= _raw["seniority"].isin(f["seniority"])
    lo, hi = f["salary"]
    if (lo, hi) != (1000, 17000):
        mask &= _raw["avg_salary"].between(lo, hi)
    return _raw[mask]


skills = filtered_skills(skills_raw, filters)
market_median = market["avg_salary"].median()

summary = (
    skills.groupby("skill", observed=True)
    .agg(
        postings=("avg_salary", "size"),
        median_salary=("avg_salary", "median"),
        entry_share=("is_entry_friendly", "mean"),
        median_years=("min_years_experience", "median"),
    )
    .reset_index()
)
summary = summary[summary["postings"] >= 300]
summary["premium_pct"] = (summary["median_salary"] / market_median - 1) * 100
summary["entry_share"] = summary["entry_share"] * 100

st.caption(
    f"**{len(skills):,}** title-to-skill matches across **{summary['skill'].nunique()}** terms, "
    f"benchmarked against the market median of **{money(market_median)}**."
)

# ---------------------------------------------------------------------------
# Chart 1 - treemap: which terms dominate the market
# ---------------------------------------------------------------------------
st.markdown("## How often each term appears")

tree = summary.sort_values("postings", ascending=False).head(30)
finding(
    f"<b>{tree.iloc[0]['skill']}</b> appears in {int(tree.iloc[0]['postings']):,} job titles — "
    f"the most common single term in Singapore hiring. Area is how many postings mention the "
    "term; colour is what those postings pay."
)

fig = go.Figure(
    go.Treemap(
        labels=tree["skill"],
        parents=[""] * len(tree),
        values=tree["postings"],
        marker=dict(
            colors=tree["median_salary"],
            colorscale=SEQUENTIAL_SCALE,
            line=dict(color=COLORS["surface"], width=2),
            colorbar=dict(
                title=dict(text="Median<br>salary", side="top"), tickprefix="$", thickness=14
            ),
        ),
        texttemplate="<b>%{label}</b><br>%{value:,}",
        hovertemplate="<b>%{label}</b><br>%{value:,} postings<br>"
        "Median: $%{color:,.0f}<extra></extra>",
        textfont=dict(size=13),
        tiling=dict(pad=2),
        root=dict(color=COLORS["surface"]),
    )
)
fig.update_layout(title="The 30 most-mentioned terms in Singapore job titles", margin=dict(t=64))
show(fig, height=560)

# ---------------------------------------------------------------------------
# Chart 2 - diverging bar: what each term is worth
# ---------------------------------------------------------------------------
st.markdown("## What each term is worth")

n_show = st.slider("Number of terms to show at each end", 5, 20, 12, key="skill_n")
ranked = summary.sort_values("premium_pct", ascending=False)
ends = pd.concat([ranked.head(n_show), ranked.tail(n_show)]).sort_values("premium_pct")

best = ranked.iloc[0]
worst = ranked.iloc[-1]
finding(
    f"A title mentioning <b>{best['skill']}</b> pays {best['premium_pct']:+.0f}% against the "
    f"market median ({money(best['median_salary'])}), while <b>{worst['skill']}</b> pays "
    f"{worst['premium_pct']:+.0f}% ({money(worst['median_salary'])}). "
    "That gap is the clearest argument in this dataset for which skills to invest in."
)

fig = go.Figure(
    go.Bar(
        x=ends["premium_pct"],
        y=ends["skill"],
        orientation="h",
        marker=dict(
            color=ends["premium_pct"],
            colorscale=DIVERGING_SCALE,
            cmid=0,
            reversescale=True,
            line=dict(width=0),
            cornerradius=4,
        ),
        customdata=ends[["postings", "median_salary", "median_years"]],
        hovertemplate="<b>%{y}</b><br>%{x:+.0f}% vs market median<br>"
        "Median: $%{customdata[1]:,.0f} · %{customdata[0]:,} postings<extra></extra>",
        text=[f"{v:+.0f}%" for v in ends["premium_pct"]],
        textposition="outside",
        textfont=dict(color=COLORS["text_secondary"], size=11),
    )
)
fig.add_vline(x=0, line=dict(color=COLORS["text_secondary"], width=1.5))
fig.update_layout(
    title=f"Salary premium against the market median of {money(market_median)}",
    xaxis_title="% above / below the market median",
    yaxis_title=None,
    showlegend=False,
)
fig.update_xaxes(range=[ends["premium_pct"].min() * 1.25, ends["premium_pct"].max() * 1.25])
show(fig, height=40 + 26 * len(ends))

# ---------------------------------------------------------------------------
# Chart 3 - premium against accessibility
# ---------------------------------------------------------------------------
st.markdown("## Pay premium versus how easy the term is to acquire")

finding(
    "The terms in the <b>upper right</b> are the interesting ones: they pay above the market "
    "<i>and</i> appear in plenty of entry-friendly postings, so you can enter without years of "
    "prior experience. The upper left pays well but is gated behind experience."
)

scatter = summary[summary["postings"] >= 500]
fig = go.Figure(
    go.Scatter(
        x=scatter["entry_share"],
        y=scatter["premium_pct"],
        mode="markers+text",
        marker=dict(
            size=scatter["postings"],
            sizemode="area",
            sizeref=2.0 * scatter["postings"].max() / (45**2),
            sizemin=5,
            color=COLORS["primary"],
            opacity=0.75,
            line=dict(color=COLORS["surface"], width=1.5),
        ),
        text=[
            s if abs(p) > 18 or e > 55 else ""
            for s, p, e in zip(scatter["skill"], scatter["premium_pct"], scatter["entry_share"])
        ],
        textposition="top center",
        textfont=dict(size=10, color=COLORS["text_secondary"]),
        customdata=scatter[["skill", "postings", "median_salary"]],
        hovertemplate="<b>%{customdata[0]}</b><br>%{x:.0f}% of postings entry-friendly<br>"
        "%{y:+.0f}% pay premium<br>%{customdata[1]:,} postings<extra></extra>",
    )
)
fig.add_hline(y=0, line=dict(color=COLORS["text_secondary"], width=1.2))
fig.update_layout(
    title="Does the term pay more, and can you get in without experience?",
    xaxis_title="% of postings that ask for ≤ 1 year of experience",
    yaxis_title="Salary premium vs market median (%)",
    showlegend=False,
)
show(fig, height=560)

caveat(
    "**These are title keywords, not verified skills.** The dataset has no skills field, so we "
    "infer requirements from the words employers put in the job title. A Python developer whose "
    "advert is titled 'Software Engineer' will not be counted under Python. Read these as "
    "*what employers advertise for*, which is exactly what a job seeker has to match, but do "
    "not read them as a complete skills census."
)
