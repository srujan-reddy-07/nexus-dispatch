
class DispatchGrader:
    def __init__(self, difficulty="easy"):
        self.difficulty = difficulty

    def grade(self, state) -> float:
        max_calls = 1 if self.difficulty == "easy" else (3 if self.difficulty == "medium" else 6)
        completion = state.lives_saved / max_calls
        accuracy = state.specialization_accuracy
        efficiency = max(0.0, 1.0 - (state.avg_response_time / 100.0))
        
        if self.difficulty == "easy":
            score = (completion * 0.7) + (accuracy * 0.3)
        elif self.difficulty == "medium":
            score = (completion * 0.5) + (accuracy * 0.3) + (efficiency * 0.2)
        else:
            score = (completion * 0.4) + (accuracy * 0.4) + (efficiency * 0.2)
        return min(0.99, max(0.01, score))
