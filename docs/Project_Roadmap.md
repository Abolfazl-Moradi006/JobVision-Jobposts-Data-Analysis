# JobVision Job Market Analysis: Project Roadmap

This is the plan for our final project. It explains what we have to deliver, what the data looks like, and what we do at each step, in the order we will do it.

---

## 1. The project in plain words

JobVision is one of Iran's biggest job websites. It released about **364,838 job ads** (43 columns) on Hugging Face. Our job is to act like a data team and turn those ads into advice that a business owner, an HR manager, a job seeker or a policymaker can actually use.

The final result should not be "a pile of charts". Each finding should end with a clear decision, for example: *how much should I pay, when should I post, what should I ask for in the ad?*

### What we must deliver

| # | Deliverable | What it is |
|---|---|---|
| 1 | **PDF report** | Answers every question in the same order as the brief. Includes an executive summary, a step-by-step cleaning section, charts, and a short business takeaway after each section. |
| 2 | **15-minute presentation (PDF)** | A story, not a list of answers. We choose the best findings and may add new analysis. |
| 3 | **GitHub repo** | All notebooks and scripts, `requirements.txt`, and a README that explains the run order. Anyone must be able to repeat our results. |

### The questions at a glance

| Part | Topic | Number of tasks |
|---|---|---|
| A | Cleaning, feature building, first exploration (EDA) | 4 |
| B | Modeling, trends and comparisons | 9 |
| C | Clustering, skills network, advice for business owners | 3 + 2 bonus + 1 |

---

## 2. What the data dictionary tells us

Now that we have seen the dictionary, here are the facts that shape the whole plan.

### 2.1 Key facts

- **Time range:** March 2022 to March 2024, given as a `YYYY-MM` text in `Jobpost_ActivationTime_YEAR_MONTH`. That is the Gregorian calendar, and we only have the **month**, not the exact day. So we can do monthly analysis, but not weekly or daily.
- **The brief says "years 1402 and 1403"**, but the data actually covers roughly Persian years 1401, 1402 and the very start of 1403. We trust the data and check this early.
- **Salary:** `Jobpost_MinSalary` is between 2 and 70, and `Jobpost_MaxSalary` between 3 and 100. These are almost certainly **millions of Toman per month**. We must verify this before any money analysis.
- **No company ID.** Company names are removed, so we cannot group ads by employer. Employer clustering has to be done on ad rows.
- **`RowNumber` is not a real post ID.** It is just a row counter.
- **Education is hidden inside JSON.** There is no simple "education level" column. We must read `DegreeLevel` from `Jobpost_AcademicFields`.
- **Skills are JSON text.** Software skills and language skills need parsing before use.
- **Possible duplicates.** Some companies post the same role many times.
- **A typo in the source:** the column is called `Comany_CompanyOwnershipTypesFa` (not "Company").
- **License:** CC BY-NC 4.0. Non-commercial use is fine, but we must credit JobVision. We will add this to the README.

### 2.2 Brief names vs real column names

| In the brief | Real column in the data |
|---|---|
| Min / max age | `Jobpost_RequiredMinAge`, `Jobpost_RequiredMaxAge` |
| Experience | `Jobpost_RequiredExperienceYears` |
| Gender | `Jobpost_PreferredGender` (5 values: no preference, male only, female only, male preferred, female preferred) |
| Employment type | `Jobpost_WorkTypeEn` (Full Time, Part Time, Full Time Or Part Time, Project-based) |
| Working hours | `Jobpost_CompanyWorkTimesDescription` (free Persian text) |
| Education level | Inside `Jobpost_AcademicFields` (`DegreeLevel`) |
| Skills | `Jobpost_SoftwareSkills`, `Jobpost_LanguageSkills` |
| Job sector | `Jobpost_MainJobCategory` (77 values) |
| Industry | `Jobpost_IndustryEn` (44 values) |
| Province | `Jobpost_ProvinceEn` (32 values) |
| Company size / age / ownership | `Company_SizeEn`, `Company_AgeFromEstablishmentYear`, `Company_CompanyOwnershipTypesEn` |
| Benefits | `Jobpost_BenefitEn` (comma-separated) |
| Remote work | `Jobpost_IsRemote` |
| Salary shown or "negotiable" | `Jobpost_SalaryCanBeShown` |

### 2.3 What the data cannot tell us

We keep this list in mind and mention it in the report:

