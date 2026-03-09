from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="AI Codebase Explainer",
    version="1.0.0"
)

app.include_router(router)


@app.get("/")
def root():
    return {"message": "AI Codebase Explainer API running"}