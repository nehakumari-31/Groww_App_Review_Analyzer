import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
import os

# Page Config
st.set_page_config(
    page_title="Groww Review Pulse",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Groww Aesthetic (Glassmorphism + Branding)
st.markdown("""
    <style>
    :root {
        --groww-green: #00D09C;
        --groww-dark: #121212;
        --glass-bg: rgba(255, 255, 255, 0.05);
        --glass-border: rgba(255, 255, 255, 0.1);
    }
    
    .stApp {
        background-color: var(--groww-dark);
        color: white;
    }
    
    .pulse-card {
        background: var(--glass-bg);
        border: 1px solid var(--glass-border);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 20px;
        transition: transform 0.3s ease;
    }
    
    .pulse-card:hover {
        transform: translateY(-5px);
        border-color: var(--groww-green);
    }
    
    .pulse-header {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #00D09C, #00B686);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    
    .theme-tag {
        display: inline-block;
        padding: 5px 15px;
        border-radius: 20px;
        background: rgba(0, 208, 156, 0.1);
        border: 1px solid var(--groww-green);
        color: var(--groww-green);
        margin: 5px;
        font-size: 0.8rem;
    }
    
    .quote-card {
        font-style: italic;
        border-left: 4px solid var(--groww-green);
        padding-left: 15px;
        margin: 15px 0;
        color: #E0E0E0;
    }
    
    .idea-card {
        background: rgba(255, 255, 255, 0.03);
        padding: 10px 15px;
        border-radius: 8px;
        margin-bottom: 10px;
        border-left: 4px solid #FFD700;
    }
    </style>
""", unsafe_allow_html=True)

# Helper to load data
def load_analysis_data():
    pulse_path = 'data/analysis/review_pulse.json'
    categorized_path = 'data/analysis/categorized_reviews.csv'
    
    pulse = None
    df = None
    
    if os.path.exists(pulse_path):
        with open(pulse_path, 'r') as f:
            pulse = json.load(f)
            
    if os.path.exists(categorized_path):
        df = pd.read_csv(categorized_path)
        
    return pulse, df

# Load Data
pulse, df = load_analysis_data()

# Hero Section
st.markdown("<div class='pulse-header'>Groww Review Pulse</div>", unsafe_allow_html=True)
st.markdown("Automated insights from the last 8-12 weeks of customer feedback.")

if pulse:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("<div class='pulse-card'>", unsafe_allow_html=True)
        st.subheader("🎯 Key Themes")
        for theme in pulse.get('key_themes', []):
            st.markdown(f"<span class='theme-tag'>{theme.upper()}</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col2:
        st.markdown("<div class='pulse-card'>", unsafe_allow_html=True)
        st.subheader("💬 Voice of Customer")
        for quote in pulse.get('critical_quotes', []):
            st.markdown(f"<div class='quote-card'>\"{quote}\"</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col3:
        st.markdown("<div class='pulse-card'>", unsafe_allow_html=True)
        st.subheader("💡 Product Ideas")
        for idea in pulse.get('actionable_ideas', []):
            st.markdown(f"<div class='idea-card'>{idea}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
else:
    st.warning("No pulse data found. Run Phase 2 analysis first (src/analysis/analyzer.py).")

# Visualizations
if df is not None:
    st.divider()
    t_col1, t_col2 = st.columns([2, 1])
    
    with t_col1:
        st.subheader("📈 Theme Distribution")
        theme_counts = df['theme'].value_counts().reset_index()
        theme_counts.columns = ['Theme', 'Count']
        
        fig = px.bar(
            theme_counts, 
            x='Theme', 
            y='Count',
            color='Count',
            color_continuous_scale=['#00D09C', '#00B686'],
            template="plotly_dark"
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_title="",
            yaxis_title="Total Reviews",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with t_col2:
        st.subheader("⭐ Ratings by Theme")
        rating_avg = df.groupby('theme')['rating'].mean().reset_index()
        
        fig_radar = px.line_polar(
            rating_avg, r='rating', theta='theme', 
            line_close=True, template="plotly_dark",
            color_discrete_sequence=['#00D09C']
        )
        fig_radar.update_traces(fill='toself')
        fig_radar.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    # Raw Data Section
    with st.expander("🔍 Explore Raw Processed Data"):
        st.dataframe(df, use_container_width=True)
else:
    st.info("Run Phase 2 to see interactive visualizations.")

# Footer
st.markdown("""
<div style='text-align: center; margin-top: 50px; opacity: 0.5; font-size: 0.8rem;'>
    Powered by Groq Llama 3 • Developed with n8n Architecture
</div>
""", unsafe_allow_html=True)
