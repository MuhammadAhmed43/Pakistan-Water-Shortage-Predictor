"""
Pakistan Water Shortage Prediction Dashboard
Main Application Entry Point
"""
import streamlit as st
import sys
from pathlib import Path
from utils.ui import apply_styling

# Configure page
st.set_page_config(
    page_title="Pakistan Water Shortage Dashboard",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply global styling
apply_styling()

# Hero Section
st.markdown("""
<div class="hero-container">
    <h1 class="hero-title">Pakistan Water Shortage Dashboard</h1>
    <p class="hero-subtitle">Empowering Agriculture with AI-Driven Water Intelligence</p>
</div>
""", unsafe_allow_html=True)

# Vision Section
st.markdown("""
<div class="vision-container">
    <h2 class="vision-title">Our Vision</h2>
    <p style="font-size: 1.1rem; line-height: 1.6; color: #444;">
        To revolutionize agricultural water management in Pakistan by providing farmers and policymakers with 
        accurate, data-driven insights. We aim to mitigate water scarcity risks, optimize crop yields, and 
        ensure sustainable food security for the nation through the power of advanced machine learning.
    </p>
</div>
""", unsafe_allow_html=True)

# Key Metrics
st.markdown("### Project Impact")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">26</div>
        <div class="metric-label">Districts Covered</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">16</div>
        <div class="metric-label">Major Crops</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">9+</div>
        <div class="metric-label">Years of Data</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">AI</div>
        <div class="metric-label">Powered Analysis</div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p><strong>Pakistan Water Shortage Prediction Dashboard</strong></p>
    <p>Built for sustainable agriculture in Pakistan</p>
    <p style="font-size: 0.8rem; margin-top: 1rem;">© 2025 Water Intelligence Initiative</p>
</div>
""", unsafe_allow_html=True)
