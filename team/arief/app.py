# --- Part 2: Streamlit ---
from pathlib import Path  
import pandas as pd
import streamlit as st  
import plotly.express as px

st.set_page_config(page_title="Singapore Job Market Dashboard", layout="wide")  

@st.cache_data
def load_data():    
    DATA_PATH = Path(__file__).resolve().parent / "dfcopy.parquet"    
    df = pd.read_parquet(DATA_PATH)
    
    # 1. Standardize temporal parsing utilizing metadata_newPostingDate
    if "metadata_newPostingDate" in df.columns:
        df["posted_date"] = pd.to_datetime(df["metadata_newPostingDate"], errors='coerce')
    elif "metadata_postedCompany_postedDate" in df.columns:
        df["posted_date"] = pd.to_datetime(df["metadata_postedCompany_postedDate"], errors='coerce')
    else:
        df["posted_date"] = pd.to_datetime(df["metadata_createdAt"], errors='coerce')

    # 2. Map raw position levels into five standardized career segments
    position_mapping = {
        "Fresh/entry level": "Entry",
        "Non-executive": "Entry",
        "Junior Executive": "Junior",
        "Executive": "Mid",
        "Professional": "Mid",
        "Senior Executive": "Senior",
        "Manager": "Management",
        "Middle Management": "Management",
        "Senior Management": "Management",
    }
    if "positionLevels" in df.columns:
        df["seniority_level"] = df["positionLevels"].map(position_mapping).fillna("Mid")
    else:
        df["seniority_level"] = "Mid"
        
    # 3. Drop raw metadata columns safely using errors='ignore'
    columns_to_drop = [
        "categories", "metadata_isPostedOnBehalf", "metadata_jobPostId", 
        "metadata_repostCount", "metadata_totalNumberOfView", 
        "salary_maximum", "salary_minimum"
    ]
    df = df.drop(columns=[col for col in columns_to_drop if col in df.columns], errors='ignore')
    
    return df  

try:
    df = load_data()
except Exception as e:
    st.error(f"Error reading dfcopy.parquet from directory: {e}")
    st.stop()

st.title("Singapore Job Market Dashboard")  

# ---------------------------------------------------------------------------
# Global Sidebar Filters
# ---------------------------------------------------------------------------
with st.sidebar:    
    st.header("Filters")    
    category_options = sorted(df["parsed_categories"].dropna().unique())    
    selected_categories = st.multiselect(        
        "Category", category_options, default=category_options    
    )  

    employment_options = sorted(df["employmentTypes"].dropna().unique()) if "employmentTypes" in df.columns else []
    selected_employment = st.selectbox("Employment Type", ["All"] + employment_options)  

    open_only = st.checkbox("Show only open postings", value=False)  

    min_exp = int(df["minimumYearsExperience"].min()) if "minimumYearsExperience" in df.columns else 0
    max_exp = int(df["minimumYearsExperience"].max()) if "minimumYearsExperience" in df.columns else 15
    experience_range = st.slider(        
        "Minimum Years Experience", min_exp, max_exp, (min_exp, max_exp)    
    )  

# Filter operations
if selected_categories:
    df = df[df["parsed_categories"].isin(selected_categories)]
if selected_employment != "All":    
    df = df[df["employmentTypes"] == selected_employment]
if open_only and "status_jobStatus" in df.columns:    
    df = df[df["status_jobStatus"] == "Open"]
if "minimumYearsExperience" in df.columns:
    df = df[df["minimumYearsExperience"].between(*experience_range)]

# ---------------------------------------------------------------------------
# Layout Tabs
# ---------------------------------------------------------------------------
tab_overview, tab_drilldown, tab_trends, tab_recommender = st.tabs([
    "📊 Overview", 
    "🔍 Drill-Down View", 
    "📈 Time Trend View",
    "⭐ Career Recommender",
])

