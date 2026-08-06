# Summary of the Streamlit Job Market Dashboard

## What this script does

This script builds a Streamlit web dashboard for exploring Singapore job market data. It loads a Parquet dataset, prepares it for analysis, and presents the information through interactive charts and filters.

## Main features

- Loads job data from a local Parquet file named dfcopy.parquet.
- Parses and standardizes dates, seniority levels, and other fields for easier analysis.
- Provides sidebar filters for job category, employment type, open postings, and experience level.
- Displays a multi-tab dashboard with:
  - an overview of postings and salary trends,
  - a drill-down view for specific categories and seniority levels,
  - a time trend view showing posting volume over time,
  - a career recommender that ranks suitable career tracks based on user preferences.

## Data preparation

The code performs several preprocessing steps on a cleaned copy of the raw dataset, named dfcopy, before building the dashboard:

- Initial data cleanup includes dropping unused columns such as `occupationId`, `status_id`, and `salary_type`.
- Converts posting dates into a usable datetime format for time-based analysis.
- Handles missing and invalid values in key fields such as `positionLevels`, `average_salary`, and `minimumYearsExperience`.
- Masks unrealistic values and fills missing numeric values with medians to improve data quality.
- Parses the categories field into a cleaner `parsed_categories` column for easier grouping and filtering.
- Maps raw position levels into standardized career segments such as Entry, Junior, Mid, Senior, and Management.
- Removes unnecessary metadata columns to keep the dataset cleaner.
- Stores the cleaned dataset as dfcopy.parquet for efficient reuse in the Streamlit app.

## Dashboard sections

### Overview
- Shows total postings, median salary, and total applications.
- Visualizes the most common job categories and salary distribution.

### Drill-down view
- Allows users to inspect job listings by seniority level and category focus.
- Displays a table of relevant job titles and salary information.

### Time trend view
- Displays the number of job postings over time using a line chart.

### Career recommender
- Asks the user for experience, target salary, preferred seniority levels, and optional fields of interest.
- Scores career tracks using demand, compensation, experience fit, and popularity.
- Returns a ranked list of recommended career tracks.

## How the recommendation score is computed

The recommender evaluates each career track using four component scores:

- **Demand Score**: measures how many job postings exist for that track relative to the highest-volume track.
- **Compensation Score**: rewards tracks whose median salary meets or exceeds the user’s target salary.
- **Experience Score**: checks whether the track’s typical experience requirement is a good match for the user's background.
- **Popularity Score**: reflects how much applicant interest the track attracts compared with the most competitive track.

### The Synthesis: Weighted Balancing
The composite formula combines these scores using intentional weights:
```
Score = (Demand * 0.30) + (Compensation * 0.35) + (Experience * 0.20) + (Popularity * 0.15)
```
This structure prioritizes **Immediate Opportunity (30%)** and **Financial Viability (35%)**, while checking against **Realistic Prerequisites (20%)** and **Competitive Friction (15%)** to deliver an actionable, reliable path forward.