- No information about **who was hired**, how long hiring took, or how many people applied. So we can describe market practice, but we cannot prove that a tactic "works".
- Salaries are **offered ranges**, not actual pay.
- Gender and age columns are **what the employer asks for**, not who gets the job.
- Only **about 25 months** of data. That is too short to claim long-term trends.
- Many salaries are missing, and the missing ones may not be random.

---

## 3. Repository structure

```
jobvision-labor-market/
├── README.md
├── requirements.txt
├── download_data.py        # downloads the raw data, so we never commit it
├── data/
│   ├── raw/                # ignored by git
│   ├── interim/
│   └── processed/          # cleaned data saved as parquet
├── notebooks/
│   ├── 00_data_inspection.ipynb
│   ├── 01_missing_values.ipynb
│   ├── 02_feature_engineering.ipynb
│   ├── 03_income_per_hour.ipynb
│   ├── 04_distributions_correlations.ipynb
│   ├── 05_salary_modeling.ipynb
│   ├── 06_time_series_seasonality.ipynb
│   ├── 07_inflation_sector_dynamics.ipynb
│   ├── 08_gender_education_age.ipynb
│   ├── 09_geography.ipynb
│   ├── 10_global_comparison.ipynb
│   ├── 11_job_clustering.ipynb
│   ├── 12_employer_clustering_bonus.ipynb
│   ├── 13_skill_network_bonus.ipynb
│   └── 14_business_recommendations.ipynb
├── src/                    # reusable code (parsers, cleaning, plots, date tools)
├── outputs/
│   ├── figures/
│   └── tables/
├── report/
└── presentation/
```

### Working rules

1. **Reusable code goes in `src/`.** Notebooks should mostly tell the story and call functions from `src/`.
2. **Fix the random seed** (`random_state=42`) everywhere.
3. **Save data as parquet**, not CSV. It is faster and keeps data types.
4. **Never upload the raw data.** `download_data.py` fetches it.
5. **Save every figure and key number to `outputs/`** as we go, so writing the report later is easy.

---

## 4. The plan, phase by phase

### Phase 0: Setup and getting to know the data

**Goal:** have a clean working environment and understand every column.

1. Create the environment with: pandas, numpy, scipy, statsmodels, scikit-learn, matplotlib, seaborn, plotly, networkx, kmodes, gower, jdatetime, pyarrow, arabic-reshaper, python-bidi, hazm (Persian text tools) and umap-learn.
2. Write `download_data.py`, download the dataset, and save it as parquet.
3. Check the shape. We expect **364,838 rows and 43 columns**.
4. **Build our own data dictionary** (type, meaning, missing %, notes). Start from the provided one and add what we discover. This becomes an appendix in the report.
5. **Fix Persian text problems** before anything else:
   - Arabic vs Persian letters (ي → ی, ك → ک)
   - Persian vs English digits (۱ vs 1)
   - Zero-width non-joiner and extra spaces
   - If we skip this, the same category gets split into several groups without us noticing.
6. **Build the date tools.** Convert `YYYY-MM` into a proper date, and also into a Persian (Jalali) month using `jdatetime`. Because we only know the month, the match between Gregorian and Persian months is approximate, and we will say so.
7. **Remove duplicates carefully.** Check how many rows are identical on title, company attributes and month. Decide whether to drop them, and report the count.
8. **Decide on chart language.** English labels on charts are the safest. If we want Persian labels, we need `arabic-reshaper`, `bidi` and a Persian font (for example Vazirmatn), and the PDF tool must support it. We decide this now, not at the end.

**Output:** `00_data_inspection.ipynb`, the data dictionary, and a first cleaned parquet file.

---

### Phase 1: Cleaning, features and exploration (Part A)

#### A1. Missing values and the "negotiable salary" problem

**What we do**

- Count missing values and the percentage per column. Show them in a sorted bar chart and a missing-data map.
- Split missing values into two kinds:
  - **Not applicable** (for example, no software skills needed), and
  - **Truly missing** (information the ad should have had).
- Look at `Jobpost_SalaryCanBeShown`. Note that ads can be `False` (salary hidden) and also have empty salary values. Check how these two relate.
- Test if hiding the salary is random:
  - Chi-square test plus **Cramér's V** against province, company size, job category, industry and period.
  - A **logistic regression** that predicts "salary hidden", with odds ratios and AUC.

**What we conclude**

If hiding depends on things like company size or province, then the missing salaries are **not random**. That means every later salary result describes only the ads that show their salary. We repeat this warning wherever salary is used.

#### A2. Turning text into numbers (feature engineering)

