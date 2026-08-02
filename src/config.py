"""
Career Compass SG - central configuration.

Every magic number, mapping and colour used by the ETL, the notebook and the
dashboard lives here, so a reviewer can audit our cleaning decisions in one
file instead of hunting through the code.
"""

from pathlib import Path

# --------------------------------------------------------------------------
# Paths
# --------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_CSV = PROJECT_ROOT / "SGJobData.csv"
DATA_DIR = PROJECT_ROOT / "data"
PROCESSED_DIR = DATA_DIR / "processed"
REPORTS_DIR = PROJECT_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"

# ETL outputs
JOBS_PARQUET = PROCESSED_DIR / "jobs_clean.parquet"          # one row per job posting
JOBS_CATEGORY_PARQUET = PROCESSED_DIR / "jobs_by_category.parquet"  # one row per job x category
SKILLS_PARQUET = PROCESSED_DIR / "jobs_by_skill.parquet"     # one row per job x skill
QUALITY_REPORT = PROCESSED_DIR / "data_quality_report.json"  # audit trail of the cleaning

# Aggregate outputs (what the dashboard actually reads)
AGG_CATEGORY = PROCESSED_DIR / "agg_category.parquet"
AGG_CATEGORY_SENIORITY = PROCESSED_DIR / "agg_category_seniority.parquet"
AGG_MONTHLY = PROCESSED_DIR / "agg_monthly.parquet"
AGG_SKILL = PROCESSED_DIR / "agg_skill.parquet"
AGG_TITLE = PROCESSED_DIR / "agg_title.parquet"
AGG_COMPANY = PROCESSED_DIR / "agg_company.parquet"
AGG_EXPERIENCE = PROCESSED_DIR / "agg_experience.parquet"
CAREER_TRACKS = PROCESSED_DIR / "career_tracks.parquet"      # the recommender's scoring table

# --------------------------------------------------------------------------
# Load settings
# --------------------------------------------------------------------------
CHUNK_SIZE = 200_000          # rows per chunk; ~6 chunks for the 1.05M row file
SAMPLE_ROWS = 50_000          # the "taste a spoonful" sample used in the notebook

# Columns dropped at load time and why (documented in the report)
DROP_COLUMNS = {
    "occupationId": "100% null across all 1,048,864 rows - carries no information",
    "status_id": "redundant numeric duplicate of status_jobStatus",
}

USE_COLUMNS = [
    "categories",
    "employmentTypes",
    "metadata_expiryDate",
    "metadata_isPostedOnBehalf",
    "metadata_jobPostId",
    "metadata_newPostingDate",
    "metadata_originalPostingDate",
    "metadata_repostCount",
    "metadata_totalNumberJobApplication",
    "metadata_totalNumberOfView",
    "minimumYearsExperience",
    "numberOfVacancies",
    "positionLevels",
    "postedCompany_name",
    "salary_maximum",
    "salary_minimum",
    "salary_type",
    "status_jobStatus",
    "title",
    "average_salary",
]

# --------------------------------------------------------------------------
# Cleaning thresholds - the "impossible value" rules (Lesson 1.8 Part 2.3)
# --------------------------------------------------------------------------
SALARY_FLOOR = 500        # below this a monthly SGD salary is a data-entry error, not a wage
SALARY_CEILING = 60_000   # above this is almost always an annual figure typed into a monthly field
MAX_YEARS_EXPERIENCE = 40  # a 50-year requirement is a typo, not a job
MAX_VACANCIES = 500        # mass-hiring posts above this are bulk/placeholder entries
WINSOR_LOWER_Q = 0.01      # capping quantiles for salary outliers (we cap, never delete rows)
WINSOR_UPPER_Q = 0.99

