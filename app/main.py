"""API FastAPI — service de classification de criticité (M0-B1).

Expose un modèle scikit-learn pré-entraîné (cf. `model/train_baseline.py`) via
deux routes :

- `GET /health`  : santé du service (déjà fonctionnel)
- `POST /predict` : prédiction de criticité (🎯 à compléter par l'apprenant)

Le modèle est chargé une seule fois au démarrage via le `lifespan` FastAPI puis
réutilisé pour chaque requête.

Lancement local :
    uvicorn app.main:app --reload
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

import joblib
from fastapi import FastAPI, HTTPException
from loguru import logger

from app.schemas import HealthResponse, MachineInput, PredictionResponse

from time import perf_counter
import pandas as pd

MODEL_PATH = Path(__file__).resolve().parents[1] / "model" / "model.joblib"

"""Cretae log File"""
LOG_PATH = Path(__file__).resolve().parents[1] / "logs" / "api.log"
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
logger.add(
    LOG_PATH,
    rotation="5 MB",
    retention="7 days",
    compression="zip",
    encoding="utf-8",
    enqueue=True,
    format=(
        "{time:YYYY-MM-DD HH:mm:ss.SSS} | "
        "{level:<8} | "
        "{message}"
    ),
)
# Mémoire d'application — peuplée par le lifespan
state: dict[str, Any] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Charge le modèle au démarrage, libère à l'arrêt.

    Args:
        app: instance FastAPI.
    """
    if not MODEL_PATH.is_file():
        logger.error(
            f"Modèle introuvable : {MODEL_PATH}. "
            f"Lance d'abord : python model/train_baseline.py"
        )
        raise RuntimeError(f"Modèle introuvable : {MODEL_PATH}")

    logger.info(f"Chargement du modèle depuis {MODEL_PATH}")
    state["model"] = joblib.load(MODEL_PATH)
    logger.info("Modèle chargé.")

    yield

    state.clear()
    logger.info("Service arrêté, état libéré.")


app = FastAPI(
    title="FastIA — Service de criticité maintenance prédictive",
    description=(
        "API d'exposition d'un modèle scikit-learn de classification de criticité "
        "d'incidents machine (3 classes : basse, moyenne, haute)."
    ),
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """Retourne le statut du service et du modèle.

    Returns:
        HealthResponse — `status="ok"` si le modèle est chargé, `degraded` sinon.
    """
    is_loaded = "model" in state
    return HealthResponse(
        status="ok" if is_loaded else "degraded",
        model_loaded=is_loaded,
    )


@app.post("/predict", response_model=PredictionResponse)
def predict(item: MachineInput) -> PredictionResponse:
    """Prédit la criticité d'une machine à partir de ses caractéristiques.

    🎯 **À COMPLÉTER PAR L'APPRENANT.**

    Indices d'implémentation :

    1. Construire un DataFrame pandas à 1 ligne à partir de `item.model_dump()`.
       Le pipeline scikit-learn attend les colonnes dans le même ordre qu'à
       l'entraînement (cf. `model/train_baseline.py`, `NUM_FEATURES` + `CAT_FEATURES`).
    2. Récupérer le modèle via `state["model"]`.
    3. Appeler `model.predict(df)[0]` pour obtenir la classe prédite (str).
    4. Appeler `model.predict_proba(df)[0]` pour obtenir les probabilités.
       Les classes correspondantes sont dans `model.classes_`.
    5. Construire et retourner un `PredictionResponse`.
    6. Logger l'entrée + la classe prédite + le temps de réponse via Loguru.

    Args:
        item: caractéristiques de la machine (cf. `schemas.MachineInput`).

    Returns:
        PredictionResponse avec la classe prédite et les probabilités.
    """
    """Prédit la criticité d'une machine à partir de ses caractéristiques."""
    
    start_time = perf_counter()
    input_data = item.model_dump()

    model = state.get("model")

    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Le modèle n'est pas chargé.",
        )

    try:
        dataframe = pd.DataFrame([input_data])

        predicted_class = str(model.predict(dataframe)[0])
        predicted_probabilities = model.predict_proba(dataframe)[0]

        probabilities = {
            str(class_name): float(probability)
            for class_name, probability in zip(
                model.classes_,
                predicted_probabilities,
                strict=True,
            )
        }

        duration_ms = (perf_counter() - start_time) * 1000

        logger.info(
            "Prédiction | entrée={} | criticité={} | durée_ms={:.2f}",
            input_data,
            predicted_class,
            duration_ms,
        )

        return PredictionResponse(
            criticite=predicted_class,
            probabilites=probabilities,
        )

    except Exception as error:
        duration_ms = (perf_counter() - start_time) * 1000

        logger.exception(
            "Erreur de prédiction | entrée={} | durée_ms={:.2f} | erreur={}",
            input_data,
            duration_ms,
            str(error),
        )

        raise HTTPException(
            status_code=500,
            detail="Une erreur est survenue pendant la prédiction.",
        ) from error
   
