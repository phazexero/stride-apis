from typing import List

def evaluate_summary(original_text: str, summary: str) -> float:
    # Simple heuristic evaluation: length ratio and keyword presence
    original_words = set(original_text.split())
    summary_words = set(summary.split())
    length_ratio = len(summary) / len(original_text)
    keyword_match = len(original_words.intersection(summary_words)) / len(original_words)

    # Combine length ratio and keyword match for a simple score
    score = 0.5 * (1 - length_ratio) + 0.5 * keyword_match
    return score
