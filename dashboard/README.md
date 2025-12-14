# Pakistan Water Shortage Prediction Dashboard 💧

A comprehensive machine learning-powered dashboard for predicting agricultural water shortage across Pakistan's districts.

![Dashboard Banner](https://img.shields.io/badge/Version-1.0-brightgreen) ![Python](https://img.shields.io/badge/Python-3.9+-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-1.29-red) ![License](https://img.shields.io/badge/License-MIT-yellow)

## 🌟 Features

- **🎯 Single Prediction**: Get instant water shortage predictions for specific locations
- **Interactive Map**: Visualize water shortage across Pakistan districts with Folium
- **Rich Visualizations**: Gauge charts, bar charts, time series analysis
- **Smart Recommendations**: Actionable insights based on shortage severity
- **📈 Batch Analysis**: Process multiple predictions simultaneously
- **📥 Data Export**: Download predictions as CSV files
- **🎨 Professional UI**: Pakistan flag-themed design with responsive layout

## 📸 Screenshots

### Home Page
Beautiful landing page with dashboard overview and statistics

### Prediction Page
Interactive form with real-time predictions and visualizations

### Map View
Interactive Pakistan map with district-level water shortage visualization

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

### Installation

1. **Clone or navigate to the project directory**
```bash
cd c:\Users\muham\Downloads\MLPROJECT\dashboard
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the dashboard**
```bash
streamlit run Dashboard.py
```

4. **Open in browser**
The dashboard will automatically open at `http://localhost:8501`

## 📁 Project Structure

```
dashboard/
├── Dashboard.py                    # Main application entry point
├── config.py                       # Configuration settings
├── requirements.txt                # Python dependencies
├── pages/                          # Streamlit pages
│   ├── 01_Make_Prediction.py      # Single prediction interface
│   ├── 02_Map_View.py             # Interactive Pakistan map
│   └── 03_About.py                # Documentation & info
├── utils/                          # Utility modules
│   ├── predictor.py               # Prediction logic & calculations
│   ├── map_generator.py           # Folium map generation
│   └── visualizations.py          # Plotly chart functions
├── models/                         # Trained ML models
│   └── (model files)
├── data/                           # Data files
└── assets/                         # Images and static files
```

## 🔬 Model Information

### Algorithm
- **Type**: Stacking Ensemble Regressor
- **Base Models**: Gradient Boosting + Random Forest
- **Performance**: MAE = 1.41, R² = 0.0645

### Training Data
- **Records**: 33,696 data points
- **Time Period**: 2015-2023
- **Districts**: 26 major agricultural districts in Punjab
- **Crops**: 16 types including wheat, rice, cotton, sugarcane

### Input Features
1. District (26 options)
2. Crop Type (16 options)
3. Month & Year
4. Temperature (°C)
5. Humidity (%)
6. Rainfall (mm)
7. Wind Speed (m/s)
8. Solar Radiation (MJ/m²/day)
9. Soil Type (5 types)

### Output
- Water Shortage Index (0-100)
- Shortage Category (No shortage / Mild / Moderate / Severe / Critical)
- Recommendations based on severity

## 💻 Usage

### Making a Single Prediction

1. Navigate to **Make Prediction** page
2. Select your district and crop
3. Enter weather parameters
4. Click "Predict Water Shortage"
5. View results with visualizations and recommendations

### Viewing Map Visualization

1. Go to **Map View** page
2. Select filters (crop, month, year)
3. Click "Generate Map"
4. Explore interactive map with district markers
5. Click districts to see detailed information

### Understanding Results

- **Shortage Index**: 0-100 scale indicating water deficit severity
- **Category Colors**:
  - 🟢 Green (0-20): No shortage
  - 🔵 Blue (20-40): Mild
  - 🟡 Yellow (40-60): Moderate
  - 🟠 Orange (60-80): Severe
  - 🔴 Red (80-100): Critical

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Visualizations**: Plotly, Folium
- **ML Framework**: Scikit-learn
- **Data Processing**: Pandas, NumPy
- **Maps**: Folium + Streamlit-Folium

## Key Calculations

### Reference Evapotranspiration (ET₀)
Uses simplified Penman-Monteith equation

### Crop Water Demand
```
CWD = ET₀ × Crop Coefficient × Days
```

### Water Shortage Index
```
Index = (Deficit / Crop Water Demand) × 100
```

## 🌾 Supported Crops

Paddy, Wheat, Cotton, Sugarcane, Maize, Barley, Millets, Tobacco, Oil seeds, Pulses, Mungbean, Blackgram, Lentil, Banana, Mango, Grapes

## 📍 Covered Districts

26 major agricultural districts across Punjab province including Lahore, Faisalabad, Multan, Rawalpindi, and more.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📝 License

This project is licensed under the MIT License.

## ⚠️ Disclaimer

This dashboard provides predictions based on historical data and machine learning models. Predictions should be used as guidance alongside local expertise and field observations.

## 🙏 Acknowledgments

- Data sources: NASA POWER, Pakistan Bureau of Statistics
- Based on FAO guidelines for crop water requirements
- Built with Streamlit and open-source Python libraries

## 📞 Support

For questions or support, please refer to the About page in the dashboard or check the documentation.

---

**Built with ❤️ for sustainable agriculture in Pakistan 🇵🇰**

Version 1.0 | December 2024
