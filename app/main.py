from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.routers import playground, tools, templates, ab_test, evaluation, workflows
import os

app = FastAPI(title="LLM Testing Interface")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(playground.router)
app.include_router(tools.router)
app.include_router(templates.router)
app.include_router(ab_test.router)
app.include_router(evaluation.router)
app.include_router(workflows.router)

# Static Files
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
