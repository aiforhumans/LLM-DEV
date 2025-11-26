import httpx
import os
from openai import AsyncOpenAI
from typing import List, Dict, Any, Optional, AsyncGenerator

# Default to LM Studio local address
LM_STUDIO_BASE_URL = os.getenv("LM_STUDIO_BASE_URL", "http://127.0.0.1:1234/v1")

class LocalLLMService:
    def __init__(self):
        self.base_url = LM_STUDIO_BASE_URL
        self.client = AsyncOpenAI(base_url=self.base_url, api_key="lm-studio")
        self.http_client = httpx.AsyncClient(base_url=self.base_url)

    async def check_health(self) -> Dict[str, Any]:
        """
        Quick ping to check if the server is reachable and list models.
        Equivalent to: curl http://127.0.0.1:1234/v1/models/
        """
        try:
            response = await self.http_client.get("/models")
            response.raise_for_status()
            data = response.json()
            return {
                "status": "online",
                "models": data.get("data", []),
                "message": "LM Studio is reachable"
            }
        except Exception as e:
            print(f"Health check failed: {e}")
            return {
                "status": "offline",
                "models": [],
                "message": f"Could not connect to LM Studio at {self.base_url}. Error: {str(e)}"
            }

    async def list_models(self) -> List[Dict[str, Any]]:
        try:
            response = await self.client.models.list()
            return [model.model_dump() for model in response.data]
        except Exception as e:
            print(f"List models failed: {e}")
            return []

    async def chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        model: str, 
        temperature: float = 0.7, 
        max_tokens: int = -1,
        stream: bool = False
    ) -> Any:
        params = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "stream": stream
        }
        if max_tokens > 0:
            params["max_tokens"] = max_tokens

        return await self.client.chat.completions.create(**params)

    async def create_response(
        self,
        model: str,
        input_text: str,
        previous_response_id: Optional[str] = None,
        reasoning_effort: Optional[str] = None,
        stream: bool = False
    ) -> Any:
        payload = {
            "model": model,
            "input": input_text,
            "stream": stream
        }
        
        if previous_response_id:
            payload["previous_response_id"] = previous_response_id
            
        if reasoning_effort:
            payload["reasoning"] = {"effort": reasoning_effort}

        # Use httpx directly as this is a custom endpoint
        if stream:
            return self._stream_response(payload)
        else:
            response = await self.http_client.post("/responses", json=payload)
            response.raise_for_status()
            return response.json()

    async def _stream_response(self, payload: Dict[str, Any]):
        async with self.http_client.stream("POST", "/responses", json=payload) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if line.startswith("event:"):
                    self.current_event = line.replace("event:", "").strip()
                elif line.startswith("data:"):
                    data = line.replace("data:", "").strip()
                    if data and self.current_event:
                        yield {"event": self.current_event, "data": data}
                        self.current_event = None

service = LocalLLMService()
