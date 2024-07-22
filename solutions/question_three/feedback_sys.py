user_feedback = []

def collect_feedback(feedback: str):
    user_feedback.append(feedback)

def adjust_prompt_based_on_feedback(prompt: str) -> str:
    if "too long" in user_feedback:
        prompt += "\n\nPlease make the summary shorter."
    if "too short" in user_feedback:
        prompt += "\n\nPlease make the summary more detailed."
    if "unclear" in user_feedback:
        prompt += "\n\nPlease make the summary clearer."
    
    return prompt
