import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2"

def run_llm(prompt: str) -> str:
    """
    Call Ollama LLM API and return the response.
    Raises exceptions if connection fails or response is invalid.
    """
    try:
        print(f"[DEBUG] Sending request to Ollama at {OLLAMA_URL}")
        print(f"[DEBUG] Using model: {MODEL_NAME}")
        
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )
        
        response.raise_for_status()
        
        data = response.json()
        if "response" not in data:
            raise ValueError("Response format is unexpected - missing 'response' field")
        
        llm_response = data.get("response", "")
        print(f"[DEBUG] Ollama returned {len(llm_response)} characters")
        return llm_response
        
    except requests.exceptions.ConnectionError as e:
        print(f"[ERROR] Cannot connect to Ollama server at {OLLAMA_URL}")
        print(f"[ERROR] Make sure Ollama is running with: ollama serve")
        raise ConnectionError(f"Ollama server not reachable: {e}")
        
    except requests.exceptions.Timeout as e:
        print(f"[ERROR] Ollama request timed out after 60 seconds")
        raise TimeoutError(f"LLM request timeout: {e}")
        
    except requests.exceptions.HTTPError as e:
        print(f"[ERROR] Ollama HTTP error: {e}")
        raise
        
    except Exception as e:
        print(f"[ERROR] Unexpected error calling Ollama: {str(e)}")
        raise
   
