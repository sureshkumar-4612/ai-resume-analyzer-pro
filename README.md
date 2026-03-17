# 🤖 AI Resume Analyzer Agent

> **Production-grade autonomous AI agent** for resume analysis, powered by **LangChain** + **OpenRouter** (DeepSeek R1).

---

## ✨ Features

| # | Capability | Tool |
|---|-----------|------|
| 1 | Resume Loading (PDF/TXT/MD) | `ResumeLoaderTool` |
| 2 | Structured Parsing | `ResumeParserTool` |
| 3 | Skill Extraction & Categorisation | `SkillExtractionTool` |
| 4 | Weighted Resume Scoring (0–100) | `ResumeScoringTool` |
| 5 | ATS Compatibility Analysis | `ATSAnalyzerTool` |
| 6 | Weakness Detection | `WeaknessDetectionTool` |
| 7 | Improvement Suggestions | `ResumeImprovementTool` |
| 8 | Job Role Matching | `RoleMatcherTool` |
| 9 | Structured Report Generation | `ReportGeneratorTool` |

---

## 🏗️ Architecture

```
User Input
     │
Resume Loader          ← validates & loads PDF / TXT / MD
     │
Resume Parser          ← extracts structured sections
     │
Skill Extraction       ← categorises technical, soft, tools, languages
     │
Resume Scoring         ← 0-100 weighted score
     │
ATS Analysis           ← applicant tracking system check
     │
Weakness Detection     ← finds vague bullets, missing metrics
     │
Improvement Generator  ← suggests stronger wording
     │
Role Matcher           ← matches top 5 job roles
     │
Report Generator       ← compiles final structured report
     │
Final Output
```

---

## 🚀 Quick Start

### 1. Clone & Install

```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Key

```bash
# Copy example env and add your OpenRouter key
copy .env.example .env         # Windows
# cp .env.example .env         # macOS / Linux
```

Edit `.env` and set your key:

```
OPENROUTER_API_KEY=sk-or-v1-your-key-here
```

Get a free key at [openrouter.ai/keys](https://openrouter.ai/keys).

### 3. Run Analysis (CLI)

```bash
python main.py sample_resume.md
```

### 4. Run Analysis (API)

```bash
uvicorn api:app --reload --port 8000
```

Then upload a resume:

```bash
curl -X POST http://localhost:8000/analyze \
  -F "file=@sample_resume.md"
```

---

## 📊 Scoring Weights

| Category          | Weight |
|-------------------|--------|
| Content Quality   | 30     |
| Skills Relevance  | 20     |
| Experience Depth  | 20     |
| Formatting        | 10     |
| ATS Compatibility | 20     |

---

## 🔧 Model Configuration

| Setting      | Value |
|-------------|-------|
| Model        | `deepseek/deepseek-r1:free` |
| Temperature  | `0.2` |
| Max Tokens   | `4000` |
| API Endpoint | `https://openrouter.ai/api/v1/chat/completions` |

---

## 📁 Project Structure

```
project-2/
├── main.py                  # CLI entry point
├── api.py                   # FastAPI service layer
├── agent.py                 # LangChain agent orchestration
├── llm_client.py            # OpenRouter API client
├── config.py                # Configuration & env vars
├── models.py                # Pydantic data models
├── requirements.txt         # Python dependencies
├── .env                     # API key (not committed)
├── .env.example             # Example env file
├── sample_resume.md         # Sample resume for testing
├── tools/
│   ├── __init__.py
│   ├── resume_loader.py     # Tool 1: File loading
│   ├── resume_parser.py     # Tool 2: Section parsing
│   ├── skill_extraction.py  # Tool 3: Skill categorisation
│   ├── resume_scoring.py    # Tool 4: Weighted scoring
│   ├── ats_analyzer.py      # Tool 5: ATS compatibility
│   ├── weakness_detection.py# Tool 6: Problem detection
│   ├── resume_improvement.py# Tool 7: Improvement suggestions
│   ├── role_matcher.py      # Tool 8: Role matching
│   └── report_generator.py  # Tool 9: Final report
└── read.md                  # Original specification
```

---

## 📝 Example Output

```
Resume Score: 82 / 100
ATS Score: 70%

Top Skills:
  Python, SQL, Machine Learning

Strengths:
  ✅ Strong technical stack
  ✅ Clear work history

Weaknesses:
  ⚠️ Missing measurable achievements

Improvements:
  💡 Add quantifiable metrics

Suggested Roles:
  🎯 Data Scientist (85%)
  🎯 Machine Learning Engineer (78%)
  🎯 Backend Developer (74%)
```

---

## 🛡️ Error Handling

The agent handles:
- Corrupted files → request reprocessing
- Missing sections → fallback to raw text analysis
- Empty resumes → clear error message
- Incomplete contact info → partial extraction

---

## 🔮 Future Extensions

- LinkedIn profile analysis
- Portfolio scoring
- Job description matching
- Interview preparation module
- Recruiter recommendation engine
