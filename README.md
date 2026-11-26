# JobVision Job Market Analysis

## 1. Project description

This project analyzes about **364,838 job ads (43 columns)** published by JobVision, one of Iran's largest job websites. We act as a data team and turn the ads into decisions for business owners, HR managers, job seekers and policymakers: how much to pay, when to post, and what to ask for in an ad.

The analysis has four parts:

| Part | Topic |
|---|---|
| A | Cleaning, feature building and first exploration (EDA) |
| B | Time, location and industry analysis |
| C | Salary modeling and what drives pay |
| D | Clustering job titles and employers |

Final deliverables: a PDF report, a 15-minute presentation (PDF), and this repository.

## 2. Dataset source and license

- **Source:** [JobVision/JobVision_Jobposts_Dataset](https://huggingface.co/datasets/JobVision/JobVision_Jobposts_Dataset) on Hugging Face
- **Publisher:** JobVision
- **Period:** March 2022 to March 2024 (month-level only)
- **License:** **CC BY-NC 4.0**. Non-commercial use is allowed, and **attribution to JobVision is required**.

The raw data is **not** stored in this repository. See section 5 for how to get it.

## 3. Folder structure

```
JobVision-Jobposts-Data-Analysis/
├── README.md
├── requirements.txt
├── pyproject.toml          # makes src/ importable in notebooks
├── download_data.py        # downloads the raw data and converts it to parquet
├── data/
│   ├── raw/                # original CSV (ignored by git)
│   ├── interim/            # raw parquet and temporary files (ignored by git)
│   └── processed/          # cleaned data saved as parquet
├── notebooks/              # 00 to 15, the story of the analysis
├── src/                    # reusable code: config, parsers, cleaning, plots, date tools
├── outputs/
│   ├── figures/
│   └── tables/
├── docs/                   # data dictionary and project notes
├── report/
└── presentation/
```

## 4. Environment setup

**Python version:** `3.12`
```bash
# 1. Clone the repository
git clone https://github.com/Abolfazl-Moradi006/JobVision-Jobposts-Data-Analysis.git
cd JobVision-Jobposts-Data-Analysis

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install the exact library versions
pip install -r requirements.txt

# 4. Install the project code (makes `src/` importable from every notebook)
pip install -e .
```

Everyone must use the versions in `requirements.txt`. When you add a library, pin its version and update the file in your Pull Request.

**Troubleshooting:** if a notebook shows `ModuleNotFoundError: No module named 'src'`, run `pip install -e .` from the project root in the same environment your Jupyter kernel uses, then restart the kernel.

## 5. How to download the data

From the project root, run:

```bash
python download_data.py
```

The script:
1. Uses a CSV already in `data/raw/` if there is one, otherwise downloads from Hugging Face.
2. Converts it to parquet in `data/interim/jobposts_raw.parquet`.
3. Checks that the data has about 364,838 rows and 43 columns.

It is safe to run twice: steps that are already done are skipped.

**If the download fails:** get the CSV from the Hugging Face page, place it in `data/raw/`, and run the script again.

## 6. How to run the notebooks

Make sure you ran `pip install -e .` (section 4), then run `download_data.py` and open the notebooks in order. Shared settings (paths, `RANDOM_STATE = 42`) come from `src/config.py`.

| Step | Notebook | Needs | Produces |
|---|---|---|---|
| 0 | `download_data.py` | internet or CSV in `data/raw/` | `data/interim/jobposts_raw.parquet` |
| 1 | `00_data_inspection` | raw parquet | data dictionary, first cleaned parquet |
| 2 | `01_missing_values` | cleaned parquet | missing-value tables, salary-hiding tests |
| 3 | `02_feature_engineering` | cleaned parquet | feature table, mapping dictionaries |
| 4 | `03_income_per_hour` | feature table | `Income_Per_Hour` index |
| 5 | `04_distributions_relationships` | feature table | distributions, outliers, correlations |
| 6 | `05_seasonality` | feature table | monthly and seasonal patterns |
| 7 | `06_wage_dynamics_inflation` | feature table, price index | real-wage analysis |
| 8 | `07_geography` | feature table | province analysis |
| 9 | `08_industry_job_sectors` | feature table | industry by job-category tables |
| 10 | `09_salary_modeling` | feature table | salary models, variable ranking |
| 11 | `10_gender` | feature table | gender tests and regression |
| 12 | `11_sector_share_change` | feature table | growing and shrinking sectors |
| 13 | `12_education_vs_experience` | feature table | degree vs experience value |
| 14 | `13_peak_income_age` | feature table | peak-pay age curves |
| 15 | `14_job_clustering` | feature table | job-title clusters |
| 16 | `15_employer_clustering_optional` | feature table | employer types |

*(Update the "Needs" and "Produces" columns as the notebooks are finished.)*

## 7. Main findings

*To be filled in when the analysis is finished.*

- Part A: ...
- Part B: ...
- Part C: ...
- Part D: ...

## 8. Limitations

- **No hiring outcomes.** The data has no information about who was hired, how long hiring took, or how many people applied. We describe market practice, not what "works".
- **Offered ranges, not actual pay.** Salaries are what employers advertise.
- **Hidden salaries are not random.** Many ads hide their salary, so salary results describe only ads that show it.
- **Employer requirements, not worker facts.** Gender and age columns show what employers ask for, not who gets the job.
- **Short period.** About 25 months is too short to claim long-term trends or formal seasonality.
- **No company ID.** Employers cannot be grouped, so employer clustering is done on ad rows.
- **Calendar mismatch.** The data uses Gregorian months, so the match with Jalali months is approximate.

## 9. Team workflow

- One branch per issue, named like `issue-3-missing-values`.
- Changes go into `main` through a Pull Request, reviewed by at least one teammate.
- Never commit raw data or large files.

## 10. Credits

Dataset by **JobVision**, released under CC BY-NC 4.0.