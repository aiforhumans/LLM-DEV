from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from pydantic import BaseModel
from app.models.service import service
import asyncio

router = APIRouter()

class ABTestRequest(BaseModel):
    prompt: str
    models: List[str]
    temperature: float = 0.7

@router.post("/api/ab-test")
async def run_ab_test(request: ABTestRequest):
    """Run the same prompt against multiple models in parallel"""
    
    async def call_model(model_name):
        try:
            response = await service.chat_completion(
                messages=[{"role": "user", "content": request.prompt}],
                model=model_name,
                temperature=request.temperature
            )
            return {
                "model": model_name,
                "response": response.choices[0].message.content,
                "status": "success"
            }
        except Exception as e:
            return {
                "model": model_name,
                "error": str(e),
                "status": "error"
            }

    results = await asyncio.gather(*(call_model(m) for m in request.models))
    return {"results": results}
