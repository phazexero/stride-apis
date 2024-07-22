import os
import together
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("TOGETHER_API_KEY")
togetherai_client = together.Client(api_key= API_KEY)

def summarize_text(text: str, style: str) -> str:
    if style == "bullet_points":
        prompt = f"<s>[INST] <<SYS>> Summarize the following text into bullet points:\n\n{text}\n\n- <</SYS>> [/INST]"
    elif style == "headline":
        prompt = f"<s>[INST] <<SYS>>Provide a concise headline for the following text:\n\n{text}\n\nHeadline: <</SYS>> [/INST]"
    else:  # default to paragraph
        prompt = f"<s>[INST] <<SYS>>Summarize the following text into a concise paragraph:\n\n{text}\n\nSummary: <</SYS>> [/INST]"

    base_model_name = "mistralai/Mistral-7B-Instruct-v0.2"

    output = together.Complete.create(
                                        prompt = prompt,
                                        model = base_model_name,
                                        max_tokens = 256,
                                        temperature = 0.7,
                                        top_k = 90,
                                        top_p = 0.8,
                                        repetition_penalty = 1.1,
                                        stop = ['</s>', '[/INST]']
                                        )

    return output["choices"][0]["text"].strip()

