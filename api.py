"""
AI Resume Analyzer Agent — FastAPI Service Layer
─────────────────────────────────────────────────
Provides a REST API for resume analysis.

Endpoints:
    POST /analyze          — upload a resume file for analysis
    GET  /health           — health check
    GET  /                 — welcome page

Run:
    uvicorn api:app --reload --port 8000
"""

from __future__ import annotations

import os
import tempfile
import time

from fastapi import FastAPI, UploadFile, File, HTTPException  # type: ignore[import-untyped]
from fastapi.responses import JSONResponse, FileResponse  # type: ignore[import-untyped]
from fastapi.middleware.cors import CORSMiddleware  # type: ignore[import-untyped]

from agent import run_analysis  # type: ignore[import-untyped]
from config import SUPPORTED_EXTENSIONS  # type: ignore[import-untyped]

app = FastAPI(
    title="AI Resume Analyzer Agent",
    description=(
        "Production-grade AI agent for resume evaluation. "
        "Upload a PDF, TXT, or Markdown resume to receive a "
        "structured analysis report."
    ),
    version="1.0.0",
)

# ── CORS ─────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root() -> FileResponse:
    """Serve the modern frontend UI."""
    return FileResponse("index.html")


@app.get("/health")
async def health() -> dict:
    return {"status": "healthy"}


@app.post("/analyze")
async def analyze_resume(file: UploadFile = File(...)) -> JSONResponse:
    """
    Upload a resume file (PDF, TXT, or MD) and receive a
    structured evaluation report.
    """
    # ── Validate extension ───────────────────────────────────
    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Unsupported file type '{ext}'. "
                f"Accepted: {', '.join(SUPPORTED_EXTENSIONS)}"
            ),
        )

    # ── Save to temp file ────────────────────────────────────
    contents: bytes = await file.read()
    fd, tmp_path = tempfile.mkstemp(suffix=ext, dir=tempfile.gettempdir())
    try:
        os.write(fd, contents)
    finally:
        os.close(fd)

    # ── Run pipeline ─────────────────────────────────────────
    elapsed: float = 0.0
    try:
        start = time.time()
        result = run_analysis(tmp_path)
        elapsed = time.time() - start
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    finally:
        os.unlink(tmp_path)

    report = result.get("report", {})
    steps = [s["tool"] for s in result.get("steps", [])]

    processing_time: float = float(f"{elapsed:.2f}")

    return JSONResponse(
        content={
            "report": report,
            "pipeline_steps": steps,
            "processing_time_seconds": processing_time,
        }
    )
