def enhance_prompt(prompt: str) -> str:
    # Add instructions to the prompt for better quality
    enhanced_prompt = (
        "You are a summarization assistant. Your goal is to generate clear, concise, and accurate summaries. "
        "Consider the main points and avoid unnecessary details. "
        f"Here is the text to summarize:\n\n{prompt}"
    )
    return enhanced_prompt
