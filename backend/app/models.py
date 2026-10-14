from __future__ import annotations

import random
from typing import List, Tuple

import torch
import torch.nn as nn


class PersonalPreferenceModel(nn.Module):
    def __init__(self, input_dim: int = 5, hidden_dim: int = 16):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Linear(hidden_dim // 2, input_dim),
            nn.Sigmoid(),
        )

    def forward(self, x):
        return self.net(x)


def train_model(data: List[Tuple[List[float], List[float]]], epochs: int = 30, batch_size: int = 32, learning_rate: float = 0.02):
    model = PersonalPreferenceModel()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    loss_fn = nn.MSELoss()

    x = torch.tensor([d[0] for d in data], dtype=torch.float32)
    y = torch.tensor([d[1] for d in data], dtype=torch.float32)

    for _ in range(epochs):
        perm = torch.randperm(len(x))
        for i in range(0, len(x), batch_size):
            idx = perm[i:i + batch_size]
            xb = x[idx]
            yb = y[idx]
            optimizer.zero_grad()
            pred = model(xb)
            loss = loss_fn(pred, yb)
            loss.backward()
            optimizer.step()

    return model


def predict_preferences(model: PersonalPreferenceModel, features: List[float]) -> List[float]:
    with torch.no_grad():
        tensor = torch.tensor([features], dtype=torch.float32)
        pred = model(tensor)[0].tolist()
    return [float(v) for v in pred]


def evaluate_feedback(model: PersonalPreferenceModel, features: List[float], answer_score: float):
    base = predict_preferences(model, features)
    adjusted = []
    for i, value in enumerate(base):
        # Move the prediction toward the user-rated preference style
        adjusted.append(float(value + (answer_score - 0.5) * 0.15))
    return adjusted
