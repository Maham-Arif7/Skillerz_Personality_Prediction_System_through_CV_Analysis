# 🧠 Personality Prediction System Through CV Analysis

An NLP-powered Streamlit app that analyzes a candidate's CV/resume and predicts
**Big Five (OCEAN)** personality traits — Openness, Conscientiousness, Extraversion,
Agreeableness, and Emotional Stability — purely from the language used in the resume.
Built for recruiters to get a fast, explainable, data-driven read on culture/role fit,
alongside the usual skills/experience review.

Runs **100% offline** — no OpenAI/Anthropic/Google API key required. All analysis
happens locally using classic NLP techniques.

---

## Features

- **Upload PDF / DOCX / TXT** resumes — text is extracted automatically.
- **Big Five trait scoring (0–100)** via a curated psycholinguistic keyword-lexicon
  engine (inspired by LIWC / IBM Watson Personality Insights), with an achievement/
  quantification-density signal layered on top.
- **Explainability** — every score comes with the exact words in the CV that
  triggered it ("why this score?").
- **Interactive radar + bar charts** (Plotly) for a clear visual personality profile.
- **Automatic role-fit suggestions** (e.g. R&D, Sales, Project Management, HR/Support)
  based on trait combinations.
- **Top resume keywords** via TF-IDF, independent of the fixed trait lexicons.
- **Downloadable one-page PDF report** per candidate.
- **Batch / Compare mode** — upload multiple CVs, rank and compare candidates
  side-by-side in a sortable table + grouped bar chart, export to CSV.
- Clean, dark, recruiter-friendly UI.

## How the prediction works

1. **Text extraction** — `pdfplumber` / `python-docx` pull raw text from the uploaded file.
2. **Cleaning & tokenizing** — lowercased, punctuation-stripped, tokenized.
3. **Lexicon matching** — each of the 5 traits has a hand-built dictionary of
   word families (e.g. Conscientiousness: *organized, meticulous, deadline,
   disciplined...*) with evidence weights. The text is scanned for whole-word/
   phrase matches.
4. **Achievement signal** — the density of numbers/percentages/metrics in the text
   (a common marker of results-oriented, conscientious writing) nudges
   Conscientiousness and Openness.
5. **Emotional Stability** — computed from the balance of composure/resilience
   language vs. stress/struggle language, centered at a neutral 50.
6. **Scaling** — raw weighted hits are normalized by document length and mapped to
   0–100 with a saturating curve, so short and long resumes are comparable and no
   score linearly explodes with resume length.
7. **Role fit** — trait-combination rules (e.g. high Extraversion + Agreeableness →
   Sales/Client-facing roles) rank suggested role categories.

## Project structure

```
personality_cv_analyzer/
├── app.py                  # Streamlit UI (single + batch/compare modes)
├── core/
│   ├── extractor.py        # PDF/DOCX/TXT text extraction + name/contact detection
│   ├── lexicons.py         # Big Five keyword lexicons + role-fit rules
│   ├── analyzer.py         # Scoring engine (NLP + scaling logic)
│   └── report.py           # PDF report generator
├── sample_cv.txt           # Sample resume to try the app with
├── requirements.txt
└── README.md
```

## Setup & run

```bash
# 1. Create and activate a virtual environment (recommended)
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

The app opens in your browser at `http://localhost:8501`. Try it instantly with the
included `sample_cv.txt`.

## Tech stack

- **Streamlit** — web UI
- **pdfplumber**, **python-docx** — resume text extraction
- **scikit-learn** (`TfidfVectorizer`) — keyword extraction
- **Plotly** — radar/bar visualizations
- **pandas** — candidate comparison tables
- **fpdf2** — PDF report generation

## Disclaimer

This is an educational/demo tool. Lexicon-based personality inference from resume
text is a simplified, approximate model — it is **not** a validated psychometric
instrument (unlike clinically validated tools such as the NEO-PI-R) and should never
be the sole basis for a real hiring decision. It's best used as one supporting signal
alongside interviews, skills assessments, and reference checks.

## Possible extensions

- Train a supervised classifier (e.g. logistic regression / fine-tuned transformer)
  on a labeled personality-essay dataset for statistically validated scoring.
- Add spaCy-based Named Entity Recognition to auto-extract skills, companies, and
  job titles into a structured profile.
- Add authentication + a database so recruiters can save candidate history over time.
