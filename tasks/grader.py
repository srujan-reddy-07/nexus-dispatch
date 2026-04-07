def calculate_easy_score(steps_taken, total_reward, active_calls_remaining):
    if steps_taken == 0:
        return 0.01
    efficiency = total_reward / steps_taken
    coverage = 1.0 if active_calls_remaining == 0 else 0.0
    score = (efficiency * 0.6) + (coverage * 0.4)
    # Clamp strictly between (0, 1)
    return min(0.99, max(0.01, score))


def calculate_medium_score(steps_taken, total_reward, active_calls_remaining, max_steps):
    if steps_taken == 0:
        return 0.01
    efficiency = total_reward / steps_taken
    speed_bonus = max(0.0, 1.0 - (steps_taken / max_steps))
    coverage = 1.0 if active_calls_remaining == 0 else max(0.0, 1.0 - (active_calls_remaining * 0.2))
    score = (efficiency * 0.5) + (coverage * 0.3) + (speed_bonus * 0.2)
    # Clamp strictly between (0, 1)
    return min(0.99, max(0.01, score))


def calculate_hard_score(steps_taken, total_reward, active_calls_remaining, max_steps):
    if steps_taken == 0:
        return 0.01
    efficiency = total_reward / steps_taken
    speed_bonus = max(0.0, 1.0 - (steps_taken / max_steps))
    coverage = 1.0 if active_calls_remaining == 0 else max(0.0, 1.0 - (active_calls_remaining * 0.15))
    score = (efficiency * 0.4) + (coverage * 0.4) + (speed_bonus * 0.2)
    # Clamp strictly between (0, 1)
    return min(0.99, max(0.01, score))


class DispatchGrader:
    def __init__(self, difficulty="easy"):
        self.difficulty = difficulty

    def grade(self, steps_taken: int, total_reward: float, active_calls_remaining: int, max_steps: int = 10) -> float:
        if self.difficulty == "easy":
            raw_score = calculate_easy_score(steps_taken, total_reward, active_calls_remaining)
        elif self.difficulty == "medium":
            raw_score = calculate_medium_score(steps_taken, total_reward, active_calls_remaining, max_steps)
        else:
            raw_score = calculate_hard_score(steps_taken, total_reward, active_calls_remaining, max_steps)
        
        # Final safety clamp just in case
        return min(0.99, max(0.01, raw_score))
