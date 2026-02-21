import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import openai
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://traceflow.in"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI(title="TraceFlow AI")

# --------- Load prompts ---------
def load_prompt(path):
    with open(path, "r") as f:
        return f.read()

LOG_ANALYZER_PROMPT = load_prompt("prompts/log_analyzer_prompt.txt")
TESTGEN_PROMPT = load_prompt("prompts/testgen_prompt.txt")

# --------- Request models ---------
class LogRequest(BaseModel):
    logs: str

class TestGenRequest(BaseModel):
    requirement: str

# --------- Log Analyzer Endpoint ---------
@app.post("/api/log-analyzer")
def analyze_logs(req: LogRequest):
    response = openai.ChatCompletion.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": LOG_ANALYZER_PROMPT},
            {"role": "user", "content": f"Logs:\n{req.logs}"}
        ],
        temperature=0.2
    )

    return {"result": response.choices[0].message.content}

# --------- TestGen Endpoint ---------
@app.post("/api/testgen")
def generate_tests(req: TestGenRequest):
    response = openai.ChatCompletion.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": TESTGEN_PROMPT},
            {"role": "user", "content": req.requirement}
        ],
        temperature=0.2
    )

    return {"result": response.choices[0].message.content}

@app.get("/")
def health_check():
    return {
        "service": "TraceFlow AI",
        "status": "running"
    }

