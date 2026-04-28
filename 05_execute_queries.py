"""
Execute SQL queries from 04_powerbi_sql_queries.sql
Export results as CSVs for Power BI import
"""

import sqlite3
import pandas as pd

conn = sqlite3.connect('healthcare_data.db')

print("=" * 80)
print("EXECUTING SQL QUERIES FOR POWER BI")
print("=" * 80)

# Query 1: Spending Trends
print("\n[1/8] Spending Trends with Growth Analysis...")
query1 = """
WITH spending_trends AS (
    SELECT 
        income_segment,
        year,
        healthcare_spend_pct_income,
        out_of_pocket_pct,
        insurance_coverage_pct,
        household_catastrophic_health_exp_pct,
        LAG(healthcare_spend_pct_income) OVER (PARTITION BY income_segment ORDER BY year) as prev_year_spend,
        LAG(insurance_coverage_pct) OVER (PARTITION BY income_segment ORDER BY year) as prev_year_insurance
    FROM healthcare_spending
)
SELECT 
    income_segment,
    year,
    healthcare_spend_pct_income,
    out_of_pocket_pct,
    insurance_coverage_pct,
    household_catastrophic_health_exp_pct,
    ROUND(((healthcare_spend_pct_income - prev_year_spend) / prev_year_spend * 100), 2) as spend_growth_pct,
    ROUND(((insurance_coverage_pct - prev_year_insurance) / prev_year_insurance * 100), 2) as insurance_growth_pct,
    CASE 
        WHEN insurance_coverage_pct < 20 THEN 'Critical Gap'
        WHEN insurance_coverage_pct < 50 THEN 'Significant Gap'
        WHEN insurance_coverage_pct < 75 THEN 'Moderate Gap'
        ELSE 'Well Covered'
    END as insurance_status,
    CASE 
        WHEN household_catastrophic_health_exp_pct > 50 THEN 'High Risk'
        WHEN household_catastrophic_health_exp_pct > 10 THEN 'Medium Risk'
        ELSE 'Low Risk'
    END as health_expenditure_risk
FROM spending_trends
ORDER BY year DESC, income_segment;
"""
df1 = pd.read_sql_query(query1, conn)
df1.to_csv('powerbi_01_spending_trends.csv', index=False)
print(f"✓ Exported: powerbi_01_spending_trends.csv ({len(df1)} rows)")

# Query 2: Insurance Gap Analysis
print("[2/8] Insurance Coverage Gap Analysis...")
query2 = """
SELECT 
    i.state,
    i.income_segment,
    i.insurance_coverage_pct,
    i.scheme_type,
    i.beneficiaries,
    i.year,
    ROUND((100 - i.insurance_coverage_pct), 2) as insurance_gap_pct,
    ROUND((100 - i.insurance_coverage_pct) * i.beneficiaries / 100, 0) as uninsured_beneficiaries,
    CASE 
        WHEN i.income_segment = 'India1' THEN 'Affluent'
        WHEN i.income_segment = 'India2' THEN 'Missing Middle (Opportunity)'
        WHEN i.income_segment = 'India3' THEN 'Low Income'
    END as segment_classification,
    CASE 
        WHEN (100 - i.insurance_coverage_pct) > 85 THEN 'CRITICAL - Massive Opportunity'
        WHEN (100 - i.insurance_coverage_pct) > 50 THEN 'HIGH - Major Gap'
        WHEN (100 - i.insurance_coverage_pct) > 20 THEN 'MEDIUM - Moderate Gap'
        ELSE 'LOW - Well Covered'
    END as gap_severity
FROM insurance_penetration i
ORDER BY i.year DESC, i.income_segment, (100 - i.insurance_coverage_pct) DESC;
"""
df2 = pd.read_sql_query(query2, conn)
df2.to_csv('powerbi_02_insurance_gap.csv', index=False)
print(f"✓ Exported: powerbi_02_insurance_gap.csv ({len(df2)} rows)")

