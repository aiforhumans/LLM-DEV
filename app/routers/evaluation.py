from fastapi import APIRouter, HTTPException
from app.models.eval_store import eval_store
from app.models.evaluators import BUILTIN_EVALUATORS
from typing import List, Dict, Any

router = APIRouter()

# Datasets
@router.get("/api/datasets")
async def list_datasets():
    return await eval_store.list_datasets()

@router.post("/api/datasets")
async def create_dataset(dataset: Dict[str, Any]):
    return await eval_store.save_dataset(dataset)

# Evaluators
@router.get("/api/evaluators")
async def list_evaluators():
    custom = await eval_store.list_evaluators()
    builtin = [{"name": name, "type": "builtin"} for name in BUILTIN_EVALUATORS.keys()]
    return {"builtin": builtin, "custom": custom}

@router.post("/api/evaluators/custom")
async def create_custom_evaluator(evaluator: Dict[str, Any]):
    return await eval_store.save_evaluator(evaluator)

# Jobs
@router.get("/api/eval-jobs")
async def list_jobs():
    return await eval_store.list_jobs()

@router.post("/api/eval-jobs")
async def create_job(job: Dict[str, Any]):
    return await eval_store.save_job(job)

@router.post("/api/eval-jobs/{id}/run")
async def run_job(id: str):
    # Placeholder for job execution logic
    return {"status": "started", "message": "Evaluation job execution not yet implemented"}
