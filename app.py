import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import openai
from prompts import SYSTEM_PROMPT

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI(title="TraceFlow AI")

class LogRequest(BaseModel):
    logs: str

@app.post("/analyze")
async def analyze_logs(req: LogRequest):
    response = openai.ChatCompletion.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": req.logs}
        ],
        temperature=0.2
    )

    return {
        "analysis": response.choices[0].message.content
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

