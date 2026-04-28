-- HEALTHCARE MARKET DYNAMICS - ADVANCED SQL QUERIES FOR POWER BI
-- Shows: JOINs, CTEs, Window Functions, Aggregations, Calculations

-- ============================================================================
-- QUERY 1: SPENDING COMPARISON WITH TRENDS (Shows CTEs + Window Functions)
-- ============================================================================

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

-- ============================================================================
-- QUERY 2: INSURANCE COVERAGE GAP ANALYSIS (Shows JOINs + Calculations)
-- ============================================================================

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
ORDER BY i.year DESC, i.income_segment, i.insurance_gap_pct DESC;

-- ============================================================================
-- QUERY 3: TELEMEDICINE ADOPTION & TREND ANALYSIS (Shows Window Functions)
-- ============================================================================

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
    END as adoption_status,
    recency_rank
FROM adoption_analysis
ORDER BY year DESC;

-- ============================================================================
-- QUERY 4: HEALTHCARE STARTUP ECOSYSTEM ANALYSIS (Shows Aggregation + CTEs)
-- ============================================================================

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
    ROUND((exited_companies::float / total_companies * 100), 1) as exit_rate_pct,
    ROUND((operating_companies::float / total_companies * 100), 1) as operating_rate_pct,
    (2024 - oldest_company_year) as sector_maturity_years,
    CASE 
        WHEN (exited_companies::float / total_companies) > 0.5 THEN 'Mature (High Exit Rate)'
        WHEN total_funding_crores > 500 THEN 'Well Funded'
        WHEN total_companies > 3 THEN 'Crowded'
        ELSE 'Early Stage'
    END as sector_stage,
    RANK() OVER (ORDER BY total_funding_crores DESC) as funding_rank
FROM startup_metrics
ORDER BY total_funding_crores DESC;

-- ============================================================================
-- QUERY 5: VC MISALIGNMENT - FUNDING VS NEED (Shows Business Logic)
-- ============================================================================

WITH opportunity_analysis AS (
    SELECT 
        'Telemedicine' as healthcare_segment,
        8 as current_vc_focus_score,
        3 as india2_need_score,
        50 as tam_billions,
        800 as funding_raised_crores
    UNION ALL
    SELECT 'Diagnostics', 7, 7, 40, 600
    UNION ALL
    SELECT 'Hospital Software', 5, 4, 20, 200
    UNION ALL
    SELECT 'Medical Financing', 2, 8, 80, 150
    UNION ALL
    SELECT 'Affordable Insurance', 3, 8, 60, 100
    UNION ALL
    SELECT 'Preventive Care', 2, 7, 50, 50
    UNION ALL
    SELECT 'Pharmacy Delivery', 6, 6, 35, 400
)
SELECT 
    healthcare_segment,
    current_vc_focus_score,
    india2_need_score,
    (india2_need_score - current_vc_focus_score) as investment_gap_score,
    tam_billions,
    funding_raised_crores,
    ROUND((funding_raised_crores / tam_billions * 100), 2) as penetration_pct,
    CASE 
        WHEN (india2_need_score - current_vc_focus_score) > 4 THEN 'MASSIVELY UNDERINVESTED'
        WHEN (india2_need_score - current_vc_focus_score) > 2 THEN 'Underinvested'
        WHEN (india2_need_score - current_vc_focus_score) < 0 THEN 'Overinvested'
        ELSE 'Well Balanced'
    END as investment_status,
    CASE 
        WHEN current_vc_focus_score > india2_need_score THEN 'Solving Wrong Problem'
        WHEN (india2_need_score - current_vc_focus_score) > 4 THEN 'BIGGEST OPPORTUNITY'
        ELSE 'Aligned'
    END as strategic_implication
FROM opportunity_analysis
ORDER BY investment_gap_score DESC;

-- ============================================================================
-- QUERY 6: SEGMENT COMPARISON SCORECARD (Shows CASE Statements + Metrics)
-- ============================================================================

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
    END as is_critical_opportunity,
    ROUND((out_of_pocket_pct - 35) / 35 * 100, 1) as oop_burden_vs_india1_pct
FROM healthcare_spending
ORDER BY year DESC, 
    CASE 
        WHEN income_segment = 'India1' THEN 1
        WHEN income_segment = 'India2' THEN 2
        WHEN income_segment = 'India3' THEN 3
    END;

-- ============================================================================
-- QUERY 7: KEY METRICS SUMMARY (For KPI Cards)
-- ============================================================================

SELECT 
    'India2 Population' as metric_name,
    '490' as metric_value,
    'Millions' as unit,
    '35% of India' as context
UNION ALL
SELECT 'Insurance Coverage Gap', '60', 'percentage points', 'India1: 75% vs India2: 15%'
UNION ALL
SELECT 'Out-of-Pocket Burden', '65', 'percent of costs', 'vs 35% in India1'
UNION ALL
SELECT 'Catastrophic Health Exp', '58', 'percent of households', 'vs 2% in India1'
UNION ALL
SELECT 'Telemedicine Adoption India2', '12', 'percent', 'Plateauing since 2022'
UNION ALL
SELECT 'Medical Financing Funding', '150', 'Crores', 'vs 800Cr in Telemedicine'
UNION ALL
SELECT 'Affordable Insurance Funding', '100', 'Crores', 'vs 8Cr needed for India2'
UNION ALL
SELECT 'Healthcare Startup Total Funding', '2465', 'Crores', '10 companies'
ORDER BY metric_name;

-- ============================================================================
-- QUERY 8: DETAILED COMPANY DATA (For Power BI Table)
-- ============================================================================

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

-- ============================================================================
-- NOTES FOR POWER BI
-- ============================================================================
-- These queries are designed to be imported into Power BI as:
-- 1. Direct SQL queries (if using SQL Server/Database connection)
-- 2. Or results exported to CSV and imported as data sources
--
-- Key features demonstrated:
-- ✓ CTEs (Common Table Expressions) - Query 1, 4, 5
-- ✓ Window Functions - Query 1, 3, 4
-- ✓ JOINs - Query 2
-- ✓ Aggregation Functions - Query 4
-- ✓ CASE Statements - Query 5, 6, 8
-- ✓ Ranking/Row Numbering - Query 4
-- ✓ Complex calculations - Query 2, 5
-- ✓ Business logic - Query 5, 6, 7
--
-- These form the data layer for Power BI calculations and visualizations