# Query 3: Telemedicine Adoption
print("[3/8] Telemedicine Adoption & Trends...")
query3 = """
WITH adoption_analysis AS (
    SELECT 
        metric_name,
        year,
        india1_pct as segment_1_adoption,
        india2_pct as segment_2_adoption,
        india3_pct as segment_3_adoption,
        (india1_pct + india2_pct + india3_pct) / 3 as avg_adoption,
        LAG(india2_pct) OVER (PARTITION BY metric_name ORDER BY year) as prev_year_india2,
        ROW_NUMBER() OVER (PARTITION BY metric_name ORDER BY year DESC) as recency_rank
    FROM healthcare_adoption
    WHERE metric_name = 'Telemedicine Adoption'
)
SELECT 
    metric_name,
    year,
    segment_1_adoption,
    segment_2_adoption,
    segment_3_adoption,
    avg_adoption,
    ROUND((segment_2_adoption - prev_year_india2), 2) as yoy_growth_india2,
    CASE 
        WHEN (segment_2_adoption - prev_year_india2) < 2 THEN 'Plateauing'
        WHEN (segment_2_adoption - prev_year_india2) < 4 THEN 'Slow Growth'
        ELSE 'Strong Growth'
    END as adoption_trajectory,
    CASE 
        WHEN segment_2_adoption < 15 THEN 'Low Adoption - Opportunity'
        WHEN segment_2_adoption < 30 THEN 'Emerging'
        ELSE 'Established'
    END as adoption_status
FROM adoption_analysis
ORDER BY year DESC;
"""
df3 = pd.read_sql_query(query3, conn)
df3.to_csv('powerbi_03_telemedicine_adoption.csv', index=False)
print(f"✓ Exported: powerbi_03_telemedicine_adoption.csv ({len(df3)} rows)")

# Query 4: Startup Ecosystem
print("[4/8] Healthcare Startup Ecosystem Analysis...")
query4 = """
WITH startup_metrics AS (
    SELECT 
        sector,
        COUNT(*) as total_companies,
        SUM(funding_raised) as total_funding_crores,
        AVG(funding_raised) as avg_funding_per_company,
        COUNT(CASE WHEN status = 'Operating' THEN 1 END) as operating_companies,
        COUNT(CASE WHEN status IN ('Acquired', 'IPO') THEN 1 END) as exited_companies,
        COUNT(CASE WHEN status = 'Defunct' THEN 1 END) as defunct_companies,
        MIN(founding_year) as oldest_company_year,
        MAX(founding_year) as newest_company_year
    FROM healthcare_companies
    GROUP BY sector
)
SELECT 
    sector,
    total_companies,
    total_funding_crores,
    ROUND(avg_funding_per_company, 2) as avg_funding_crores,
    operating_companies,
    exited_companies,
    defunct_companies,
    ROUND((exited_companies * 100.0 / total_companies), 1) as exit_rate_pct,
    ROUND((operating_companies * 100.0 / total_companies), 1) as operating_rate_pct,
    (2024 - oldest_company_year) as sector_maturity_years,
    CASE 
        WHEN (exited_companies * 1.0 / total_companies) > 0.5 THEN 'Mature (High Exit Rate)'
        WHEN total_funding_crores > 500 THEN 'Well Funded'
        WHEN total_companies > 3 THEN 'Crowded'
        ELSE 'Early Stage'
    END as sector_stage
FROM startup_metrics
ORDER BY total_funding_crores DESC;
"""
df4 = pd.read_sql_query(query4, conn)
df4.to_csv('powerbi_04_startup_ecosystem.csv', index=False)
print(f"✓ Exported: powerbi_04_startup_ecosystem.csv ({len(df4)} rows)")

# Query 5: VC Misalignment
print("[5/8] VC Misalignment - Funding vs Need...")
# Using pandas to create this instead of complex SQL
gap_data = pd.DataFrame({
    'healthcare_segment': ['Telemedicine', 'Diagnostics', 'Hospital Software', 'Medical Financing', 
                           'Affordable Insurance', 'Preventive Care', 'Pharmacy Delivery'],
    'current_vc_focus_score': [8, 7, 5, 2, 3, 2, 6],
    'india2_need_score': [3, 7, 4, 8, 8, 7, 6],
    'tam_billions': [50, 40, 20, 80, 60, 50, 35],
    'funding_raised_crores': [800, 600, 200, 150, 100, 50, 400]
})
gap_data['investment_gap_score'] = gap_data['india2_need_score'] - gap_data['current_vc_focus_score']
gap_data['penetration_pct'] = (gap_data['funding_raised_crores'] / gap_data['tam_billions'] * 100).round(2)
gap_data['investment_status'] = gap_data['investment_gap_score'].apply(
    lambda x: 'MASSIVELY UNDERINVESTED' if x > 4 else ('Underinvested' if x > 2 else ('Overinvested' if x < 0 else 'Well Balanced'))
)
gap_data['strategic_implication'] = gap_data.apply(
    lambda row: 'BIGGEST OPPORTUNITY' if row['investment_gap_score'] > 4 else ('Solving Wrong Problem' if row['current_vc_focus_score'] > row['india2_need_score'] else 'Aligned'),
    axis=1
)
gap_data.to_csv('powerbi_05_vc_misalignment.csv', index=False)
print(f"✓ Exported: powerbi_05_vc_misalignment.csv ({len(gap_data)} rows)")

