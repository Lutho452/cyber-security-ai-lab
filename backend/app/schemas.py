from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    features: list[float] = Field(..., min_length=5, max_length=5)


class FeedbackRequest(BaseModel):
    user_tone: float = Field(0.5, ge=0.0, le=1.0)
    user_length: float = Field(0.5, ge=0.0, le=1.0)
    user_technicality: float = Field(0.5, ge=0.0, le=1.0)
    user_urgency: float = Field(0.5, ge=0.0, le=1.0)
    user_clarity: float = Field(0.5, ge=0.0, le=1.0)
    rating: float = Field(0.5, ge=0.0, le=1.0)


class TrainRequest(BaseModel):
    epochs: int = Field(default=20, ge=1, le=200)
    batch_size: int = Field(default=32, ge=1, le=256)
    learning_rate: float = Field(default=0.02, ge=1e-5, le=1.0)
