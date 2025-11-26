# LLM Testing Interface

A comprehensive Python-based FastAPI backend with a rich web UI for testing, evaluating, and orchestrating local LLM models and agent workflows.

This project is designed to work seamlessly with **LM Studio** (or any OpenAI-compatible local LLM server) to provide a powerful environment for prompt engineering, model comparison, and agent development.

## 🚀 Features

### 1. Interactive Playground
- **Multi-turn chat** with conversation history
- **Streaming responses** via Server-Sent Events (SSE) with Markdown rendering
- **System Instructions** editor for defining agent personas
- **Reasoning Effort** configuration (Low, Medium, High) for supported models
- **Stateful Conversations** using LM Studio's new Responses API
- **AI-powered prompt improvement** with the ✨ Prompt Generator
- **File attachments** support (images, text files)
- Configurable model, agent, max tokens, and temperature

### 2. Prompt Builder
- Create reusable **prompt templates** with `{{variable}}` placeholders
- Define system and user prompts separately
- **Live preview** with variable substitution
- Apply templates directly to Playground
- Persisted in `app/data/prompt_templates.json`

### 3. A/B Response Tester
- Compare responses from **2+ models/agents** side-by-side
- Same prompt sent to all variants simultaneously
- View latency metrics for each response
- **Vote feedback** (Better/Worse) for manual evaluation

### 4. Evaluation Suite
- **Dataset Management**: Create datasets with query/ground_truth pairs (JSONL format)
- **Built-in Templates**: Factual Q&A, Math, Summarization, Sentiment, Translation, Code Generation, Classification, RAG
- **Evaluators**: F1 Score, BLEU, Similarity, Exact Match, Contains Match, Length Ratio, and Custom LLM-based evaluators
- **Evaluation Jobs**: Run datasets against multiple evaluators with live streaming progress

### 5. Agent Orchestrator
- **Visual workflow builder** for multi-step agent pipelines
- **Node types**: Start, Agent, Tool, Condition, End
- **Drag-and-drop** canvas with edge connections
- **Conditional routing** and variable interpolation (`{{input}}`, `{{prev_output}}`)
- Execute workflows with JSON input and view step-by-step execution history

### 6. Tools Management
- Define tools with name, description, endpoint, and input schema
- Associate tools with specific models or agents
- Toggle enabled/disabled state

## 📋 Requirements

