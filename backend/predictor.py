"""
Streamlit-free predictor core.

Mirrors the prediction logic from dashboard/utils/predictor.py but without any
Streamlit dependency, so it can be served from a plain FastAPI process.
The trained model is built once on first call and cached for the lifetime of
the process via module-level globals.
"""
from __future__ import annotations

import os
import threading
from functools import lru_cache
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import LabelEncoder


# Resolve the dataset path relative to this file so the app works from any CWD.
_HERE = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(_HERE)
DATASET_PATH = os.path.join(
    _PROJECT_ROOT,
    "dashboard",
    "data",
    "Cleaned_Pakistan_Water_Dataset_updated.csv",
)

FEATURES = [
    "Rainfall_lag1",
    "Month_sin",
    "Month_cos",
    "Year",
    "Temperature_C",
    "Humidity_Percent",
    "Wind_Speed",
    "Solar_Radiation",
]

_CACHE_LOCK = threading.Lock()
_CACHE: Dict[str, object] = {}


def _train() -> Tuple[GradientBoostingRegressor, pd.DataFrame, Dict[str, LabelEncoder]]:
    if not os.path.exists(DATASET_PATH):
        raise FileNotFoundError(
            f"Dataset not found at {DATASET_PATH}. Place "
            "Cleaned_Pakistan_Water_Dataset_updated.csv in dashboard/data/."
        )

    df = pd.read_csv(DATASET_PATH)

    df = df.rename(
        columns={
            "Soil Type": "Soil_Type",
            "Crop": "Crop_Type",
            "Rainfall_mm": "Rainfall",
        }
    )

    leakage_cols = ["Water_Shortage_Level", "Water_Balance_mm"]
    df.drop(columns=[c for c in leakage_cols if c in df.columns], inplace=True)

    df = df.sort_values(by=["District", "Year", "Month"])
    df = df.dropna().reset_index(drop=True)

    label_encoders: Dict[str, LabelEncoder] = {}
    for col in ["District", "Crop_Type", "Soil_Type", "Season"]:
        if col not in df.columns:
            continue
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le

    df = df.sort_values(by=["District", "Year", "Month"])
    df["Rainfall_lag1"] = df.groupby("District")["Rainfall"].shift(1)
    df["Month_sin"] = np.sin(2 * np.pi * df["Month"] / 12)
    df["Month_cos"] = np.cos(2 * np.pi * df["Month"] / 12)
    df = df.dropna().reset_index(drop=True)

    X = df[FEATURES]
    y = df["Rainfall"]

    model = GradientBoostingRegressor(random_state=42)
    model.fit(X, y)
    return model, df, label_encoders


def get_model_bundle():
    """Train (or return cached) model, dataframe, and label encoders."""
    if "model" not in _CACHE:
        with _CACHE_LOCK:
            if "model" not in _CACHE:
                model, df, encoders = _train()
                _CACHE["model"] = model
                _CACHE["df"] = df
                _CACHE["encoders"] = encoders
    return _CACHE["model"], _CACHE["df"], _CACHE["encoders"]


def classify_severity(wsi: float) -> str:
    if wsi >= 100.0:
        return "No Shortage"
    if wsi >= 80.0:
        return "Mild"
    if wsi >= 60.0:
        return "Moderate"
    if wsi >= 40.0:
        return "Severe"
    return "Critical"


SEVERITY_HEX = {
    "No Shortage": "#2F7D4F",
    "Mild": "#6DA579",
    "Moderate": "#D6A848",
    "Severe": "#C7702C",
    "Critical": "#8E2A1F",
}


