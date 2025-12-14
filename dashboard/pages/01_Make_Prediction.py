"""
Single Prediction Page - Water Shortage Prediction
"""
import streamlit as st
import pandas as pd
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))
import config
from utils.predictor import (
    predict_water_shortage_logic, 
    get_recommendations, 
    get_shortage_color,
    get_historical_monthly_stats,
    get_crop_monthly_demand
)
from utils.visualizations import (
    create_water_balance_chart, 
    create_shortage_gauge,
    create_seasonal_trend_chart,
    create_water_source_pie_chart
)
from utils.ui import apply_styling, create_page_header, create_interactive_header

st.set_page_config(page_title="Make Prediction", page_icon="💧", layout="wide")
apply_styling()

# Header
create_page_header(
    "Water Shortage Prediction",
    "Get instant predictions for your location and crop using advanced ML models"
)

# Instructions
with st.expander("📖 How to use this page", expanded=False):
    st.markdown("""
    **Step 1**: Select your district and crop type  
    **Step 2**: Choose the time period (month and year)  
    **Step 3**: Select the soil type
    **Step 4**: Click "Predict Water Shortage" to get results
    
    The system will automatically retrieve historical weather data and predict rainfall and water shortage.
    """)

# Input Form
st.subheader("📝 Input Parameters")

col1, col2 = st.columns(2)

with col1:
    # Location and Crop
    st.markdown("#### 📍 Location & Crop Information")
    
    district = st.selectbox(
        "District",
        options=config.DISTRICTS,
        help="Select the agricultural district"
    )
    
    crop = st.selectbox(
        "Crop Type",
        options=config.CROPS,
        help="Select the crop you're cultivating or planning to cultivate"
    )
    
    soil_type = st.selectbox(
        "Soil Type",
        options=config.SOIL_TYPES,
        help="Soil type affects water retention capacity"
    )

with col2:
    # Time period
    st.markdown("#### 📅 Time Period")
    
    col_month, col_year = st.columns(2)
    with col_month:
        month = st.selectbox(
            "Month",
            options=list(range(1, 13)),
            format_func=lambda x: datetime(2000, x, 1).strftime('%B'),
            help="Month for prediction"
        )
    
    with col_year:
        year = st.number_input(
            "Year",
            min_value=2015,
            max_value=2030,
            value=2024,
            help="Year for prediction"
        )
    
    # Irrigation Input
    st.markdown("#### 💧 Supplemental Water")
    irrigation_mm = st.slider(
        "Estimated Irrigation (mm)",
        min_value=0,
        max_value=300,
        value=0,
        step=10,
        help="Add water from tube wells, canals, or other sources."
    )
    
    st.info("Weather parameters (Temperature, Humidity, etc.) will be automatically retrieved/predicted based on historical data.")

