import os
import json
from openai import OpenAI
from env.engine import NexusEnv
from env.models import Action
from tasks.grader import DispatchGrader

BENCHMARK = "nexus_dispatch"

TASKS = [
    {"name": "easy_dispatch", "difficulty": "easy", "max_steps": 5},
    {"name": "medium_dispatch", "difficulty": "medium", "max_steps": 10},
    {"name": "hard_dispatch", "difficulty": "hard", "max_steps": 15},
]

def format_action(action: Action) -> str:
    if action.type == "DISPATCH":
        return f"DISPATCH({action.unit_id},{action.call_id})"
    return "WAIT()"

def get_llm_action(client: OpenAI, model: str, obs) -> Action:
    prompt = f"""
    You are an emergency dispatcher. 
    Observation:
    Calls: {obs.calls}
    Units: {obs.units}

    Respond with ONLY a JSON object:
    {{"type": "DISPATCH", "unit_id": "ID_OF_UNIT", "call_id": "ID_OF_CALL"}}
    OR
    {{"type": "WAIT"}}
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )
        content = response.choices[0].message.content.strip()
        if content.startswith("```json"):
            content = content.split("```json")[1].split("```")[0].strip()
        elif content.startswith("```"):
            content = content.split("```")[1].split("```")[0].strip()
        data = json.loads(content)
        return Action(**data)
    except Exception:
        return Action(type="WAIT")

def run_task(sim: NexusEnv, client: OpenAI, model_name: str, task_name: str, difficulty: str, max_steps: int):
    grader = DispatchGrader(difficulty=difficulty)
    rewards = []
    print(f"[START] task={task_name} env={BENCHMARK} model={model_name}", flush=True)
    obs = sim.reset(task=task_name)
    for _ in range(max_steps):
        reward = 0.0
        done = False
        error = "null"
        move = get_llm_action(client, model_name, obs)
        try:
            obs, reward, done, _ = sim.step(move)
        except Exception as e:
            error = str(e)
            done = True
        rewards.append(reward)
        action_str = format_action(move)
        done_str = "true" if done else "false"
        print(f"[STEP] step={len(rewards)} action={action_str} reward={reward:.2f} done={done_str} error={error}", flush=True)
        if done:
            break
    env_state = sim.state()
    score = grader.grade(
        steps_taken=len(rewards),
        total_reward=sum(rewards),
        active_calls_remaining=env_state.active_calls,
        max_steps=max_steps
    )
    success_str = "true" if env_state.active_calls == 0 else "false"
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={success_str} steps={len(rewards)} score={score:.4f} rewards={rewards_str}", flush=True)

def run_test():
    API_BASE_URL = os.environ.get("API_BASE_URL", "https://router.huggingface.co/v1")
    API_KEY = os.environ.get("API_KEY") or os.environ.get("HF_TOKEN")
    MODEL_NAME = os.environ.get("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
    if not API_KEY:
        return
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
    sim = NexusEnv()
    for task in TASKS:
        run_task(sim=sim, client=client, model_name=MODEL_NAME, task_name=task["name"], difficulty=task["difficulty"], max_steps=task["max_steps"])

if __name__ == "__main__":
    run_test()
