"""Agent abstraction with a Mock LLM and optional HTTP provider integration.

This small Agent demonstrates how to structure calls: keep model-specific logic
encapsulated so the app can switch between a mock LLM for testing and a real
HTTP-based provider by setting `GEMINI_API_KEY` and `GEMINI_API_ENDPOINT`.
"""
import os
import requests
import json


class MockLLM:
    def generate(self, prompt: str) -> str:
        # Simple rule-based reply to illustrate behaviour
        return f"[MockLLM] Received prompt ({len(prompt)} chars). Short reply: " \
               f"'Thanks — I would test and iterate.'"


class HTTPProvider:
    def __init__(self, endpoint: str, api_key: str):
        self.endpoint = endpoint.rstrip('/')
        self.api_key = api_key

    def generate(self, prompt: str) -> str:
        url = f"{self.endpoint}/chat"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {
            "model": "gemini-ao-small",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,
        }
        resp = requests.post(url, headers=headers, json=payload, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        # Try to extract common shapes (choices[].message.content or output.text)
        if isinstance(data, dict):
            choices = data.get("choices")
            if choices and isinstance(choices, list):
                return choices[0].get("message", {}).get("content") or json.dumps(data)
            if "output" in data and isinstance(data["output"], dict):
                return data["output"].get("text") or json.dumps(data)
        return json.dumps(data)


class Agent:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        endpoint = os.getenv("GEMINI_API_ENDPOINT")
        if api_key and endpoint:
            self.model = HTTPProvider(endpoint, api_key)
            self.mode = "http"
        else:
            self.model = MockLLM()
            self.mode = "mock"

    def ask(self, prompt: str) -> str:
        """Ask the configured model and return the string reply."""
        return self.model.generate(prompt)