# Tab 1: Overview
with tab_overview:
    st.header("Overview")  
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Postings", f"{len(df):,.0f}")
    col2.metric(
        "Average Salary",
        f"${df['average_salary'].median():,.0f}" if len(df) and 'average_salary' in df.columns else "N/A",
    )
    applicants = df["metadata_totalNumberJobApplication"].sum() if "metadata_totalNumberJobApplication" in df.columns else 0
    col3.metric("Total Applications", f"{int(applicants):,.0f}")  

    st.write("---")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Top Roles Based on Categories")
        if len(df) > 0 and "parsed_categories" in df.columns:
            top_cats = df["parsed_categories"].value_counts().head(10).reset_index()
            top_cats.columns = ["Category", "Postings"]
            fig_cats = px.bar(top_cats, x="Postings", y="Category", orientation="h", template="plotly_white")
            fig_cats.update_layout(yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig_cats, use_container_width=True)
    with c2:
        st.subheader("Average Salary by Categories")
        if len(df) > 0 and "average_salary" in df.columns and "parsed_categories" in df.columns:
            cat_sal = df.groupby("parsed_categories")["average_salary"].median().reset_index()
            cat_sal.columns = ["Category", "Median Salary"]
            cat_sal = cat_sal.sort_values(by="Median Salary", ascending=False).head(10)
            fig_sal = px.bar(cat_sal, x="Median Salary", y="Category", orientation="h", template="plotly_white")
            fig_sal.update_layout(yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig_sal, use_container_width=True)

# Tab 2: Drill-Down View
with tab_drilldown:
    st.header("Drill-Down View")
    dd_level = st.selectbox("Position Level", ["All"] + sorted(df["seniority_level"].dropna().unique()))
    df_dd = df.copy()
    if dd_level != "All":
        df_dd = df_dd[df_dd["seniority_level"] == dd_level]
        
    dd_category = st.selectbox("Category Focus", ["All"] + sorted(df_dd["parsed_categories"].dropna().unique())[:100])
    if dd_category != "All":
        df_dd = df_dd[df_dd["parsed_categories"] == dd_category]
        
    st.dataframe(df_dd[["title", "parsed_categories", "seniority_level", "average_salary", "minimumYearsExperience"]].head(50), use_container_width=True)

# Tab 3: Time Trend View
with tab_trends:
    st.header("Time Trend View")
    if len(df) > 0 and "posted_date" in df.columns and not df["posted_date"].isna().all():
        df_ts = df.dropna(subset=["posted_date"]).copy()
        df_ts["Month"] = df_ts["posted_date"].dt.to_period("M").astype(str)
        ts_grouped = df_ts.groupby("Month").size().reset_index(name="Postings")
        
        fig_trend = px.line(ts_grouped, x="Month", y="Postings", title="Postings Over Time", markers=True, template="plotly_white")
        st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.info("No time trend metrics available for the filtered dataset. Verify that metadata_newPostingDate contains valid date components.") 

