
import os, json
from openai import OpenAI
from env.engine import NexusEnv
from env.models import Action
from tasks.grader import DispatchGrader

def get_llm_action(client, model, obs) -> Action:
    prompt = f"Dispatcher Task. Rules: Match types (Medical:Ambulance, Fire:FireTruck, Police:PoliceUnit, Rescue:RescueTeam). Optimize distance. Obs: {obs.model_dump()}. Respond ONLY JSON: {{\"type\": \"DISPATCH\", \"unit_id\": \"UNIT-XX\", \"call_id\": \"CALL-XX\"}}"
    try:
        res = client.chat.completions.create(model=model, messages=[{"role": "user", "content": prompt}], temperature=0.0)
        content = res.choices[0].message.content.strip()
        if "```" in content: content = content.split("```")[1].split("```")[0].strip().replace("json", "")
        return Action(**json.loads(content))
    except: return Action(type="WAIT")

def run_task(sim, client, model, name, diff, max_s):
    grader = DispatchGrader(difficulty=diff)
    rewards, obs = [], sim.reset(task=name)
    print(f"[START] task={name} env=nexus_dispatch model={model}")
    for _ in range(max_s):
        move = get_llm_action(client, model, obs)
        obs, r, d, _ = sim.step(move)
        rewards.append(r)
        print(f"[STEP] step={len(rewards)} action={move.type} reward={r:.2f} done={'true' if d else 'false'} error=null")
        if d: break
    print(f"[END] success={'true' if sim.state().active_calls==0 else 'false'} steps={len(rewards)} score={grader.grade(sim.state()):.4f} rewards={','.join(f'{r:.2f}' for r in rewards)}")

def main():
    api_url = os.environ.get("API_BASE_URL", "https://router.huggingface.co/v1")
    api_key = os.environ.get("API_KEY") or os.environ.get("HF_TOKEN")
    model = os.environ.get("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
    if not api_key: return
    client, sim = OpenAI(base_url=api_url, api_key=api_key), NexusEnv()
    for t in [{"name": "easy_dispatch", "diff": "easy", "ms": 10}, {"name": "medium_dispatch", "diff": "medium", "ms": 20}, {"name": "hard_dispatch", "diff": "hard", "ms": 30}]:
        run_task(sim, client, model, t["name"], t["diff"], t["ms"])

if __name__ == "__main__": main()
