"""
ResumeLoaderTool
────────────────
Validates the resume file and extracts raw text.
Supports PDF, TXT, and Markdown files.
"""

import os
from tools.base import BaseTool  # type: ignore[import-untyped]
import pdfplumber  # type: ignore[import-untyped]


class ResumeLoaderTool(BaseTool):
    name: str = "ResumeLoaderTool"
    description: str = (
        "Receives a file path, validates it, and loads raw text content "
        "from PDF, TXT, or Markdown resume files."
    )

    def _run(self, file_path: str) -> str:
        """Load and return the raw text of a resume file."""
        file_path = file_path.strip().strip('"').strip("'")

        # ── Validation ───────────────────────────────────────
        if not os.path.exists(file_path):
            return f"ERROR: File not found — {file_path}"

        ext = os.path.splitext(file_path)[1].lower()
        supported = {".pdf", ".txt", ".md"}
        if ext not in supported:
            return (
                f"ERROR: Unsupported file type '{ext}'. "
                f"Supported formats: {', '.join(sorted(supported))}"
            )

        # ── Extraction ───────────────────────────────────────
        try:
            if ext == ".pdf":
                return self._load_pdf(file_path)
            else:
                return self._load_text(file_path)
        except Exception as exc:
            return f"ERROR: Failed to load file — {exc}"

    def _load_pdf(self, path: str) -> str:
        pages: list[str] = []
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    pages.append(text)
        if not pages:
            return "ERROR: PDF appears empty — no extractable text found."
        return "\n\n".join(pages)

    def _load_text(self, path: str) -> str:
        with open(path, "r", encoding="utf-8") as fh:
            content = fh.read().strip()
        if not content:
            return "ERROR: File is empty."
        return content
