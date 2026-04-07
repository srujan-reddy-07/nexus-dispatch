import os
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

def run_task(sim: NexusEnv, model_name: str, task_name: str, difficulty: str, max_steps: int):
    grader = DispatchGrader(difficulty=difficulty)
    rewards = []

    print(f"[START] task={task_name} env={BENCHMARK} model={model_name}", flush=True)

    obs = sim.reset(task=task_name)
    move = None

    for _ in range(max_steps):
        reward = 0.0
        done = False
        error = "null"

        try:
            if obs.calls and obs.units:
                available_unit = next((u for u in obs.units if u.status == "Available"), None)
                if available_unit:
                    sorted_calls = sorted(obs.calls, key=lambda c: c.severity, reverse=True)
                    call_to_handle = sorted_calls[0]
                    move = Action(
                        type="DISPATCH",
                        unit_id=available_unit.id,
                        call_id=call_to_handle.id
                    )
                else:
                    move = Action(type="WAIT")
            else:
                move = Action(type="WAIT")

            obs, reward, done, _ = sim.step(move)

        except Exception as e:
            error = str(e)
            done = True

        rewards.append(reward)
        
        action_str = format_action(move) if move else "null"
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
    print(f"[END] success={success_str} steps={len(rewards)} score={score:.2f} rewards={rewards_str}", flush=True)

def run_test():
    API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
    MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
    HF_TOKEN = os.getenv("HF_TOKEN")
    
    API_KEY = HF_TOKEN or os.getenv("API_KEY")
    LOCAL_IMAGE_NAME = os.getenv("LOCAL_IMAGE_NAME")

    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

    sim = NexusEnv()

    for task in TASKS:
        run_task(
            sim=sim,
            model_name=MODEL_NAME,
            task_name=task["name"],
            difficulty=task["difficulty"],
            max_steps=task["max_steps"]
        )

if __name__ == "__main__":
    run_test()
