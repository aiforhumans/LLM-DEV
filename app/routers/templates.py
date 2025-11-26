from fastapi import APIRouter, HTTPException
from app.models.templates_store import templates_store
from typing import List, Dict, Any

router = APIRouter()

@router.get("/api/prompt-templates")
async def list_templates():
    return await templates_store.list_templates()

@router.post("/api/prompt-templates")
async def create_template(template: Dict[str, Any]):
    return await templates_store.save_template(template)

@router.delete("/api/prompt-templates/{id}")
async def delete_template(id: str):
    success = await templates_store.delete_template(id)
    if not success:
        raise HTTPException(status_code=404, detail="Template not found")
    return {"success": True}
