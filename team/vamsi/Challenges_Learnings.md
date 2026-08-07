# Challenges and Learnings
**🏆Challenge 1: A data quality trap that would have inverted our conclusions**\
The engagement break at Jun 2023 was invisible in summary statistics and only appeared when we plotted the counters over time.\
Had we trusted them, the market would have looked uncontested everywhere and the recommender would have sent
users into the most crowded tracks.\
**🧠Learning: Plot every metric against time before you trust it even when you have no reason to suspect it**\
<br>

**🏆Challenge 2: The double-counting bug we shipped to ourselves**\
Exploding categories turns 1.04M postings into 1.77M rows.\
Our first overview page reported 1.66M postings and a $3,750 median — both wrong, and both plausible enough that nobody would have questioned them.\
Fixed by adding an integer job_key and routing every market-level statistic through a de-duplication step\
**🧠Learning: When one row means two different things in two tables, make the distinction structural rather than remembered**\
<br>

**🏆Challenge 3: An unlisted trap in .duplicated()**\
It reported 289 duplicate job ids in our sample. All 289 were repeated blanks\
**🧠Learning: .dropna() before .duplicated() , and check what a suspicious count is actually made of before acting on it**\
<br>

**🏆Challenge 4: Performance on 1M rows**\
Memory Constraints: Processing 1M rows repeatedly caused notebook crashes due to low memory limits in WSL
Naïvely re-reading the CSV per interaction made the dashboard unusable.\
Parquet + categorical dtypes + `@st.cache_data` brought the working set to 170 MB and interactions to 0.06 s, which is what let us keep live filtering instead of falling back to pre-computed aggregates.\
Parquet format to dramatically reduce read/write times and file size compared to CSV, and caching `st.cache_data` keeps the active working memory usage low and made UI interactions much faster.\
**🧠Learning: tbc**\
<br>

**🏆Challenge 5: Restraint in the charts**\
Our first opportunity map labelled all 43 categories and was unreadable.\
Cutting to nine labels made the point immediately\
**🧠Learning: A chart's job is one sentence; anything not serving that sentence is noise**\
<br>

**🏆Challenge 6: Multiple values in categories**\
The *categories* column contains multiple values (an array) as a single job may belong to more than one category.\
Taking 'First Category' found is the simplest, but it ignores the other categories.\
We expanded all categories so each gets its own row. While this ensures no data is lost, it increases the total row count and may result in double-counting jobs.\
**🧠Learning: Take expand all categories approach and take note during de-duplication step**\
<br>

# Next Steps
1. Skills are inferred from job titles, since the dataset has no skills field. Parsing job descriptions would turn a keyword proxy into a real skills taxonomy.
2. Resolve agencies to real employers, so "who is hiring" reflects employers rather than recruiters.
3. A saved user profile and alerts — the natural product step from a dashboard to a system: store the user's
weights and notify them when a track's score moves.
4. A fresher, single-pass extract would remove the engagement-window restriction entirely and let competition be measured across the full period.