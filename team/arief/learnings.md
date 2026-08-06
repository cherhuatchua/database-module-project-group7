### Data exploration

**1. Performance on 1M rows**

Memory Constraints: Processing 1M rows repeatedly caused notebook crashes due to low memory limits in WSL

- **Business-Driven Filtering**: Defining a clear business objective upfront helps filter out non-essential data early, reducing both memory usage and dataset noise

- **Performance optimization**: 1) Parquet format to dramatically reduce read/write times and file size compared to CSV, and 2) caching `st.cache_data` keeps the active working memory usage low and made UI interactions much faster.

**2. Multiple values in categories**

The *categories* column contains multiple values (an array) as a single job may belong to more than one category. Approches are:

- Take the **first category** found (sorted or unsorted): This is the simplest, but it ignores the other categories 

- **Expand (explode) all categories**: Extract all categories so each gets its own row. While this ensures no data is lost, it increases the total row count and may result in double-counting jobs.

*Team decision*: Take expand all categories approach and take note during de-duplication step


