"""
Personality Prediction System Through CV Analysis
"""

import io
import sys
import os

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

sys.path.append(os.path.dirname(__file__))

from core.extractor import extract_text, guess_candidate_name, find_contact_info
from core.analyzer import analyze_cv, trait_summary_sentence
from core.report import build_pdf_report
from core.lexicons import TRAIT_DESCRIPTIONS, TRAIT_ICONS

TRAIT_ORDER = ["Openness", "Conscientiousness", "Extraversion", "Agreeableness", "Emotional Stability"]

# ------------------------------------------------------------------ #
# PAGE CONFIG + THEME
# ------------------------------------------------------------------ #
st.set_page_config(
    page_title="Personality Prediction System",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

CUSTOM_CSS = """
<style>
    .stApp {
        background: radial-gradient(circle at 85% 15%, #17203f 0%, #0c1024 55%, #090b1a 100%);
        color: #eef0fb;
    }
    section[data-testid="stSidebar"] {
        background: #0e1230;
        border-right: 1px solid #262b52;
    }
    h1, h2, h3, h4 { color: #f4f5ff !important; }
    .metric-card {
        background: linear-gradient(145deg, #161b3d, #10132b);
        border: 1px solid #2a2f5c;
        border-radius: 14px;
        padding: 18px 20px;
        margin-bottom: 12px;
    }
    .trait-title { font-size: 1.05rem; font-weight: 700; color: #ffffff; }
    .trait-desc { font-size: 0.82rem; color: #9aa0c9; margin-top: 2px;}
    .role-pill {
        display:inline-block; background:#2b3070; color:#dfe3ff;
        padding:4px 12px; border-radius:20px; margin:3px 4px 0 0; font-size:0.8rem;
    }
    .badge {
        background:#5a6ee8; color:white; padding:2px 10px; border-radius:12px; font-size:0.75rem;
    }
    div[data-testid="stMetricValue"] { color: #ffffff; }
    .stTabs [data-baseweb="tab"] { color: #b6bbe6; }
    .keyword-chip {
        display:inline-block; background:#1c2150; border:1px solid #363c76;
        color:#c8ccf5; padding:3px 10px; border-radius:8px; margin:3px; font-size:0.78rem;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

ACCENT_COLORS = {
    "Openness": "#8e7cff",
    "Conscientiousness": "#5ac8fa",
    "Extraversion": "#ff9f6e",
    "Agreeableness": "#5ee6b8",
    "Emotional Stability": "#f8d56b",
}


# ------------------------------------------------------------------ #
# HELPERS
# ------------------------------------------------------------------ #
def radar_chart(scores: dict) -> go.Figure:
    categories = TRAIT_ORDER + [TRAIT_ORDER[0]]
    values = [scores.get(t, 0) for t in TRAIT_ORDER] + [scores.get(TRAIT_ORDER[0], 0)]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill="toself",
        fillcolor="rgba(120,130,255,0.25)",
        line=dict(color="#8e97ff", width=2),
        marker=dict(size=6, color="#c7cbff"),
        name="Trait Score",
    ))
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0, 100], gridcolor="#2c315e", tickfont=dict(color="#9aa0c9")),
            angularaxis=dict(gridcolor="#2c315e", tickfont=dict(color="#eef0fb", size=12)),
        ),
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=40, r=40, t=30, b=30),
        height=420,
    )
    return fig


def trait_bar(scores: dict) -> go.Figure:
    fig = go.Figure(go.Bar(
        x=[scores.get(t, 0) for t in TRAIT_ORDER],
        y=TRAIT_ORDER,
        orientation="h",
        marker_color=[ACCENT_COLORS[t] for t in TRAIT_ORDER],
        text=[f"{scores.get(t, 0):.0f}" for t in TRAIT_ORDER],
        textposition="outside",
    ))
    fig.update_layout(
        xaxis=dict(range=[0, 105], gridcolor="#2c315e", tickfont=dict(color="#9aa0c9")),
        yaxis=dict(tickfont=dict(color="#eef0fb", size=12)),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=10, b=10),
        height=280,
    )
    return fig


def render_trait_cards(scores: dict, evidence: dict):
    cols = st.columns(len(TRAIT_ORDER))
    for col, trait in zip(cols, TRAIT_ORDER):
        with col:
            st.markdown(
                f"""<div class="metric-card">
                        <div class="trait-title">{TRAIT_ICONS.get(trait,'')} {trait}</div>
                        <div class="badge">{scores.get(trait,0):.0f}/100</div>
                        <div class="trait-desc">{TRAIT_DESCRIPTIONS.get(trait,'')}</div>
                    </div>""",
                unsafe_allow_html=True,
            )
    with st.expander("🔍 Why these scores? (word-level evidence)"):
        for trait in TRAIT_ORDER:
            words = []
            for concept, hits in evidence.get(trait, {}).items():
                for form, count in hits:
                    words.append(f"{form} (×{count})")
            st.markdown(f"**{trait}:** " + (", ".join(words) if words else "_no strong signal words detected_"))


def analyze_and_display(uploaded_file, key_prefix=""):
    raw_text = extract_text(uploaded_file)
    if not raw_text.strip():
        st.error(f"Couldn't extract readable text from **{uploaded_file.name}**. Try a text-based PDF/DOCX (not a scanned image).")
        return None

    candidate_name = guess_candidate_name(raw_text, uploaded_file.name)
    contact = find_contact_info(raw_text)
    result = analyze_cv(raw_text)
    result["candidate_name"] = candidate_name
    result["contact"] = contact
    result["raw_text"] = raw_text
    return result


# ------------------------------------------------------------------ #
# SIDEBAR
# ------------------------------------------------------------------ #
with st.sidebar:
    st.markdown("## 🧠 Personality Predictor")
    st.caption("CV Analysis → Big Five (OCEAN) Traits")
    st.markdown("---")
    mode = st.radio("Mode", ["Single Candidate", "Compare Candidates (Batch)"])
    st.markdown("---")
    st.markdown("#### How it works")
    st.caption(
        "The engine parses resume text, matches it against curated "
        "psycholinguistic keyword lexicons for each trait, factors in "
        "achievement/quantification density, and scales the result "
        "into a 0-100 score per trait — fully offline, no external AI API."
    )


# ------------------------------------------------------------------ #
# MAIN — SINGLE CANDIDATE MODE
# ------------------------------------------------------------------ #
if mode == "Single Candidate":
    st.title("Personality Prediction System Through CV Analysis")
    st.write("Upload a candidate's CV/resume (PDF, DOCX, or TXT) to predict their personality traits from resume language.")

    uploaded = st.file_uploader("Upload CV", type=["pdf", "docx", "txt"], key="single_upload")

    if uploaded:
        with st.spinner("Analyzing resume language..."):
            result = analyze_and_display(uploaded)

        if result:
            st.success(f"Analysis complete for **{result['candidate_name']}**")
            tabs = st.tabs(["📊 Personality Profile", "🧾 Extracted Info", "💼 Role Fit", "📄 Report"])

            with tabs[0]:
                c1, c2 = st.columns([1.1, 1])
                with c1:
                    st.plotly_chart(radar_chart(result["scores"]), use_container_width=True)
                with c2:
                    st.plotly_chart(trait_bar(result["scores"]), use_container_width=True)
                st.info(trait_summary_sentence(result["scores"]))
                render_trait_cards(result["scores"], result["evidence"])

            with tabs[1]:
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Candidate (detected)**")
                    st.write(result["candidate_name"])
                    st.markdown("**Contact info (detected)**")
                    st.write(result["contact"].get("email") or "—")
                    st.write(result["contact"].get("phone") or "—")
                with col2:
                    st.markdown("**Resume length**")
                    st.write(f"{result['word_count']} words")
                    st.markdown("**Achievement/metric density**")
                    st.write(f"{result['achievement_density']:.2f} per 300 words")
                st.markdown("**Top resume keywords**")
                st.markdown(
                    " ".join(f'<span class="keyword-chip">{kw}</span>' for kw in result["top_keywords"]),
                    unsafe_allow_html=True,
                )
                with st.expander("View extracted raw text"):
                    st.text_area("Raw text", result["raw_text"], height=300, label_visibility="collapsed")

            with tabs[2]:
                st.subheader("Recommended role fit")
                for fit in result["role_fit"]:
                    st.markdown(f"**{fit['category']}** — match score {fit['match_score']:.0f}/100")
                    st.markdown(" ".join(f'<span class="role-pill">{r}</span>' for r in fit["roles"]), unsafe_allow_html=True)
                    st.progress(min(int(fit["match_score"]), 100))
                    st.markdown("")

            with tabs[3]:
                st.subheader("Downloadable report")
                pdf_bytes = build_pdf_report(result["candidate_name"], result["contact"], result)
                st.download_button(
                    "⬇️ Download PDF Report",
                    data=pdf_bytes,
                    file_name=f"{result['candidate_name'].replace(' ', '_')}_personality_report.pdf",
                    mime="application/pdf",
                )
                st.caption("A one-page recruiter-friendly summary with trait scores, role fit, and top keywords.")


# ------------------------------------------------------------------ #
# MAIN — BATCH / COMPARE MODE
# ------------------------------------------------------------------ #
else:
    st.title("Compare Candidates")
    st.write("Upload multiple CVs to rank and compare candidates side by side — useful for recruiter shortlisting.")

    uploaded_files = st.file_uploader(
        "Upload multiple CVs", type=["pdf", "docx", "txt"], accept_multiple_files=True, key="batch_upload"
    )

    if uploaded_files:
        rows = []
        results_by_name = {}
        with st.spinner(f"Analyzing {len(uploaded_files)} resumes..."):
            for f in uploaded_files:
                result = analyze_and_display(f)
                if result:
                    row = {"Candidate": result["candidate_name"]}
                    row.update({t: result["scores"].get(t, 0) for t in TRAIT_ORDER})
                    row["Top Role Fit"] = result["role_fit"][0]["category"] if result["role_fit"] else "—"
                    rows.append(row)
                    results_by_name[result["candidate_name"]] = result

        if rows:
            df = pd.DataFrame(rows).set_index("Candidate")
            st.subheader("Candidate comparison table")
            st.dataframe(
                df.style.background_gradient(cmap="Purples", subset=TRAIT_ORDER, vmin=0, vmax=100).format("{:.0f}", subset=TRAIT_ORDER),
                use_container_width=True,
            )

            csv = df.reset_index().to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Download comparison as CSV", data=csv, file_name="candidate_comparison.csv", mime="text/csv")

            st.subheader("Trait comparison")
            fig = go.Figure()
            for trait in TRAIT_ORDER:
                fig.add_trace(go.Bar(name=trait, x=df.index, y=df[trait], marker_color=ACCENT_COLORS[trait]))
            fig.update_layout(
                barmode="group",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(tickfont=dict(color="#eef0fb")),
                yaxis=dict(gridcolor="#2c315e", tickfont=dict(color="#9aa0c9"), range=[0, 105]),
                legend=dict(font=dict(color="#eef0fb")),
                height=420,
            )
            st.plotly_chart(fig, use_container_width=True)

            st.subheader("Individual profile")
            chosen = st.selectbox("View a candidate's full radar profile", list(results_by_name.keys()))
            if chosen:
                st.plotly_chart(radar_chart(results_by_name[chosen]["scores"]), use_container_width=True)
                render_trait_cards(results_by_name[chosen]["scores"], results_by_name[chosen]["evidence"])
    else:
        st.info("Upload two or more CVs to compare candidates.")
