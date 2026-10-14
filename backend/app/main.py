from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import PredictionRequest, FeedbackRequest, TrainRequest
from app.models import PersonalPreferenceModel, train_model, predict_preferences, evaluate_feedback
from app.data import generate_training_examples

app = FastAPI(
    title="Personal AI Agent Trainer",
    version="0.1.0",
    description="Hybrid personal AI agent prototype with local feedback learning and cloud training."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL = None
DATA = []


def bootstrap():
    global MODEL, DATA
    DATA = generate_training_examples(300)
    MODEL = PersonalPreferenceModel(input_dim=5, hidden_dim=16)
    MODEL = train_model(DATA, epochs=30, batch_size=32, learning_rate=0.02)


@app.on_event("startup")
async def startup_event():
    bootstrap()


@app.get("/health")
async def health():
    return {"status": "ok", "message": "Personal AI agent backend is running."}


@app.get("/status")
async def status():
    return {
        "samples": len(DATA),
        "model_loaded": MODEL is not None,
        "model_version": "0.1.0",
    }


@app.post("/predict")
async def predict(payload: PredictionRequest):
    if MODEL is None:
        raise RuntimeError("Model not initialized")

    vector = predict_preferences(MODEL, payload.features)
    return {
        "recommendation": {
            "tone": vector[0],
            "length": vector[1],
            "technicality": vector[2],
            "urgency": vector[3],
            "clarity": vector[4],
        },
        "raw": vector,
    }


@app.post("/feedback")
async def feedback(payload: FeedbackRequest):
    global DATA
    # Store the example as a learning sample and update local model state.
    example = [
        payload.user_tone,
        payload.user_length,
        payload.user_technicality,
        payload.user_urgency,
        payload.user_clarity,
    ]
    DATA.append((example, [payload.rating]))
    return {"status": "accepted", "stored": len(DATA)}


@app.post("/train")
async def train(payload: TrainRequest):
    global MODEL
    if not DATA:
        return {"status": "no-data", "message": "No training samples available."}
    MODEL = train_model(DATA, epochs=payload.epochs, batch_size=payload.batch_size, learning_rate=payload.learning_rate)
    return {"status": "trained", "samples": len(DATA), "epochs": payload.epochs}


@app.get("/")
async def root():
    return {"message": "Personal AI Agent Trainer"}
