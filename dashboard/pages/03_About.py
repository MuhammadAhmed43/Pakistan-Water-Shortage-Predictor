"""
About Page - Dashboard Information
"""
import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path to import config
sys.path.append(str(Path(__file__).parent.parent))
import config
from utils.ui import apply_styling, create_page_header, create_interactive_header

st.set_page_config(page_title="About", page_icon="💧", layout="wide")
apply_styling()

# Header
create_page_header(
    "About This Dashboard",
    "Information, Documentation & User Guide"
)

# Overview Section
create_interactive_header("Overview")
st.markdown("""
<div class="custom-card">
    <p style="font-size: 1.1rem; line-height: 1.6;">
        The <strong>Pakistan Water Shortage Prediction Dashboard</strong> is an advanced machine learning-powered tool designed to help farmers, policymakers, and agricultural researchers predict and manage water shortage risks across Pakistan's agricultural districts.
    </p>
    <h4 style="color: #01411C; margin-top: 1.5rem;">Mission</h4>
    <p>
        To provide accurate, actionable insights on agricultural water availability, enabling better water resource management and crop planning decisions.
    </p>
</div>
""", unsafe_allow_html=True)

# Model Information
create_interactive_header("Model Information")
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="custom-card" style="height: 100%;">
        <h4 style="color: #01411C;">Machine Learning Algorithm</h4>
        <ul style="list-style-type: none; padding-left: 0;">
            <li><strong>Type:</strong> Stacking Ensemble Regressor</li>
            <li><strong>Base Models:</strong> Gradient Boosting, Random Forest</li>
            <li><strong>Final Estimator:</strong> Ridge Regression</li>
        </ul>
        
        <h4 style="color: #01411C; margin-top: 1rem;">Performance Metrics</h4>
        <ul style="list-style-type: none; padding-left: 0;">
            <li><strong>MAE:</strong> 1.41</li>
            <li><strong>RMSE:</strong> 2.28</li>
            <li><strong>R² Score:</strong> 0.0645</li>
            <li><strong>Training Data:</strong> 33,696 records (2015-2023)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="custom-card" style="height: 100%;">
        <h4 style="color: #01411C;">Input Features</h4>
        <ul style="list-style-type: none; padding-left: 0;">
            <li><strong>Location:</strong> 26 Districts in Punjab</li>
            <li><strong>Crops:</strong> 16 Major types</li>
            <li><strong>Time:</strong> Month and Year</li>
            <li><strong>Weather:</strong> Temp, Humidity, Rainfall, Wind, Solar</li>
            <li><strong>Soil:</strong> 5 Major types</li>
        </ul>
        
        <h4 style="color: #01411C; margin-top: 1rem;">Output</h4>
        <ul style="list-style-type: none; padding-left: 0;">
            <li><strong>Index:</strong> 0-100 Water Shortage Index</li>
            <li><strong>Categories:</strong> No shortage to Critical</li>
            <li><strong>Advice:</strong> Actionable recommendations</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Methodology
create_interactive_header("Methodology")
st.markdown("""
<div class="custom-card">
    <h4 style="color: #01411C;">Calculation Process</h4>
    <p>The model combines machine learning predictions with established agricultural formulas:</p>
    <ol>
        <li><strong>Evapotranspiration (ET₀):</strong> Calculated using the Penman-Monteith equation based on weather parameters.</li>
        <li><strong>Crop Water Demand:</strong> Derived from ET₀ and specific crop coefficients (Kc).</li>
        <li><strong>Water Sufficiency Index (WSI):</strong> Calculated by comparing predicted rainfall (supply) against crop demand, adjusted for soil retention.</li>
    </ol>
    <p style="background-color: #e8f5e9; padding: 1rem; border-radius: 5px; border-left: 4px solid #28A745;">
        <strong>Interpretation:</strong> A WSI ≥ 100% indicates no shortage, while values below 100% indicate varying degrees of water scarcity.
    </p>
</div>
""", unsafe_allow_html=True)

# Coverage
create_interactive_header("Coverage")
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="custom-card">
        <h4 style="color: #01411C;">Supported Districts</h4>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; font-size: 0.9rem;">
    """, unsafe_allow_html=True)
    
    # Generate district list HTML
    for d in config.DISTRICTS:
        st.markdown(f"<div>• {d}</div>", unsafe_allow_html=True)
        
    st.markdown("</div></div>", unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="custom-card">
        <h4 style="color: #01411C;">Supported Crops</h4>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; font-size: 0.9rem;">
    """, unsafe_allow_html=True)
    
    # Generate crop list HTML
    for c in config.CROPS:
        st.markdown(f"<div>• {c}</div>", unsafe_allow_html=True)
        
    st.markdown("</div></div>", unsafe_allow_html=True)

# User Guide
create_interactive_header("User Guide")
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="custom-card" style="height: 100%;">
        <h4 style="color: #01411C;">For Farmers</h4>
        <p><strong>Making a Prediction:</strong></p>
        <ol>
            <li>Go to the <strong>Make Prediction</strong> page</li>
            <li>Select your district and crop type</li>
            <li>Enter current weather conditions</li>
            <li>Get instant water shortage forecast</li>
        </ol>
        <p><strong>Understanding Results:</strong></p>
        <ul style="list-style-type: none; padding-left: 0;">
            <li><span style="color:green">●</span> <strong>No Shortage (0-20):</strong> Adequate supply</li>
            <li><span style="color:orange">●</span> <strong>Moderate (40-60):</strong> Significant shortage</li>
            <li><span style="color:red">●</span> <strong>Critical (80-100):</strong> Extreme shortage</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="custom-card" style="height: 100%;">
        <h4 style="color: #01411C;">For Policy Makers</h4>
        <p><strong>Using the Map View:</strong></p>
        <ol>
            <li>Navigate to <strong>Map View</strong></li>
            <li>Select time period and crop</li>
            <li>Generate district-wide predictions</li>
            <li>Identify high-risk areas for resource allocation</li>
        </ol>
        <p><strong>Export Data:</strong></p>
        <ul>
            <li>Download prediction results as CSV</li>
            <li>Use for reports and further analysis</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Technical & Disclaimer
create_interactive_header("Additional Information")
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="custom-card" style="height: 100%;">
        <h4 style="color: #01411C;">Technical Stack</h4>
        <ul style="list-style-type: none; padding-left: 0;">
            <li><strong>Frontend:</strong> Streamlit</li>
            <li><strong>ML Framework:</strong> Scikit-learn</li>
            <li><strong>Data:</strong> NASA POWER, Pakistan Bureau of Statistics</li>
            <li><strong>Version:</strong> 1.0 (Dec 2024)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="custom-card" style="height: 100%;">
        <h4 style="color: #01411C;">Disclaimer</h4>
        <p style="font-size: 0.9rem;">
            This dashboard provides predictions based on historical data and machine learning models. While we strive for accuracy, predictions should be used as one of many tools for decision-making. Always consult with local agricultural experts and consider on-ground conditions.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div style='text-align: center; padding: 2rem 0; color: #666; border-top: 1px solid #eee; margin-top: 2rem;'>
    <p><strong>Pakistan Water Shortage Prediction Dashboard v1.0</strong></p>
    <p>© 2024 | Built for sustainable agriculture in Pakistan</p>
</div>
""", unsafe_allow_html=True)
