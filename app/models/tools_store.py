import json
import os
from typing import List, Dict, Any, Optional
import aiofiles

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
TOOLS_FILE = os.path.join(DATA_DIR, "tools.json")

class ToolsStore:
    def __init__(self):
        self._ensure_data_dir()

    def _ensure_data_dir(self):
        os.makedirs(DATA_DIR, exist_ok=True)
        if not os.path.exists(TOOLS_FILE):
            with open(TOOLS_FILE, 'w') as f:
                json.dump([], f)

    async def list_tools(self) -> List[Dict[str, Any]]:
        async with aiofiles.open(TOOLS_FILE, 'r') as f:
            content = await f.read()
            return json.loads(content)

    async def save_tool(self, tool: Dict[str, Any]) -> Dict[str, Any]:
        tools = await self.list_tools()
        # Check if update or create
        existing_idx = next((i for i, t in enumerate(tools) if t["name"] == tool["name"]), -1)
        
        if existing_idx >= 0:
            tools[existing_idx] = tool
        else:
            tools.append(tool)
            
        async with aiofiles.open(TOOLS_FILE, 'w') as f:
            await f.write(json.dumps(tools, indent=2))
        
        return tool

    async def delete_tool(self, name: str) -> bool:
        tools = await self.list_tools()
        initial_len = len(tools)
        tools = [t for t in tools if t["name"] != name]
        
        if len(tools) < initial_len:
            async with aiofiles.open(TOOLS_FILE, 'w') as f:
                await f.write(json.dumps(tools, indent=2))
            return True
        return False

    async def get_tool(self, name: str) -> Optional[Dict[str, Any]]:
        tools = await self.list_tools()
        return next((t for t in tools if t["name"] == name), None)

tools_store = ToolsStore()
