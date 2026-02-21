import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI

# ---------------- ENV ----------------
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set")

client = OpenAI(api_key=OPENAI_API_KEY)

# ---------------- APP (MUST BE FIRST) ----------------
app = FastAPI(title="TraceFlow AI")

# ---------------- CORS (AFTER app exists) ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://traceflow.in",
        "https://www.traceflow.in",
        "http://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- PROMPTS ----------------
def load_prompt(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

LOG_ANALYZER_PROMPT = load_prompt("prompts/log_analyzer_prompt.txt")
TESTGEN_PROMPT = load_prompt("prompts/testgen_prompt.txt")

# ---------------- REQUEST MODELS ----------------
class LogRequest(BaseModel):
    logs: str

class TestGenRequest(BaseModel):
    requirement: str

# ---------------- ENDPOINTS ----------------
@app.post("/api/log-analyzer")
def analyze_logs(req: LogRequest):
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": LOG_ANALYZER_PROMPT},
            {"role": "user", "content": f"Logs:\n{req.logs}"}
        ],
        temperature=0.2,
    )
    return {"result": response.choices[0].message.content}

@app.post("/api/testgen")
def generate_tests(req: TestGenRequest):
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": TESTGEN_PROMPT},
            {"role": "user", "content": req.requirement}
        ],
        temperature=0.2,
    )
    return {"result": response.choices[0].message.content}

@app.get("/")
def health():
    return {"service": "TraceFlow AI", "status": "running"}