def predict(
    year: int,
    month: int,
    district_name: str,
    soil_type_name: str,
    crop_type_name: str,
    irrigation_mm: float = 0.0,
) -> Dict:
    model, df, encoders = get_model_bundle()

    try:
        encoded_district = encoders["District"].transform([district_name])[0]
    except (KeyError, ValueError):
        return {"error": f"District '{district_name}' not in dataset."}

    try:
        encoded_soil = encoders["Soil_Type"].transform([soil_type_name])[0]
    except (KeyError, ValueError):
        return {"error": f"Soil Type '{soil_type_name}' not in dataset."}

    try:
        encoded_crop = encoders["Crop_Type"].transform([crop_type_name])[0]
    except (KeyError, ValueError):
        return {"error": f"Crop Type '{crop_type_name}' not in dataset."}

    # Lagged rainfall: look up previous month, fall back to district average,
    # then to global mean.
    prev_year, prev_month = (year, month - 1) if month > 1 else (year - 1, 12)
    prev = df[
        (df["Year"] == prev_year)
        & (df["Month"] == prev_month)
        & (df["District"] == encoded_district)
    ]
    if not prev.empty:
        last_month_rainfall = float(prev["Rainfall"].mean())
    else:
        avg = df[
            (df["District"] == encoded_district)
            & (df["Month"] == prev_month)
        ]["Rainfall"].mean()
        last_month_rainfall = float(
            avg if not pd.isna(avg) else df["Rainfall"].mean()
        )

    # Environmental features for the target month: exact match if it exists,
    # else seasonal average for the district + month.
    ctx = df[
        (df["Year"] == year)
        & (df["Month"] == month)
        & (df["District"] == encoded_district)
        & (df["Soil_Type"] == encoded_soil)
        & (df["Crop_Type"] == encoded_crop)
    ]
    if not ctx.empty:
        row = ctx.iloc[0]
        temperature = float(row["Temperature_C"])
        humidity = float(row["Humidity_Percent"])
        wind = float(row["Wind_Speed"])
        solar = float(row["Solar_Radiation"])
        soil_capacity = float(row["Soil_Water_Capacity"])
        crop_demand = float(row["Crop_Water_Demand_mm"])
    else:
        seasonal = (
            df[(df["District"] == encoded_district) & (df["Month"] == month)]
            .agg(
                {
                    "Temperature_C": "mean",
                    "Humidity_Percent": "mean",
                    "Wind_Speed": "mean",
                    "Solar_Radiation": "mean",
                }
            )
            .to_dict()
        )
        temperature = float(seasonal.get("Temperature_C", df["Temperature_C"].mean()))
        humidity = float(seasonal.get("Humidity_Percent", df["Humidity_Percent"].mean()))
        wind = float(seasonal.get("Wind_Speed", df["Wind_Speed"].mean()))
        solar = float(seasonal.get("Solar_Radiation", df["Solar_Radiation"].mean()))

        soil_avg = df[df["Soil_Type"] == encoded_soil]["Soil_Water_Capacity"].mean()
        soil_capacity = float(
            soil_avg if not pd.isna(soil_avg) else df["Soil_Water_Capacity"].mean()
        )

        crop_avg = df[df["Crop_Type"] == encoded_crop]["Crop_Water_Demand_mm"].mean()
        crop_demand = float(
            crop_avg if not pd.isna(crop_avg) else df["Crop_Water_Demand_mm"].mean()
        )

    month_sin = float(np.sin(2 * np.pi * month / 12))
    month_cos = float(np.cos(2 * np.pi * month / 12))

    X_user = pd.DataFrame(
        [
            [
                last_month_rainfall,
                month_sin,
                month_cos,
                year,
                temperature,
                humidity,
                wind,
                solar,
            ]
        ],
        columns=FEATURES,
    )

    rainfall_pred = float(model.predict(X_user)[0])
    soil_factor = soil_capacity / float(df["Soil_Water_Capacity"].max())
    if crop_demand == 0:
        crop_demand = 1e-6

    effective_supply = (rainfall_pred * soil_factor) + float(irrigation_mm)
    wsi = (effective_supply / crop_demand) * 100.0
    severity = classify_severity(wsi)
    deficit = max(crop_demand - effective_supply, 0.0)

    return {
        "rainfall_pred": rainfall_pred,
        "irrigation_added": float(irrigation_mm),
        "effective_supply": effective_supply,
        "deficit": deficit,
        "wsi": wsi,
        "severity": severity,
        "severity_color": SEVERITY_HEX[severity],
        "temperature": temperature,
        "humidity": humidity,
        "wind": wind,
        "solar": solar,
        "soil_capacity": soil_capacity,
        "crop_demand": crop_demand,
        "soil_factor": soil_factor,
    }