# Tab 4: Career Recommender
with tab_recommender:
    st.header("⭐ Career Recommender")
    st.markdown(
        "Tell us where you are and what you care about. We score all "
        f"\*\*{len(df):,.0f} career tracks\*\* (category × seniority) on four dimensions and rank them "
        "for \*you\* — with every component of the score shown, so you can disagree with it."
    )

    SENIORITY_ORDER = ["Entry", "Junior", "Mid", "Senior", "Management"]  
    st.markdown("### 1. Your situation")  

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
        options=sorted(df["parsed_categories"].dropna().unique()),
        default=[],
        placeholder="All fields — leave empty if you are exploring",
    )

    st.markdown("### 2. Customize Scoring Weights")
    st.caption("Adjust preferences below. The aggregate total must sum to exactly 100%.")
    w_col1, w_col2, w_col3, w_col4 = st.columns(4)
    with w_col1:
        w_demand = st.slider("Demand Weight (%)", 0, 100, 30, step=5) / 100.0
    with w_col2:
        w_comp = st.slider("Compensation Weight (%)", 0, 100, 35, step=5) / 100.0
    with w_col3:
        w_exp = st.slider("Experience Fit Weight (%)", 0, 100, 20, step=5) / 100.0
    with w_col4:
        w_pop = st.slider("Popularity Weight (%)", 0, 100, 15, step=5) / 100.0

    total_weight = w_demand + w_comp + w_exp + w_pop
    if not (0.99 <= total_weight <= 1.01):
        st.warning(f"⚠️ Your current allocation sums to {int(total_weight * 100)}%. Please rebalance sliders to equal exactly 100%.")

    df_rec = df.copy()
    if interests:
        df_rec = df_rec[df_rec["parsed_categories"].isin(interests)]
    if levels:
        df_rec = df_rec[df_rec["seniority_level"].isin(levels)]

    if len(df_rec) > 0 and "average_salary" in df_rec.columns:
        grouped = df_rec.groupby(["parsed_categories", "seniority_level"]).agg(
            median_salary=("average_salary", "median"),
            job_postings=("average_salary", "count"),   # to count how many posting occurence (rows)
            avg_exp=("minimumYearsExperience", "mean") if "minimumYearsExperience" in df_rec.columns else ("average_salary", lambda x: 0),
            total_apps=("metadata_totalNumberJobApplication", "sum") if "metadata_totalNumberJobApplication" in df_rec.columns else ("average_salary", lambda x: 0)
        ).reset_index()
        
        max_posts = grouped["job_postings"].max() if grouped["job_postings"].max() > 0 else 1
        max_apps = grouped["total_apps"].max() if grouped["total_apps"].max() > 0 else 1
        
        # -------------------------------------------------------------------------------------------------------------------------------------------
        # What It Does: This calculation applies a min-max relative scale to the absolute volume of job advertisements within a single career track. 
        # The category-seniority track containing the single highest concentration of vacancies (max_posts) receives a baseline score of 100%, and 
        # all other tracks are graded proportionally down to 0%.
        # -------------------------------------------------------------------------------------------------------------------------------------------   
        grouped["Demand_Score"] = (grouped["job_postings"] / max_posts) * 100
        
        # -------------------------------------------------------------------------------------------------------------------------------------------
        # What It Does: This functions as a one-sided satisficing filter. If a career track's median market salary meets or exceeds 
        # the user's input (target_salary), it receives a perfect score of 100%. If it falls short, the score degrades linearly based on how close 
        # the median pay is to the user's target threshold.
        # -------------------------------------------------------------------------------------------------------------------------------------------
        grouped["Comp_Score"] = grouped["median_salary"].apply(lambda s: 100 if s >= target_salary else (s / target_salary) * 100)
        
        # -------------------------------------------------------------------------------------------------------------------------------------------
        # What It Does: If a track's average requirement is less than or equal to the candidate's current experience level (years), it receives a 
        # 100% score. If the track demands more experience than the user possesses, it applies a sharp penalty—losing 25% for every year of missing 
        # experience, bottoming out at 0%.
        # -------------------------------------------------------------------------------------------------------------------------------------------
        grouped["Exp_Score"] = grouped["avg_exp"].apply(lambda e: 100 if e <= years else max(0, 100 - (e - years) * 25))
        
        # -------------------------------------------------------------------------------------------------------------------------------------------
        #  What It Does: This normalizes total job application volume across all domains against the single most competitive track in Singapore's 
        # job market (max_apps).
        # -------------------------------------------------------------------------------------------------------------------------------------------
        grouped["Popularity_Score"] = (grouped["total_apps"] / max_apps) * 100
        
        grouped["Score"] = (grouped["Demand_Score"] * 0.3 + grouped["Comp_Score"] * 0.35 + grouped["Exp_Score"] * 0.2 + grouped["Popularity_Score"] * 0.15)
        ranked = grouped.sort_values(by="Score", ascending=False).head(10)
        
        st.markdown("### 🎯 Recommended Career Tracks Match Matrix")
        st.dataframe(
            ranked.style.format({
                "median_salary": "SGD ${:,.0f}",
                "avg_exp": "{:.1f} yrs",
                "Score": "{:.1f}%",
                "Demand_Score": "{:.1f}%",
                "Comp_Score": "{:.1f}%",
                "Exp_Score": "{:.1f}%",
                "Popularity_Score": "{:.1f}%"
            }),
            use_container_width=True,
            hide_index=True
        )
        
        if not ranked.empty:
            top_track = ranked.iloc[0]
            st.success(f"💡 **Conclusive Recommendation:** Based on your personalized criteria weights, your optimal choice is the **{top_track['parsed_categories']}** sector at the **{top_track['seniority_level']}** level, achieving a high compatibility score of **{top_track['Score']:.1f}%** (Median Salary: SGD {top_track['median_salary']:,.0f}, Active Postings: {top_track['job_postings']}).")
    else:
        st.info("No matching configuration records available for recommendation parameters.")        
