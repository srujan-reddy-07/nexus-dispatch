
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from env.engine import NexusEnv
from env.models import Action
import os, uvicorn

app = FastAPI(title="Nexus Dispatch API")
env = NexusEnv()

@app.get("/", response_class=HTMLResponse)
def dashboard():
    path = os.path.join(os.path.dirname(__file__), "templates", "dashboard.html")
    with open(path, "r") as f: return f.read()

@app.post("/reset")
def reset(task: str = Query(default="easy_dispatch")):
    global env
    env = NexusEnv()
    return {"observation": env.reset(task=task).model_dump()}

@app.post("/step")
def step(action: Action):
    obs, r, d, i = env.step(action)
    return {"observation": obs.model_dump(), "reward": r, "done": d, "info": i}

@app.get("/state")
def state():
    res = env.state().model_dump()
    obs = env._get_observation().model_dump()
    res["calls"], res["units"] = obs["calls"], obs["units"]
    return res

@app.get("/tasks")
def list_tasks():
    return {"tasks": [{"name": "easy_dispatch", "difficulty": "easy", "max_steps": 10},
                     {"name": "medium_dispatch", "difficulty": "medium", "max_steps": 20},
                     {"name": "hard_dispatch", "difficulty": "hard", "max_steps": 30}]}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