# Predict button
st.markdown("---")
if st.button("Predict Water Shortage", type="primary", use_container_width=True):
    with st.spinner("Calculating water shortage prediction..."):
        # Call the new prediction logic
        result = predict_water_shortage_logic(
            year=year,
            month=month,
            district_name=district,
            soil_type_name=soil_type,
            crop_type_name=crop,
            irrigation_mm=irrigation_mm
        )
        
        if result is None:
            st.error("Failed to load model or data. Please check if the dataset exists.")
        elif "error" in result:
            st.error(result["error"])
        else:
            # Extract results
            rainfall_pred = result['rainfall_pred']
            irrigation_added = result.get('irrigation_added', 0)
            effective_supply = result.get('effective_supply', rainfall_pred)
            wsi = result['wsi']
            category = result['severity']
            temperature = result['temperature']
            humidity = result['humidity']
            wind_speed = result['wind']
            solar_radiation = result['solar']
            soil_capacity = result['soil_capacity']
            crop_demand = result['crop_demand']
            
            color = get_shortage_color(category)
            
            # Display results
            st.markdown("---")
            create_interactive_header("Prediction Results")
            
            # Main result card
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, {color}33, {color}11); 
                        padding: 2rem; 
                        border-radius: 15px; 
                        border-left: 8px solid {color};
                        margin: 1rem 0;">
                <h2 style="color: {color}; margin: 0;">{category}</h2>
                <p style="font-size: 1.2rem; margin: 0.5rem 0;">Water Sufficiency Index (WSI): <strong>{wsi:.2f}%</strong></p>
            </div>
            """, unsafe_allow_html=True)
            
            # Metrics row
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Predicted Rainfall",
                    f"{rainfall_pred:.1f} mm",
                    help="Predicted rainfall based on historical patterns"
                )
            
            with col2:
                st.metric(
                    "Irrigation Added",
                    f"{irrigation_added:.1f} mm",
                    help="Supplemental water from irrigation"
                )
            
            with col3:
                st.metric(
                    "Effective Supply",
                    f"{effective_supply:.1f} mm",
                    help="Total water available (Rainfall + Irrigation) * Soil Factor"
                )
            
            with col4:
                st.metric(
                    "Crop Water Demand",
                    f"{crop_demand:.1f} mm",
                    delta=f"{crop}",
                    help="Water required by the crop"
                )
            
            # Additional Weather Metrics
            create_interactive_header("Environmental Factors Used", level=3)
            w_col1, w_col2, w_col3, w_col4 = st.columns(4)
            with w_col1:
                st.metric("Temperature", f"{temperature:.1f}°C")
            with w_col2:
                st.metric("Humidity", f"{humidity:.1f}%")
            with w_col3:
                st.metric("Wind Speed", f"{wind_speed:.1f} m/s")
            with w_col4:
                st.metric("Solar Radiation", f"{solar_radiation:.1f} MJ/m²/day")

            # Visualizations
            create_interactive_header("Detailed Analysis")
            
            # Row 1: Gauge and Pie Chart
            col1, col2 = st.columns([1, 1])
            
            with col1:
                create_interactive_header("Water Sufficiency Index", level=3)
                gauge_fig = create_shortage_gauge(wsi) 
                st.plotly_chart(gauge_fig, use_container_width=True, key="gauge_chart")
            
            with col2:
                create_interactive_header("Water Balance Composition", level=3)
                # Calculate effective supply and deficit
                # WSI = (Supply / Demand) * 100
                # Supply = (WSI * Demand) / 100
                # effective_supply is already calculated in result
                deficit = crop_demand - effective_supply
                
                pie_fig = create_water_source_pie_chart(effective_supply, deficit, irrigation_added)
                st.plotly_chart(pie_fig, use_container_width=True, key="pie_chart")
            
            # Row 2: Seasonal Trend
            create_interactive_header("Seasonal Trends", level=3)
            
            # Fetch historical data
            monthly_stats = get_historical_monthly_stats(district)
            monthly_demand = get_crop_monthly_demand(crop)
            
            if monthly_stats is not None and monthly_demand is not None:
                trend_fig = create_seasonal_trend_chart(
                    monthly_stats, 
                    monthly_demand, 
                    month, 
                    district, 
                    crop
                )
                st.plotly_chart(trend_fig, use_container_width=True, key="trend_chart")
            else:
                st.info("Historical trend data not available.")
            
            # Recommendations
            create_interactive_header("Recommendations")
            recommendations = get_recommendations(category, crop)
            
            # Create grid layout for recommendations
            for i in range(0, len(recommendations), 2):
                col1, col2 = st.columns(2)
                
                # Card 1
                with col1:
                    st.markdown(f"""
                    <div class="recommendation-card">
                        <p style="margin:0; color:#444; font-size: 1.1rem; line-height: 1.5;">{recommendations[i]}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Card 2 (if exists)
                if i + 1 < len(recommendations):
                    with col2:
                        st.markdown(f"""
                        <div class="recommendation-card">
                            <p style="margin:0; color:#444; font-size: 1.1rem; line-height: 1.5;">{recommendations[i+1]}</p>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Add spacing between rows
                st.markdown("<div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True)
            
            # Export data
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col2:
                # Convert to DataFrame for export
                export_data = result.copy()
                export_df = pd.DataFrame([export_data])
                csv = export_df.to_csv(index=False)
                
                st.download_button(
                    label="Download Prediction Data (CSV)",
                    data=csv,
                    file_name=f"water_shortage_prediction_{district}_{crop}_{year}-{month:02d}.csv",
                    mime="text/csv",
                    use_container_width=True
                )

# Sidebar info
with st.sidebar:
    st.markdown("### Current Input Summary")
    st.info(f"""
    **District:** {district if 'district' in locals() else 'Not selected'}  
    **Crop:** {crop if 'crop' in locals() else 'Not selected'}  
    **Period:** {f"{datetime(2000, month, 1).strftime('%B')} {year}" if 'month' in locals() and 'year' in locals() else 'Not selected'}
    """)