- Python 3.9+
- [LM Studio](https://lmstudio.ai/) (or any OpenAI-compatible local LLM server)

## 🛠️ Installation

1. **Clone the repository** (if applicable) or navigate to the project root.

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv .venv
   
   # Windows
   .\.venv\Scripts\activate
   
   # Linux/macOS
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 🏃‍♂️ Running the App

1. **Start your Local LLM Server** (e.g., LM Studio):
   - Ensure the server is running.
   - Default endpoint expected: `http://127.0.0.1:1234/v1`
   
   **Verify Connection:**
   
   *Curl:*
   ```bash
   curl http://127.0.0.1:1234/v1/models/
   ```
   
   *PowerShell:*
   ```powershell
   Invoke-RestMethod -Uri "http://127.0.0.1:1234/v1/models/"
   ```

2. **Start the Backend Server**:
   ```bash
   # Development mode (auto-reload on file changes)
   uvicorn app.main:app --reload
   
   # Production mode
   uvicorn app.main:app
   ```

3. **Access the Interface**:
   - Open your browser and navigate to `http://127.0.0.1:8000/`.

## 📂 Project Structure

```
app/
├── main.py                 # App initialization and router registration
├── routers/                # API route definitions
│   ├── playground.py       # Chat, generate, models endpoints
│   ├── tools.py            # Tool management endpoints
│   ├── templates.py        # Prompt template endpoints
│   ├── ab_test.py          # A/B testing endpoints
│   ├── evaluation.py       # Datasets, evaluators, jobs endpoints
│   └── workflows.py        # Workflow orchestration endpoints
├── models/
│   ├── service.py          # LocalLLMService - core business logic
│   ├── *_store.py          # JSON persistence for tools, templates, etc.
│   └── evaluators.py       # Built-in evaluator functions
├── static/
│   ├── index.html          # Main UI
│   ├── main.js             # Frontend logic
│   └── style.css           # Dark theme styling
└── data/                   # JSON persistence (auto-created)
```

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/models` | GET | List available LLM models |
| `/api/health` | GET | Quick ping to check server status |
| `/api/chat` | POST | Multi-turn chat (supports streaming) |
| `/api/ab-test` | POST | A/B test multiple variants |
| `/api/tools` | GET/POST | List/create tools |
| `/api/prompt-templates` | GET/POST | List/create templates |
| `/api/datasets` | GET/POST | List/create datasets |
| `/api/evaluators` | GET | List all evaluators |
| `/api/workflows` | GET/POST | List/create workflows |

## 🔧 Advanced Configuration

### Local LLM Integration
The project uses LM Studio's OpenAI-compatible HTTP API by default:
- **Base URL**: `http://127.0.0.1:1234/v1`
- **Responses API**: Supports the new `/v1/responses` endpoint for stateful chat and reasoning.
- To use a different backend (Ollama, vLLM, etc.), modify `LocalLLMService` in `app/models/service.py`.

### Creating Custom Tools
Tools extend agent capabilities by connecting to external endpoints. Define them in the **Tools** tab or via API.

### Example Tool Definitions

#### 1. Web Search Tool
```json
{
  "name": "web_search",
  "description": "Search the web for current information. Use for questions about recent events, facts, or topics requiring up-to-date data.",
  "endpoint": "https://api.example.com/search",
  "input_schema": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "The search query"
      },
      "num_results": {
        "type": "integer",
        "description": "Number of results to return",
        "default": 5
      }
    },
    "required": ["query"]
  },
  "enabled": true
}
```

#### 2. Calculator Tool
```json
{
  "name": "calculator",
  "description": "Perform mathematical calculations. Use for arithmetic, algebra, or any numeric computation.",
  "endpoint": "/api/tools/calculator",
  "input_schema": {
    "type": "object",
    "properties": {
      "expression": {
        "type": "string",
        "description": "Mathematical expression to evaluate (e.g., '2 + 2 * 3')"
      }
    },
    "required": ["expression"]
  },
  "enabled": true
}
```

#### 3. Database Query Tool
```json
{
  "name": "query_database",
  "description": "Query the product database. Use to look up inventory, prices, or product details.",
  "endpoint": "/api/tools/db-query",
  "input_schema": {
    "type": "object",
    "properties": {
      "table": {
        "type": "string",
        "enum": ["products", "orders", "customers"],
        "description": "Database table to query"
      },
      "filters": {
        "type": "object",
        "description": "Key-value pairs for filtering results"
      },
      "limit": {
        "type": "integer",
        "default": 10
      }
    },
    "required": ["table"]
  },
  "enabled": true,
  "agents": ["sales-agent", "support-agent"]
}
```

#### 4. Code Execution Tool
```json
{
  "name": "run_python",
  "description": "Execute Python code in a sandboxed environment. Use for data processing, calculations, or generating outputs.",
  "endpoint": "/api/tools/python-sandbox",
  "input_schema": {
    "type": "object",
    "properties": {
      "code": {
        "type": "string",
        "description": "Python code to execute"
      },
      "timeout": {
        "type": "integer",
        "description": "Maximum execution time in seconds",
        "default": 30
      }
    },
    "required": ["code"]
  },
  "enabled": true,
  "models": ["gpt-4", "claude-3"]
}
```

#### 5. Email Sender Tool
```json
{
  "name": "send_email",
  "description": "Send an email to a recipient. Use when user explicitly requests to send an email.",
  "endpoint": "/api/tools/email",
  "input_schema": {
    "type": "object",
    "properties": {
      "to": {
        "type": "string",
        "format": "email",
        "description": "Recipient email address"
      },
      "subject": {
        "type": "string",
        "description": "Email subject line"
      },
      "body": {
        "type": "string",
        "description": "Email body content (plain text or HTML)"
      },
      "cc": {
        "type": "array",
        "items": { "type": "string", "format": "email" },
        "description": "CC recipients"
      }
    },
    "required": ["to", "subject", "body"]
  },
  "enabled": true
}
```

### Using Tools in Workflows (Orchestrator)

In the Agent Orchestrator, tools are integrated as **Tool Nodes**:

1. **Add a Tool Node** to your workflow canvas
2. **Configure the node**:
   - Set `Tool ID` to match your tool name (e.g., `web_search`)
   - Set `Input Template` using variables:
     ```
     {"query": "{{prev_output}}"}
     ```
3. **Connect edges** from Agent nodes to Tool nodes

#### Workflow Example: Research Assistant

```
[Start] → [Agent: Parse Query] → [Tool: web_search] → [Agent: Summarize] → [End]
```

**Node Configurations:**

- **Agent: Parse Query**
  - Prompt: `Extract the main search topic from: {{input}}`
  
- **Tool: web_search**
  - Input Template: `{"query": "{{prev_output}}", "num_results": 3}`
  
- **Agent: Summarize**
  - Prompt: `Summarize these search results:\n{{prev_output}}`

### Conditional Tool Selection

Use **Condition Nodes** to dynamically choose tools:

```
[Start] → [Agent: Classify] → [Condition: contains:math] 
                                    ├─ Yes → [Tool: calculator]
                                    └─ No  → [Tool: web_search]
```

**Condition expressions:**
- `contains:math` - Check if output contains "math"
- `equals:search` - Exact match
- `startswith:calculate` - Prefix match
- `>:100` - Numeric comparison (for scores/counts)

### Best Practices

1. **Write clear descriptions** - Agents use descriptions to decide when to call tools
2. **Define strict schemas** - Validate inputs with required fields and types
3. **Use enums for fixed options** - Prevents invalid inputs
4. **Set reasonable defaults** - Reduce required parameters
5. **Scope to specific agents** - Not all tools should be available to all agents
6. **Test with A/B Tester** - Compare tool-enabled vs tool-disabled responses
7. **Monitor in Evaluation** - Create datasets to test tool usage accuracy

### Implementing Tool Endpoints

Tool endpoints receive POST requests with the input data. You can add them to a new router or an existing one.

```python
# Example: Create app/routers/custom_tools.py

from fastapi import APIRouter, Request

router = APIRouter()

@router.post("/api/tools/calculator")
async def calculator_tool(request: Request):
    data = await request.json()
    expression = data.get("expression", "")
    
    try:
        # WARNING: Use a safe evaluator in production!
        result = eval(expression)
        return {"result": result, "success": True}
    except Exception as e:
        return {"error": str(e), "success": False}

# Then register the router in app/main.py
# app.include_router(custom_tools.router)
```

## 🔮 Upcoming Features

- **Latency Dashboard**: Response time tracking and performance metrics
- **Guardrail Tester**: Safety filters and PII detection testing
- **Template Modes**: Role-play, Chain-of-Thought, few-shot templates
- **Multi-Turn Chat Lab**: Conversation simulation with branching paths
- **History & Replay**: Request/response logging with replay capability
