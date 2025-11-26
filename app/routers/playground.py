from fastapi import APIRouter, HTTPException, Request
from sse_starlette.sse import EventSourceResponse
from app.models.service import service
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

router = APIRouter()

class ChatRequest(BaseModel):
    messages: List[Dict[str, str]]
    model: str
    temperature: float = 0.7
    max_tokens: int = -1
    stream: bool = False
    # New fields for /v1/responses
    input: Optional[str] = None
    previous_response_id: Optional[str] = None
    reasoning_effort: Optional[str] = None

@router.get("/api/models")
async def list_models():
    """List available models from LM Studio"""
    models = await service.list_models()
    return {"data": models}

@router.get("/api/health")
async def check_health():
    """Quick ping to check server status"""
    return await service.check_health()

@router.post("/api/chat")
async def chat_completion(request: ChatRequest):
    """Multi-turn chat with optional streaming"""
    if request.stream:
        return EventSourceResponse(
            chat_generator(request),
            media_type="text/event-stream"
        )
    else:
        # Use new API if input is provided
        if request.input:
            return await service.create_response(
                model=request.model,
                input_text=request.input,
                previous_response_id=request.previous_response_id,
                reasoning_effort=request.reasoning_effort,
                stream=False
            )
        
        # Fallback to standard chat completion
        response = await service.chat_completion(
            messages=request.messages,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            stream=False
        )
        return response.model_dump()

async def chat_generator(request: ChatRequest):
    if request.input:
        # New API Streaming
        stream = service.create_response(
            model=request.model,
            input_text=request.input,
            previous_response_id=request.previous_response_id,
            reasoning_effort=request.reasoning_effort,
            stream=True
        )
        async for event in await stream:
            # Forward the event and data
            # event['data'] is a JSON string from the upstream service
            yield {"event": event["event"], "data": event["data"]}
    else:
        # Standard API Streaming
        stream = await service.chat_completion(
            messages=request.messages,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            stream=True
        )
        async for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                # Format as SSE data - wrap in dict so sse-starlette serializes it to JSON
                yield {"data": {"data": content}}
