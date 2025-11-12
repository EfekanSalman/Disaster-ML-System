import pandas as pd
import joblib
import json  # <-- NEW import to load the JSON model
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
import os

# --- Prophet Serialization ---
# REQUIRED to load the Prophet model (.json)
try:
    from prophet.serialize import model_from_json

    print("Prophet (JSON) loader imported.")
except ImportError:
    print("ERROR: 'prophet' library is missing in the 'src/main.py' environment!")
    model_from_json = None  # Prevent system crash

# --- Schema Imports ---
# Import schemas for THREE different problems
from src.schemas.damage import (
    DamagePredictionInput, DamagePredictionOutput,
    ClassificationInput, ClassificationOutput
)
from src.schemas.timeseries import (
    TimeSeriesInput, TimeSeriesOutput, ForecastItem  # <-- NEW
)

# --- Model Paths ---
# Define the paths for all THREE models
REGRESSION_MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'damage_model_v1.joblib')
CLASSIFICATION_MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'classification_model_v1.joblib')
TIMESERIES_MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'timeseries_model_v1.json')  # <-- NEW

# Global Model Storage (Cache)
models = {}


# --- 'lifespan' Context Manager ---
# UPDATE: 'lifespan' will now load all THREE models
@asynccontextmanager
async def lifespan(app: FastAPI):
    # API Startup
    global models

    # 1. Regression Model (.joblib)
    print(f"Loading model: {REGRESSION_MODEL_PATH}")
    try:
        models["regression"] = joblib.load(REGRESSION_MODEL_PATH)
        print("Regression model (Problem 1) loaded successfully.")
    except Exception as e:
        print(f"ERROR (Regression): {e}")
        models["regression"] = None

    # 2. Classification Model (.joblib)
    print(f"Loading model: {CLASSIFICATION_MODEL_PATH}")
    try:
        models["classification"] = joblib.load(CLASSIFICATION_MODEL_PATH)
        print("Classification model (Problem 2) loaded successfully.")
    except Exception as e:
        print(f"ERROR (Classification): {e}")
        models["classification"] = None

    # 3. Time Series Model (.json)
    # UPDATE: This is loaded with 'json' NOT 'joblib'
    print(f"Loading model: {TIMESERIES_MODEL_PATH}")
    try:
        if model_from_json is None:  # If the 'prophet' library is missing
            raise ImportError("Prophet library could not be loaded.")

        with open(TIMESERIES_MODEL_PATH, 'r') as f_in:
            models["timeseries"] = model_from_json(f_in.read())
        print("Time Series model (Problem 3) loaded successfully.")
    except Exception as e:
        print(f"ERROR (Time Series): {e}")
        models["timeseries"] = None

    yield  # Waits here while the API is running

    # API Shutdown
    print("API shutting down, clearing all models from memory.")
    models.clear()


# --- FastAPI Application (Final Version) ---
app = FastAPI(
    title="Disaster ML API (Multi-Model System)",
    description="ML System example for Emdat data (Regression + Classification + Time Series).",
    version="3.0.0",  # <-- Switched to v3
    lifespan=lifespan
)


# --- API Endpoints ---

@app.get("/")
def get_root():
    return {"status": "OK", "message": "Disaster ML API (v3 - Final) is running."}


# --- PROBLEM 1 ENDPOINT (UNCHANGED) ---
@app.post("/predict_damage", response_model=DamagePredictionOutput)
def post_predict_damage(input_data: DamagePredictionInput):
    model = models.get("regression")
    if model is None:
        raise HTTPException(status_code=503, detail="Regression model (Problem 1) could not be loaded.")
    try:
        input_df = pd.DataFrame([input_data.model_dump(by_alias=True)], index=[0])
        log_prediction = model.predict(input_df)[0]
        real_damage_prediction = 10 ** log_prediction
        return DamagePredictionOutput(
            log_damage_prediction=log_prediction,
            estimated_damage_usd_thousands=real_damage_prediction,
            model_version="damage_model_v1"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Problem 1 prediction error: {str(e)}")


# --- PROBLEM 2 ENDPOINT (UNCHANGED) ---
@app.post("/predict_subgroup", response_model=ClassificationOutput)
def post_predict_subgroup(input_data: ClassificationInput):
    model = models.get("classification")
    if model is None:
        raise HTTPException(status_code=503, detail="Classification model (Problem 2) could not be loaded.")
    try:
        input_df = pd.DataFrame([input_data.model_dump(by_alias=True)], index=[0])
        prediction = model.predict(input_df)[0]
        return ClassificationOutput(
            predicted_subgroup=prediction,
            model_version="classification_model_v1"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Problem 2 prediction error: {str(e)}")


# --- NEW: PROBLEM 3 ENDPOINT ---
@app.post("/predict_timeseries", response_model=TimeSeriesOutput)
def post_predict_timeseries(input_data: TimeSeriesInput):
    """
    (Problem 3) Forecasts the number of Flood events in Asia (Time Series)
    for the next N months (periods).
    """
    model = models.get("timeseries")
    if model is None:
        raise HTTPException(status_code=503, detail="Time Series model (Problem 3) could not be loaded.")

    try:
        # 1. Create the 'future' DataFrame using the model
        # We are sure to use 'ME' (Month-End) (from Step 22)
        future_df = model.make_future_dataframe(
            periods=input_data.periods_to_forecast,
            freq='ME'
        )

        # 2. Make the forecast
        forecast = model.predict(future_df)

        # 3. Filter only the 'future' predictions
        # (The user wants the future, not the history)
        future_predictions = forecast.iloc[-input_data.periods_to_forecast:]

        # 4. Convert the output to our Pydantic schema (List[ForecastItem])
        output_items = []
        for _, row in future_predictions.iterrows():
            output_items.append(
                ForecastItem(
                    date=row['ds'].date(),  # Get only the date (not the time)
                    predicted_count=row['yhat']  # 'yhat' is Prophet's prediction column
                )
            )

        return TimeSeriesOutput(
            model_version="timeseries_model_v1",
            forecast=output_items
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Problem 3 prediction error: {str(e)}")