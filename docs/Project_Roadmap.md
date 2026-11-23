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
| B | Time, location and industry analysis | 4 |
| C | Salary modeling and what drives pay | 5 |
| D | Clustering job titles and employers | 1 + 1 optional |

The report must answer the questions **one by one, in this same order**.

---

## 2. What the data dictionary tells us

Here are the facts that shape the whole plan.

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
│   ├── 04_distributions_relationships.ipynb
│   ├── 05_seasonality.ipynb
│   ├── 06_wage_dynamics_inflation.ipynb
│   ├── 07_geography.ipynb
│   ├── 08_industry_job_sectors.ipynb
│   ├── 09_salary_modeling.ipynb
│   ├── 10_gender.ipynb
│   ├── 11_sector_share_change.ipynb
│   ├── 12_education_vs_experience.ipynb
│   ├── 13_peak_income_age.ipynb
│   ├── 14_job_clustering.ipynb
│   └── 15_employer_clustering_optional.ipynb
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

1. Create the environment with: pandas, numpy, scipy, statsmodels, scikit-learn, matplotlib, seaborn, plotly, kmodes, gower, jdatetime, pyarrow, arabic-reshaper, python-bidi, hazm (Persian text tools) and umap-learn.
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

- Count missing values and the percentage for **every column**, and report them in a table. Add a sorted bar chart to make it easy to read.
- Split missing values into two kinds:
  - **Not applicable** (for example, no software skills needed), and
  - **Truly missing** (information the ad should have had).
- Since a big part of the project is about salary amounts, study **how often salary values actually appear**. Look at `Jobpost_SalaryCanBeShown`. Note that ads can be `False` (salary hidden) and also have empty salary values. Check how these two relate.
- Test if hiding the salary is random:
  - Chi-square test plus **Cramér's V** against province, company size, job category, industry and period.
  - A **logistic regression** that predicts "salary hidden", with odds ratios and AUC.
- **Find groups with almost no salary information.** For every group (job category, industry, province, company size), compute the number and share of ads with a shown salary. Report the groups where this is close to zero. These groups cannot be analyzed reliably later, so we list them and avoid strong claims about them.

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
3. **Plot and describe the distribution** of Income_Per_Hour (histogram, log scale, summary numbers).
4. Compare Income_Per_Hour across job categories, job titles (with a minimum number of ads), experience groups and education levels.
5. **Full-time vs part-time vs project:** compare using a Mann-Whitney test and an effect size. The question is simple: *do part-time or project jobs pay more per hour than full-time jobs?*

**Important warning:** for part-time and project jobs, the salary column may mean "per project" or "per hour", not "per month". We read some real examples before comparing, and explain what we find.

#### A4. Distributions and relationships

- Draw the distribution of the key variables: monthly salary, hourly income, required experience and age range. Report **skewness** (on normal and log scales) and analyze **outliers**.
- Find outliers with the **IQR rule** (and optionally the modified Z-score on log values). We **flag** outliers with a column instead of deleting them, and compare results with and without them.
- Show how variables relate to each other with **scatter plots, comparison charts (box plots by group)** and a **correlation matrix** of the numeric variables. We use Spearman next to Pearson when the data is skewed.
- Check **multicollinearity** with VIF. We expect min/max salary, min/max age and min/max experience to be strongly related.
- Show **non-linear relationships** (diminishing returns of experience or age on salary) with binned averages and a smoothed curve (LOWESS).

**Output of Phase 1:** `01` to `04` notebooks, the cleaned dataset in `data/processed/`, the mapping tables, and the first set of figures.

---

### Phase 2: Time, location and industry analysis (Part B)

#### B1. Seasonality (when do ads peak?)

- Plot the number of ads per **month** and per **season**.
- We only have month-level data over 25 months, so a few months appear twice (and March appears three times: 2022, 2023, 2024). We **compare the same month across years** instead of using a heavy seasonal model.
- Is there a clear seasonal pattern? Find the peak months overall.
- **Find which groups and industries peak when.** Repeat the monthly view for the biggest industries and job categories, and show it as a heatmap (month × industry).
- Explain the jumps using the **Iranian work calendar** and how each economic activity works (for example the Nowruz slowdown, hiring after Nowruz, summer, autumn hiring, budget cycles, seasonal work in agriculture, construction or tourism). We call these **explanations that fit the timing**, not proven causes.

