def calculate_dispatch_score(state):
    if state.steps == 0:
        return 0.0
    
    efficiency = state.score / state.steps
    coverage = 1.0 if state.active_calls == 0 else 0.5
    
    final_grade = (efficiency * 0.7) + (coverage * 0.3)
    return min(1.0, max(0.0, final_grade))

class DispatchGrader:
    def __init__(self, difficulty="easy"):
        self.difficulty = difficulty

    def grade(self, environment_state):
        return calculate_dispatch_score(environment_state)