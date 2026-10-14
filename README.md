# Personal AI Agent Trainer

A hybrid edge + cloud personal AI prototype for learning user preferences and improving responses over time.

## Features

- FastAPI backend
- PyTorch preference model
- Feedback-driven learning loop
- React dashboard for tuning preferences
- Docker Compose setup

## Run locally

```bash
docker compose up --build
```

Then open:

- Frontend: http://localhost:5173
- Backend docs: http://localhost:8000/docs

## Why this project matters

This is a realistic starting point for a personal AI agent that learns from user preferences rather than trying to pretend a giant AGI runs on a small phone. It is built as a hybrid system:

- local UI + tiny edge logic
- cloud training + memory
- feedback loop for continual learning

## Safety note

This is for personal experimentation and controlled use only. Do not use it for unauthorized data collection or sensitive personal monitoring without explicit opt-in, legal review, and proper governance. 
