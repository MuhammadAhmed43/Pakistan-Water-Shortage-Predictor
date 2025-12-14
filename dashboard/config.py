"""
Configuration settings for Water Shortage Dashboard
"""

# Model configuration
MODEL_VERSION = "v1.0"
MODEL_NAME = "Stacking Ensemble (GradientBoosting + RandomForest)"
MODEL_PATH = "models/water_shortage_model.pkl"

# District list (26 districts from Pakistan)
DISTRICTS = [
    "Lahore", "Faisalabad", "Rawalpindi", "Multan", "Gujranwala",
    "Sialkot", "Bahawalpur", "Rahim Yar Khan", "Sahiwal", "Okara",
    "Sargodha", "Sheikhupura", "Jhang", "Gujrat", "Kasur",
    "Dera Ghazi Khan", "Hafizabad", "Mandi Bahauddin", "Chiniot",
    "Attock", "Jhelum", "Chakwal", "Khushab", "Mianwali", "Bhakkar", "Layyah"
]

# Crop types (from your dataset)
CROPS = [
    "Paddy", "Maize", "Pulses", "Millets", "Sugarcane", 
    "Mungbean", "Blackgram", "Lentil", "Wheat", 
    "Banana", "Mango", "Grapes", "Cotton"
]

# Soil types
SOIL_TYPES = ["Red", "Clayey", "Black", "Loamy"]

# Seasons
SEASONS = ["Rabi", "Kharif"]

# Water shortage thresholds and categories (Based on WSI Sufficiency Index)
# WSI = (Supply / Demand) * 100
# Higher is Better.
SHORTAGE_THRESHOLDS = {
    "Critical": (0, 40),
    "Severe": (40, 60),
    "Moderate": (60, 80),
    "Mild": (80, 100),
    "No shortage": (100, 1000)
}

# Crop coefficients (Kc values)
CROP_KC = {
    'Paddy': 1.15, 'Sugarcane': 1.25, 'Cotton': 0.75, 'Maize': 0.60,
    'Wheat': 0.50, 'Tobacco': 0.85, 'Barley': 0.45, 'Millets': 0.40,
    'Oil seeds': 0.55, 'Pulses': 0.50, 'Mungbean': 0.70, 'Blackgram': 0.70,
    'Lentil': 0.70, 'Banana': 0.70, 'Mango': 0.70, 'Grapes': 0.70
}

# Soil water capacity (mm)
SOIL_WATER_CAPACITY = {
    'Sandy': 100, 
    'Loamy': 140, 
    'Red': 120, 
    'Black': 180, 
    'Clayey': 200
}

# Color scheme (Pakistan flag colors)
PRIMARY_COLOR = "#01411C"  # Dark green
SECONDARY_COLOR = "#FFFFFF"  # White
ACCENT_COLOR = "#FFB81C"  # Golden yellow
SUCCESS_COLOR = "#28A745"
WARNING_COLOR = "#FFC107"
DANGER_COLOR = "#DC3545"

# Severity colors for visualization
SEVERITY_COLORS = {
    "No Shortage": "#28A745",  # Green
    "Mild": "#17A2B8",  # Cyan
    "Moderate": "#FFC107",  # Yellow
    "Severe": "#FD7E14",  # Orange
    "Critical": "#DC3545"  # Red
}

# Default parameter ranges
PARAM_RANGES = {
    "temperature": (8.0, 40.0, 25.0),  # (min, max, default)
    "humidity": (10.0, 85.0, 50.0),
    "rainfall": (0.0, 350.0, 50.0),
    "wind_speed": (0.5, 4.5, 2.0),
    "solar_radiation": (2.0, 8.0, 5.0)
}

# Pakistan map center coordinates
PAKISTAN_CENTER = [30.3753, 69.3451]
MAP_ZOOM = 6

# District coordinates (approximate centers)
DISTRICT_COORDS = {
    "Lahore": [31.5497, 74.3436],
    "Faisalabad": [31.4504, 73.1350],
    "Rawalpindi": [33.5651, 73.0169],
    "Multan": [30.1575, 71.5249],
    "Gujranwala": [32.1877, 74.1945],
    "Sialkot": [32.4945, 74.5229],
    "Bahawalpur": [29.3544, 71.6911],
    "Rahim Yar Khan": [28.4202, 70.2952],
    "Sahiwal": [30.6682, 73.1114],
    "Okara": [30.8081, 73.4596],
    "Sargodha": [32.0836, 72.6711],
    "Sheikhupura": [31.7167, 73.9850],
    "Jhang": [31.2681, 72.3181],
    "Gujrat": [32.5740, 74.0789],
    "Kasur": [31.1177, 74.4507],
    "Dera Ghazi Khan": [30.0489, 70.6345],
    "Hafizabad": [32.0711, 73.6878],
    "Mandi Bahauddin": [32.5861, 73.4917],
    "Chiniot": [31.7167, 72.9850],
    "Attock": [33.7681, 72.3600],
    "Jhelum": [32.9425, 73.7257],
    "Chakwal": [32.9328, 72.8630],
    "Khushab": [32.2967, 72.3522],
    "Mianwali": [32.5853, 71.5436],
    "Bhakkar": [31.6333, 71.0667],
    "Layyah": [30.9615, 70.9324]
}
