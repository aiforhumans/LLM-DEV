# LLM Testing Interface Instructions

## Project Overview
A comprehensive Python-based FastAPI backend with a rich web UI for testing, evaluating, and orchestrating local LLM models and agent workflows.
The system uses **LM Studio** as the local LLM runtime via its OpenAI-compatible HTTP API.

## Local LLM Integration (LM Studio)
- **Base URL**: `http://127.0.0.1:1234/v1`
- **Models Endpoint**: `/v1/models`
- **Chat Endpoint**: `/v1/chat/completions`

### Quick Ping / Model Load Verification
To verify the server is reachable and list loaded models:

**Curl:**
```bash
curl http://127.0.0.1:1234/v1/models/
```

**PowerShell (Windows):**
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:1234/v1/models/"
```

## Project Structure
```
app/
├── main.py                 # App initialization
├── routers/                # API endpoints
├── models/                 # Business logic & storage
├── static/                 # Frontend assets
└── data/                   # JSON persistence
```
