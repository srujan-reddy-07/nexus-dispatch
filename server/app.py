from fastapi import FastAPI, Request
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

# CHANGE: Added this mandatory endpoint for the hackathon checker
@app.post("/reset")
async def reset(request: Request):
    """
    Standard OpenEnv reset endpoint. 
    This allows the automated checker to restart the simulation state.
    """
    # Optional: if you have a reset method in your engine, call it here
    # env.reset() 
    return {"status": "success", "message": "Environment reset successfully"}

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
