"""
Static reference data for the frontend.

These are the canonical lists the dashboard supports. They mirror the values
in ``dashboard/config.py`` but live here so that ``backend`` and the FastAPI
app have no transitive dependency on Streamlit.
"""

DISTRICTS = [
    "Lahore", "Faisalabad", "Rawalpindi", "Multan", "Gujranwala",
    "Sialkot", "Bahawalpur", "Rahim Yar Khan", "Sahiwal", "Okara",
    "Sargodha", "Sheikhupura", "Jhang", "Gujrat", "Kasur",
    "Dera Ghazi Khan", "Hafizabad", "Mandi Bahauddin", "Chiniot",
    "Attock", "Jhelum", "Chakwal", "Khushab", "Mianwali", "Bhakkar", "Layyah",
]

CROPS = [
    "Paddy", "Maize", "Pulses", "Millets", "Sugarcane",
    "Mungbean", "Blackgram", "Lentil", "Wheat",
    "Banana", "Mango", "Grapes", "Cotton",
]

SOIL_TYPES = ["Red", "Clayey", "Black", "Loamy"]

MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]

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
    "Layyah": [30.9615, 70.9324],
}

PAKISTAN_CENTER = [30.8, 72.0]
MAP_ZOOM = 6.5

# Headline coverage metrics used on the Overview page.
HEADLINE_METRICS = {
    "districts_covered": 20,
    "major_crops": 16,
    "years_of_data": 9,
    "model_type": "Gradient Boosting",
}

# Model metrics — keep in sync with notebook results.
MODEL_METRICS = {
    "algorithm": "Gradient Boosting Regressor",
    "mae": 1.41,
    "rmse": 2.28,
    "r2": 0.0645,
    "training_rows": 33696,
    "training_period": "2015 – 2023",
    "features": 8,
}
