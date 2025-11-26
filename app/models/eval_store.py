import json
import os
from typing import List, Dict, Any, Optional
import aiofiles
import uuid

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
DATASETS_FILE = os.path.join(DATA_DIR, "datasets.json")
EVALUATORS_FILE = os.path.join(DATA_DIR, "evaluators.json")
JOBS_FILE = os.path.join(DATA_DIR, "eval_jobs.json")

class EvalStore:
    def __init__(self):
        self._ensure_data_dir()

    def _ensure_data_dir(self):
        os.makedirs(DATA_DIR, exist_ok=True)
        for fpath in [DATASETS_FILE, EVALUATORS_FILE, JOBS_FILE]:
            if not os.path.exists(fpath):
                with open(fpath, 'w') as f:
                    json.dump([], f)

    async def _load(self, filepath: str) -> List[Dict[str, Any]]:
        async with aiofiles.open(filepath, 'r') as f:
            return json.loads(await f.read())

    async def _save(self, filepath: str, data: List[Dict[str, Any]]):
        async with aiofiles.open(filepath, 'w') as f:
            await f.write(json.dumps(data, indent=2))

    # Datasets
    async def list_datasets(self) -> List[Dict[str, Any]]:
        return await self._load(DATASETS_FILE)

    async def save_dataset(self, dataset: Dict[str, Any]) -> Dict[str, Any]:
        items = await self.list_datasets()
        if "id" not in dataset:
            dataset["id"] = str(uuid.uuid4())
        
        idx = next((i for i, x in enumerate(items) if x["id"] == dataset["id"]), -1)
        if idx >= 0:
            items[idx] = dataset
        else:
            items.append(dataset)
        await self._save(DATASETS_FILE, items)
        return dataset

    # Evaluators
    async def list_evaluators(self) -> List[Dict[str, Any]]:
        return await self._load(EVALUATORS_FILE)

    async def save_evaluator(self, evaluator: Dict[str, Any]) -> Dict[str, Any]:
        items = await self.list_evaluators()
        if "id" not in evaluator:
            evaluator["id"] = str(uuid.uuid4())
            
        idx = next((i for i, x in enumerate(items) if x["id"] == evaluator["id"]), -1)
        if idx >= 0:
            items[idx] = evaluator
        else:
            items.append(evaluator)
        await self._save(EVALUATORS_FILE, items)
        return evaluator

    # Jobs
    async def list_jobs(self) -> List[Dict[str, Any]]:
        return await self._load(JOBS_FILE)

    async def save_job(self, job: Dict[str, Any]) -> Dict[str, Any]:
        items = await self.list_jobs()
        if "id" not in job:
            job["id"] = str(uuid.uuid4())
            
        idx = next((i for i, x in enumerate(items) if x["id"] == job["id"]), -1)
        if idx >= 0:
            items[idx] = job
        else:
            items.append(job)
        await self._save(JOBS_FILE, items)
        return job

    async def get_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        jobs = await self.list_jobs()
        return next((j for j in jobs if j["id"] == job_id), None)

eval_store = EvalStore()
