"""
analyzer.py
------------------------------------------------------------------
Core NLP + scoring engine.

Pipeline
--------
1. Clean & tokenize CV text.
2. Score each Big Five trait via weighted lexicon matching
   (multi-word phrases matched first, then single tokens).
3. Add secondary signals:
     - Achievement/quantification density (numbers, %, metrics)
       -> nudges Conscientiousness & Openness.
     - Sentence-length / structure variety -> nudges Openness.
     - Emotional-stability = f(positive stress-coping language,
       negative stress language).
4. Squash raw evidence counts into a 0-100 scale with a smooth
   logistic curve so scores don't just linearly explode with CV
   length, and normalize by document length so short and long CVs
   are comparable.
5. Return per-trait scores + the exact evidence words found (for
   explainability) + top TF-IDF-style keywords + a role-fit
   suggestion.
"""

import math
import re
from collections import Counter

from sklearn.feature_extraction.text import TfidfVectorizer

from .lexicons import (
    TRAITS,
    EMOTIONAL_STABILITY_POSITIVE,
    EMOTIONAL_STABILITY_NEGATIVE,
    ROLE_FIT_RULES,
    STOPWORDS,
)

NUMBER_PATTERN = re.compile(r"\b\d+(\.\d+)?%?\b")


def _clean(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9%.\-\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _tokenize(text: str):
    return re.findall(r"[a-z][a-z\-]*", text)


def _match_lexicon(clean_text: str, lexicon: dict):
    """
    For each canonical concept in a lexicon, search for any of its
    surface forms as whole-word / whole-phrase matches. Returns:
      raw_score (float), evidence (dict: concept -> [matched words])
    """
    raw_score = 0.0
    evidence = {}
    for concept, (forms, weight) in lexicon.items():
        hits = []
        for form in forms:
            pattern = r"\b" + re.escape(form) + r"\b"
            count = len(re.findall(pattern, clean_text))
            if count:
                hits.append((form, count))
                raw_score += weight * count
        if hits:
            evidence[concept] = hits
    return raw_score, evidence


def _logistic_scale(raw_score: float, word_count: int, decay: float = 9.0) -> float:
    """
    Normalizes raw weighted-hit-count by document length (per 300
    words, a typical one-page resume section), then maps to 0-100
    via a saturating exponential curve: 0 evidence -> 0, moderate
    keyword density (~6-10 per 300 words) -> ~50-65, very
    keyword-dense resumes approach (but rarely fully reach) 100.
    This avoids the "everything saturates to 100" problem of a
    steep logistic while still rewarding richer language.
    """
    if word_count == 0:
        return 0.0
    # Floor the denominator so very short CVs/snippets aren't wildly
    # extrapolated up to a full "per 300 words" density from just a
    # handful of matches (e.g. 2 hits in 60 words != 10 hits in 300).
    effective_words = max(word_count, 150)
    density = raw_score / (effective_words / 300.0)
    score = 100 * (1 - math.exp(-density / decay))
    return round(score, 1)


def _count_numbers(clean_text: str) -> int:
    return len(NUMBER_PATTERN.findall(clean_text))


def _achievement_density(clean_text: str, word_count: int) -> float:
    """Per-300-word density, used only for the display metric (not
    for raw score contribution, which uses the unnormalized count -
    see analyze_cv)."""
    if word_count == 0:
        return 0.0
    return (_count_numbers(clean_text) / word_count) * 300


def analyze_cv(raw_text: str) -> dict:
    clean_text = _clean(raw_text)
    tokens = _tokenize(clean_text)
    word_count = max(len(tokens), 1)

    trait_scores = {}
    trait_evidence = {}

    for trait_name, lexicon in TRAITS.items():
        raw, evidence = _match_lexicon(clean_text, lexicon)
        trait_evidence[trait_name] = evidence
        trait_scores[trait_name] = raw  # temp: raw, scaled below

    # Achievement/quantification bonus nudges Conscientiousness + Openness.
    # Uses the raw (unnormalized) number count so it combines correctly
    # with the other raw lexicon-hit sums before the single length
    # normalization step in _logistic_scale.
    achievement_count = _count_numbers(clean_text)
    achievement = _achievement_density(clean_text, word_count)  # for display only
    trait_scores["Conscientiousness"] += achievement_count * 0.5
    trait_scores["Openness"] += achievement_count * 0.2

    # Scale all four core traits
    for trait_name in TRAITS:
        trait_scores[trait_name] = _logistic_scale(trait_scores[trait_name], word_count)

    # Emotional stability: positive coping language minus stress language
    pos_raw, pos_evidence = _match_lexicon(clean_text, EMOTIONAL_STABILITY_POSITIVE)
    neg_raw, neg_evidence = _match_lexicon(clean_text, EMOTIONAL_STABILITY_NEGATIVE)
    net = pos_raw - neg_raw * 1.3  # negative language weighted slightly heavier
    trait_scores["Emotional Stability"] = _emotional_stability_scale(net, word_count)
    trait_evidence["Emotional Stability"] = {**pos_evidence, **{f"(stress) {k}": v for k, v in neg_evidence.items()}}

    top_keywords = _extract_top_keywords(clean_text)

    role_fit = _suggest_roles(trait_scores)

    return {
        "scores": trait_scores,
        "evidence": trait_evidence,
        "word_count": word_count,
        "top_keywords": top_keywords,
        "role_fit": role_fit,
        "achievement_density": round(achievement, 2),
    }


def _emotional_stability_scale(net_raw: float, word_count: int) -> float:
    """
    Emotional stability starts from a neutral baseline (50 - most
    resumes are written in a composed register with little explicit
    emotional language either way) and shifts up with resilience/
    composure language or down with stress language, saturating
    smoothly at the extremes.
    """
    if word_count == 0:
        return 50.0
    effective_words = max(word_count, 150)
    density = net_raw / (effective_words / 300.0)  # can be negative
    shift = 45 * (1 - math.exp(-abs(density) / 6.0))
    score = 50 + shift if density >= 0 else 50 - shift
    return round(max(0.0, min(100.0, score)), 1)


def _extract_top_keywords(clean_text: str, top_n: int = 12):
    """TF-IDF-lite keyword surfacing over the resume's own sentences,
    used to show the user WHY the model saw what it saw, independent
    of the fixed trait lexicons."""
    sentences = [s for s in re.split(r"[.\n]", clean_text) if len(s.split()) > 2]
    if len(sentences) < 2:
        # Not enough structure for TF-IDF; fall back to simple frequency
        tokens = [t for t in _tokenize(clean_text) if t not in STOPWORDS and len(t) > 3]
        return [w for w, _ in Counter(tokens).most_common(top_n)]

    try:
        vectorizer = TfidfVectorizer(stop_words=list(STOPWORDS), max_features=200, ngram_range=(1, 2))
        matrix = vectorizer.fit_transform(sentences)
        scores = matrix.sum(axis=0).A1
        terms = vectorizer.get_feature_names_out()
        ranked = sorted(zip(terms, scores), key=lambda x: x[1], reverse=True)
        return [term for term, _ in ranked[:top_n]]
    except Exception:
        tokens = [t for t in _tokenize(clean_text) if t not in STOPWORDS and len(t) > 3]
        return [w for w, _ in Counter(tokens).most_common(top_n)]


def _suggest_roles(trait_scores: dict, top_n: int = 2):
    """Score each role-fit rule by the average of its associated
    trait scores, return the best matches."""
    ranked = []
    for rule in ROLE_FIT_RULES:
        avg = sum(trait_scores.get(t, 0) for t in rule["traits"]) / len(rule["traits"])
        ranked.append((avg, rule))
    ranked.sort(key=lambda x: x[0], reverse=True)
    return [
        {"category": rule["name"], "match_score": round(avg, 1), "roles": rule["roles"]}
        for avg, rule in ranked[:top_n]
    ]


def dominant_trait(scores: dict) -> str:
    return max(scores, key=scores.get)


def trait_summary_sentence(scores: dict) -> str:
    dom = dominant_trait(scores)
    sorted_traits = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top_two = ", ".join(f"{t}" for t, _ in sorted_traits[:2])
    return f"This candidate's resume most strongly reflects **{top_two}**, suggesting a profile suited to roles that reward those strengths."
