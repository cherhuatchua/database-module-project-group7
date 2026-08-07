# Challenges and Learnings
**🏆Challenge 1: A data quality trap that would have inverted our conclusions.**\
The engagement break (Jun 2023) was invisible in summary statistics and only appeared when we plotted over time.\
Had we trusted them, the market would have looked uncontested everywhere and the recommender would have sent
users into the most crowded tracks.\
**🧠Learning: Plot every metric against time before trusting it, even when there is no reason for suspicion.**\
<br>&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;![alt text](image-1.png)
<br><br><br>

**🏆Challenge 2: The double-counting bug we shipped to ourselves.**\
Double-counting bug caused by exploding categories, leading to plausible but incorrect reporting of postings and median values.\
Exploding categories turns 1.04M postings into 1.77M rows.\
Our first overview page reported 1.66M postings and a $3,750 median — both wrong, and both plausible enough that nobody would have questioned them.\
Fixed by adding an integer job_key and routing every market-level statistic through a de-duplication step.\
**🧠Learning: When one row means two different things in two tables, make the distinction structural rather than remembered.**\
<br>&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;![alt text](image-2.png)
<br><br><br>

**🏆Challenge 3: An unlisted trap in .duplicated()**\
The .duplicated() function reported duplicate job IDs that were actually just repeated blanks.\
It reported 289 duplicate job ids in our sample. All 289 were repeated blanks.\
**🧠Learning: Use .dropna() before .duplicated() and verify what a suspicious count is actually composed of before acting.**\
<br>&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;![alt text](image-3.png)
<br><br><br>

**🏆Challenge 4: Performance on 1M rows.**\
Unusable dashboard performance on 1M rows caused by naively re-reading CSV files per interaction due to memory constraints.\
Parquet format to dramatically reduce read/write times and file size compared to CSV, and caching `st.cache_data` keeps the active working memory usage low and made UI interactions much faster.\
**🧠Learning: Use Parquet, categorical dtypes, and caching `@st.cache_data` to reduce memory footprint (to 170MB) and latency (0.06s) for live filtering.**\
<br>&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;![alt text](image-4.png)
<br><br><br>

**🏆Challenge 5: Restraint in the charts.**\
Our first opportunity map labelled all 43 categories and was unreadable.\
Cutting to nine labels made the point immediately.\
**🧠Learning: A chart's job is one sentence; anything not serving that sentence is noise.**\
<br>&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;![alt text](image-5.png)
<br><br><br><br>

# Next Steps
'1. Skills are inferred from job titles, since the dataset has no skills field. Parsing job descriptions would turn a keyword proxy into a real skills taxonomy.

'2. Resolve agencies to real employers, so "who is hiring" reflects employers rather than recruiters.

'3. A saved user profile and alerts — the natural product step from a dashboard to a system: store the user's
weights and notify them when a track's score moves.

'4. A fresher, single-pass extract would remove the engagement-window restriction entirely and let competition be measured across the full period.