#### B2. Wages vs inflation

- Compute the monthly **mean and median** of offered salary and plot how they change over time.
- Compare with inflation. Take the price index from an official source (Statistical Centre of Iran or the Central Bank of Iran) and cite it. We do not use numbers from memory.
- Compute the **real wage** (nominal salary divided by the price index) to see if offered pay kept up.
- Find job categories (and industries) whose offered salary **grew the most or fell the most** compared with the market average. Use a minimum number of ads per group.

#### B3. Provinces

- Count ads per province and show the distribution (bar chart and map-style table).
- Say in which provinces ads are **most frequent and have the most reach**. Also compute each province's share of all ads.
- **Is there a province with a very small share of ads?** List them.
- If we can find population data (an official source, cited), add "ads per 100,000 people" to measure real reach, not just size.
- **Note:** there are two province fields. `Jobpost_Province*` is where the job is, and `Company_Province*` is where the company is based. We use the job province, and also look at ads where the two differ.

#### B4. Most popular job sectors in each industry

- For each industry, build the share of each job category (cross-table, normalized by row). Show it as a heatmap.
- Make a "top 3 job categories per industry" table.
- Go one level deeper and list the most requested **job titles and specialties** in each industry (using the cleaned title text, with a minimum count).

**Output of Phase 2:** notebooks `05` to `08`, the figures, and a short written conclusion per question.

---

### Phase 3: Salary modeling (Part C)

#### C1. Salary models and what matters most

- **Target:** `log(avg_salary)`, because salaries are skewed.
- **Inputs:** job category, province, company size and age, ownership, education, experience, top skills, employment type, benefits, remote flag, hours.
- **One model per period.** The brief says "per year", but we only have 25 months. We use the following choice and explain it clearly in the report:
  - Period 1: 2022-03 to 2023-02
  - Period 2: 2023-03 to 2024-02
  - 2024-03 is a single month, so we leave it out of the models or merge it with Period 2.
- **Main model: OLS regression** with standardized coefficients (easy to explain), with R² and robust standard errors. We keep only variables with **significant coefficients** when we rank importance.
- **Optional check:** a Random Forest or Gradient Boosting with permutation importance, to confirm the ranking and catch non-linear effects.
- Rank the most powerful variables in each period and compare them with a **slope chart**: what changed between the periods?
- **Check the signs.** For every important variable, say whether the sign of its coefficient matches what we expected (for example more experience → higher pay, larger company → higher pay) and explain any surprise.
- Remember: models only see ads that show their salary (selection bias).

#### C2. Gender

- Test salary differences by preferred gender with **Welch's t-test**, plus **Mann-Whitney** as a backup. Report effect size (Cohen's d) and confidence intervals.
- Show **where the gap or preference is strongest** across job categories and seniority levels (experience groups) with a heatmap.
- Run a regression that controls for category, experience and province.
- **Be clear:** this shows what employers *ask for* and *offer*, not real pay gaps between workers.

#### C3. Changing sector shares

- Count ads and compute share (%) of each job category per period (or per quarter).
- Show growth or decline in percentage points and in relative change. Use a slope or bump chart.
- Name the sectors that are **growing** and the ones that are **shrinking**, with a minimum number of ads.

#### C4. Education vs experience

- Measure how much a higher degree changes the offered salary, controlling for experience.
- Compare the money value of **a degree** with the money value of **a year of experience** (regression with interaction terms).
- Find industries and job categories where **experience clearly replaces a degree** (a flat degree effect with a strong experience effect).

#### C5. Age and peak income

- Use the middle of the requested age range (`Jobpost_RequiredMinAge`, `Jobpost_RequiredMaxAge`) as the age value.
- Plot salary by age group and fit a **quadratic or spline** curve to find the age where offered pay peaks.
- Compare IT, manufacturing and finance. Is the peak age different?
- **Warning:** many ads have no age limits, and ages are employer requirements, not worker ages.

**Output of Phase 3:** notebooks `09` to `13`, all figures, and a short written conclusion per question.

---

### Phase 4: Clustering (Part D)

#### D1. Grouping job titles by skills and education

