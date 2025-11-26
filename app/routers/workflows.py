from fastapi import APIRouter, HTTPException
from app.models.workflow_store import workflow_store
from typing import List, Dict, Any

router = APIRouter()

@router.get("/api/workflows")
async def list_workflows():
    return await workflow_store.list_workflows()

@router.post("/api/workflows")
async def create_workflow(workflow: Dict[str, Any]):
    return await workflow_store.save_workflow(workflow)

@router.get("/api/workflows/{id}")
async def get_workflow(id: str):
    workflow = await workflow_store.get_workflow(id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return workflow

@router.put("/api/workflows/{id}")
async def update_workflow(id: str, workflow: Dict[str, Any]):
    if workflow.get("id") != id:
        raise HTTPException(status_code=400, detail="ID mismatch")
    return await workflow_store.save_workflow(workflow)

@router.delete("/api/workflows/{id}")
async def delete_workflow(id: str):
    success = await workflow_store.delete_workflow(id)
    if not success:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return {"success": True}

@router.post("/api/workflows/{id}/run")
async def run_workflow(id: str, input_data: Dict[str, Any]):
    # Placeholder for workflow execution logic
    # In a real implementation, this would invoke the orchestrator
    return {"status": "started", "job_id": "mock-job-id", "message": "Workflow execution not yet implemented"}
