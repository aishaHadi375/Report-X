import streamlit as st
import pandas as pd
from datetime import datetime
import time
import asyncio
from data_processor import DataProcessor
from anomalies import AnomalyDetector
from summarize import TrendAnalyzer
from business_insight import BusinessInsightGenerator
from ai_report_generator import AIReportGenerator
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import time
# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="REPORT-X | AI Workflow Engine",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)
# 2. PROFESSIONAL THEME INJECTION
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=JetBrains+Mono:wght@400;600&display=swap');

    :root {
        --bg-primary: #0a0e1a;
        --bg-card: #141b2d;
        --accent-gradient: linear-gradient(135deg, #00ff88 0%, #00d4ff 100%);
        --text-primary: #f0f4ff;
        --text-secondary: #8892b0;
        --border-color: #1e2a45;
        --glow-green: #00ff88;
    }

    .stApp { background-color: var(--bg-primary); font-family: 'Inter', sans-serif; color: var(--text-primary); }

    /* Glowy Headings */
    h1, h2, h3, h4, h5 {
        background: linear-gradient(135deg, #00ff88, #00d4ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        text-shadow: 0 0 8px rgba(0,255,136,0.6);
    }

    /* Glass Cards */
    .glass-card {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 25px;
        margin-bottom: 15px;
    }

    /* Professional Buttons with Green Glow */
    .stButton > button {
        background: var(--accent-gradient) !important;
        color: #000 !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 8px !important;
        width: 100%;
        transition: 0.3s ease;
        box-shadow: 0 0 15px rgba(0, 255, 136, 0.5);
    }
    .stButton > button:hover { transform: translateY(-2px); box-shadow: 0 0 25px rgba(0, 255, 136, 0.8); }

    /* File Uploader Box */
    [data-testid="stFileUploader"] {
        background-color: #0d1117;
        border: 2px dashed #1e2a45;
        border-radius: 12px;
        padding: 40px !important;
    }

    /* Hide default button in uploader */
    [data-testid="stFileUploader"] section > button {
        display: none;
    }

    /* Feature Cards */
    .feature-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 20px;
        margin-top: 30px;
    }
    .feature-card {
        background-color: #0d1117;
        border: 1px solid #1e2a45;
        border-radius: 12px;
        padding: 30px;
        transition: transform 0.2s;
    }
    .feature-card:hover { border-color: #00ff88; transform: translateY(-5px); }
    .feature-icon {
        background-color: rgba(0, 255, 136, 0.1);
        width: 50px;
        height: 50px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 20px;
        font-size: 24px;
        color: #00ff88;
    }

    /* Metrics / Timer / Sections */
    .analysis-heading {
        color: #00ff88;
        font-size: 1.5rem;
        font-weight: 700;
        margin-top: 2rem;
        text-shadow: 0 0 8px rgba(0,255,136,0.6);
    }
    /* Metric Card Styling */
    .metric-container {
        display: flex;
        gap: 15px;
        margin: 20px 0;
    }
    .metric-card {
        background: #0d1619; /* Darker background */
        border: 1px solid #1e2a45;
        border-radius: 12px;
        padding: 20px;
        flex: 1;
        min-width: 200px;
    }
    .metric-container {
        display: flex;
        gap: 15px;
        margin-bottom: 25px;
    }
    .metric-card-styled {
        background: #0d121f;
        border: 1px solid #00ff88; /* Green border */
        border-radius: 12px;
        padding: 20px;
        flex: 1;
    }
    .metric-card-styled.gold {
        border-color: #f1c40f; /* Gold/Yellow border */
    }
    .metric-icon-box {
        width: 35px;
        height: 35px;
        background: rgba(255,255,255,0.05);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 15px;
    }
    .val-text {
        font-size: 2rem;
        font-weight: 800;
        color: white;
        margin: 0;
    }
    .label-text {
        color: #8892b0;
        font-size: 1 rem;
    }

    .output-section h2 { color: #00ff88 !important; text-shadow: 0 0 8px rgba(0,255,136,0.6); }
    .timer-badge { background-color:#0d1117; border:1px solid #00ff88; padding:5px 10px; border-radius:12px; font-weight:700; }

</style>
""", unsafe_allow_html=True)

# BRANDING
st.markdown("""
<div style="display: flex; align-items: center; gap: 15px;">
    <div style="background: linear-gradient(135deg, #00ff88 0%, #00d4ff 100%); padding: 10px; border-radius: 12px; font-size: 24px;">📄</div>
    <div style="font-size: 1.8rem; font-weight: 800; letter-spacing: 2px; background: linear-gradient(135deg, #00ff88 0%, #00d4ff 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">REPORT-X</div>
</div>
<div style="text-align: center; padding: 40px 0;">
    <h1 style="font-size: 3.5rem; font-weight: 800; margin-bottom: 10px; color: white;">AI <span style="background: linear-gradient(135deg, #00ff88 0%, #00d4ff 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Workflow and Report Generation</span> Engine</h1>
    <p style="color: #8892b0; font-size: 1.2rem;">Enterprise Intelligence & Automated Reporting</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'data_processor' not in st.session_state:
    st.session_state.data_processor = None
if 'current_df' not in st.session_state:
    st.session_state.current_df = None
if 'original_df' not in st.session_state:
    st.session_state.original_df = None
if 'show_trends' not in st.session_state:
    st.session_state.show_trends = False
if 'show_anomalies' not in st.session_state:
    st.session_state.show_anomalies = False
if 'show_actions' not in st.session_state:
    st.session_state.show_actions = False
if 'show_report' not in st.session_state:
    st.session_state.show_report = False
if 'execution_times' not in st.session_state:
    st.session_state.execution_times = {}
if 'cleaning_performed' not in st.session_state:
    st.session_state.cleaning_performed = False
if 'generated_report' not in st.session_state:
    st.session_state.generated_report = None

\
# NEW: Auto-cleaning function
def auto_clean_data(df, processor):
    """Automatically clean data based on detected issues"""
    cleaning_summary = []
    
    # Check for issues
    missing_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
    dup_count = df.duplicated().sum()
    
    needs_cleaning = False
    
    # Decision logic for auto-cleaning
    if dup_count > 0:
        needs_cleaning = True
        cleaning_summary.append(f"🔧 Removed {dup_count} duplicate records")
    
    if missing_pct > 5:
        needs_cleaning = True
        # Drop columns with >70% missing
        cols_to_drop = [col for col in df.columns if df[col].isnull().sum() / len(df) > 0.7]
        if cols_to_drop:
            cleaning_summary.append(f"🔧 Removed {len(cols_to_drop)} columns with >70% missing data")
    
    if needs_cleaning:
        # Perform cleaning
        report = processor.clean_data(
            remove_duplicates=True,
            handle_missing='drop_cols',
            missing_threshold=0.7,
            remove_outliers=False
        )
        
        return processor.processed_df, cleaning_summary, True
    
    return df, ["✅ Data is already clean - no automatic cleaning needed"], False

# File upload section with Quick Guide
st.markdown("<h3 style='color:#00ff99'>Quick Guide</h3>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div style='
        background-color:#141a2b;
        border-radius:12px;
        padding:20px;
        text-align:center;
        border:1px solid #1e2a40'>
        <h2 style='color:#00ff99'>1</h2>
        <p style='font-weight:600'>Upload CSV</p>
        <p style='color:#a0aec0'>Select your data file</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='
        background-color:#141a2b;
        border-radius:12px;
        padding:20px;
        text-align:center;
        border:1px solid #1e2a40'>
        <h2 style='color:#00ff99'>2</h2>
        <p style='font-weight:600'>Auto-Clean</p>
        <p style='color:#a0aec0'>Remove duplicates & fix data</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style='
        background-color:#141a2b;
        border-radius:12px;
        padding:20px;
        text-align:center;
        border:1px solid #1e2a40'>
        <h2 style='color:#00ff99'>3</h2>
        <p style='font-weight:600'>Analyze</p>
        <p style='color:#a0aec0'>Choose your analysis type</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div style='
        background-color:#141a2b;
        border-radius:12px;
        padding:20px;
        text-align:center;
        border:1px solid #1e2a40'>
        <h2 style='color:#00ff99'>4</h2>
        <p style='font-weight:600'>Export</p>
        <p style='color:#a0aec0'>Download insights & reports</p>
    </div>
    """, unsafe_allow_html=True)


# -------------------- FILE UPLOAD (Visual Implementation) --------------------
st.markdown("<h3 style='color:#ffffff; margin-bottom:20px;'>📂 Upload Your Data</h3>", unsafe_allow_html=True)

# The actual file uploader (hidden UI but functional)
uploaded_file = st.file_uploader("", type=['csv'], key="file_upload_ui")

# The visual "dotted box" overlay
if not uploaded_file:
    st.markdown("""
        <div style="text-align: center; margin-top: -120px; pointer-events: none;">
            <div style="color: #00ff88; font-size: 40px; margin-bottom: 10px;">↑</div>
            <div style="color: #00ff88; font-weight: bold; font-size: 1.1rem;">Click to upload <span style="color: #ffffff">or drag and drop</span></div>
            <div style="color: #8892b0; font-size: 0.85rem; margin-top: 5px;">CSV files only</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Hero Text below the uploader
    st.markdown("""
        <div style="text-align: center; margin-top: 100px; margin-bottom: 60px;">
            <h1 style="font-size: 3.5rem; font-weight: 800; color: white;">Transform Your Data Into <span style="color: #00ff88;">Actionable Insights</span></h1>
            <p style="color: #8892b0; font-size: 1.2rem; max-width: 800px; margin: 20px auto;">Upload your CSV file to unlock powerful AI-driven analysis, trend detection, and business recommendations.</p>
        </div>
    """, unsafe_allow_html=True)

    # -------------------- FEATURE GRID (Visual Implementation) --------------------
    st.markdown("""
    <div class="feature-container">
        <div class="feature-card">
            <div class="feature-icon">✩</div>
            <div class="feature-title">Summarize Trends</div>
            <div class="feature-desc">Get instant overview of your data patterns, metrics performance, and key trends.</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">✩</div>
            <div class="feature-title">Identify Anomalies</div>
            <div class="feature-desc">Automatically detect unusual values, missing data, and quality issues.</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">✩</div>
            <div class="feature-title">Business Actions</div>
            <div class="feature-desc">Receive prioritized, actionable recommendations with clear timelines.</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">✩</div>
            <div class="feature-title">AI Reports</div>
            <div class="feature-desc">Generate comprehensive business intelligence reports automatically.</div>
        </div>
    </div>

    """, unsafe_allow_html=True)
if uploaded_file and st.session_state.data_processor is None:
    # (Keep your existing data processing logic here)
    processor = DataProcessor()
    df = processor.load_data(uploaded_file)
    st.session_state.original_df = df.copy()
    cleaned_df, cleaning_summary, was_cleaned = auto_clean_data(df, processor)
    st.session_state.data_processor = processor
    st.session_state.current_df = cleaned_df
    st.session_state.cleaning_summary = cleaning_summary
    st.session_state.cleaning_performed = was_cleaned
    st.rerun()

# -------------------- ACTION BUTTONS (AFTER UPLOAD) --------------------
if st.session_state.current_df is not None:
    st.markdown("---")
    st.markdown("### 🎯 Choose Your Analysis")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("📈 Summarize Trends", type="primary", use_container_width=True, key="btn_trends"):
            st.session_state.show_trends = True
            st.session_state.show_anomalies = False
            st.session_state.show_actions = False
            st.session_state.show_report = False
            st.rerun()
    with col2:
        if st.button("🔍 Identify Anomalies", type="primary", use_container_width=True, key="btn_anomalies"):
            st.session_state.show_trends = False
            st.session_state.show_anomalies = True
            st.session_state.show_actions = False
            st.session_state.show_report = False
            st.rerun()
    with col3:
        if st.button("💡 Suggest Business Actions", type="primary", use_container_width=True, key="btn_actions"):
            st.session_state.show_trends = False
            st.session_state.show_anomalies = False
            st.session_state.show_actions = True
            st.session_state.show_report = False
            st.rerun()
    with col4:
        if st.button("📄 Generate AI Report", type="primary", use_container_width=True, key="btn_report"):
            st.session_state.show_trends = False
            st.session_state.show_anomalies = False
            st.session_state.show_actions = False
            st.session_state.show_report = True
            st.rerun()

# Process uploaded file
if uploaded_file and st.session_state.data_processor is None:
    processor = DataProcessor()
    df = processor.load_data(uploaded_file)
    st.session_state.original_df = df.copy()
    cleaned_df, cleaning_summary, was_cleaned = auto_clean_data(df, processor)
    st.session_state.data_processor = processor
    st.session_state.current_df = cleaned_df
    st.session_state.cleaning_summary = cleaning_summary
    st.session_state.cleaning_performed = was_cleaned

    # Show cleaning summary
    st.markdown("<div class='glass-card'><h4>Data Cleaning Summary</h4>", unsafe_allow_html=True)
    for line in st.session_state.cleaning_summary:
        st.markdown(f"- {line}", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
   
if st.session_state.current_df is not None:
    df = st.session_state.current_df
    
    # Calculation Logic
    total_records = len(df)
    total_fields = len(df.columns)
    
    # Calculate Missing Data %
    total_cells = np.prod(df.shape)
    null_cells = df.isnull().sum().sum()
    missing_pct = (null_cells / total_cells) * 100 if total_cells > 0 else 0
    
    # Calculate Quality Score
    # (100 minus penalty for missing data and duplicates)
    dup_pct = (df.duplicated().sum() / len(df)) * 100 if len(df) > 0 else 0
    quality_score = max(0, 100 - (missing_pct + dup_pct))

    # Display Styled Cards
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-card-styled">
            <div class="metric-icon-box" style="color:#00ff88;">◈</div>
            <p class="val-text">{total_records}</p>
            <p class="label-text">Total Records</p>
        </div>
        <div class="metric-card-styled">
            <div class="metric-icon-box" style="color:#00ff88;">◈</div>
            <p class="val-text">{total_fields}</p>
            <p class="label-text">Data Fields</p>
        </div>
        <div class="metric-card-styled">
            <div class="metric-icon-box" style="color:#00ff88;">◈</div>
            <p class="val-text">{missing_pct:.1f}%</p>
            <p class="label-text">Missing Data</p>
        </div>
        <div class="metric-card-styled gold">
            <div class="metric-icon-box" style="color:#f1c40f;"></div>
            <p class="val-text">{quality_score:.0f}/100</p>
            <p class="label-text">Quality Score</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
# Main analysis output display
if st.session_state.current_df is not None:
    
    # 1. SUMMARIZE TRENDS OUTPUT
    if st.session_state.show_trends:
        start_time = time.time()
        
        with st.spinner("🔄 Analyzing trends and patterns..."):
            df = st.session_state.current_df
            processor = st.session_state.data_processor
            trend_analyzer = TrendAnalyzer(df, processor.column_datatypes)
            
            trends = trend_analyzer.analyze_trends()
            execution_time = time.time() - start_time
            st.session_state.execution_times['trends'] = execution_time
        
        st.markdown(f"""<div class="output-section">
        <h2>📈 Trend Analysis Report</h2>
        <span class="timer-badge">⚡ Generated in {execution_time:.2f} seconds</span>
        </div>""", unsafe_allow_html=True)
       
        
        # Numeric trends
        st.markdown("#### 🔢 Numeric Metrics Performance")
        numeric_trends = trends['numeric_trends']
        
        if numeric_trends:
            trend_data = []
            for col, info in numeric_trends.items():
                trend_emoji = "📈" if info['trend_direction'] == 'increasing' else "📉" if info['trend_direction'] == 'decreasing' else "➡️"
                variability = "High 🔴" if info.get('coefficient_of_variation', 0) > 50 else "Low 🟢"
                
                trend_data.append({
                    "Metric": col.replace('_', ' ').title(),
                    "Average": f"{info['mean']:.2f}",
                    "Range": f"{info['min']:.1f} - {info['max']:.1f}",
                    "Trend": f"{trend_emoji} {info['trend_direction'].title()}",
                    "Variability": variability
                })
            
            st.dataframe(pd.DataFrame(trend_data), use_container_width=True, hide_index=True)
            
            # Key insights
            st.markdown("<div class='analysis-heading'>💡 Key Insights</div>", unsafe_allow_html=True)
            increasing = sum(1 for v in numeric_trends.values() if v['trend_direction'] == 'increasing')
            decreasing = sum(1 for v in numeric_trends.values() if v['trend_direction'] == 'decreasing')
            stable = sum(1 for v in numeric_trends.values() if v['trend_direction'] == 'stable')
            
            col1, col2 = st.columns(2)
            with col1:
                st.success(f"✅ **{increasing} metrics showing growth** - positive momentum detected")
                if decreasing > 0:
                    st.warning(f"⚠️ **{decreasing} metrics declining** - may need attention")
            with col2:
                st.info(f"ℹ️ **{stable} metrics stable** - consistent performance")
        
        # Visualizations
        st.markdown("#### 📊 Visual Analysis")
        
        fig1, insight1 = trend_analyzer.visualize_numeric_distributions(top_n=3)
        if fig1:
            st.plotly_chart(fig1, use_container_width=True)
            with st.expander("📖 How to Read This Chart"):
                st.info(insight1)
        
        fig2, insight2 = trend_analyzer.visualize_correlation_pie()
        if fig2:
            st.plotly_chart(fig2, use_container_width=True)
            with st.expander("📖 How to Read This Chart"):
                st.info(insight2)
        
        fig3, insight3 = trend_analyzer.visualize_categorical_distribution()
        if fig3:
            st.plotly_chart(fig3, use_container_width=True)
            with st.expander("📖 How to Read This Chart"):
                st.info(insight3)
    
    # 2. IDENTIFY ANOMALIES OUTPUT
    elif st.session_state.show_anomalies:
        start_time = time.time()
        
        with st.spinner("🔍 Detecting anomalies and data quality issues..."):
            df = st.session_state.current_df
            processor = st.session_state.data_processor
            anomaly_detector = AnomalyDetector(df, processor.column_datatypes)
            
            anomalies = anomaly_detector.detect_all_anomalies()
            execution_time = time.time() - start_time
            st.session_state.execution_times['anomalies'] = execution_time
        
        st.markdown(f"""<div class="output-section">
        <h2>🔍 Anomaly Detection Report</h2>
        <span class="timer-badge">⚡ Generated in {execution_time:.2f} seconds</span>
        </div>""", unsafe_allow_html=True)
        
        # Overall quality score
        st.markdown("<div class='analysis-heading'>🎯 Overall Data Quality Score</div>", unsafe_allow_html=True)
        fig_quality, insight_quality = anomaly_detector.visualize_data_quality_score()
        if fig_quality:
            col1, col2 = st.columns([1, 2])
            with col1:
                st.plotly_chart(fig_quality, use_container_width=True)
            with col2:
                st.markdown(insight_quality)
        
        st.markdown("---")
        
        # Outliers
        st.markdown("<div class='analysis-heading'>🎯 Unusual Values (Outliers)</div>", unsafe_allow_html=True)
        fig1, insight1 = anomaly_detector.visualize_outliers(top_n=3)
        if fig1:
            st.plotly_chart(fig1, use_container_width=True)
            with st.expander("📖 What This Means"):
                st.info(insight1)
        else:
            st.success(insight1)
        
        # Missing Data
        st.markdown("<div class='analysis-heading'>❓ Missing Information</div>", unsafe_allow_html=True)
        fig2, insight2 = anomaly_detector.visualize_missing_data()
        if fig2:
            st.plotly_chart(fig2, use_container_width=True)
            with st.expander("📖 What This Means"):
                st.info(insight2)
        else:
            st.success(insight2)
        
        # Duplicates
        st.markdown("<div class='analysis-heading'>📋 Duplicate Records</div>", unsafe_allow_html=True)
        fig3, insight3 = anomaly_detector.visualize_duplicate_analysis()
        st.plotly_chart(fig3, use_container_width=True)
        with st.expander("📖 What This Means"):
            st.info(insight3)
        
        # Data Quality Issues Summary
        st.markdown("<div class='analysis-heading'>⚠️ Data Quality Issues</div>", unsafe_allow_html=True)
        quality_issues = anomalies['data_quality_issues']
        
        if quality_issues:
            issues_found = []
            if 'constant_columns' in quality_issues:
                issues_found.append(f"🔴 **Constant Columns:** {', '.join(quality_issues['constant_columns'])} (all values are the same)")
            if 'mostly_missing' in quality_issues:
                issues_found.append(f"🔴 **Mostly Empty:** {', '.join(quality_issues['mostly_missing'])} (>70% missing)")
            if 'high_cardinality' in quality_issues:
                issues_found.append(f"🟡 **Too Many Unique Values:** {', '.join(quality_issues['high_cardinality'])}")
            
            for issue in issues_found:
                st.warning(issue)
        else:
            st.success("✅ No major data quality issues detected!")
    
    # 3. SUGGEST BUSINESS ACTIONS OUTPUT
    elif st.session_state.show_actions:
        start_time = time.time()
        
        with st.spinner("💡 Generating actionable business recommendations..."):
            df = st.session_state.current_df
            processor = st.session_state.data_processor
            trend_analyzer = TrendAnalyzer(df, processor.column_datatypes)
            insight_generator = BusinessInsightGenerator(trend_analyzer)
            
            summary = insight_generator.generate_executive_summary()
            actions = insight_generator.generate_business_actions()
            top_3 = insight_generator.generate_top_3_insights()
            
            execution_time = time.time() - start_time
            st.session_state.execution_times['actions'] = execution_time
        
        st.markdown(f"""<div class="output-section">
        <h2>💡 Business Action Plan</h2>
        <span class="timer-badge">⚡ Generated in {execution_time:.2f} seconds</span>
        </div>""", unsafe_allow_html=True)

        # Executive Summary
        st.markdown("<div class='analysis-heading'>📋 Executive Summary</div>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
<div class="summary-dataset">
    <strong>📊 Dataset Overview:</strong><br/>
    - {summary['dataset_size']}<br/>
    - Data Quality: <strong>{summary['data_quality']['score']}%</strong> {summary['data_quality']['grade']}
</div>
<div class="summary-assessment">
    <strong>💡 Assessment:</strong><br/>
    {summary['data_quality']['recommendation']}
</div>
            """, unsafe_allow_html=True)

        with col2:
            metrics_html = "<div class='summary-metrics'><strong>🎯 Key Metrics Status:</strong>"
            metrics_html += "<ul style='margin:0.5rem 0 0 1rem; padding-left:1rem;'>"
            for metric in summary['key_metrics'][:3]:
                metrics_html += f"<li>• <strong>{metric['name']}</strong>: {metric['trend']} (Avg: {metric['average']})</li>"
            metrics_html += "</ul></div>"
            st.markdown(metrics_html, unsafe_allow_html=True)
        
        # Alerts (Immediate Attention) - All under one highlight
        if summary['alerts']:
            alerts_html = "<div class='summary-alerts'><strong>🚨 Immediate Attention Required:</strong><ul>"
            for alert in summary['alerts']:
                alerts_html += f"<li>{alert}</li>"
            alerts_html += "</ul></div>"
            st.markdown(alerts_html, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # TOP 3 PRIORITY ACTIONS
        st.markdown("<div class='analysis-heading'>🎯 TOP 3 PRIORITY ACTIONS</div>", unsafe_allow_html=True)
        
        for i, action in enumerate(top_3, 1):
            priority_color = "#dc3545" if "🔴" in action['Priority'] else "#ffc107" if "🟡" in action['Priority'] else "#28a745"

            with st.container():
                st.markdown(f"""
                <div style="border-left: 5px solid {priority_color}; padding: 1rem; margin: 1rem 0; background: linear-gradient(90deg,#071224 0%, #0b1630 100%); color: #e6f7ff; border-radius: 5px;">
                    <h3 style="margin: 0; color: {priority_color};">#{i}: {action['Action']}</h3>
                    <p style="margin: 0.5rem 0;"><strong>{action['Priority']}</strong> | {action['Category']}</p>
                </div>
                """, unsafe_allow_html=True)

                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"""
**🎯 Why This Matters:**
{action['Reason']}

**💥 Business Impact:**
{action['Impact']}
                    """)

                with col2:
                    st.markdown(f"""
**⚡ Quick Win (Immediate):**
{action['Quick Win']}

**🎯 Long-term Strategy:**
{action['Long Term']}

**✨ Expected Benefit:**
{action['Expected Benefit']}
                    """)

                st.markdown(f"**👤 Owner:** {action['Owner']} | **⏰ Timeline:** {action['Timeline']}")
                st.markdown("---")
        
        # All Actions Summary
        st.markdown(f"<div class='analysis-heading'>📊 All Recommendations ({len(actions)} Total)</div>", unsafe_allow_html=True)
        
        critical = [a for a in actions if "🔴" in a['Priority']]
        high = [a for a in actions if "🟡" in a['Priority']]
        strategic = [a for a in actions if "🟢" in a['Priority']]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🔴 Critical Priority", len(critical))
        with col2:
            st.metric("🟡 High Priority", len(high))
        with col3:
            st.metric("🟢 Strategic Opportunities", len(strategic))
        
        with st.expander("📋 View All Recommendations"):
            for action in actions:
                st.markdown(f"""
**{action['Action']}** {action['Priority']}
- **Category:** {action['Category']}
- **Reason:** {action['Reason']}
- **Quick Win:** {action['Quick Win']}
- **Owner:** {action['Owner']}
                """)
                st.markdown("---")
    
    # 4. GENERATE AI REPORT OUTPUT (NEW!)
    elif st.session_state.show_report:
        start_time = time.time()
        
        st.markdown("### 📄 AI-Powered Report Generation")
        
        # Report type selection
        col1, col2 = st.columns(2)
        with col1:
            report_type = st.selectbox(
                "Report Type",
                ["Executive Summary (1 page)", "Complete Business Report", "Technical Deep Dive"],
                help="Choose the type of report you need"
            )
        
        with col2:
            include_charts = st.checkbox("Include Charts in Report", value=False, 
                                        help="Embed visualizations (increases generation time)")
        
        if st.button("🤖 Generate AI Report Now", type="primary", use_container_width=True):
            with st.spinner("🤖 AI is analyzing your data and writing your report... This may take 10-20 seconds"):
                
                df = st.session_state.current_df
                processor = st.session_state.data_processor
                
                # Initialize analyzers
                trend_analyzer = TrendAnalyzer(df, processor.column_datatypes)
                anomaly_detector = AnomalyDetector(df, processor.column_datatypes)
                insight_generator = BusinessInsightGenerator(trend_analyzer)
                ai_report_gen = AIReportGenerator(trend_analyzer, anomaly_detector, insight_generator)
                
                # Generate report based on type
                if report_type == "Executive Summary (1 page)":
                    summary = insight_generator.generate_executive_summary()
                    actions = insight_generator.generate_business_actions()
                    report = ai_report_gen.generate_one_page_summary(summary, actions)
                    st.session_state.generated_report = report
                else:
                    # Use fallback for now (can integrate actual API call here)
                    summary = insight_generator.generate_executive_summary()
                    actions = insight_generator.generate_business_actions()
                    report = ai_report_gen._generate_fallback_report(summary, actions)
                    st.session_state.generated_report = report
                
                execution_time = time.time() - start_time
                st.session_state.execution_times['report'] = execution_time
            
            # Display report
            st.markdown(f"""<div class="output-section">
            <h2>📊 YOUR BUSINESS REPORT</h2>
            <span class="timer-badge">⚡ Generated in {execution_time:.2f} seconds</span>
            </div>""", unsafe_allow_html=True)
            
            st.markdown(f"*Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}*")
            
            # Show report
            with st.expander("📖 Read Full Report", expanded=True):
                st.markdown(st.session_state.generated_report)
            
            # Download buttons
            st.markdown("### 💾 Download Your Report")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.download_button(
                    label="📄 Download as Text",
                    data=st.session_state.generated_report,
                    file_name=f"business_report_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                    mime="text/plain"
                )
            
            with col2:
                st.download_button(
                    label="📝 Download as Markdown",
                    data=st.session_state.generated_report,
                    file_name=f"business_report_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
                    mime="text/markdown"
                )
            
            with col3:
                generated_report_html = st.session_state.generated_report.replace("\n", "<br>")
                html_report = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Business Report</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; max-width: 900px; margin: 40px auto; padding: 20px; line-height: 1.6; }}
        h1 {{ color: #1f77b4; border-bottom: 3px solid #1f77b4; padding-bottom: 10px; }}
        h2 {{ color: #2ca02c; margin-top: 30px; }}
        .highlight {{ background: #fff3cd; padding: 15px; border-left: 4px solid #ffc107; margin: 20px 0; }}
        .critical {{ background: #f8d7da; padding: 15px; border-left: 4px solid #dc3545; margin: 20px 0; }}
    </style>
</head>
<body>
{generated_report_html}
<hr>
<p><small>Report Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}<br>
Analysis Tool: REPORT-X</small></p>
</body>
</html>
                """
                st.download_button(
                    label="🌐 Download as HTML",
                    data=html_report,
                    file_name=f"business_report_{datetime.now().strftime('%Y%m%d_%H%M')}.html",
                    mime="text/html"
                )
            
            st.success("✅ Report generated successfully! Use the buttons above to download in your preferred format.")
    
    # Show performance summary
    if st.session_state.execution_times:
        st.markdown("---")
        st.markdown("<div class='analysis-heading'>⚡ Performance Summary</div>", unsafe_allow_html=True)
        
        cols = st.columns(len(st.session_state.execution_times))
        for idx, (analysis_type, exec_time) in enumerate(st.session_state.execution_times.items()):
            with cols[idx]:
                status = "✅" if exec_time < 5 else "⚠️"
                st.metric(
                    f"{status} {analysis_type.title()}",
                    f"{exec_time:.2f}s",
                    delta=f"{5-exec_time:.2f}s to target" if exec_time < 5 else None,
                    delta_color="normal" if exec_time < 5 else "inverse"
                )

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem 0 1rem 0;">
    <p style="font-size: 1.1rem; margin-bottom: 0.5rem;">
        <strong>🤖 REPORT-X</strong>
    </p>
    <p style="font-size: 0.9rem; color: #999;">
        Powered by Advanced Analytics | Built for Business Users | Zero ML Knowledge Required
    </p>
    <p style="font-size: 0.8rem; color: #bbb; margin-top: 1rem;">
        Upload • Analyze • Act
    </p>
</div>
""", unsafe_allow_html=True)
import os
from chat_engine import ChatEngine

api_key = os.getenv("OPENAI_API_KEY")  # This reads from environment variable)  # Reads the API key
chat = ChatEngine(api_key)
