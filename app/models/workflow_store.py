import json
import os
from typing import List, Dict, Any, Optional
import aiofiles
import uuid

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
WORKFLOWS_FILE = os.path.join(DATA_DIR, "workflows.json")

class WorkflowStore:
    def __init__(self):
        self._ensure_data_dir()

    def _ensure_data_dir(self):
        os.makedirs(DATA_DIR, exist_ok=True)
        if not os.path.exists(WORKFLOWS_FILE):
            with open(WORKFLOWS_FILE, 'w') as f:
                json.dump([], f)

    async def list_workflows(self) -> List[Dict[str, Any]]:
        async with aiofiles.open(WORKFLOWS_FILE, 'r') as f:
            content = await f.read()
            return json.loads(content)

    async def save_workflow(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        workflows = await self.list_workflows()
        
        if "id" not in workflow:
            workflow["id"] = str(uuid.uuid4())
            
        existing_idx = next((i for i, w in enumerate(workflows) if w["id"] == workflow["id"]), -1)
        
        if existing_idx >= 0:
            workflows[existing_idx] = workflow
        else:
            workflows.append(workflow)
            
        async with aiofiles.open(WORKFLOWS_FILE, 'w') as f:
            await f.write(json.dumps(workflows, indent=2))
        
        return workflow

    async def delete_workflow(self, workflow_id: str) -> bool:
        workflows = await self.list_workflows()
        initial_len = len(workflows)
        workflows = [w for w in workflows if w["id"] != workflow_id]
        
        if len(workflows) < initial_len:
            async with aiofiles.open(WORKFLOWS_FILE, 'w') as f:
                await f.write(json.dumps(workflows, indent=2))
            return True
        return False

    async def get_workflow(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        workflows = await self.list_workflows()
        return next((w for w in workflows if w["id"] == workflow_id), None)

workflow_store = WorkflowStore()
