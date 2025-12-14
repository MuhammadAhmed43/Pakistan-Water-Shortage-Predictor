"""
Interactive Map View - Pakistan Water Shortage Visualization
"""
import streamlit as st
import pandas as pd
import sys
from pathlib import Path
from streamlit_folium import st_folium
from datetime import datetime

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))
import config
from utils.map_generator import create_pakistan_map
from utils.predictor import predict_water_shortage_logic
from utils.ui import apply_styling, create_page_header

st.set_page_config(page_title="Map View", page_icon="💧", layout="wide")
apply_styling()

# Header
create_page_header(
    "Pakistan Water Shortage Map",
    "Interactive visualization of water shortage across districts using ML predictions"
)

# Filter controls
st.subheader("Map Filters")

col1, col2, col3, col4 = st.columns(4)

with col1:
    selected_crop = st.selectbox("Crop Type", options=["All"] + config.CROPS)

with col2:
    selected_month = st.selectbox(
        "Month",
        options=list(range(1, 13)),
        format_func=lambda x: datetime(2000, x, 1).strftime('%B'),
        index=5  # June
    )

with col3:
    selected_year = st.number_input("Year", min_value=2015, max_value=2030, value=2024)

with col4:
    soil_filter = st.selectbox("Soil Type", options=["All"] + config.SOIL_TYPES)

# Irrigation Input
st.markdown("#### 💧 Supplemental Water")
irrigation_mm = st.slider(
    "Estimated Irrigation (mm)",
    min_value=0,
    max_value=300,
    value=0,
    step=10,
    help="Add water from tube wells, canals, or other sources to see impact on all districts."
)

# Generate predictions for all districts
if st.button("Generate Map", type="primary"):
    with st.spinner("Generating predictions for all districts... This may take a moment."):
        
        predictions = []
        
        # Generate prediction for each district
        for district in config.DISTRICTS:
            soil = soil_filter if soil_filter != "All" else "Loamy" # Default if All
            crop = selected_crop if selected_crop != "All" else "Wheat" # Default if All
            
            # Call new prediction logic
            result = predict_water_shortage_logic(
                year=selected_year,
                month=selected_month,
                district_name=district,
                soil_type_name=soil,
                crop_type_name=crop,
                irrigation_mm=irrigation_mm
            )
            
            if result and "error" not in result:
                # Flatten result for DataFrame
                flat_result = result.copy()
                flat_result['District'] = district
                flat_result['Crop'] = crop
                flat_result['Soil Type'] = soil
                
                # Map generator expects 'water_shortage_index' and 'shortage_category'
                # We use the raw WSI (Supply/Demand * 100) to be consistent with the Prediction page.
                # WSI >= 100 is Good (No Shortage), WSI < 100 is Bad (Shortage).
                
                wsi = result['wsi']
                
                flat_result['water_shortage_index'] = wsi
                flat_result['raw_wsi'] = wsi
                flat_result['shortage_category'] = result['severity']
                
                predictions.append(flat_result)
        
        if not predictions:
            st.error("No predictions generated. Please check if the dataset is available.")
        else:
            # Convert to DataFrame
            pred_df = pd.DataFrame(predictions)
            
            # Store in session state
            st.session_state['map_predictions'] = pred_df
            st.success(f"Generated predictions for {len(predictions)} districts")

# Display map
st.markdown("---")
st.subheader("District-Level Water Shortage")

if 'map_predictions' in st.session_state:
    # Create and display map
    map_data = st.session_state['map_predictions']
    
    # Show statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_shortage = map_data['water_shortage_index'].mean()
        st.metric("Average WSI", f"{avg_shortage:.2f}")
    
    with col2:
        critical_count = len(map_data[map_data['shortage_category'] == 'Critical'])
        st.metric("Critical Districts", f"{critical_count}", delta="Districts")
    
    with col3:
        avg_rainfall = map_data['rainfall_pred'].mean()
        st.metric("Avg Predicted Rainfall", f"{avg_rainfall:.1f} mm")
        
    with col4:
        avg_temp = map_data['temperature'].mean()
        st.metric("Avg Temperature", f"{avg_temp:.1f}°C")

    # Map
    m = create_pakistan_map(map_data)
    st_folium(m, width=1200, height=600)
    
    # Data Table
    with st.expander("View Detailed Data"):
        st.dataframe(
            map_data[['District', 'Crop', 'water_shortage_index', 'shortage_category', 'rainfall_pred', 'temperature', 'humidity']],
            use_container_width=True
        )
else:
    st.info("Click 'Generate Map' to see the water shortage analysis.")
