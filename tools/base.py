"""
Base Tool class for the AI Resume Analyzer Agent.
A lightweight replacement for langchain.tools.BaseTool that avoids
Pydantic V1 compatibility issues on Python 3.14.
"""

from abc import ABC, abstractmethod


class BaseTool(ABC):
    """Minimal base class for pipeline tools."""

    name: str = "BaseTool"
    description: str = ""

    @abstractmethod
    def _run(self, input_text: str) -> str:
        """Execute the tool and return its output as a string."""
        ...

    def __repr__(self) -> str:
        return f"<{self.name}>"
