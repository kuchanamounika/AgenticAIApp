# AgenticAIApp — Sample Agentic AI application

This folder contains a minimal, runnable sample Agentic AI application built with FastAPI. It demonstrates a small Agent abstraction that either uses a mock LLM locally or forwards prompts to an HTTP model provider if `GEMINI_API_KEY` and `GEMINI_API_ENDPOINT` are set.

Features
- `app/main.py`: FastAPI app exposing `/health` and `/ask` endpoints.
- `app/agent.py`: `Agent` class with `ask(prompt)` that uses a Mock LLM or calls a provider.
- `requirements.txt`: Python dependencies.
- `run.ps1`: PowerShell convenience command to run locally with `uvicorn`.
- `Dockerfile`: lightweight image for the app.

Quick start (PowerShell)
```powershell
cd D:/ML/AgenticAIApp
pip install -r requirements.txt
# optional: set provider env vars
$env:GEMINI_API_KEY = "your_key"
$env:GEMINI_API_ENDPOINT = "https://api.your-provider.com/v1"
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Try the endpoints
- Health: `GET http://localhost:8000/health`
- Ask the agent (POST):

```http
POST http://localhost:8000/ask
Content-Type: application/json

{"prompt":"Explain the benefits of unit testing in one sentence."}
```

Notes
- The built-in mock LLM is for demo and offline testing only. The provider-integration example uses a simple HTTP POST to `${GEMINI_API_ENDPOINT}/chat` and expects a JSON response; adapt to your provider's exact API shape for production.
- This sample is intentionally small and focused on structure; feel free to ask me to expand it (authentication, streaming, more agents, task scheduling, etc.).
