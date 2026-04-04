from fastapi import FastAPI
from env.engine import NexusEnv
from env.models import Action
import uvicorn

app = FastAPI(title="Nexus Dispatch API")
env = NexusEnv()

@app.get("/")
def read_root():
    return {"status": "Nexus Dispatch Online", "port": 7860}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/step")
def step(action: Action):
    obs, reward, done, info = env.step(action)
    return {
        "observation": obs.model_dump() if hasattr(obs, 'model_dump') else obs,
        "reward": reward,
        "done": done,
        "info": info
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)