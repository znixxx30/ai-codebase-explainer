from fastapi import FastAPI

app = FastAPI(
    title="AI Codebase Explainer",
    version="1.0.0"
)


@app.get("/")
def root():
    return {"message": "AI Codebase Explainer API running"}