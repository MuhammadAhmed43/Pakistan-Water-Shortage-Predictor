# Pakistan Water Shortage Predictor

An end-to-end machine-learning system that predicts agricultural water shortage at
the district level across Punjab, Pakistan. The project pairs a Jupyter notebook
that documents the full data-science workflow (data cleaning, feature engineering,
model training and evaluation) with an interactive Streamlit dashboard intended for
farmers, extension officers, agricultural researchers and policymakers.

The predictor combines a Gradient-Boosting regressor for monthly rainfall with
standard agronomic formulas (FAO-style crop water demand, soil water retention,
and a Water Sufficiency Index) to produce an interpretable per-district forecast.

---

## Table of Contents

1. [Project Goals](#project-goals)
2. [System Overview](#system-overview)
3. [Repository Layout](#repository-layout)
4. [Methodology](#methodology)
5. [Data](#data)
6. [Model](#model)
7. [Dashboard Features](#dashboard-features)
8. [Installation](#installation)
9. [Running the Application](#running-the-application)
10. [Usage Guide](#usage-guide)
11. [Configuration Reference](#configuration-reference)
12. [Output Schema](#output-schema)
13. [Limitations and Disclaimer](#limitations-and-disclaimer)
14. [Roadmap](#roadmap)
15. [Contributing](#contributing)
16. [License](#license)
17. [Acknowledgements](#acknowledgements)

---

## Project Goals

Pakistan's agricultural sector accounts for roughly 90 percent of national
freshwater withdrawal, yet farmers and planners often lack timely, district-level
visibility into how much rainfall a coming month is likely to deliver and whether
it will meet the water demand of the crops they have planted. This project sets
out to:

- Quantify expected water shortage for any combination of district, crop, soil
  type, month and year covered by the dataset.
- Surface that information through a single, decision-oriented interface rather
  than raw model output.
- Make the underlying assumptions, formulas and limitations explicit so that
  results can be audited and improved.
- Provide a reproducible baseline (notebook plus dashboard) that future work can
  extend with additional regions, crops or data sources.

## System Overview

The system has three logical layers:

1. **Data layer.** A cleaned, merged dataset of historical weather, crop and soil
   observations for 26 Punjab districts spanning 2015 through 2023, stored as a
   single CSV.
2. **Modelling layer.** A monthly rainfall regressor trained on lagged and
   cyclical features, plus deterministic agronomic calculations that convert the
   predicted supply into a per-crop sufficiency index.
3. **Application layer.** The project ships with two interchangeable
   frontends that share the same predictor:
   - **FastAPI + Stitch UI** (primary): a polished, editorial dashboard
     designed in [Stitch](https://stitch.withgoogle.com) and served by
     FastAPI. Lives in `app.py`, `backend/`, `frontend/`. Run with
     `uvicorn app:app`.
   - **Streamlit** (legacy): the original multi-page Streamlit dashboard.
     Lives in `dashboard/`. Run with `streamlit run dashboard/Dashboard.py`.

The notebook `ML_project.ipynb` contains the offline workflow used during
development (exploratory analysis, feature engineering, model comparison and
metrics). Both application layers reuse the same preprocessing and modelling
logic at runtime; the FastAPI layer talks to `backend.predictor` (no Streamlit
dependency), while the Streamlit layer talks to `dashboard.utils.predictor`.

## Repository Layout

```
.
├── ML_project.ipynb                 Full data-science workflow and model comparison
├── README.md                        This document
├── .gitignore
├── requirements.txt                 FastAPI app dependencies
├── app.py                           FastAPI entry point
├── backend/                         Streamlit-free predictor + reference data
│   ├── predictor.py                 Model training, encoding and WSI calculation
│   └── constants.py                 Districts, crops, soils, coordinates, metrics
├── frontend/                        Stitch-designed UI
│   ├── templates/                   Jinja2 templates (base, overview, predict, map, about)
│   ├── static/
│   │   ├── css/custom.css
│   │   └── js/                      predict.js, map.js
│   └── stitch-original/             Raw HTML downloaded from Stitch (reference)
└── dashboard/                       Legacy Streamlit application
    ├── Dashboard.py                 Landing page and entry point
    ├── config.py                    Districts, crops, soil types, colours, thresholds
    ├── requirements.txt             Streamlit-app dependencies
    ├── .streamlit/config.toml       Streamlit theme configuration
    ├── pages/                       Streamlit page scripts
    │   ├── 01_Make_Prediction.py
    │   ├── 02_Map_View.py
    │   └── 03_About.py
    ├── utils/                       Reusable Python modules
    │   ├── predictor.py             Streamlit-wrapped predictor
    │   ├── map_generator.py         Folium choropleth and marker layer
    │   ├── visualizations.py        Plotly gauges, pies, trend charts
    │   └── ui.py                    Global styling and layout helpers
    ├── data/
    │   └── Cleaned_Pakistan_Water_Dataset_updated.csv
    └── models/                      Reserved for serialised model artifacts
```

## Methodology

The Water Sufficiency Index (WSI) is the dashboard's headline output. It is
defined as the ratio of effective water supply to crop water demand, expressed as
a percentage, so that values at or above 100 indicate no shortage and values
below 100 indicate progressively worse deficit.

### Step 1 — Predict monthly rainfall

The model predicts rainfall (in millimetres) for the chosen district, month and
year using eight features:

| Feature           | Description                                                      |
|-------------------|------------------------------------------------------------------|
| `Rainfall_lag1`   | Previous month's rainfall in the same district (mean if missing) |
| `Month_sin`       | sin(2 pi * Month / 12), cyclical encoding of seasonality         |
| `Month_cos`       | cos(2 pi * Month / 12), cyclical encoding of seasonality         |
| `Year`            | Calendar year                                                    |
| `Temperature_C`   | Monthly mean air temperature                                     |
| `Humidity_Percent`| Monthly mean relative humidity                                   |
| `Wind_Speed`      | Monthly mean wind speed                                          |
| `Solar_Radiation` | Monthly mean solar radiation (MJ/m^2/day)                        |

When the user has not supplied weather values for a future month, the
application looks them up from the historical average for that district and
month.

### Step 2 — Derive effective water supply

Not all rainfall is usable by crops; some runs off or percolates beyond the root
zone. The dashboard approximates this with a soil-retention factor:

```
soil_factor          = soil_water_capacity / max(soil_water_capacity over dataset)
effective_supply_mm  = (predicted_rainfall_mm * soil_factor) + supplemental_irrigation_mm
```

`supplemental_irrigation_mm` is a user-supplied estimate of water added from
tube wells, canals or other off-rainfall sources.

### Step 3 — Compute crop water demand

Crop water demand is taken directly from the dataset where available, or
imputed as the mean demand for that crop. The dataset's demand column itself is
derived from reference evapotranspiration (Penman–Monteith ET₀) multiplied by a
crop coefficient (Kc) over the relevant growing window, following standard FAO
Irrigation and Drainage Paper 56 guidance.

Indicative Kc values used by the configuration layer:

| Crop      | Kc   | Crop     | Kc   |
|-----------|------|----------|------|
| Paddy     | 1.15 | Pulses   | 0.50 |
| Sugarcane | 1.25 | Mungbean | 0.70 |
| Cotton    | 0.75 | Blackgram| 0.70 |
| Maize     | 0.60 | Lentil   | 0.70 |
| Wheat     | 0.50 | Banana   | 0.70 |
| Tobacco   | 0.85 | Mango    | 0.70 |
| Barley    | 0.45 | Grapes   | 0.70 |
| Millets   | 0.40 | Oil seeds| 0.55 |

### Step 4 — Water Sufficiency Index and severity class

```
WSI = (effective_supply_mm / crop_water_demand_mm) * 100
```

The continuous WSI is mapped to a five-level severity class for human
interpretation:

| Category    | WSI range        | Interpretation                                      |
|-------------|------------------|-----------------------------------------------------|
| No Shortage | WSI >= 100       | Supply meets or exceeds demand                      |
| Mild        | 80 <= WSI < 100  | Minor deficit, low-cost mitigation usually enough   |
| Moderate    | 60 <= WSI < 80   | Visible stress likely without active management     |
| Severe      | 40 <= WSI < 60   | Significant yield risk, intervention required       |
| Critical    | WSI < 40         | Crop failure risk; emergency response indicated     |

## Data

- **Source files.** Raw monthly observations sourced from publicly available
  weather records (e.g. NASA POWER) and Pakistan Bureau of Statistics crop
  series, cleaned and merged into `Cleaned_Pakistan_Water_Dataset_updated.csv`.
- **Coverage.** 26 districts across Punjab; 16 crop categories; 2015 to 2023.
- **Granularity.** One row per district / month / year / crop / soil-type
  combination (~33,700 rows after cleaning).
- **Engineered columns.** `Rainfall_lag1`, `Month_sin`, `Month_cos`,
  `Crop_Water_Demand_mm`, `Soil_Water_Capacity`, label-encoded categoricals.
- **Leakage controls.** `Water_Shortage_Level` and `Water_Balance_mm` are
  dropped before training because they directly encode the target.

## Model

### Notebook workflow (`ML_project.ipynb`)

The notebook compares several regressors on a held-out time-aware split,
including Linear Regression, Random Forest, Gradient Boosting and a stacking
ensemble that combines Gradient Boosting and Random Forest with a Ridge final
estimator. Headline metrics on the held-out test set:

| Metric  | Value |
|---------|-------|
| MAE     | 1.41  |
| RMSE    | 2.28  |
| R^2     | 0.0645 |

The low R^2 reflects the intrinsic difficulty of forecasting monthly rainfall
from a small feature set; the model is most useful as a relative ranking tool
across districts and months rather than as an absolute precipitation forecaster.
Future work should add satellite-derived NDVI, ENSO indices and longer history
windows to improve skill.

### Runtime model (`dashboard/utils/predictor.py`)

To keep the dashboard self-contained and avoid shipping a serialised model
binary, the runtime layer retrains a `GradientBoostingRegressor` on the cleaned
dataset on first use and caches it in memory with `@st.cache_resource`. This
typically completes in a few seconds on a modern laptop. The `models/`
directory is reserved for a future workflow in which the stacking ensemble
trained inside the notebook is exported with `joblib.dump` and loaded here
directly.

## Dashboard Features

- **Landing page.** Project summary, mission statement and headline coverage
  metrics.
- **Make Prediction.** Single-point form for district, crop, soil, month, year
  and optional supplemental irrigation. Produces:
  - Headline WSI percentage and severity class.
  - Predicted rainfall, irrigation added, effective supply and crop demand.
  - Gauge chart, supply / deficit pie chart and seasonal trend chart.
  - Recommendation panel keyed to the severity class.
  - CSV download of the full result payload.
- **Map View.** Generates predictions for every supported district under a
  chosen crop / soil / month / year combination and renders them as an
  interactive Folium map with colour-coded markers and per-district pop-ups.
  Includes aggregated summary metrics (average WSI, count of critical
  districts, average predicted rainfall, average temperature).
- **About.** In-app documentation covering methodology, supported districts and
  crops, technical stack, and a disclaimer.

## Installation

### Prerequisites

- Python 3.9 or newer.
- pip (bundled with modern Python distributions).
- An active internet connection for the first run, so that Folium tile servers
  and any missing wheels can be reached.

### Set up a virtual environment

It is strongly recommended to install dependencies into a project-local
virtual environment to avoid conflicts with system Python.

Windows (PowerShell):

```powershell
python -m venv dashboard\venv
dashboard\venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
python3 -m venv dashboard/venv
source dashboard/venv/bin/activate
```

### Install dependencies

```bash
pip install --upgrade pip
pip install -r dashboard/requirements.txt
```

The pinned dependency set is:

```
streamlit>=1.29.0
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.3.0
plotly>=5.17.0
folium>=0.15.0
streamlit-folium>=0.15.0
streamlit-option-menu>=0.3.6
joblib>=1.3.2
matplotlib>=3.7.0
seaborn>=0.12.0
Pillow>=10.0.0
```

## Running the Application

### Primary: FastAPI + Stitch UI

This is the production-style frontend, built on a Stitch-designed UI served
through FastAPI templates with a small JSON API for the prediction logic.

Install the FastAPI dependencies (in addition to the Streamlit ones, which
share most of the same packages):

```bash
pip install -r requirements.txt
```

Then launch from the repository root:

```bash
uvicorn app:app --reload --port 8000
```

Open `http://127.0.0.1:8000`. The first request triggers a one-off training
pass on the CSV; subsequent requests are served from cache.

The app exposes four pages and a small JSON API:

| Path           | What it serves                                              |
|----------------|-------------------------------------------------------------|
| `GET /`        | Overview / landing page                                     |
| `GET /predict` | Single-point prediction form and results                    |
| `GET /map`     | District-wide map view with Leaflet                         |
| `GET /about`   | Methodology and model card                                  |
| `POST /api/predict`     | JSON prediction for one district / crop                |
| `POST /api/map`         | JSON predictions for every supported district          |
| `POST /api/predict/csv` | CSV download of one prediction                         |
| `GET /api/health`       | Liveness check; returns 200 when the model is loaded   |

The Stitch source files that the templates were derived from are kept in
`frontend/stitch-original/` for reference and future re-design rounds.

### Legacy: Streamlit dashboard

The original Streamlit dashboard is still in `dashboard/` and remains
fully functional. From the repository root:

```bash
streamlit run dashboard/Dashboard.py
```

Streamlit prints both a local URL (typically `http://localhost:8501`) and a
network URL. The first prediction triggers a one-off training pass on the CSV
and is therefore slower than subsequent calls.

To bind a different port (useful when 8501 is in use):

```bash
streamlit run dashboard/Dashboard.py --server.port 8502
```

To run on a remote host while keeping the UI reachable from another machine,
launch with `--server.address 0.0.0.0` and ensure the host's firewall permits
inbound traffic on the chosen port.

## Usage Guide

### Producing a single prediction

1. Open the dashboard in a browser and select **Make Prediction** in the
   sidebar.
2. Choose a district, crop and soil type.
3. Pick a month and year. Years outside 2015–2023 are allowed; the model will
   extrapolate using historical seasonal averages and lagged rainfall.
4. Optionally specify supplemental irrigation in millimetres to represent
   non-rainfall water inputs.
5. Click **Predict Water Shortage**.
6. Inspect the WSI, severity class, supporting metrics, charts and
   recommendations. Use the **Download Prediction Data (CSV)** button to
   persist the full payload for record-keeping or downstream analysis.

### Generating a district-wide map

1. Navigate to **Map View**.
2. Choose crop, month, year, soil filter and optional supplemental irrigation.
3. Click **Generate Map**. The application iterates over every configured
   district, runs the prediction pipeline for each, and assembles the results
   into a Folium map.
4. Review the summary metrics above the map, then click individual district
   markers for per-location detail. The accompanying expandable data table
   exposes the underlying values for further inspection.

## Configuration Reference

`dashboard/config.py` is the single source of truth for static reference data:

- `DISTRICTS` — supported district list (Punjab, Pakistan).
- `CROPS` — supported crop list.
- `SOIL_TYPES` — supported soil categories used by the encoder.
- `SHORTAGE_THRESHOLDS` — numeric ranges that drive severity classification.
- `CROP_KC` — crop coefficients used for water-demand calculations.
- `SOIL_WATER_CAPACITY` — reference soil water retention values, in millimetres.
- `PARAM_RANGES` — default sliders / numeric ranges for weather inputs.
- `DISTRICT_COORDS` — latitude / longitude pairs used by the map view.
- `PAKISTAN_CENTER`, `MAP_ZOOM` — default Folium viewport.
- Colour palette constants (`PRIMARY_COLOR`, `ACCENT_COLOR`, etc.) used by the
  Streamlit theme.

To extend the project to additional districts or crops, update these constants
and ensure the underlying dataset contains the corresponding rows; no other
code changes are required.

## Output Schema

The CSV exported from the prediction page (and, internally, the dictionary
returned from `predict_water_shortage_logic`) contains the following fields:

| Field                | Type    | Description                                                |
|----------------------|---------|------------------------------------------------------------|
| `rainfall_pred`      | float   | Model-predicted rainfall in millimetres                    |
| `irrigation_added`   | float   | User-supplied supplemental irrigation in millimetres       |
| `effective_supply`   | float   | (rainfall_pred * soil_factor) + irrigation_added           |
| `wsi`                | float   | Water Sufficiency Index, percentage                        |
| `severity`           | string  | One of No Shortage / Mild / Moderate / Severe / Critical   |
| `shortage_category`  | string  | Alias of `severity` retained for backward compatibility    |
| `temperature`        | float   | Temperature used during inference (°C)                     |
| `humidity`           | float   | Relative humidity used during inference (%)                |
| `wind`               | float   | Wind speed used during inference (m/s)                     |
| `solar`              | float   | Solar radiation used during inference (MJ/m^2/day)         |
| `soil_capacity`      | float   | Soil water capacity used during inference (mm)             |
| `crop_demand`        | float   | Crop water demand for the chosen crop (mm)                 |
| `soil_factor`        | float   | Normalised soil retention factor (0–1)                     |

## Limitations and Disclaimer

- The rainfall model's R^2 is low. Predictions should be treated as a planning
  aid rather than a precise meteorological forecast.
- Coverage is currently limited to Punjab; other provinces and tehsil-level
  granularity are out of scope for the current release.
- Soil retention is modelled with a single coefficient per soil type. Real
  field conditions vary with depth, organic content, slope and irrigation
  practices.
- The supplemental-irrigation input is user-supplied; the dashboard does not
  attempt to estimate canal or tube-well allocations independently.
- Outputs are descriptive, not prescriptive. Decisions about cropping patterns,
  irrigation schedules or emergency response should be made in consultation
  with local agricultural extension services and on-ground observation.

## Roadmap

Indicative next steps, ordered by approximate impact:

1. Export the notebook's stacking ensemble to `dashboard/models/` and load it
   at runtime rather than retraining on every cold start.
2. Add a held-out evaluation page that surfaces backtest accuracy, calibration
   plots and feature importances.
3. Extend coverage beyond Punjab and to tehsil-level granularity where data
   permits.
4. Incorporate satellite-derived NDVI, soil-moisture estimates and ENSO indices
   as additional features.
5. Containerise the dashboard (Docker / `pyproject.toml` based packaging) and
   add a continuous-integration pipeline for linting, tests and model
   regression checks.
6. Provide an HTTP API wrapper around `predict_water_shortage_logic` so that
   third-party tools can consume the same predictions without going through
   Streamlit.

## Contributing

Contributions are welcome. To propose a change:

1. Open an issue describing the problem or feature.
2. Fork the repository and create a topic branch.
3. Keep the change focused; one concern per pull request.
4. Include a brief description of how to verify the change locally.
5. Ensure new Python files follow the existing module layout
   (`utils/` for reusable logic, `pages/` for Streamlit views, `config.py` for
   static reference data).

## License

This project is released under the MIT License. See `LICENSE` for the full
text when present, or treat the standard MIT terms as applicable in the
interim.

## Acknowledgements

- Reference evapotranspiration methodology follows FAO Irrigation and Drainage
  Paper 56 (Allen et al., 1998).
- Historical weather observations leverage publicly available reanalysis data
  such as NASA POWER.
- Crop production statistics draw on the Pakistan Bureau of Statistics and
  related provincial agricultural reports.
- The dashboard is built on top of the Streamlit, scikit-learn, Plotly, Folium
  and pandas open-source projects, without which this work would not be
  feasible.
