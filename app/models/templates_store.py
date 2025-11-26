import json
import os
from typing import List, Dict, Any, Optional
import aiofiles
import uuid

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
TEMPLATES_FILE = os.path.join(DATA_DIR, "prompt_templates.json")

class TemplatesStore:
    def __init__(self):
        self._ensure_data_dir()

    def _ensure_data_dir(self):
        os.makedirs(DATA_DIR, exist_ok=True)
        if not os.path.exists(TEMPLATES_FILE):
            with open(TEMPLATES_FILE, 'w') as f:
                json.dump([], f)

    async def list_templates(self) -> List[Dict[str, Any]]:
        async with aiofiles.open(TEMPLATES_FILE, 'r') as f:
            return json.loads(await f.read())

    async def save_template(self, template: Dict[str, Any]) -> Dict[str, Any]:
        items = await self.list_templates()
        if "id" not in template:
            template["id"] = str(uuid.uuid4())
            
        idx = next((i for i, x in enumerate(items) if x["id"] == template["id"]), -1)
        if idx >= 0:
            items[idx] = template
        else:
            items.append(template)
            
        async with aiofiles.open(TEMPLATES_FILE, 'w') as f:
            await f.write(json.dumps(items, indent=2))
        return template

    async def delete_template(self, template_id: str) -> bool:
        items = await self.list_templates()
        initial_len = len(items)
        items = [x for x in items if x["id"] != template_id]
        
        if len(items) < initial_len:
            async with aiofiles.open(TEMPLATES_FILE, 'w') as f:
                await f.write(json.dumps(items, indent=2))
            return True
        return False

templates_store = TemplatesStore()
