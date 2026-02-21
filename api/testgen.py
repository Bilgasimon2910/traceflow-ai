import os
from openai import OpenAI
from utils.prompt_loader import load_prompt

TESTGEN_PROMPT = load_prompt("prompts/testgen_prompt.txt")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_tests(requirement: str) -> str:
    if not requirement.strip():
        return "No requirement provided."

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": TESTGEN_PROMPT},
            {"role": "user", "content": requirement}
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content