| Raw column | What we create | Method |
|---|---|---|
| `Jobpost_AcademicFields` (JSON) | Required degree level: associate, bachelor, master, etc. When several are listed, we use the **lowest accepted** level (and also keep the highest). Also a "field of study" group. | Parse JSON, then **ordinal encoding** |
| `Jobpost_SoftwareSkills` (JSON) | List of skills, number of skills, skill level, and a 0/1 table for the top N skills (use the English name) | Parse JSON, multi-hot |
| `Jobpost_LanguageSkills` (JSON) | Has English required, English level (10% to 90%), number of languages | Parse JSON, map to numbers |
| `Jobpost_WorkTypeEn` | Employment type | **One-hot** |
| `Jobpost_PreferredGender` | Gender preference | One-hot (and a simple "female-only / male-only / any" version) |
| `Jobpost_CompanyWorkTimesDescription` | Weekly hours, monthly hours, night shift, Thursday off, rotating shift | Regex parser (see below) |
| `Jobpost_BenefitEn` | Number of benefits and a 0/1 table per benefit (Loan, Bonus, Insurance, ...) | Split on commas, strip spaces |
| `Jobpost_SecondaryJobCategories` | Number of extra categories | Split on commas |
| `Company_SizeEn`, `Company_AgeFromEstablishmentYear` | Ordered numbers (small to large, young to old) | **Ordinal encoding** |
| `Jobpost_MainJobCategory`, province, industry | Frequency encoding for models that need numbers, labels for grouping | Frequency encoding |
| Salary | `avg_salary = (min + max) / 2`, `salary_range_width`, `salary_disclosed` | Simple formulas |
| Boolean columns | Convert to 0/1 | Direct |

**Extra care**

- **JSON parsing:** some aliases contain commas, so we must parse the JSON properly instead of splitting on commas. Count the rows that fail to parse.
- **Salary edge cases:** if only the min or only the max exists, decide whether to use it as the average. Document the choice.
- **Mapping dictionary:** save every encoding (original value → number) as a CSV/JSON file and show it in the report. This is a required deliverable.
- **Working-hours parser:** this is the hardest and most important feature. Examples in the data look like `شنبه تا چهارشنبه 8 الی 17`. The parser must read days and hours, handle ranges and breaks, and flag odd cases. **Validate it by hand on 200 random rows** and report the success rate. Rows that cannot be parsed get a missing value, not a guess.
- **Avoid data leakage:** if we use target encoding, we do it only after splitting data into train and test.

#### A3. The `Income_Per_Hour` index

**Formula**

```
monthly_hours = weekly_hours × 4.33          (main choice)
Income_Per_Hour = avg_salary (million Toman) × 1,000,000 / monthly_hours
```

We also try a second convention (22 working days × daily hours) and compare, to show the result does not depend on this choice.

**Steps**

1. Check the salary unit first (see section 2.1).
2. Remove or flag impossible hours (below 5 or above about 100 per week). Report how many.
3. Compare Income_Per_Hour across job categories, job titles (with a minimum number of ads), experience groups and education levels.
4. **Full-time vs part-time vs project:** compare using a Mann-Whitney test and an effect size.

**Important warning:** for part-time and project jobs, the salary column may mean "per project" or "per hour", not "per month". We read some real examples before comparing, and explain what we find.

#### A4. Distributions and correlations

- Draw histograms and KDE plots for salary, hourly income, experience and age. Report **skewness and kurtosis**, on both normal and log scales.
- Find outliers with the **IQR rule** and the **modified Z-score** (on log values). We **flag** outliers with a column instead of deleting them, and compare results with and without them.
- Compute **Pearson and Spearman** correlations side by side. Where they disagree, the relationship is not a straight line.
- Check **multicollinearity** with VIF. We expect min/max salary, min/max age and experience to be strongly related.
- Show **diminishing returns** (salary vs experience, salary vs age) with binned averages and LOWESS curves.

**Output of Phase 1:** `01` to `04` notebooks, the cleaned dataset in `data/processed/`, the mapping tables, and the first set of figures.

---

### Phase 2: Modeling and time analysis (Part B)

#### B1. Salary models and what matters most

- **Target:** `log(avg_salary)`, because salaries are skewed.
- **Inputs:** job category, province, company size and age, ownership, education, experience, top skills, employment type, benefits, remote flag, hours.
- **One model per period.** The brief says "per year", but we only have 25 months. We use the following choice and explain it clearly in the report:
  - Period 1: 2022-03 to 2023-02
  - Period 2: 2023-03 to 2024-02
  - 2024-03 is a single month, so we leave it out of the models or merge it with Period 2.
