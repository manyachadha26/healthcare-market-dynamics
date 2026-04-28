import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Set page config
st.set_page_config(
    page_title="Healthcare Market Dynamics",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 0rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    h1 {
        color: #1f77b4;
    }
    </style>
    """, unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    spending = pd.read_csv('powerbi_01_spending_trends.csv')
    insurance = pd.read_csv('powerbi_02_insurance_gap.csv')
    telemedicine = pd.read_csv('powerbi_03_telemedicine_adoption.csv')
    startups = pd.read_csv('powerbi_04_startup_ecosystem.csv')
    gap = pd.read_csv('powerbi_05_vc_misalignment.csv')
    segment = pd.read_csv('powerbi_06_segment_comparison.csv')
    kpi = pd.read_csv('powerbi_07_kpi_metrics.csv')
    companies = pd.read_csv('powerbi_08_company_details.csv')
    return spending, insurance, telemedicine, startups, gap, segment, kpi, companies

spending, insurance, telemedicine, startups, gap, segment, kpi, companies = load_data()

# Sidebar navigation
st.sidebar.title("📊 Healthcare Analytics")
page = st.sidebar.radio(
    "Select Page:",
    ["🎯 Key Metrics", "💰 Spending Analysis", "📱 Telemedicine Adoption", 
     "🚀 Startup Ecosystem", "⚠️ The Gap: VC Focus vs India2 Need"]
)

# ============================================================================
# PAGE 1: KEY METRICS
# ============================================================================
if page == "🎯 Key Metrics":
    st.title("🏥 Healthcare Market Dynamics: Key Metrics")
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="India2 Population",
            value="490M",
            delta="35% of India",
            delta_color="off"
        )
    
    with col2:
        st.metric(
            label="Insurance Gap",
            value="60%",
            delta="India1: 75% vs India2: 15%",
            delta_color="inverse"
        )
    
    with col3:
        st.metric(
            label="Out-of-Pocket Burden",
            value="65%",
            delta="vs 35% in India1",
            delta_color="inverse"
        )
    
    with col4:
        st.metric(
            label="Catastrophic Health Exp",
            value="58%",
            delta="vs 2% in India1",
            delta_color="inverse"
        )
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Key Findings")
        st.markdown("""
        **The Missing Middle Problem:**
        - India2 (490M people) has massive healthcare affordability crisis
        - 58% face catastrophic health expenditure
        - Only 15% have insurance coverage
        - 65% pay out-of-pocket (vs 35% in India1)
        
        **Investment Opportunity:**
        - Medical financing is underinvested (<₹150Cr funded)
        - Affordable insurance solutions needed
        - Diagnostics adoption at only 28% (vs 45% overall)
        """)
    
    with col2:
        st.subheader("📊 Segment Overview")
        segment_2023 = segment[segment['year'] == 2023]
        fig = go.Figure()
        
        for idx, row in segment_2023.iterrows():
            fig.add_trace(go.Bar(
                name=row['segment_description'],
                x=['Insurance Coverage %', 'Out-of-Pocket %', 'Catastrophic Health Exp %'],
                y=[
                    row['insurance_coverage_pct'],
                    row['out_of_pocket_pct'],
                    row['household_catastrophic_health_exp_pct']
                ]
            ))
        
        fig.update_layout(height=400, title="Healthcare Metrics by Segment (2023)")
        st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# PAGE 2: SPENDING ANALYSIS
# ============================================================================
elif page == "💰 Spending Analysis":
    st.title("💰 Healthcare Spending & Insurance Gap Analysis")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Insurance Coverage by Segment (2023)")
        spending_2023 = spending[spending['year'] == 2023]
        fig = px.bar(
            spending_2023,
            x='income_segment',
            y='insurance_coverage_pct',
            color='income_segment',
            title="Insurance Coverage % by Segment",
            labels={'income_segment': 'Income Segment', 'insurance_coverage_pct': 'Coverage %'},
            color_discrete_map={'India1': '#1f77b4', 'India2': '#ff7f0e', 'India3': '#2ca02c'}
        )
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Out-of-Pocket Payment Burden (2023)")
        fig = px.bar(
            spending_2023,
            x='income_segment',
            y='out_of_pocket_pct',
            color='income_segment',
            title="OOP Burden % by Segment",
            labels={'income_segment': 'Income Segment', 'out_of_pocket_pct': 'OOP %'},
            color_discrete_map={'India1': '#1f77b4', 'India2': '#ff7f0e', 'India3': '#2ca02c'}
        )
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.subheader("📈 Insurance Coverage Trend (2021-2023)")
    
    fig = go.Figure()
    for segment_name in spending['income_segment'].unique():
        segment_data = spending[spending['income_segment'] == segment_name].sort_values('year')
        fig.add_trace(go.Scatter(
            x=segment_data['year'],
            y=segment_data['insurance_coverage_pct'],
            mode='lines+markers',
            name=segment_name,
            line=dict(width=3)
        ))
    
    fig.update_layout(
        title="Insurance Coverage Trend by Segment",
        xaxis_title="Year",
        yaxis_title="Insurance Coverage %",
        height=400,
        hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.subheader("📊 Detailed Insurance Gap Analysis")
    
    insurance_display = insurance[['state', 'income_segment', 'insurance_coverage_pct', 'gap_severity', 'year']].sort_values('year', ascending=False)
    st.dataframe(insurance_display, use_container_width=True)

# ============================================================================
# PAGE 3: TELEMEDICINE ADOPTION
# ============================================================================
elif page == "📱 Telemedicine Adoption":
    st.title("📱 Telemedicine Adoption Trends")
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Adoption Trend by Segment (2021-2023)")
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=telemedicine['year'],
            y=telemedicine['segment_1_adoption'],
            mode='lines+markers',
            name='India1 (Affluent)',
            line=dict(color='#1f77b4', width=3)
        ))
        fig.add_trace(go.Scatter(
            x=telemedicine['year'],
            y=telemedicine['segment_2_adoption'],
            mode='lines+markers',
            name='India2 (Missing Middle)',
            line=dict(color='#ff7f0e', width=3)
        ))
        fig.add_trace(go.Scatter(
            x=telemedicine['year'],
            y=telemedicine['segment_3_adoption'],
            mode='lines+markers',
            name='India3 (Low Income)',
            line=dict(color='#2ca02c', width=3)
        ))
        
        fig.update_layout(
            title="Telemedicine Adoption % Over Time",
            xaxis_title="Year",
            yaxis_title="Adoption %",
            height=400,
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Key Insight")
        st.markdown("""
        **India2 Adoption Plateauing:**
        - 2021: 8%
        - 2022: 10%
        - 2023: 12%
        
        **Growth:** Only +2% per year
        
        **Status:** 
        🔴 **PLATEAUING** - Not accelerating
        
        **Implication:**
        Telemedicine is luxury for India1, not essential for India2
        """)
    
    st.markdown("---")
    st.subheader("Adoption Status by Segment")
    
    telemedicine_display = telemedicine[['year', 'segment_1_adoption', 'segment_2_adoption', 'segment_3_adoption', 'adoption_status', 'adoption_trajectory']]
    st.dataframe(telemedicine_display, use_container_width=True)

# ============================================================================
# PAGE 4: STARTUP ECOSYSTEM
# ============================================================================
elif page == "🚀 Startup Ecosystem":
    st.title("🚀 Healthcare Startup Ecosystem")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Funding by Sector")
        fig = px.bar(
            startups.sort_values('total_funding_crores', ascending=False),
            x='sector',
            y='total_funding_crores',
            color='total_funding_crores',
            title="Total Funding Raised by Sector",
            labels={'total_funding_crores': 'Funding (₹Cr)', 'sector': 'Healthcare Sector'},
            color_continuous_scale='Blues'
        )
        fig.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Company Status Distribution")
        status_data = {
            'Operating': startups['operating_companies'].sum(),
            'Exited': startups['exited_companies'].sum(),
            'Defunct': startups['defunct_companies'].sum()
        }
        fig = px.pie(
            values=list(status_data.values()),
            names=list(status_data.keys()),
            title="Healthcare Companies by Status",
            color_discrete_map={'Operating': '#2ca02c', 'Exited': '#1f77b4', 'Defunct': '#d62728'}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.subheader("📊 Detailed Startup Metrics")
    
    startups_display = startups[['sector', 'total_companies', 'total_funding_crores', 'operating_companies', 'exited_companies', 'sector_stage']]
    st.dataframe(startups_display, use_container_width=True)
    
    st.markdown("---")
    st.subheader("🏢 Company Details")
    
    companies_display = companies[['company_name', 'sector', 'funding_crores', 'status', 'market_segment', 'funding_stage']]
    st.dataframe(companies_display, use_container_width=True)

# ============================================================================
# PAGE 5: THE GAP - VC FOCUS VS INDIA2 NEED
# ============================================================================
elif page == "⚠️ The Gap: VC Focus vs India2 Need":
    st.title("⚠️ VC Investment Misalignment: Where Capital Should Flow")
    st.markdown("---")
    
    st.subheader("The Problem: VC Focus vs Actual India2 Need")
    st.markdown("""
    VCs are investing in "sexy" problems (Telemedicine, Diagnostics)
    but ignoring the REAL opportunity where India2 has massive unmet need.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Investment Gap Visualization")
        fig = px.scatter(
            gap,
            x='current_vc_focus_score',
            y='india2_need_score',
            size='funding_raised_crores',
            hover_name='healthcare_segment',
            color='investment_status',
            title="VC Focus (X) vs India2 Need (Y)",
            labels={
                'current_vc_focus_score': 'Current VC Focus Score',
                'india2_need_score': 'India2 Need Score',
                'funding_raised_crores': 'Funding (₹Cr)'
            },
            color_discrete_map={
                'MASSIVELY UNDERINVESTED': '#d62728',
                'Underinvested': '#ff7f0e',
                'Well Balanced': '#2ca02c',
                'Overinvested': '#1f77b4'
            }
        )
        
        # Add diagonal line (ideal alignment)
        fig.add_shape(type="line",
            x0=0, y0=0, x1=10, y1=10,
            line=dict(color="gray", width=2, dash="dash"),
            name="Perfect Alignment"
        )
        
        fig.update_layout(height=500, hovermode='closest')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🔴 BIGGEST OPPORTUNITIES (Underinvested)")
        
        underinvested = gap[gap['investment_status'] == 'MASSIVELY UNDERINVESTED'].sort_values('investment_gap_score', ascending=False)
        
        for idx, row in underinvested.iterrows():
            st.markdown(f"""
            **{row['healthcare_segment']}**
            - VC Focus Score: {row['current_vc_focus_score']}/10
            - India2 Need Score: {row['india2_need_score']}/10
            - Gap: {row['investment_gap_score']} points
            - TAM: ₹{row['tam_billions']}B
            - Current Funding: ₹{row['funding_raised_crores']}Cr
            - Penetration: {row['penetration_pct']:.2f}%
            
            **Status:** {row['strategic_implication']}
            """)
            st.divider()
    
    st.markdown("---")
    st.subheader("📊 Complete Gap Analysis Table")
    
    gap_display = gap[['healthcare_segment', 'current_vc_focus_score', 'india2_need_score', 
                       'investment_gap_score', 'tam_billions', 'funding_raised_crores', 
                       'investment_status', 'strategic_implication']]
    st.dataframe(gap_display, use_container_width=True)
    
    st.markdown("---")
    st.subheader("💡 Key Insight")
    st.markdown("""
    **Medical Financing** is the biggest gap:
    - VC Focus: 2/10 (almost ignored)
    - India2 Need: 8/10 (critical need)
    - Gap Score: 6 (MASSIVELY UNDERINVESTED)
    - TAM: ₹80B
    - Current Funding: ₹150Cr (0.19% of TAM)
    
    **This is where the real opportunity is.**
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Healthcare Market Dynamics Analysis | Data-driven insights for healthcare investing</p>
    <p><small>Built with Streamlit | SQL + Python | Advanced Data Analytics</small></p>
</div>
""", unsafe_allow_html=True)