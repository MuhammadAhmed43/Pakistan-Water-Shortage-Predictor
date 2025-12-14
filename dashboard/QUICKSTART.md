# Quick Start Guide 🚀

## Installation & Launch

### Step 1: Install Dependencies
```bash
cd c:\Users\muham\Downloads\MLPROJECT\dashboard
pip install -r requirements.txt
```

### Step 2: Launch the Dashboard
```bash
streamlit run app.py
```

The dashboard will open automatically in your browser at `http://localhost:8501`

---

## First Time Setup

### ⚠️ Note: Model File Required

The dashboard currently runs with calculated predictions directly (no trained model file needed for basic functionality). All predictions use the ET0 calculation and water balance formulas.

**If you want to use the trained ML model:**

1. Open your Jupyter notebook `main (3).ipynb`
2. Run all cells up to the model training section
3. Add this cell to save the model:

```python
import joblib

# Save the best model (Stacking ensemble)
best_model = trained_models["Stacking"]
joblib.dump(best_model, "dashboard/models/water_shortage_model.pkl")

print("✅ Model saved successfully!")
```

4. Run the cell to save the model

---

## Using the Dashboard

### 1. Make a Prediction

- Click **"Make Prediction"** in sidebar
- Fill in the form:
  - Select district (e.g., Lahore)
  - Choose crop (e.g., Wheat)
  - Set month and year
  - Enter weather parameters
- Click **"Predict Water Shortage"**
- View results, charts, and recommendations

### 2. View Map

- Click **"🗺️ Map View"** in sidebar
- Select crop and time period
- Click **"Generate Map"**
- Explore interactive map
- Click districts for details

### 3. Learn More

- Click **"ℹ️ About"** for full documentation
- Read methodology and user guide
- Understand model details

---

## Troubleshooting

### ImportError: No module named 'streamlit'
```bash
pip install streamlit
```

### Port already in use
```bash
streamlit run app.py --server.port 8502
```

### Map not showing
- Check internet connection (map tiles require online access)
- Refresh the page

---

## Features at a Glance

✅ Single district predictions  
✅ Interactive Pakistan map  
✅ Professional UI with Pakistan colors  
✅ Gauge charts and visualizations  
✅ CSV export functionality  
✅ Actionable recommendations  
✅ Responsive design  

---

## Next Steps

1. **Test the dashboard** with sample data
2. **Try different districts and crops**
3. **Export predictions** for your records
4. **Explore the map view** for district-wide analysis

Enjoy using the Pakistan Water Shortage Dashboard! 💧🇵🇰
