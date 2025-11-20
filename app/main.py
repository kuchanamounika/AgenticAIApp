from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .agent import Agent

app = FastAPI(title="AgenticAI Sample App")
agent = Agent()


class AskRequest(BaseModel):
    prompt: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask")
def ask(req: AskRequest):
    try:
        resp = agent.ask(req.prompt)
        return {"answer": resp}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
