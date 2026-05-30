"""
FastAPI entry point for the Pakistan Water Shortage Predictor.

Serves the Stitch-designed UI as Jinja2 templates and exposes a small JSON
API that wraps ``backend.predictor`` for client-side fetch calls.
"""
from __future__ import annotations

import csv
import io
import os
from typing import List, Optional

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from backend import constants
from backend.predictor import (
    get_crop_monthly_demand,
    get_historical_monthly_stats,
    get_model_bundle,
    get_recommendations,
    predict,
)

_HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(_HERE, "frontend", "templates")
STATIC_DIR = os.path.join(_HERE, "frontend", "static")

app = FastAPI(
    title="Pakistan Water Shortage Predictor",
    description="Decision-grade water intelligence for Pakistan's agriculture.",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATE_DIR)

# Defaults the prediction form starts with.
DEFAULT_DISTRICT = "Multan"
DEFAULT_CROP = "Wheat"
DEFAULT_SOIL = "Loamy"
DEFAULT_MONTH = 6
DEFAULT_YEAR = 2024


def _base_context(active: str) -> dict:
    return {
        "active": active,
        "districts": constants.DISTRICTS,
        "crops": constants.CROPS,
        "soil_types": constants.SOIL_TYPES,
        "months": list(enumerate(constants.MONTHS, start=1)),
        "metrics": constants.HEADLINE_METRICS,
        "model_metrics": constants.MODEL_METRICS,
    }


@app.on_event("startup")
def _warm_model() -> None:
    """Train the model on startup so the first request is fast."""
    try:
        get_model_bundle()
    except FileNotFoundError as exc:
        # Don't crash the process — the user will see the error on first request.
        print(f"[startup] Model bundle could not be loaded: {exc}")


@app.get("/", response_class=HTMLResponse)
def overview(request: Request):
    return templates.TemplateResponse(
        request, "overview.html", _base_context("overview")
    )


@app.get("/predict", response_class=HTMLResponse)
def predict_page(request: Request):
    ctx = _base_context("predict")
    ctx.update(
        {
            "default_district": DEFAULT_DISTRICT,
            "default_crop": DEFAULT_CROP,
            "default_soil": DEFAULT_SOIL,
            "default_month": DEFAULT_MONTH,
            "default_year": DEFAULT_YEAR,
        }
    )
    return templates.TemplateResponse(request, "predict.html", ctx)


@app.get("/map", response_class=HTMLResponse)
def map_page(request: Request):
    ctx = _base_context("map")
    ctx.update(
        {
            "default_crop": DEFAULT_CROP,
            "default_soil": DEFAULT_SOIL,
            "default_month": DEFAULT_MONTH,
            "default_year": DEFAULT_YEAR,
            "district_coords": constants.DISTRICT_COORDS,
            "pakistan_center": constants.PAKISTAN_CENTER,
            "map_zoom": constants.MAP_ZOOM,
        }
    )
    return templates.TemplateResponse(request, "map.html", ctx)


@app.get("/about", response_class=HTMLResponse)
def about_page(request: Request):
    return templates.TemplateResponse(request, "about.html", _base_context("about"))


# --- JSON API ---------------------------------------------------------------


class PredictRequest(BaseModel):
    district: str
    crop: str
    soil: str
    month: int = Field(..., ge=1, le=12)
    year: int = Field(..., ge=2000, le=2050)
    irrigation_mm: float = Field(0.0, ge=0.0, le=1000.0)


@app.post("/api/predict")
def api_predict(payload: PredictRequest):
    result = predict(
        year=payload.year,
        month=payload.month,
        district_name=payload.district,
        soil_type_name=payload.soil,
        crop_type_name=payload.crop,
        irrigation_mm=payload.irrigation_mm,
    )
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    monthly_rain = get_historical_monthly_stats(payload.district) or []
    monthly_demand = get_crop_monthly_demand(payload.crop) or []

    return JSONResponse(
        {
            "input": payload.model_dump(),
            "result": result,
            "recommendations": get_recommendations(result["severity"]),
            "trend": {
                "rainfall": monthly_rain,
                "demand": monthly_demand,
            },
        }
    )


class MapRequest(BaseModel):
    crop: str
    soil: str
    month: int = Field(..., ge=1, le=12)
    year: int = Field(..., ge=2000, le=2050)
    irrigation_mm: float = Field(0.0, ge=0.0, le=1000.0)
    districts: Optional[List[str]] = None


@app.post("/api/map")
def api_map(payload: MapRequest):
    districts = payload.districts or constants.DISTRICTS
    rows = []
    for district in districts:
        result = predict(
            year=payload.year,
            month=payload.month,
            district_name=district,
            soil_type_name=payload.soil,
            crop_type_name=payload.crop,
            irrigation_mm=payload.irrigation_mm,
        )
        if "error" in result:
            continue
        coords = constants.DISTRICT_COORDS.get(district)
        rows.append(
            {
                "district": district,
                "lat": coords[0] if coords else None,
                "lon": coords[1] if coords else None,
                **result,
            }
        )

    if not rows:
        raise HTTPException(status_code=400, detail="No predictions could be generated.")

    avg_wsi = sum(r["wsi"] for r in rows) / len(rows)
    avg_rainfall = sum(r["rainfall_pred"] for r in rows) / len(rows)
    avg_temp = sum(r["temperature"] for r in rows) / len(rows)
    critical = sum(1 for r in rows if r["severity"] == "Critical")
    severe = sum(1 for r in rows if r["severity"] == "Severe")

    return JSONResponse(
        {
            "input": payload.model_dump(),
            "summary": {
                "avg_wsi": avg_wsi,
                "avg_rainfall": avg_rainfall,
                "avg_temperature": avg_temp,
                "critical_count": critical,
                "severe_count": severe,
                "total": len(rows),
            },
            "rows": rows,
        }
    )


@app.post("/api/predict/csv")
def api_predict_csv(payload: PredictRequest):
    result = predict(
        year=payload.year,
        month=payload.month,
        district_name=payload.district,
        soil_type_name=payload.soil,
        crop_type_name=payload.crop,
        irrigation_mm=payload.irrigation_mm,
    )
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(
        [
            "District", "Crop", "Soil", "Month", "Year",
            "Irrigation (mm)", "Predicted Rainfall (mm)", "Effective Supply (mm)",
            "Crop Demand (mm)", "Deficit (mm)", "WSI (%)", "Severity",
            "Temperature (C)", "Humidity (%)", "Wind (m/s)", "Solar (MJ/m^2/day)",
            "Soil Capacity (mm)",
        ]
    )
    writer.writerow(
        [
            payload.district, payload.crop, payload.soil, payload.month, payload.year,
            f"{payload.irrigation_mm:.1f}",
            f"{result['rainfall_pred']:.2f}",
            f"{result['effective_supply']:.2f}",
            f"{result['crop_demand']:.2f}",
            f"{result['deficit']:.2f}",
            f"{result['wsi']:.2f}",
            result["severity"],
            f"{result['temperature']:.2f}",
            f"{result['humidity']:.2f}",
            f"{result['wind']:.2f}",
            f"{result['solar']:.2f}",
            f"{result['soil_capacity']:.2f}",
        ]
    )
    output.seek(0)
    filename = (
        f"forecast_{payload.district}_{payload.crop}_"
        f"{payload.year}-{payload.month:02d}.csv"
    )
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@app.get("/api/health")
def health():
    try:
        get_model_bundle()
        return {"status": "ok"}
    except FileNotFoundError as exc:
        return JSONResponse({"status": "error", "detail": str(exc)}, status_code=503)
