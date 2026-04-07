from fastapi import FastAPI, Query
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

@app.post("/reset")
def reset(task: str = Query(default="easy_dispatch")):
    obs = env.reset(task=task)
    return {"observation": obs.model_dump()}

@app.post("/step")
def step(action: Action):
    obs, reward, done, info = env.step(action)
    return {
        "observation": obs.model_dump(),
        "reward": reward,
        "done": done,
        "info": info
    }

@app.get("/state")
def state():
    return env.state().model_dump()

@app.get("/tasks")
def list_tasks():
    return {
        "tasks": [
            {"name": "easy_dispatch", "difficulty": "easy", "max_steps": 5},
            {"name": "medium_dispatch", "difficulty": "medium", "max_steps": 10},
            {"name": "hard_dispatch", "difficulty": "hard", "max_steps": 15}
        ]
    }

def main():
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
