"""
Tools package – every LangChain tool used by the Resume Analyzer Agent.
"""

from tools.resume_loader import ResumeLoaderTool
from tools.resume_parser import ResumeParserTool
from tools.skill_extraction import SkillExtractionTool
from tools.resume_scoring import ResumeScoringTool
from tools.ats_analyzer import ATSAnalyzerTool
from tools.weakness_detection import WeaknessDetectionTool
from tools.resume_improvement import ResumeImprovementTool
from tools.role_matcher import RoleMatcherTool
from tools.report_generator import ReportGeneratorTool

ALL_TOOLS = [
    ResumeLoaderTool(),
    ResumeParserTool(),
    SkillExtractionTool(),
    ResumeScoringTool(),
    ATSAnalyzerTool(),
    WeaknessDetectionTool(),
    ResumeImprovementTool(),
    RoleMatcherTool(),
    ReportGeneratorTool(),
]

__all__ = [
    "ResumeLoaderTool",
    "ResumeParserTool",
    "SkillExtractionTool",
    "ResumeScoringTool",
    "ATSAnalyzerTool",
    "WeaknessDetectionTool",
    "ResumeImprovementTool",
    "RoleMatcherTool",
    "ReportGeneratorTool",
    "ALL_TOOLS",
]
