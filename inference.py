import os
from openai import OpenAI
from env.engine import NexusEnv
from env.models import Action

def run_test():
    
    HF_TOKEN = os.getenv("HF_TOKEN") 
    API_BASE_URL = os.getenv("API_BASE_URL", "https://api-inference.huggingface.co/v1")
    MODEL_NAME = os.getenv("MODEL_NAME", "meta-llama/Llama-3-70b-instruct")

    
    client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)
    
    
    sim = NexusEnv()
    
    
    print("START") 
    
    obs = sim.reset()
    
    
    for i in range(5):
        print(f"STEP {i}") 
        
        
        if obs.calls and obs.units:
            
            available_unit = next((u for u in obs.units if u.status == "Available"), None)
            
            if available_unit and obs.calls:
                call_to_handle = obs.calls[0]
                
                
                move = Action(
                    type="DISPATCH", 
                    unit_id=available_unit.id, 
                    call_id=call_to_handle.id
                )
                
                
                obs, reward, done, _ = sim.step(move)
                
                if done:
                    break
        else:
            
            move = Action(type="WAIT")
            obs, reward, done, _ = sim.step(move)
                
    print("END")

if __name__ == "__main__":
    run_test()