# Query 6: Segment Comparison
print("[6/8] Segment Comparison Scorecard...")
query6 = """
SELECT 
    income_segment,
    year,
    healthcare_spend_pct_income,
    out_of_pocket_pct,
    insurance_coverage_pct,
    medical_loan_usage_pct,
    household_catastrophic_health_exp_pct,
    CASE 
        WHEN income_segment = 'India1' THEN 1
        WHEN income_segment = 'India2' THEN 2
        WHEN income_segment = 'India3' THEN 3
    END as segment_ranking,
    CASE 
        WHEN income_segment = 'India1' THEN 'Affluent - Can afford healthcare'
        WHEN income_segment = 'India2' THEN 'Missing Middle - Affordability crisis'
        WHEN income_segment = 'India3' THEN 'Low income - Govt schemes help'
    END as segment_description,
    CASE 
        WHEN income_segment = 'India2' AND household_catastrophic_health_exp_pct > 50 
        THEN 'YES - CRITICAL OPPORTUNITY'
        ELSE 'NO'
    END as is_critical_opportunity
FROM healthcare_spending
ORDER BY year DESC, segment_ranking;
"""
df6 = pd.read_sql_query(query6, conn)
df6.to_csv('powerbi_06_segment_comparison.csv', index=False)
print(f"✓ Exported: powerbi_06_segment_comparison.csv ({len(df6)} rows)")

# Query 7: KPI Metrics
print("[7/8] KPI Metrics Summary...")
kpi_data = pd.DataFrame({
    'metric_name': [
        'India2 Population', 'Insurance Coverage Gap', 'Out-of-Pocket Burden',
        'Catastrophic Health Exp', 'Telemedicine Adoption India2', 
        'Medical Financing Funding', 'Affordable Insurance Funding',
        'Healthcare Startup Total Funding'
    ],
    'metric_value': ['490', '60', '65', '58', '12', '150', '100', '2465'],
    'unit': ['Millions', 'percentage points', 'percent of costs', 'percent of households',
             'percent', 'Crores', 'Crores', 'Crores'],
    'context': ['35% of India', 'India1: 75% vs India2: 15%', 'vs 35% in India1',
                'vs 2% in India1', 'Plateauing since 2022', 'vs 800Cr in Telemedicine',
                'vs 8Cr needed for India2', '10 companies']
})
kpi_data.to_csv('powerbi_07_kpi_metrics.csv', index=False)
print(f"✓ Exported: powerbi_07_kpi_metrics.csv ({len(kpi_data)} rows)")

# Query 8: Detailed Company Data
print("[8/8] Detailed Company Data...")
query8 = """
SELECT 
    company_name,
    sector,
    founding_year,
    status,
    funding_raised as funding_crores,
    employees,
    revenue_annual as annual_revenue_crores,
    headquarters,
    CASE 
        WHEN status = 'Operating' THEN 'Active'
        WHEN status IN ('Acquired', 'IPO') THEN 'Exited'
        WHEN status = 'Defunct' THEN 'Failed'
    END as company_status,
    CASE 
        WHEN sector LIKE '%Telemedicine%' OR sector LIKE '%Pharmacy%' THEN 'India1 Focused'
        WHEN sector LIKE '%Medical Financing%' OR sector LIKE '%Insurance%' THEN 'India2 Opportunity'
        ELSE 'Other'
    END as market_segment,
    (2024 - founding_year) as years_in_operation,
    CASE 
        WHEN funding_raised > 500 THEN 'Well Funded'
        WHEN funding_raised > 100 THEN 'Moderate Funding'
        ELSE 'Early Stage'
    END as funding_stage
FROM healthcare_companies
ORDER BY funding_raised DESC;
"""
df8 = pd.read_sql_query(query8, conn)
df8.to_csv('powerbi_08_company_details.csv', index=False)
print(f"✓ Exported: powerbi_08_company_details.csv ({len(df8)} rows)")

conn.close()

print("\n" + "=" * 80)
print("ALL QUERIES EXECUTED SUCCESSFULLY")
print("=" * 80)
print("""
CSV Files created (ready for Power BI):
1. powerbi_01_spending_trends.csv
2. powerbi_02_insurance_gap.csv
3. powerbi_03_telemedicine_adoption.csv
4. powerbi_04_startup_ecosystem.csv
5. powerbi_05_vc_misalignment.csv
6. powerbi_06_segment_comparison.csv
7. powerbi_07_kpi_metrics.csv
8. powerbi_08_company_details.csv

NEXT STEP: Import these files into Power BI Desktop
""")
