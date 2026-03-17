"""
Pydantic models representing every structured data object
used across the AI Resume Analyzer Agent pipeline.
"""

from __future__ import annotations
from pydantic import BaseModel, Field  # type: ignore[import-untyped]


class ContactInfo(BaseModel):
    """Candidate contact details extracted from a resume."""
    name: str = ""
    email: str = ""
    phone: str = ""


class ParsedResume(BaseModel):
    """Structured resume data produced by ResumeParserTool."""
    name: str = ""
    email: str = ""
    phone: str = ""
    skills: list[str] = Field(default_factory=list)
    education: list[str] = Field(default_factory=list)
    experience: list[str] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)
    projects: list[str] = Field(default_factory=list)


class SkillSet(BaseModel):
    """Categorised skills produced by SkillExtractionTool."""
    technical_skills: list[str] = Field(default_factory=list)
    soft_skills: list[str] = Field(default_factory=list)
    tools: list[str] = Field(default_factory=list)
    programming_languages: list[str] = Field(default_factory=list)


class ScoringBreakdown(BaseModel):
    """Per-category scoring breakdown produced by ResumeScoringTool."""
    content_quality: float = 0.0
    skills_relevance: float = 0.0
    experience_depth: float = 0.0
    formatting: float = 0.0
    ats_compatibility: float = 0.0
    total_score: float = 0.0


class ATSResult(BaseModel):
    """ATS compatibility result from ATSAnalyzerTool."""
    ats_score: float = 0.0
    issues: list[str] = Field(default_factory=list)


class Weakness(BaseModel):
    """A single weakness detected by WeaknessDetectionTool."""
    original: str = ""
    issue: str = ""
    improved_version: str = ""


class Improvement(BaseModel):
    """A single improvement suggestion from ResumeImprovementTool."""
    original: str = ""
    improved: str = ""
    category: str = ""


class RoleMatch(BaseModel):
    """A single job-role match from RoleMatcherTool."""
    role: str = ""
    match_percentage: float = 0.0


class FinalReport(BaseModel):
    """Complete evaluation report produced by ReportGeneratorTool."""
    name: str = ""
    email: str = ""
    resume_score: float = 0.0
    ats_score: float = 0.0
    top_skills: list[str] = Field(default_factory=list)
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    recommended_improvements: list[str] = Field(default_factory=list)
    suggested_roles: list[RoleMatch] = Field(default_factory=list)
    final_verdict: str = ""