_RECOMMENDATIONS = {
    "No Shortage": [
        ("Maintain Current Schedule",
         "Water supply meets crop demand. Continue the existing irrigation rhythm and keep monitoring weather updates."),
        ("Build a Buffer",
         "Use the surplus to top up tube-well reserves or recharge nearby ponds before the next dry stretch."),
        ("Audit Efficiency",
         "Even in surplus months, scheduled efficiency checks on canal turnouts and drip lines protect the budget for tighter periods."),
        ("Document Conditions",
         "Log soil moisture and yield observations so this month becomes a useful baseline for future comparisons."),
    ],
    "Mild": [
        ("Adopt Water-Saving Irrigation",
         "Switch from flood to drip or sprinkler where feasible. A mild deficit responds quickly to small efficiency gains."),
        ("Apply Mulch",
         "Organic or plastic mulch over the root zone cuts surface evaporation and buys back the small gap between supply and demand."),
        ("Watch Soil Moisture Daily",
         "Spot-check moisture at root depth each morning so any worsening trend is caught early."),
        ("Plan a Supplemental Run",
         "Pre-arrange a short tube-well run for the most water-sensitive growth stage."),
    ],
    "Moderate": [
        ("Prioritise Critical Growth Stages",
         "Concentrate available water on flowering, tillering, or fruit-set windows where deficit causes the largest yield loss."),
        ("Practice Deficit Irrigation",
         "Apply less water than full demand on tolerant stages, full water on sensitive ones. This is a documented coping strategy."),
        ("Improve Soil Retention",
         "Mulching, conservation tillage, and adding organic matter all raise effective soil water capacity over the next cycle."),
        ("Review Crop Mix",
         "If this district shows recurring moderate shortage, consider rotating in lower-Kc crops next season."),
    ],
    "Severe": [
        ("Trigger Emergency Irrigation",
         "Coordinate priority canal turns or tube-well runs for the most viable plots immediately."),
        ("Reduce Cropped Area",
         "Concentrating water on a smaller area is more productive than spreading a deficit across the full plot."),
        ("Apply Anti-Transpirants",
         "Spray-applied anti-transpirants and shade netting on high-value plots reduce water loss in the critical week."),
        ("Engage Local Authorities",
         "Notify the district agriculture office; severe shortage at scale changes canal allocation decisions upstream."),
    ],
    "Critical": [
        ("Activate Drought Protocols",
         "This is a crop-failure-risk forecast. Implement the district drought response plan now, not later."),
        ("Salvage the Most Viable Plots",
         "Focus remaining water on plots with the highest survival probability; accept losses on the rest."),
        ("Engage Relief Programmes",
         "Begin paperwork for crop insurance and government drought relief; these programmes have lead times."),
        ("Plan a Drought-Tolerant Next Cycle",
         "Pre-order seeds for short-duration or low-Kc varieties so the next planting window is not lost."),
    ],
}


def get_recommendations(severity: str) -> List[Dict[str, str]]:
    return [
        {"title": title, "body": body}
        for title, body in _RECOMMENDATIONS.get(severity, [])
    ]


def get_historical_monthly_stats(district_name: str) -> Optional[List[Dict]]:
    """Return per-month historical mean rainfall and temperature for a district."""
    _, df, encoders = get_model_bundle()
    try:
        encoded = encoders["District"].transform([district_name])[0]
    except (KeyError, ValueError):
        return None

    sub = df[df["District"] == encoded]
    if sub.empty:
        return None

    grouped = (
        sub.groupby("Month")
        .agg({"Rainfall": "mean", "Temperature_C": "mean"})
        .reset_index()
        .sort_values("Month")
    )
    return [
        {
            "month": int(r["Month"]),
            "rainfall": float(r["Rainfall"]),
            "temperature": float(r["Temperature_C"]),
        }
        for _, r in grouped.iterrows()
    ]


def get_crop_monthly_demand(crop_name: str) -> Optional[List[Dict]]:
    """Return per-month average water demand (mm) for a crop."""
    _, df, encoders = get_model_bundle()
    try:
        encoded = encoders["Crop_Type"].transform([crop_name])[0]
    except (KeyError, ValueError):
        return None

    sub = df[df["Crop_Type"] == encoded]
    if sub.empty:
        return None

    grouped = (
        sub.groupby("Month")["Crop_Water_Demand_mm"].mean().reset_index().sort_values("Month")
    )
    return [
        {"month": int(r["Month"]), "demand": float(r["Crop_Water_Demand_mm"])}
        for _, r in grouped.iterrows()
    ]