1. Use a cleaned job title (or `Jobpost_MainJobCategory` when titles are too messy) and keep titles with at least N ads.
2. Build a vector for every ad (or title): TF-IDF or 0/1 skills + required education level + experience (scaled).
3. Reduce dimensions (TruncatedSVD), then run **K-Means**. Pick k using the elbow method, silhouette score and Calinski-Harabasz. Optionally compare with **GMM** using BIC.
4. **Interpret the clusters:** name each one by its top skills, education level and example titles. Explain how the clusters **differ from each other**, and which job titles are close to each other and why.
5. Plot the clusters with UMAP or PCA.
6. Optional check: repeat the clustering for each period and see if titles moved between clusters.

#### D2. Employer profiles (optional)

- Features: company size, company age, ownership type, industry, province, salary-disclosure rate, number of benefits.
- There is no company ID, so we cluster **ad rows** and call the result "employer types".
- Use **K-Prototypes** (made for mixed numbers and categories), or **Gower distance** on a random sample (a full 365K × 365K distance matrix is too big), and optionally DBSCAN.
- Describe each cluster in simple words, for example "small private startups that hide salaries".
- **Answer for JobVision:** how many employer types does JobVision face, and how should it plan its partnerships with them?
- Give **a few marketing and sales ideas** for developing cooperation with some of these employer types. For example: a salary-transparency package for employers who hide salaries, a hiring bundle for fast-growing small companies, or an enterprise plan for large employers who post often.

**Output of Phase 4:** notebooks `14` and `15`, cluster descriptions, and the employer-type recommendations.

---

### Phase 5: Final deliverables

#### The report (PDF)

Structure:

1. Title and short abstract
2. Executive summary
3. Data and cleaning steps (step by step)
4. Part A answers
5. Part B answers
6. Part C answers
7. Part D answers
8. Overall strategic conclusion and limitations
9. Appendix (data dictionary, mapping tables)

Rules:

- Answer **every question, one by one, in the same order as the brief.**
- End each section with a short **"Business takeaway"** box.
- Every chart gets a title, readable labels and a one-line message in its caption.
- Test the PDF process early, especially if we use Persian text.

#### The presentation (15 minutes, about 12-15 slides)

- We do **not** need to follow the order of the questions. Pick **4-5 headline findings** that tell one story, for example:
  1. Many salaries are hidden, and not at random.
  2. The hourly-income view changes how we see jobs.
  3. When companies hire (seasonality) and how real wages changed with inflation.
  4. What really drives pay: experience, degree and location.
  5. Employer types and what JobVision can do with them.
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

## 5. Timeline (about 3 to 4 weeks)

| Week | Focus |
|---|---|
| 1 | Phase 0 and 1: setup, cleaning, features, Income_Per_Hour, EDA |
| 2 | Phase 2 and 3: seasonality, inflation, provinces, industries, salary models, gender, education, age |
| 3 | Phase 4: clustering (jobs and employers) and extra analysis for the presentation |
| 4 (or the end of week 3) | Report, slides, README, full reproducibility test |

---

## 6. Common mistakes to avoid

- **Wrong working-hours parsing.** All hourly-income results depend on it. Validate by hand.
- **Wrong salary unit.** Confirm Toman vs Rial and monthly vs other, and check for typos.
- **Forgetting the hidden-salary bias.** Mention it with every salary conclusion, and be careful with groups that have almost no shown salaries.
- **Treating patterns as causes.** We never say "X causes Y".
- **Tiny groups.** Set minimum counts before reporting growth or averages.
- **Too-strong time claims.** 25 months cannot prove long-term trends or formal seasonality.
- **Data leakage** from encoding the target before the train/test split.
- **Mixing calendars.** The data uses Gregorian months, and we explain Jalali months. Label charts clearly.
- **Counting duplicates twice.** Check for repeated ads.
- **Splitting JSON on commas.** Use a real JSON parser.
- **Answering questions out of order in the report.** Follow the brief's order exactly (Part A, B, C, D).

---

## 7. Order of work

1. Inspect the data and clean Persian text.
2. Missing values and the salary-hiding test.
3. Feature engineering (parsers in `src/`).
4. Income_Per_Hour and EDA.
5. Time, location and industry analysis.
6. Salary models and the questions about gender, sectors, education and age.
7. Clustering of job titles and employers.
8. Report, slides and README, written **along the way**, not at the end.

