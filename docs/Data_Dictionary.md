# JobVision Job Posts Dataset

## 1. Introduction

The **JobVision Job Posts Dataset** is a collection of anonymized job advertisements published on [Jobvision](https://jobvision.ir), one of Iran's largest online job boards. Each row is one job post, combining the job's requirements, location, salary range, benefits, and the profile of the hiring company.

| Property | Value |
|---|---|
| **Source** | [JobVision on Hugging Face](https://huggingface.co/datasets/JobVision/JobVision_Jobposts_Dataset) |
| **Publisher** | JobVision |
| **Rows** | ~365k (364,838) |
| **Columns** | 43 |
| **File size** | ~392 MB (CSV) |
| **Time period** | March 2022 – March 2024 (by job post activation month) |
| **Release date** | August 2025 |
| **Languages** | Persian (primary), with English translations for many categorical fields |
| **Domain** | Recruitment, Human Resources, Labor-Market Analytics |
| **License** | CC BY-NC 4.0 (non-commercial, attribution required) |

### Typical use cases

- **Salary prediction**: regression on job post features (tabular regression).
- **Job post classification**: predicting category, industry, or work type from title and requirements (text and tabular classification).
- **Labor-market analysis**: skill demand, experience requirements, hiring trends by province and industry.
- **Geospatial analysis**: job density and salary variation across Iranian provinces and cities.
- **Hiring strategy benchmarking**: benefits, remote work, and gender or age preferences by industry and company size.

---

## 2. Data Dictionary

**Naming convention:** columns are prefixed with `Jobpost_` (about the advertisement) or `Company_` (about the hiring company). Suffix `Fa` means Persian, `En` means English.

Missing values appear as empty/null. Most optional fields (salary, skills, benefits, age limits) are null when the advertiser did not provide them.

### 2.1 Identifier

| Column | Type | Description |
|---|---|---|
| `RowNumber` | int | Sequential row index (1 to ~365k). Not a job post ID from the source site. |

### 2.2 Job Metadata

| Column | Type | Description | Example |
|---|---|---|---|
| `Jobpost_RawTitle` | string | Job title exactly as written by the advertiser (Persian, may include city or gender notes). | `برنامه نویس full-stack` |
| `Jobpost_PreferredGender` | categorical (5) | Gender preference. Values: `تفاوتی ندارد` (no preference), `فقط آقا` (male only), `فقط خانم` (female only), `ترجیحاً آقا` (male preferred), `ترجیحاً خانم` (female preferred). | `فقط خانم` |
| `Jobpost_ProvinceFa` / `Jobpost_ProvinceEn` | categorical (32) | Province where the job is located. | `تهران` / `Tehran` |
| `Jobpost_WorkTypeFa` / `Jobpost_WorkTypeEn` | categorical (4) | Employment type: `Full Time`, `Part Time`, `Full Time Or Part Time`, `Project - based`. | `تمام وقت` / `Full Time` |
| `Jobpost_SalaryCanBeShown` | bool | Whether the advertiser allows the salary to be displayed. | `true` |
| `Jobpost_MinSalary` | float | Lower bound of the salary range. Null if not disclosed. Observed range: 2 to 70. | `12` |
| `Jobpost_MaxSalary` | float | Upper bound of the salary range. Null if not disclosed. Observed range: 3 to 100. | `15` |
| `Jobpost_RequiredExperienceYears` | int | Required years of work experience (0 to 30). | `3` |
| `Jobpost_RequiredRelatedExperienceInThisIndustry` | bool | Whether experience in the same industry is required. | `true` |
| `Jobpost_CompanyWorkTimesDescription` | string | Free-text description of working days and hours (Persian). | `شنبه تا چهارشنبه 8 الی 17` |
| `Jobpost_ActivationTime_YEAR_MONTH` | string (`YYYY-MM`) | Month the job post was activated. Range: 2022-03 to 2024-03. | `2023-06` |

> **Salary unit note:** The dataset card states salaries are in Iranian Toman. Because the observed values are small (2 to 100), they most likely represent **millions of Toman per month**. Verify this against the source before doing monetary analysis.

### 2.3 Categorization

| Column | Type | Description | Example |
|---|---|---|---|
| `Jobpost_MainJobCategory` | categorical (77) | Primary job category (Persian). | `مالی و حسابداری` |
| `Jobpost_SecondaryJobCategories` | string | Additional job categories, comma-separated (589 distinct combinations). Often null. | `مدیریت بیمه,...` |
| `Jobpost_IndustryFa` / `Jobpost_IndustryEn` | categorical (44) | Industry assigned to the job post. | `IT / Software / Hardware` |

### 2.4 Skills & Qualifications

| Column | Type | Description |
|---|---|---|
| `Jobpost_SoftwareSkills` | JSON string | List of required software or tools. Null if none specified. |
| `Jobpost_LanguageSkills` | JSON string | List of required languages with proficiency levels. Null if none specified. |
| `Jobpost_AcademicFields` | JSON string | List of accepted fields of study and degree levels. Null if none specified. |

**`Jobpost_SoftwareSkills` object schema**

| Key | Description | Example |
|---|---|---|
| `TitleFa` | Persian name (may be empty or contain comma-separated aliases) | `پایتون` |
| `TitleEn` | English name (a few entries are Persian-only product names) | `Python` |
| `Level` | `مقدماتی` (basic), `متوسط` (intermediate), `پیشرفته` (advanced) | `پیشرفته` |

```json
[{"TitleFa":"پایتون","TitleEn":"Python","Level":"پیشرفته"},
 {"TitleFa":"","TitleEn":"PostgreSql","Level":"پیشرفته"}]
```

**`Jobpost_LanguageSkills` object schema**

| Key | Description | Example |
|---|---|---|
| `Languages_TitleFa` | Language name in Persian | `انگلیسی` |
| `Languages_TitleEn` | Language name in English | `English` |
| `Level` | Proficiency label with percentage. Observed levels: `مقدماتی ۱۰٪`, `پایین تر از متوسط ۳۰٪`, `متوسط ۵۰٪`, `بالاتر از متوسط ۷۰٪`, `پیشرفته ۹۰٪` | `متوسط ۵۰٪` |

```json
[{"Languages_TitleFa":"انگلیسی","Languages_TitleEn":"English","Level":"متوسط ۵۰٪"}]
```

**`Jobpost_AcademicFields` object schema**

| Key | Description | Example |
|---|---|---|
| `FieldType` | Field of study (Persian) | `کامپیوتر - فناوری اطلاعات` |
| `DegreeLevel` | Degree level, e.g. `کاردانی` (associate), `کارشناسی` (bachelor's), `کارشناسی ارشد` (master's) | `کارشناسی` |

```json
[{"FieldType":"کامپیوتر - فناوری اطلاعات","DegreeLevel":"کارشناسی"}]
```

### 2.5 Benefits & Policies

| Column | Type | Description | Example |
|---|---|---|---|
| `Jobpost_BenefitFa` / `Jobpost_BenefitEn` | string | Comma-separated list of benefits offered (e.g. Transportation, Loan, Bonus, Commission, Health insurance, Lunch). Entries in the English column may have trailing spaces. | `Loan,Bonus` |
| `Jobpost_HasDisabilitySupport` | bool | Whether the employer supports applicants with disabilities. | `false` |
| `Jobpost_RequiredMinAge` | float | Minimum applicant age (18 to 50). Null if unspecified. | `25` |
| `Jobpost_RequiredMaxAge` | float | Maximum applicant age (18 to 60). Null if unspecified. | `35` |
| `Jobpost_RequiredMilitaryServiceCard` | bool | Whether a military service completion/exemption card is required (relevant for male applicants in Iran). | `true` |
| `Jobpost_IsRemote` | bool | Whether the job can be done remotely. | `false` |
| `Jobpost_IsInternship` | bool | Whether the post is an internship. | `false` |
| `Jobpost_PriorityWithLocalCandidate` | bool | Whether candidates local to the job's location are given priority. | `true` |

### 2.6 Company Details

| Column | Type | Description | Example |
|---|---|---|---|
| `Company_AgeFromEstablishmentYear` | categorical | Company age bucket. Observed: `5 - 9 years`, `10 - 14 years`, `15 - 19 years`, `more than 20 years`. | `10 - 14 years` |
| `Company_ProvinceFa` / `Company_ProvinceEn` | categorical (31) | Province of the company's headquarters. May differ from the job's province. | `Tehran` |
| `Company_CityFa` / `Company_CityEn` | categorical (323) | City of the company. | `Mashhad` |
| `Comany_CompanyOwnershipTypesFa` | categorical (3) | Ownership type in Persian. **Note: the column name has a typo (`Comany`) in the source file.** | `خصوصی` |
| `Company_CompanyOwnershipTypesEn` | categorical (3) | Ownership type in English, e.g. `Privately held`, `Non - profit / NGO / Charity`. | `Privately held` |
| `Company_SizeFa` / `Company_SizeEn` | categorical (7) | Employee count bucket, e.g. `Less than 10 employees`, `11 - 50 employees`, `51 - 200 employees`, `201 - 500 employees`, `501 - 1000 employees`, `1001 - 5000 employees`. | `11 - 50 employees` |
| `Company_ActivityTypeFa` / `Company_ActivityTypeEn` | categorical (3) | Customer scope, e.g. `Iranian company dealing only with Iranian entities`, `Iranian company dealing with Iranian and foreign customers`. | |
| `Company_IndustryFa` / `Company_IndustryEn` | string | One or more industries of the **company**, comma-separated. Can differ from `Jobpost_Industry*`. | `Trading / International Affairs,Marketing / Advertising` |

---

## 3. Data Quality Notes

- **Missing data is common.** Salary, skills, academic fields, benefits, and age limits are frequently null. Check `Jobpost_SalaryCanBeShown` and null rates before modeling.
- **Possible near-duplicates.** Some companies post the same role multiple times with identical attributes. Consider de-duplicating on title, company attributes, and activation month.
- **Mixed-language text.** `Jobpost_RawTitle` and many fields are Persian; use a Persian-aware tokenizer or normalizer (e.g. [Hazm](https://github.com/roshan-research/hazm)) for NLP.
- **Multi-valued columns.** `Jobpost_SecondaryJobCategories`, `Jobpost_Benefit*`, and `Company_Industry*` are comma-separated strings; split them for analysis. Note that a few labels themselves contain commas inside JSON aliases.
- **Anonymization.** Company names and contact details are not included.
- **Time coverage.** Data spans only March 2022 to March 2024, so salaries reflect the high-inflation Iranian economy over that period; adjust or control for time when comparing salaries.

---

## 4. License & Citation

This dataset is released under [**CC BY-NC 4.0**](https://creativecommons.org/licenses/by-nc/4.0/).

- ✅ Research, academic, and other non-commercial use is allowed with attribution to JobVision.
- ❌ Commercial use (including training models for commercial purposes) is not allowed. For commercial licensing, contact **info@jobvision.ir**.

Suggested attribution:

> JobVision. *JobVision Job Posts Dataset*. Hugging Face, 2025. https://huggingface.co/datasets/JobVision/JobVision_Jobposts_Dataset
