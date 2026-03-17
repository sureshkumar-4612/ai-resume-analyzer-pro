# AI Resume Analyzer Agent

## Overview

The AI Resume Analyzer Agent is an autonomous system designed to analyze resumes, extract candidate information, evaluate strengths and weaknesses, and generate actionable improvement recommendations.

The system uses **LangChain for orchestration** and **OpenRouter API for LLM inference**.

This project is intended to run as a **production-grade modular AI agent** capable of:

* Resume parsing
* Skill extraction
* ATS compatibility analysis
* Role matching
* Resume improvement suggestions
* Structured report generation

---

# Core Objective

Given a resume file (PDF or text), the agent must:

1. Extract structured information
2. Analyze the resume quality
3. Detect missing elements
4. Evaluate ATS compatibility
5. Generate improvement suggestions
6. Produce a structured evaluation report

---

# Model Configuration

Use the following OpenRouter model:

```
deepseek/deepseek-r1:free
```

API Endpoint:

```
https://openrouter.ai/api/v1/chat/completions
```

Environment variables required:

```
OPENROUTER_API_KEY
```

---

# Technology Stack

Core Components:

* Python 3.10+
* LangChain
* OpenRouter API
* FAISS (optional memory)
* Pydantic
* FastAPI (optional service layer)
* PDF parsing tools

Libraries:

```
langchain
langchain-community
pydantic
python-dotenv
pdfplumber
fastapi
uvicorn
faiss-cpu
```

---

# Agent Architecture

The system operates as a **tool-enabled reasoning agent**.

Architecture:

```
User Input
     │
Resume Loader
     │
Resume Parser
     │
Skill Extraction Module
     │
ATS Analysis Module
     │
Resume Scoring Engine
     │
Improvement Recommendation Generator
     │
Structured Report Generator
     │
Final Output
```

---

# Agent Workflow

## Step 1 — Input Acquisition

Input formats supported:

* PDF
* TXT
* Markdown

Agent must:

1. Receive file path
2. Validate file
3. Load file content

Tools required:

```
ResumeLoaderTool
```

Responsibilities:

* Validate file
* Extract raw text

---

# Step 2 — Resume Parsing

The agent must extract structured sections.

Target sections:

* Name
* Email
* Phone
* Skills
* Education
* Work Experience
* Certifications
* Projects

Output format:

```
{
  name: "",
  email: "",
  phone: "",
  skills: [],
  education: [],
  experience: [],
  projects: []
}
```

Tools:

```
ResumeParserTool
```

---

# Step 3 — Skill Extraction

Agent must identify:

* Technical skills
* Soft skills
* Tools
* Programming languages

Example:

Input:

```
Experienced Python developer with React knowledge
```

Output:

```
Python
React
JavaScript
Software Development
```

Tool:

```
SkillExtractionTool
```

---

# Step 4 — Resume Scoring

The agent must generate a score from **0–100**.

Evaluation metrics:

| Category          | Weight |
| ----------------- | ------ |
| Content Quality   | 30     |
| Skills Relevance  | 20     |
| Experience Depth  | 20     |
| Formatting        | 10     |
| ATS Compatibility | 20     |

Example Output:

```
Resume Score: 78 / 100
```

Tool:

```
ResumeScoringTool
```

---

# Step 5 — ATS Compatibility Analysis

The agent must evaluate whether the resume is optimized for Applicant Tracking Systems.

Checks include:

* keyword density
* formatting simplicity
* section labeling
* bullet usage

Output Example:

```
ATS Compatibility Score: 65%

Issues detected:
- Missing role keywords
- Poor section headings
```

Tool:

```
ATSAnalyzerTool
```

---

# Step 6 — Weakness Detection

The agent must identify problems such as:

* vague bullet points
* missing metrics
* unclear role impact
* missing skills
* inconsistent formatting

Example:

```
Weakness:
"Worked on backend systems"

Improved version:
"Developed scalable backend APIs using Python and Flask, improving response time by 40%"
```

Tool:

```
WeaknessDetectionTool
```

---

# Step 7 — Resume Improvement Generator

The agent must produce:

* stronger bullet points
* missing skill recommendations
* role-specific improvements

Example:

```
Original:
Responsible for database tasks

Improved:
Designed and optimized PostgreSQL queries improving data retrieval performance by 35%
```

Tool:

```
ResumeImprovementTool
```

---

# Step 8 — Job Role Matching

The agent should infer suitable roles.

Example roles:

* Backend Developer
* Data Analyst
* Machine Learning Engineer
* Full Stack Developer

Output:

```
Top Matching Roles:

1. Backend Engineer (87%)
2. Data Engineer (74%)
3. Machine Learning Engineer (65%)
```

Tool:

```
RoleMatcherTool
```

---

# Step 9 — Final Report Generation

The agent must generate a structured report.

Report format:

```
Candidate Overview
-------------------

Name:
Email:

Resume Score:
ATS Score:

Top Skills:

Strengths:

Weaknesses:

Recommended Improvements:

Suggested Roles:

Final Verdict:
```

Tool:

```
ReportGeneratorTool
```

---

# Agent Reasoning Strategy

The agent must follow this reasoning loop:

```
Observe → Analyze → Plan → Execute Tool → Evaluate Result → Continue
```

LangChain agent type recommended:

```
structured-chat-agent
```

Or

```
tool-calling agent
```

---

# LangChain Agent Setup

LLM Configuration:

```
model = deepseek/deepseek-r1:free
temperature = 0.2
max_tokens = 4000
```

Agent should be initialized with tools:

```
ResumeLoaderTool
ResumeParserTool
SkillExtractionTool
ResumeScoringTool
ATSAnalyzerTool
WeaknessDetectionTool
ResumeImprovementTool
RoleMatcherTool
ReportGeneratorTool
```

---

# Error Handling

Agent must handle:

* corrupted files
* missing sections
* empty resumes
* incomplete contact info

Fallback strategy:

```
If extraction fails → request reprocessing
If parsing fails → fallback to raw text analysis
```

---

# Production Requirements

The system must:

* process resumes under **10 seconds**
* support concurrent requests
* return structured JSON responses
* maintain deterministic analysis

---

# Output Example

```
Resume Score: 82 / 100
ATS Score: 70%

Top Skills:
Python
SQL
Machine Learning

Strengths:
Strong technical stack
Clear work history

Weaknesses:
Missing measurable achievements

Improvements:
Add quantifiable metrics

Suggested Roles:
Data Scientist
Machine Learning Engineer
Backend Developer
```

---

# Future Extensions

Possible upgrades:

* LinkedIn profile analysis
* portfolio scoring
* job description matching
* interview preparation module
* recruiter recommendation engine

---

# Mission Directive for Autonomous Agent

The agent must:

1. Build modular components
2. Implement LangChain tool architecture
3. Integrate OpenRouter API
4. Implement full resume analysis pipeline
5. Generate structured professional reports

The final system must operate as a **production-ready AI Resume Evaluation Agent**.
