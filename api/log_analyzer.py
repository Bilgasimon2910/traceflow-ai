import os
from openai import OpenAI
from utils.prompt_loader import load_prompt

LOG_ANALYZER_PROMPT = load_prompt("prompts/log_analyzer_prompt.txt")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_logs(logs: str) -> str:
    if not logs.strip():
        return "No logs provided."

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": LOG_ANALYZER_PROMPT},
            {"role": "user", "content": f"Logs:\n{logs}"}
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content