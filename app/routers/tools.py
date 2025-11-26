from fastapi import APIRouter, HTTPException
from app.models.tools_store import tools_store
from typing import List, Dict, Any

router = APIRouter()

@router.get("/api/tools")
async def list_tools():
    return await tools_store.list_tools()

@router.post("/api/tools")
async def create_tool(tool: Dict[str, Any]):
    return await tools_store.save_tool(tool)

@router.put("/api/tools/{name}")
async def update_tool(name: str, tool: Dict[str, Any]):
    if tool["name"] != name:
        raise HTTPException(status_code=400, detail="Tool name mismatch")
    return await tools_store.save_tool(tool)

@router.delete("/api/tools/{name}")
async def delete_tool(name: str):
    success = await tools_store.delete_tool(name)
    if not success:
        raise HTTPException(status_code=404, detail="Tool not found")
    return {"success": True}
