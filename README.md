---
title: Nexus Dispatch
emoji: 🚑
colorFrom: red
colorTo: orange
sdk: docker
app_port: 7860
pinned: false
short_description: Emergency response RL environment for OpenEnv
---

# 🚑 Nexus Dispatch

**Nexus Dispatch** is a real-world emergency response simulation environment built on the **OpenEnv** framework for the Meta PyTorch Hackathon.

## Environment Description

An AI agent acts as an emergency dispatch coordinator. Each step, it observes incoming emergency calls and available response units, and must decide which unit to dispatch to which call. Calls have varying severity (1–5); dispatching to higher-severity calls yields higher rewards.

## Tasks

| Task | Difficulty | Calls | Max Steps | Goal |
|---|---|---|---|---|
| `easy_dispatch` | Easy | 1 | 5 | Dispatch one unit to one emergency |
| `medium_dispatch` | Medium | 3 | 10 | Handle multiple calls by severity |
| `hard_dispatch` | Hard | 5 | 15 | Manage high-volume calls with limited units |

## Action Space

{
  "type": "DISPATCH",
  "unit_id": "unit_001",
  "call_id": "call_001"
}

Or a no-op:

{
  "type": "WAIT"
}

## Observation Space

{
  "calls": [
    {"id": "call_001", "type": "Medical", "severity": 4, "location": [12.34, 56.78]}
  ],
  "units": [
    {"id": "unit_001", "type": "Ambulance", "status": "Available", "location": [0.0, 0.0]}
  ]
}

## Reward Function

- DISPATCH to a valid call: severity / 5.0 (range: 0.2 – 1.0)
- WAIT or invalid action: 0.0

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | /reset?task=easy_dispatch | Reset environment for a task |
| POST | /step | Take one action |
| GET | /state | Get current environment state |
| GET | /tasks | List all available tasks |
| GET | /health | Health check |

## Setup

pip install .
uvicorn server.app:app --host 0.0.0.0 --port 7860

## Docker

docker build -t nexus-dispatch .
docker run -p 7860:7860 nexus-dispatch

## Environment Variables

| Variable | Description |
|---|---|
| HF_TOKEN | Hugging Face / API key |
| API_BASE_URL | LLM API endpoint |
| MODEL_NAME | Model identifier |
