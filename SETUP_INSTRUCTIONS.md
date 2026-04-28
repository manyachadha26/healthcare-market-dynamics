# Healthcare Market Dynamics - Local Setup Instructions

Complete guide to run the healthcare dashboard project on your computer.

---

## PREREQUISITES

- **Windows/Mac/Linux** computer
- **Python 3.8+** installed (download from python.org)
- **Power BI Desktop** (free download from powerbi.microsoft.com)
- **SQLite Browser** (optional, for viewing database)

---

## STEP-BY-STEP SETUP

### Step 1: Create Project Folder (2 min)

**Windows:**
```bash
mkdir C:\healthcare_project
cd C:\healthcare_project
```

**Mac/Linux:**
```bash
mkdir ~/healthcare_project
cd ~/healthcare_project
```

### Step 2: Download All Files (2 min)

Download these 5 files from `/mnt/user-data/outputs/`:
1. `healthcare_data.db` - Database file
2. `04_powerbi_sql_queries.sql` - SQL queries
3. `05_execute_queries.py` - Python script
4. `requirements.txt` - Dependencies
5. `SETUP_INSTRUCTIONS.md` - This file (optional)

Put all files in your `healthcare_project` folder.

**Folder should look like:**
```
healthcare_project/
├── healthcare_data.db
├── 04_powerbi_sql_queries.sql
├── 05_execute_queries.py
├── requirements.txt
└── SETUP_INSTRUCTIONS.md
```

### Step 3: Install Python Dependencies (2 min)

Open terminal/command prompt in your `healthcare_project` folder:

```bash
pip install -r requirements.txt
```

**What this does:** Installs pandas and sqlalchemy (needed to run the Python script)

### Step 4: Run Python Script to Generate CSVs (1 min)

```bash
python 05_execute_queries.py
```

**Expected output:**
```
================================================================================
EXECUTING SQL QUERIES FOR POWER BI
================================================================================

[1/8] Spending Trends with Growth Analysis...
✓ Exported: powerbi_01_spending_trends.csv (9 rows)
[2/8] Insurance Coverage Gap Analysis...
✓ Exported: powerbi_02_insurance_gap.csv (7 rows)
... (continues for all 8 files)
```

**After running:** You should see 8 new CSV files in your folder:
- powerbi_01_spending_trends.csv
- powerbi_02_insurance_gap.csv
- powerbi_03_telemedicine_adoption.csv
- powerbi_04_startup_ecosystem.csv
- powerbi_05_vc_misalignment.csv
- powerbi_06_segment_comparison.csv
- powerbi_07_kpi_metrics.csv
- powerbi_08_company_details.csv

### Step 5: Open Power BI Desktop (5 min)

1. Download Power BI Desktop from: https://powerbi.microsoft.com/en-us/downloads/
2. Install it
3. Open Power BI Desktop
4. Click "File" → "New"

### Step 6: Import CSV Files Into Power BI (15 min)

In Power BI Desktop:

1. Click "Get Data" → "Text/CSV"
2. Navigate to your `healthcare_project` folder
3. Select `powerbi_01_spending_trends.csv`
4. Click "Load"
5. Repeat for all 8 CSV files (import all of them)

**After importing all 8 files, you'll have 8 tables in Power BI**

### Step 7: Create Data Model & Relationships (20 min)

In Power BI:

1. Click "Manage relationships"
2. Create relationships between tables:
   - Most tables link by `income_segment` and `year`
   - Some by `sector` or `state`
3. Set relationships as one-to-many where appropriate

### Step 8: Build Dashboard Pages (120 min)

Create 5 report pages:

**Page 1: Key Metrics**
- Drag `powerbi_07_kpi_metrics.csv` table to canvas
- Create 4 card visuals for top metrics:
  - India2 Population: 490M
  - Insurance Gap: 60 percentage points
  - Out-of-Pocket: 65%
  - Catastrophic Health Exp: 58%

**Page 2: Spending Analysis**
- Table: `powerbi_01_spending_trends.csv` - show all columns
- Chart: Bar chart of `insurance_coverage_pct` by `income_segment`
- Chart: Line chart of `out_of_pocket_pct` by year and segment
- Add slicers: Year, Income Segment

**Page 3: Telemedicine Adoption**
- Chart: Line chart showing `segment_1_adoption`, `segment_2_adoption`, `segment_3_adoption` over years
- Insight: "Adoption plateauing in India2"
- Table: Show adoption status and trajectory

**Page 4: Startup Ecosystem**
- Table: `powerbi_04_startup_ecosystem.csv` - all columns
- Chart: Bar chart of `total_funding_crores` by `sector`
- Chart: Pie chart of company status (operating, exited, defunct)
- Details: Company details table from `powerbi_08_company_details.csv`

**Page 5: The Gap (VC Focus vs India2 Need)**
- Table: `powerbi_05_vc_misalignment.csv` - all columns
- Scatter chart:
  - X-axis: `current_vc_focus_score`
  - Y-axis: `india2_need_score`
  - Shows where VC focus doesn't match need
- Highlight: Medical Financing (score 2 vs need 8) = biggest gap
- Table: Investment status and strategic implications

### Step 9: Format & Polish (30 min)

- Add titles to each page
- Use consistent color scheme (blue, orange, gray)
- Add filters to allow drill-down
- Add text boxes with key insights
- Professional layout (aligned, clean)

### Step 10: Save & Export (10 min)

- Save as: `Healthcare_Market_Dynamics.pbix`
- Export pages to PDF/PNG for sharing

---

## THAT'S IT!

You now have:
✅ SQL queries (in 04_powerbi_sql_queries.sql)
✅ Python script that executes queries (05_execute_queries.py)
✅ 8 CSV files with data analysis
✅ Power BI dashboard (5 pages)

---

## OPTIONAL: Explore the SQL Queries

If you want to understand the SQL better:

1. Download **SQLite Browser** from: https://sqlitebrowser.org/
2. Open `healthcare_data.db` with it
3. Look at the tables:
   - healthcare_spending
   - insurance_penetration
   - healthcare_adoption
   - healthcare_companies
4. Try running queries from `04_powerbi_sql_queries.sql`
5. Modify queries and see how results change

---

## TROUBLESHOOTING

**Q: "Python command not found"**
A: Python not installed. Download from python.org, install, and add to PATH.

**Q: "ModuleNotFoundError: pandas"**
A: Run `pip install -r requirements.txt` again, or `pip install pandas`

**Q: "healthcare_data.db not found"**
A: Make sure the database file is in the same folder as the Python script.

**Q: "Power BI won't import CSV"**
A: Make sure CSV files are in the same folder. Try using "Get Data" → "Text/CSV" in Power BI.

---

## WHAT THIS SHOWS EMPLOYERS

- ✅ Advanced SQL (CTEs, Window Functions, Aggregations, CASE statements)
- ✅ Python scripting (data extraction, CSV generation)
- ✅ Power BI expertise (data modeling, visualizations, dashboards)
- ✅ Business analysis (identified "Missing Middle" insight)
- ✅ Data-driven decision making

---

## TIME ESTIMATE

- Setup: 5 min
- Python execution: 1 min
- Power BI import: 15 min
- Dashboard building: 120-150 min
- **Total: 3-4 hours**

You can have a professional, complete healthcare analytics dashboard on your computer within 4 hours.

---

Good luck! Let me know if you get stuck on any step.

