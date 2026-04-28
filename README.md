# Healthcare Market Dynamics: The Missing Middle

A comprehensive data-driven analysis of India's healthcare investment landscape, identifying critical misalignment between VC capital flows and actual market need.

## Project Overview

This project analyzes ₹2,465 crores of healthcare VC investment in India and reveals a critical insight: **VCs are funding problems that don't exist for India2 (the "Missing Middle"), while ignoring problems that are critical.**

**Key Finding:** Medical financing and affordable healthcare solutions have a ₹80 billion TAM but receive less than ₹150 crores in VC funding (0.19% penetration).

## What's Included

### 1. Interactive Dashboard
**Live URL:** https://bb86d96e-59d1-4232-be45-886a917a3c81-00-b6df2ml9ia1v.sisko.replit.dev/

**5 Interactive Pages:**
-  **Key Metrics** - KPI cards showing India2 healthcare crisis
-  **Spending Analysis** - Insurance coverage gaps and out-of-pocket burden
-  **Telemedicine Adoption** - Trend analysis showing plateauing growth
-  **Startup Ecosystem** - Funding distribution and company status
-  **The Gap** - VC focus vs India2 need (the core insight)

### 2. Professional Report (12 pages)
**📄 Download Report:** [Healthcare_Market_Dynamics_Report.pdf](file:///Users/manyachadha/Downloads/Healthcare%20Market%20Dynamics_%20The%20Missing%20Middle.pdf) 
Comprehensive analysis including:
- Executive Summary with key data
- Market Overview (India1/2/3 breakdown)
- VC Capital Misalignment Analysis
- India2 Deep Dive (the Missing Middle)
- Medical Financing Opportunity
- Affordable Insurance Gap
- Investment Thesis & Recommendations

### 3. Advanced SQL Queries
**File:** `04_powerbi_sql_queries.sql`

8 queries demonstrating:
- Common Table Expressions (CTEs)
- Window Functions (LAG, ROW_NUMBER)
- Complex Aggregations
- CASE Statements
- Data Transformations

### 4. Data Analysis
8 CSV files with analysis-ready data for Power BI or further analysis

### 5. Source Database
`healthcare_data.db` - SQLite database with all raw data

## 🔍 Key Insights

### The Three Economies
- **India1** (10%, 140M): Affluent, 75% insured, problem solved
- **India2** (35%, 490M): Missing Middle, 15% insured, **CRITICAL GAP**
- **India3** (55%, 770M): Low-income, partially addressed by Ayushman

### The Misalignment
| Segment | VC Funding | Adoption | Status |
|---------|-----------|----------|--------|
| Telemedicine | ₹800Cr | 12% (plateauing) | Overinvested |
| Medical Financing | ₹150Cr | N/A | Underinvested |
| Affordable Insurance | ₹100Cr | N/A | Underinvested |

### Why It Matters
- **58% of India2** face catastrophic health expenditure
- **65% pay out-of-pocket** (vs 35% in India1)
- **Only 15% have insurance** (vs 75% in India1)
- **₹80B TAM** in medical financing with **0.19% penetration**

## 🛠️ Technology Stack

- **Python** - Data processing and analysis
- **SQLite** - Data storage
- **Pandas** - Data manipulation
- **Plotly** - Interactive visualizations
- **Streamlit** - Interactive dashboard
- **Replit** - Deployment

## 📈 How to Use

### View the Dashboard
Visit: https://bb86d96e-59d1-4232-be45-886a917a3c81-00-b6df2ml9ia1v.sisko.replit.dev/

### Run Locally
```bash
git clone https://github.com/manyachadha26/healthcare-market-dynamics.git
cd healthcare-market-dynamics
pip install streamlit pandas plotly
streamlit run dashboard.py
```

### Access Raw Data
- Download CSV files
- Connect to `healthcare_data.db` using SQLite
- Run queries from `04_powerbi_sql_queries.sql`





**Created:** April 28, 2024  
**Status:** Complete  
**Live Dashboard:** https://bb86d96e-59d1-4232-be45-886a917a3c81-00-b6df2ml9ia1v.sisko.replit.dev/
