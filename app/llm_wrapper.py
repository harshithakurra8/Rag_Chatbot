import requests

class LLMWrapper:
    def __init__(self, base_url="http://localhost:11434", model="gemma3:4b"):
        self.base_url = base_url
        self.model = model

    def generate(self, prompt: str) -> str:
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": 200,
                    "temperature": 0.7
                }
            },
            timeout=180
    
        )
        response.raise_for_status()
        return response.json()["response"]
