"""
Prediction utilities for water shortage model based on ML_project.ipynb
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import GradientBoostingRegressor
import streamlit as st
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))
import config

# Global cache for the model and data
@st.cache_resource
def load_model_and_data():
    # Try multiple locations for the dataset
    possible_paths = [
        os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'Cleaned_Pakistan_Water_Dataset_updated.csv'),
        os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'Cleaned_Pakistan_Water_Dataset_updated.csv'),
        'Cleaned_Pakistan_Water_Dataset_updated.csv'
    ]
    
    data_path = None
    for path in possible_paths:
        if os.path.exists(path):
            data_path = path
            break
            
    if not data_path:
        st.error("Dataset 'Cleaned_Pakistan_Water_Dataset_updated.csv' not found! Please place it in the dashboard/data folder.")
        return None, None, None

    try:
        df = pd.read_csv(data_path)

        # Standardize
        df = df.rename(columns={
            'Soil Type': 'Soil_Type',
            'Crop': 'Crop_Type',
            'Rainfall_mm': 'Rainfall'
        })

        # Drop leakage
        DROP_COLS = ['Water_Shortage_Level', 'Water_Balance_mm']
        df.drop(columns=[c for c in DROP_COLS if c in df.columns], inplace=True)

        # Sort & Clean
        df = df.sort_values(by=['District', 'Year', 'Month'])
        df = df.dropna().reset_index(drop=True)

        # Encode
        label_encoders = {}
        for col in ['District', 'Crop_Type', 'Soil_Type', 'Season']:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col])
            label_encoders[col] = le

        # Lag & Seasonal
        df = df.sort_values(by=['District', 'Year', 'Month'])
        df['Rainfall_lag1'] = df.groupby('District')['Rainfall'].shift(1)
        df['Month_sin'] = np.sin(2 * np.pi * df['Month'] / 12)
        df['Month_cos'] = np.cos(2 * np.pi * df['Month'] / 12)
        df = df.dropna().reset_index(drop=True)

        # Features
        FEATURES = [
            'Rainfall_lag1', 'Month_sin', 'Month_cos', 'Year',
            'Temperature_C', 'Humidity_Percent', 'Wind_Speed', 'Solar_Radiation'
        ]

        X = df[FEATURES]
        y = df['Rainfall']

        # Train Model
        # Using GradientBoostingRegressor as identified in the notebook
        model = GradientBoostingRegressor(random_state=42)
        model.fit(X, y)

        return model, df, label_encoders
    except Exception as e:
        st.error(f"Error loading/training model: {str(e)}")
        return None, None, None

def classify_severity(wsi):
    if wsi >= 100.0:
        return 'No Shortage'
    elif wsi >= 80.0:
        return 'Mild'
    elif wsi >= 60.0:
        return 'Moderate'
    elif wsi >= 40.0:
        return 'Severe'
    else:
        return 'Critical'

def get_shortage_color(severity):
    colors = {
        'No Shortage': '#00ff00', # Green
        'Mild': '#90ee90',        # Light Green
        'Moderate': '#ffff00',    # Yellow
        'Severe': '#ffa500',      # Orange
        'Critical': '#ff0000'     # Red
    }
    return colors.get(severity, '#999999')

def predict_water_shortage_logic(year, month, district_name, soil_type_name, crop_type_name, irrigation_mm=0.0):
    model, df, label_encoders = load_model_and_data()
    
    if model is None:
        return None

    FEATURES = [
        'Rainfall_lag1', 'Month_sin', 'Month_cos', 'Year',
        'Temperature_C', 'Humidity_Percent', 'Wind_Speed', 'Solar_Radiation'
    ]

    # 1. Encode categorical inputs
    try:
        if district_name in label_encoders['District'].classes_:
            encoded_district = label_encoders['District'].transform([district_name])[0]
        else:
            return {"error": f"District '{district_name}' not found."}

        if soil_type_name in label_encoders['Soil_Type'].classes_:
            encoded_soil_type = label_encoders['Soil_Type'].transform([soil_type_name])[0]
        else:
            return {"error": f"Soil Type '{soil_type_name}' not found."}

        if crop_type_name in label_encoders['Crop_Type'].classes_:
            encoded_crop_type = label_encoders['Crop_Type'].transform([crop_type_name])[0]
        else:
            return {"error": f"Crop Type '{crop_type_name}' not found."}
    except Exception as e:
        return {"error": f"Encoding error: {str(e)}"}

    # 2. Look up 'last_month_rainfall'
    prev_month_year = year
    prev_month = month - 1
    if prev_month == 0:
        prev_month = 12
        prev_month_year -= 1

    prev_month_data = df[
        (df['Year'] == prev_month_year) &
        (df['Month'] == prev_month) &
        (df['District'] == encoded_district)
    ]

    if not prev_month_data.empty:
        last_month_rainfall = prev_month_data['Rainfall'].mean()
    else:
        # Fallback: Average rainfall for that district/month across all years
        avg_rainfall_data = df[
            (df['District'] == encoded_district) &
            (df['Month'] == prev_month)
        ]['Rainfall'].mean()
        
        if not pd.isna(avg_rainfall_data):
            last_month_rainfall = avg_rainfall_data
        else:
            # Ultimate fallback: global mean
            last_month_rainfall = df['Rainfall'].mean()

    # 3. Look up current month's environmental features
    # Try to find exact match first (unlikely for future dates, but good for testing)
    current_context_data = df[
        (df['Year'] == year) &
        (df['Month'] == month) &
        (df['District'] == encoded_district) &
        (df['Soil_Type'] == encoded_soil_type) &
        (df['Crop_Type'] == encoded_crop_type)
    ]

    if not current_context_data.empty:
        row = current_context_data.iloc[0]
        temperature = row['Temperature_C']
        humidity = row['Humidity_Percent']
        wind = row['Wind_Speed']
        solar = row['Solar_Radiation']
        soil_capacity = row['Soil_Water_Capacity']
        crop_demand = row['Crop_Water_Demand_mm']
    else:
        # Fallback: Averages
        avg_env_data = df[
            (df['District'] == encoded_district) &
            (df['Month'] == month)
        ].agg({
            'Temperature_C': 'mean',
            'Humidity_Percent': 'mean',
            'Wind_Speed': 'mean',
            'Solar_Radiation': 'mean'
        }).to_dict()

        temperature = avg_env_data.get('Temperature_C', df['Temperature_C'].mean())
        humidity = avg_env_data.get('Humidity_Percent', df['Humidity_Percent'].mean())
        wind = avg_env_data.get('Wind_Speed', df['Wind_Speed'].mean())
        solar = avg_env_data.get('Solar_Radiation', df['Solar_Radiation'].mean())

        # Soil Capacity
        avg_soil_capacity = df[(df['Soil_Type'] == encoded_soil_type)]['Soil_Water_Capacity'].mean()
        soil_capacity = avg_soil_capacity if not pd.isna(avg_soil_capacity) else df['Soil_Water_Capacity'].mean()

        # Crop Demand
        avg_crop_demand = df[(df['Crop_Type'] == encoded_crop_type)]['Crop_Water_Demand_mm'].mean()
        crop_demand = avg_crop_demand if not pd.isna(avg_crop_demand) else df['Crop_Water_Demand_mm'].mean()

    # 4. Prepare features
    month_sin = np.sin(2 * np.pi * month / 12)
    month_cos = np.cos(2 * np.pi * month / 12)

    X_user = pd.DataFrame([[
        last_month_rainfall,
        month_sin,
        month_cos,
        year,
        temperature,
        humidity,
        wind,
        solar
    ]], columns=FEATURES)

    # 5. Predict
    rainfall_pred = model.predict(X_user)[0]
    soil_factor = soil_capacity / df['Soil_Water_Capacity'].max()
    
    # Avoid division by zero
    if crop_demand == 0:
        crop_demand = 1e-6
        
    # Calculate WSI with Irrigation
    # Effective Water Supply = (Rainfall * Soil_Retention) + Irrigation
    effective_water_supply = (rainfall_pred * soil_factor) + irrigation_mm
    
    wsi = (effective_water_supply / crop_demand) * 100
    severity = classify_severity(wsi)

    return {
        "rainfall_pred": rainfall_pred,
        "irrigation_added": irrigation_mm,
        "effective_supply": effective_water_supply,
        "wsi": wsi,
        "severity": severity,
        "temperature": temperature,
        "humidity": humidity,
        "wind": wind,
        "solar": solar,
        "soil_capacity": soil_capacity,
        "crop_demand": crop_demand,
        "soil_factor": soil_factor,
        "shortage_category": severity # Alias for compatibility
    }

def get_recommendations(shortage_category, crop):
    """Get recommendations based on shortage level"""
    recommendations = {
        "No Shortage": [
            f"✅ Water supply is adequate for {crop} cultivation",
            "Continue with regular irrigation schedule",
            "Monitor weather patterns for any changes",
            "Consider water-efficient practices to maintain sustainability"
        ],
        "Mild": [
            f"⚠️ Minor water deficit detected for {crop}",
            "Implement water-saving irrigation techniques (drip/sprinkler)",
            "Monitor soil moisture levels regularly",
            "Consider mulching to reduce evaporation",
            "Plan for supplemental irrigation if needed"
        ],
        "Moderate": [
            f"⚠️ Moderate water shortage affecting {crop} growth",
            "Prioritize critical growth stages for water allocation",
            "Implement deficit irrigation strategies",
            "Use moisture-retention techniques (mulching, soil amendments)",
            "Consider drought-resistant crop varieties for next season",
            "Monitor crop health for stress symptoms"
        ],
        "Severe": [
            f"🚨 Severe water shortage - immediate action required for {crop}",
            "Prioritize water for most critical crops and growth stages",
            "Implement emergency irrigation if possible",
            "Consider crop reduction or alternative crops",
            "Apply anti-transpirants to reduce water loss",
            "Coordinate with local water authorities",
            "Plan for crop insurance claims if applicable"
        ],
        "Critical": [
            f"🔴 CRITICAL water shortage - emergency response needed for {crop}",
            "Activate drought emergency protocols",
            "Focus resources on saving the most viable crops",
            "Consider crop abandonment for severely affected areas",
            "Implement all available water conservation measures",
            "Coordinate with government relief programs",
            "Plan alternative livelihoods until conditions improve",
            "Prepare for next season with drought-resistant varieties"
        ]
    }
    return recommendations.get(shortage_category, ["Monitor situation closely"])

def get_historical_monthly_stats(district_name):
    """Get historical average rainfall and temperature per month for a district"""
    model, df, label_encoders = load_model_and_data()
    if df is None:
        return None
        
    try:
        if district_name in label_encoders['District'].classes_:
            encoded_district = label_encoders['District'].transform([district_name])[0]
        else:
            return None
            
        district_data = df[df['District'] == encoded_district]
        
        # Group by month and calculate means
        monthly_stats = district_data.groupby('Month').agg({
            'Rainfall': 'mean',
            'Temperature_C': 'mean'
        }).reset_index()
        
        return monthly_stats
    except Exception:
        return None

def get_crop_monthly_demand(crop_name):
    """Get average water demand per month for a crop"""
    model, df, label_encoders = load_model_and_data()
    if df is None:
        return None
        
    try:
        if crop_name in label_encoders['Crop_Type'].classes_:
            encoded_crop = label_encoders['Crop_Type'].transform([crop_name])[0]
        else:
            return None
            
        crop_data = df[df['Crop_Type'] == encoded_crop]
        
        # Group by month and calculate means
        monthly_demand = crop_data.groupby('Month')['Crop_Water_Demand_mm'].mean().reset_index()
        
        return monthly_demand
    except Exception:
        return None
