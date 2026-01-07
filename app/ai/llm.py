import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2"

def run_llm(prompt: str) -> str:
    response = requests.post(
            OLLAMA_URL,
            json={
                "model": "llama3.2",
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )
    response.raise_for_status()
    data = response.json()
    if "response" not in data:
        raise ValueError("Response format is unexpected")

    return data.get("response", "")
   
