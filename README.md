---
title: Nexus Dispatch
emoji: 🚑
colorFrom: red
colorTo: red
sdk: docker

app_port: 7860
pinned: false
short_description: Emergency response environment for OpenEnv
---

# 🚑 Nexus Dispatch

**Nexus Dispatch** is a high-fidelity emergency response simulation environment developed for the **OpenEnv Hackathon**.

## 🚀 Key Features
* **Smart Triage Logic**: Uses a weighted reward system where high-severity emergencies (Severity 5) provide significantly higher rewards.
* **Multi-Mode Architecture**: Supports both local validation and remote containerized deployment via Docker.
* **FastAPI Integration**: Served as a microservice on port 7860 for seamless agent interaction.

## 🛠 Technical Specifications
* **SDK**: Docker
* **Base Image**: Python 3.12-slim
* **Port**: 7860
* **Framework**: FastAPI / Uvicorn

## 📖 How to Run
### Local Validation
1. Install dependencies: `pip install .`
2. Run the OpenEnv validator: `openenv validate`

### Inference Test
```bash
python inference.py