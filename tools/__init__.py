"""
Tools package – high-performance consolidated resume tools.
"""

from tools.resume_loader import ResumeLoaderTool
from tools.master_analysis import MasterAnalysisTool

ALL_TOOLS = [
    ResumeLoaderTool(),
    MasterAnalysisTool(),
]

__all__ = [
    "ResumeLoaderTool",
    "MasterAnalysisTool",
    "ALL_TOOLS",
]