- **Two model types:**
  - **OLS regression** with standardized coefficients (easy to explain), with R² and robust standard errors.
  - **Random Forest or Gradient Boosting** with permutation importance (captures non-linear effects).
- Compare the importance of each factor between periods with a **slope chart**.
- Remember: models only see ads that show their salary (selection bias).

#### B2. Seasonality (when do ads peak?)

- Count ads per month and per season, and plot them.
- We only have month-level data over 25 months, so a few months appear twice (and March appears three times: 2022, 2023, 2024). We **compare the same month across years** instead of using a heavy seasonal model.
- Find the peak months overall and in the biggest job categories.
- Explain the peaks with the Iranian calendar and economy (Nowruz slowdown, hiring after Nowruz, summer, autumn hiring, budget cycles, currency shocks). We call these **explanations that fit the timing**, not proven causes.

#### B3. Wages vs inflation

- Compute the monthly **mean and median** of offered salary.
- Compare with inflation. Take the price index from an official source (Statistical Centre of Iran or the Central Bank of Iran) and cite it. We do not use numbers from memory.
- Compute the **real wage** (nominal salary divided by the price index).
- Find categories whose salaries grew faster or slower than the market average.

#### B4. Gender

- Test salary differences by preferred gender with **Welch's t-test**, plus **Mann-Whitney** as a backup. Report effect size (Cohen's d) and confidence intervals.
- Show where gender preference is strongest across job categories and seniority levels with a heatmap.
- Run a regression that controls for category, experience and province.
- **Be clear:** this shows what employers *ask for* and *offer*, not real pay gaps between workers.

#### B5. Changing sector shares

- Count ads and compute share (%) of each job category per period (or per quarter).
- Show growth or decline in percentage points and in relative change. Use a slope or bump chart.

#### B6. Education vs experience

- Measure the salary effect of degree level (controlling for experience) and of each year of experience (controlling for education).
- Use regression with interaction terms.
- Find categories where experience clearly matters more than degree (flat degree effect, strong experience effect).

#### B7. Age and peak income

- Use the middle of the requested age range (`MinAge`, `MaxAge`) as the age value.
- Plot salary by age group and fit a **quadratic or spline** curve to find the peak.
- Compare IT, manufacturing and finance.
- **Warning:** many ads have no age limits, and ages are employer requirements, not worker ages.

#### B8. Provinces

- Count ads per province and compute Tehran's share over time.
- Find provinces that grew faster than the national average (use a minimum number of ads).
- Look for sudden jumps of a job category in a specific province using category × province share changes.
- **Note:** there are two province fields. `Jobpost_Province*` is where the job is, and `Company_Province*` is where the company is based. We use the job province, and also look at ads where the two differ.
- If we can find population data, add "ads per person".

#### B9. Iran vs the world

- Collect specific, cited findings from **Indeed Hiring Lab** and **LinkedIn Economic Graph** for 2022 to 2024 (post-COVID hiring surge, tech layoffs in 2023, stable remote work, growth in AI skills).
- Build matching measures from our data: IT share of ads over time, `Jobpost_IsRemote` share over time, and AI-related skills (keyword search such as Python, machine learning, TensorFlow in software skills and titles).
- Discuss similarities and differences, including Iranian factors (currency swings, sanctions, emigration of skilled workers).

**Output of Phase 2:** notebooks `05` to `10`, all figures, and a short written conclusion per question.

---

### Phase 3: Clustering, skills network and business advice (Part C)

#### C1. Grouping job titles

1. Use `Jobpost_MainJobCategory` or a cleaned job title, and keep titles with at least N ads.
2. Build one vector per title: TF-IDF of skills + education level + experience (scaled).
3. Reduce dimensions (TruncatedSVD), then run **K-Means**. Pick k using the elbow method, silhouette score and Calinski-Harabasz. Also try **GMM** and choose with BIC.
4. Name each cluster by its top skills and example titles. Plot with UMAP or PCA.
5. Repeat for the two periods and compare with the **Adjusted Rand Index**. List titles that moved between clusters.

#### C2. Popular job categories in each industry

- Cross-table of industry × job category, normalized by row, shown as a heatmap, plus a "top 3 per industry" table.

#### C3. Skill changes and fast-growing titles

- For titles with enough ads, compare skill frequencies between periods. List skills gained and lost.
- Find the titles with the biggest absolute jump and the biggest percentage growth. Use a **minimum ad count**, because small bases create fake huge percentages.

#### C4. Employer profiles (bonus)

