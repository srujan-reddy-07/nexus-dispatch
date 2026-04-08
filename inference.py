
import os, json
from openai import OpenAI
from env.engine import NexusEnv
from env.models import Action
from tasks.grader import DispatchGrader

def get_llm_action(client, model, obs) -> Action:
    p = f"Dispatcher. Rules: Match types (Med:Amb, Fire:Fire, Pol:Pol, Res:Res). Optimize distance. Obs: {obs.model_dump()}. Respond ONLY JSON: {{\"type\": \"DISPATCH\", \"unit_id\": \"UNIT-XX\", \"call_id\": \"CALL-XX\"}}"
    try:
        res = client.chat.completions.create(model=model, messages=[{"role": "user", "content": p}], temperature=0.0)
        content = res.choices[0].message.content.strip()
        if "```" in content: content = content.split("```")[1].split("```")[0].strip().replace("json", "")
        return Action(**json.loads(content))
    except: return Action(type="WAIT")

def run_task(sim, client, model, name, diff, max_s):
    grader = DispatchGrader(difficulty=diff)
    rewards, obs = [], sim.reset(task=name)
    print(f"[START] task={name} env=nexus_dispatch model={model}", flush=True)
    for _ in range(max_s):
        move = get_llm_action(client, model, obs)
        obs, r, d, _ = sim.step(move)
        rewards.append(r)
        print(f"[STEP] step={len(rewards)} action={move.type} reward={r:.2f} done={'true' if d else 'false'} error=null", flush=True)
        if d: break
    print(f"[END] success={'true' if sim.state().active_calls==0 else 'false'} steps={len(rewards)} score={grader.grade(sim.state()):.4f} rewards={','.join(f'{r:.2f}' for r in rewards)}", flush=True)

def main():
    api_url = os.environ.get("API_BASE_URL", "https://router.huggingface.co/v1")
    key = os.environ.get("API_KEY") or os.environ.get("HF_TOKEN")
    model = os.environ.get("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
    if not key: return
    client, sim = OpenAI(base_url=api_url, api_key=key), NexusEnv()
    for t in [{"n": "easy_dispatch", "d": "easy", "ms": 10}, {"n": "medium_dispatch", "d": "medium", "ms": 20}, {"n": "hard_dispatch", "d": "hard", "ms": 30}]:
        run_task(sim, client, model, t["n"], t["d"], t["ms"])

if __name__ == "__main__": main()
