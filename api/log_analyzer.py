import os
from openai import OpenAI
from utils.prompt_loader import load_prompt

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_logs(logs: str) -> str:
    prompt = load_prompt("prompts/log_analyzer_prompt.txt")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": logs}
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content