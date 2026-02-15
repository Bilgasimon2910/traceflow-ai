from utils.prompt_loader import load_prompt

LOG_ANALYZER_PROMPT = load_prompt("prompts/log_analyzer_prompt.txt")

def analyze_logs(logs):
    messages = [
        {"role": "system", "content": LOG_ANALYZER_PROMPT},
        {"role": "user", "content": f"Logs:\n{logs}"}
    ]
    # call AI here