- Features: company size, age, ownership, industry, province, salary-disclosure rate, number of benefits.
- There is no company ID, so we cluster **ad rows** and call the result "employer types". Or we group by a combination of company traits to approximate employers, and explain the limit.
- Use **K-Prototypes** (mixed data), or **Gower distance** on a random sample (a full 365K × 365K distance matrix is too big), and optionally DBSCAN.
- Describe each cluster in simple words, for example "small private startups that hide salaries".

#### C5. Skill network (bonus)

- Use `networkx`. **Node size** = how often the skill appears. **Edge width** = how often two skills appear together in the same ad.
- Raw counts favor very common skills, so we also compute **PMI or lift** and keep only strong links.
- Find communities with **Louvain**, and compute degree, betweenness and eigenvector centrality.
- Make three versions: **all data**, **per period**, and **monthly** (as a small chart of how the top 10 skills' ranks change).

#### C6. The playbook for a business owner

Imagine the reader is a CEO of a growing startup or a mid-size trading/manufacturing company. They do not want statistics, only decisions. The playbook covers:

- **Writing the ad:** what to include, which benefits are common, whether to show salary.
- **Pay:** monthly and hourly ranges by role and province.
- **Timing:** best months to post (and months with more competition).
- **Requirements:** where degree can be relaxed, where experience matters, which skills add pay.
- **One-page checklist:** "If I'm hiring X in province Y, do this."

Each rule must come with a figure or number from our analysis, and an honest note that these are **market patterns**, not proven cause and effect.

**Output of Phase 3:** notebooks `11` to `14` and the draft playbook.

---

### Phase 4: Final deliverables

#### The report (PDF)

Structure:

1. Title and short abstract
2. Executive summary
3. Data and cleaning steps
4. Part A answers
5. Part B answers
6. Part C answers
7. Business playbook
8. Limitations
9. Appendix (data dictionary, mapping tables)

Rules:

- Answer **every question, one by one, in the same order as the brief.**
- End each section with a short **"Business takeaway"** box.
- Every chart gets a title, readable labels and a one-line message in its caption.
- Test the PDF process early, especially if we use Persian text.

#### The presentation (15 minutes, about 12-15 slides)

- Pick **4-5 headline findings** that tell one story, for example:
  1. Many salaries are hidden, and not at random.
  2. The hourly-income view changes how we see jobs.
  3. Seasonality and falling real wages.
  4. Skill clusters and how skills connect.
  5. Iran vs the global job market.
- Flow: hook (the problem) → the data → insights → recommendations → closing.
- One message per slide, big charts, little text.
- We may add new analysis not in the brief (for example, "which skills add the biggest salary premium").
- Imagine the audience as a JobVision manager, a business owner, a job seeker or a policymaker.

#### The README

- Project description and dataset source/license (CC BY-NC 4.0)
- Folder tree
- Setup steps and `requirements.txt` with versions
- How to download data
- **A run-order table:** each notebook, what it needs, and what it produces
- Summary of main findings and limitations
- Test it: clone into a fresh folder and run it from scratch.

---

## 5. Timeline (about 4 weeks)

| Week | Focus |
|---|---|
| 1 | Phase 0 and 1: setup, cleaning, features, Income_Per_Hour, EDA |
| 2 | Phase 2: models, seasonality, inflation, gender, education, age, provinces |
| 3 | Phase 3 and global comparison: clustering, network, bonus tasks |
| 4 | Business playbook, report, slides, README, full reproducibility test |

---

## 6. Common mistakes to avoid

- **Wrong working-hours parsing.** All hourly-income results depend on it. Validate by hand.
- **Wrong salary unit.** Confirm Toman vs Rial and monthly vs other, and check for typos.
- **Forgetting the hidden-salary bias.** Mention it with every salary conclusion.
- **Treating patterns as causes.** We never say "X causes Y".
- **Tiny groups.** Set minimum counts before reporting growth or averages.
- **Too-strong time claims.** 25 months cannot prove long-term trends or formal seasonality.
- **Data leakage** from encoding the target before the train/test split.
- **Mixing calendars.** The data uses Gregorian months, and we explain Jalali months. Label charts clearly.
- **Counting duplicates twice.** Check for repeated ads.
- **Splitting JSON on commas.** Use a real JSON parser.

---

## 7. Order of work

1. Inspect the data and clean Persian text.
2. Missing values and the salary-hiding test.
3. Feature engineering (parsers in `src/`).
4. Income_Per_Hour and EDA.
5. Models and time-based analysis.
6. Clustering and the skills network.
7. Business playbook.
8. Report, slides and README, written **along the way**, not at the end.