# --------------------------------------------------------------------------
# Feature engineering maps
# --------------------------------------------------------------------------
# 9 raw position levels -> 5 seniority bands a job seeker actually thinks in
SENIORITY_MAP = {
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
SENIORITY_ORDER = ["Entry", "Junior", "Mid", "Senior", "Management"]

EMPLOYMENT_ORDER = [
    "Permanent",
    "Full Time",
    "Contract",
    "Part Time",
    "Temporary",
    "Internship/Attachment",
    "Freelance",
    "Flexi-work",
]

SALARY_BAND_EDGES = [0, 3000, 5000, 8000, 12000, float("inf")]
SALARY_BAND_LABELS = ["Under $3k", "$3k-5k", "$5k-8k", "$8k-12k", "$12k+"]

EXPERIENCE_BAND_EDGES = [-0.1, 0.5, 2, 5, 10, float("inf")]
EXPERIENCE_BAND_LABELS = ["No experience", "1-2 yrs", "3-5 yrs", "6-10 yrs", "10+ yrs"]

# In this extract metadata_repostCount is capped at 2 (values are only 0, 1, 2),
# so "reposted twice" would flag just 1.4% of postings. Any repost at all is the
# meaningful signal: 4.1% of postings, and they pay a median $3,500 against the
# market's $3,850 - hard to fill because they underpay.
HARD_TO_FILL_REPOSTS = 1

# --------------------------------------------------------------------------
# Trust windows - the single most important EDA finding in this project
# --------------------------------------------------------------------------
# The file is two stitched extracts. Postings from 2023-07 onwards were captured
# at (or very near) posting time, so their view and application counters never
# accumulated: mean views collapse from ~111/month to ~5/month and the share of
# postings with zero applications jumps from 18% to 79%.
#
# Consequence: DEMAND and SALARY are trustworthy across the whole file, but
# COMPETITION (applications per vacancy, apply rate) is only trustworthy on
# postings up to 2023-06-30. Every competition figure in the dashboard is
# computed on that window and labelled as such.
ENGAGEMENT_RELIABLE_END = "2023-06-30"

# Monthly posting volume also ramps up from a near-empty Oct 2022, which is a
# collection artefact rather than a hiring collapse. Trend charts mark anything
# before this date as partial coverage.
VOLUME_RELIABLE_START = "2023-05-01"

# --------------------------------------------------------------------------
# Skill dictionary - regex patterns matched against the (lower-cased) job title.
# Deliberately spans tech and non-tech so the tool serves all 43 categories.
# --------------------------------------------------------------------------
SKILL_PATTERNS = {
    # --- Technology ---
    "Python": r"\bpython\b",
    "SQL": r"\bsql\b|\bmysql\b|\bpostgres",
    "Java": r"\bjava\b(?!script)",
    "JavaScript": r"\bjavascript\b|\bjs\b|\breact\b|\bangular\b|\bnode\.?js\b|\bvue\b",
    "Cloud / AWS / Azure": r"\baws\b|\bazure\b|\bgcp\b|\bcloud\b",
    "Data Analytics": r"\bdata analy|\banalytics\b|\bbusiness intelligence\b|\bpower ?bi\b|\btableau\b",
    "Data Engineering": r"\bdata engineer|\betl\b|\bbig data\b|\bhadoop\b|\bspark\b",
    "AI / Machine Learning": r"\bmachine learning\b|\bdata scien|\b(?:a\.?i\.?)\b|\bdeep learning\b|\bnlp\b",
    "Cybersecurity": r"\bcyber\b|\bsecurity engineer|\bsoc analyst\b|\binfosec\b|\bpenetration test",
    "DevOps": r"\bdevops\b|\bsre\b|\bkubernetes\b|\bdocker\b|\bci/cd\b",
    "SAP / ERP": r"\bsap\b|\berp\b|\boracle\b|\bnetsuite\b",
    "Salesforce / CRM": r"\bsalesforce\b|\bcrm\b",
    "Software Development": r"\bsoftware\b|\bdeveloper\b|\bprogrammer\b|\bfull ?stack\b|\bbackend\b|\bfrontend\b",
    "IT Support": r"\bit support\b|\bhelpdesk\b|\bhelp desk\b|\bdesktop support\b|\bservice desk\b",
    # --- Business & finance ---
    "Accounting": r"\baccount(?:ant|ing)\b|\bbookkeep|\bgl\b|\bap/ar\b",
    "Audit": r"\baudit",
    "Tax": r"\btax\b",
    "Financial Analysis": r"\bfinancial analy|\bfp&a\b|\bfinance analy",
    "Risk & Compliance": r"\brisk\b|\bcomplian|\bkyc\b|\baml\b|\bregulatory\b",
    "Excel / Reporting": r"\bexcel\b|\bms office\b|\breporting\b",
    "Project Management": r"\bproject manage|\bpmo\b|\bscrum\b|\bagile\b|\bprince2\b",
    "Business Analysis": r"\bbusiness analy|\bprocess improvement\b",
    "Sales & Business Development": r"\bsales\b|\bbusiness development\b|\baccount manager\b",
    "Digital Marketing": r"\bdigital marketing\b|\bseo\b|\bsem\b|\bsocial media\b|\becommerce\b|\be-commerce\b",
    "Customer Service": r"\bcustomer service\b|\bcustomer support\b|\bcall cent|\bcontact cent",
    "Human Resources": r"\bhr\b|\bhuman resource|\brecruit|\btalent acquisition\b|\bpayroll\b",
    "Procurement": r"\bprocurement\b|\bpurchasing\b|\bsourcing\b|\bbuyer\b",
    "Supply Chain / Logistics": r"\blogistic|\bsupply chain\b|\bwarehouse\b|\bshipping\b|\bfreight\b",
    # --- Engineering, trades, healthcare, services ---
    "Mechanical Engineering": r"\bmechanical\b|\bhvac\b|\bacmv\b",
    "Electrical Engineering": r"\belectrical\b|\bpower system|\bswitchgear\b",
    "Civil / Structural": r"\bcivil\b|\bstructural\b|\bm&e\b|\bqs\b|\bquantity survey",
    "AutoCAD / Design Software": r"\bautocad\b|\bcad\b|\bsolidworks\b|\brevit\b|\bbim\b",
    "Manufacturing / Production": r"\bproduction\b|\bmanufactur|\bassembly\b|\bfab\b|\bsemiconductor\b",
    "Quality Assurance": r"\bqa\b|\bquality (?:assurance|control|engineer)|\bqc\b|\biso\b",
    "Safety (WSH)": r"\bwsh\b|\bsafety\b|\behs\b|\bhse\b|\bworkplace safety\b",
    "Maintenance / Technician": r"\btechnician\b|\bmaintenance\b|\bfitter\b|\bmechanic\b",
    "Driving / Class 3": r"\bdriver\b|\bclass 3\b|\bclass 4\b|\bforklift\b|\bdelivery\b",
    "Nursing / Clinical": r"\bnurse\b|\bnursing\b|\bclinic|\bpatient\b|\bward\b",
    "Pharmacy / Lab": r"\bpharmac|\blaborator|\blab tech|\bassay\b",
    "Teaching / Training": r"\bteacher\b|\bteaching\b|\btutor\b|\btrainer\b|\beducat|\bcurriculum\b",
    "Culinary / F&B": r"\bchef\b|\bcook\b|\bkitchen\b|\bbarista\b|\bwaiter\b|\bwaitress\b|\bservice crew\b",
    "Retail Operations": r"\bretail\b|\bstore\b|\bcashier\b|\bmerchandis|\bboutique\b",
    "Beauty / Wellness": r"\bbeaut|\btherapist\b|\bhair\b|\bspa\b|\bnail\b|\bslimming\b",
    "Security Officer": r"\bsecurity officer\b|\bguard\b|\bauxiliary police\b",
    "Cleaning / Housekeeping": r"\bcleaner\b|\bcleaning\b|\bhousekeep|\bjanitor",
    "Admin / Secretarial": r"\badmin\b|\bsecretar|\bclerk\b|\bdata entry\b|\breceptionist\b|\bcoordinator\b",
    "Legal": r"\blegal\b|\blawyer\b|\bparalegal\b|\bcontract manage|\bconveyanc",
    "Graphic / UX Design": r"\bgraphic design|\bux\b|\bui\b|\bcreative design|\bmotion graphic",
    "Interior / Architecture": r"\binterior\b|\barchitect",
    "Bilingual (Mandarin)": r"\bmandarin\b|\bchinese speak|\bbilingual\b",
}

# --------------------------------------------------------------------------
# Career Fit Score - default weights (all four are user-adjustable in the app)
# --------------------------------------------------------------------------
DEFAULT_SCORE_WEIGHTS = {
    "demand": 0.30,         # how many openings exist
    "pay": 0.30,            # median salary of the track
    "low_competition": 0.25,  # inverse of applications per vacancy
    "accessibility": 0.15,  # share of postings you already qualify for
}
MIN_POSTINGS_FOR_TRACK = 200  # a track needs this many postings before we recommend it

# --------------------------------------------------------------------------
# Visual identity - one palette for the notebook, the report and the dashboard
# --------------------------------------------------------------------------
# Categorical slots are assigned in this fixed order and never cycled: the
# ordering itself is the colour-blind-safety mechanism (adjacent pairs are the
# ones that must stay separable). Validated on a light chart surface.
CATEGORICAL_SEQUENCE = [
    "#2a78d6",  # 1 blue
    "#eb6834",  # 2 orange
    "#1baf7a",  # 3 aqua
    "#eda100",  # 4 yellow
    "#e87ba4",  # 5 magenta
    "#008300",  # 6 green
    "#4a3aa7",  # 7 violet
    "#e34948",  # 8 red
]

# Scatter / bubble charts compare every pair at once, not just neighbours, so
# they are capped at the first three slots. Beyond that we facet or fold to
# "Other" instead of inventing a ninth hue.
CATEGORICAL_ALLPAIRS_CAP = 3

COLORS = {
    "primary": "#2a78d6",     # default single series
    "accent": "#eb6834",      # "look here" - exactly one per chart
    "positive": "#1baf7a",
    "negative": "#e34948",
    "neutral": "#8a8a86",     # context that must not shout
    "grid": "#e6e5e1",
    "surface": "#fcfcfb",
    "text": "#0b0b0b",
    "text_secondary": "#52514e",
}

# One hue, light -> dark. Used for continuous magnitude only (heatmaps, bubbles).
SEQUENTIAL_SCALE = [
    [0.00, "#cde2fb"],
    [0.25, "#86b6ef"],
    [0.50, "#3987e5"],
    [0.75, "#256abf"],
    [1.00, "#104281"],
]
# Two poles + a neutral grey midpoint, for "above vs below the market".
DIVERGING_SCALE = [
    [0.0, "#184f95"],
    [0.5, "#f0efec"],
    [1.0, "#c0342f"],
]
