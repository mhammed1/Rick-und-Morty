from __future__ import annotations

from fastapi import Body, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .oracle_service import BASE_DIR, ingest_data, run_chat


app = FastAPI(title="Interdimensional Oracle API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/api/ingest")
def ingest() -> dict:
    stats = ingest_data()
    return {"status": "ok", "stats": stats}


@app.post("/api/chat")
def chat(payload: dict = Body(...)) -> dict:
    try:
        return run_chat(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


app.mount("/", StaticFiles(directory=BASE_DIR / "static", html=True), name="static")
