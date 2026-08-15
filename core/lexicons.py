"""
lexicons.py
------------------------------------------------------------------
Psycholinguistic keyword lexicons used to map CV/resume language to
the Big Five (OCEAN) personality traits.

"""

# ---------------------------------------------------------------- #
# OPENNESS TO EXPERIENCE
# Curiosity, creativity, intellectual engagement, novelty-seeking
# ---------------------------------------------------------------- #
OPENNESS = {
    "creative":        (["creative", "creativity", "creatively"], 1.8),
    "innovate":        (["innovate", "innovative", "innovation", "innovating"], 1.8),
    "design":          (["design", "designed", "designing", "designer"], 1.3),
    "explore":         (["explore", "exploring", "exploration", "explored"], 1.6),
    "research":        (["research", "researched", "researching", "researcher"], 1.4),
    "novel":           (["novel", "original", "originality", "unconventional"], 1.7),
    "curious":         (["curious", "curiosity", "inquisitive"], 1.8),
    "learn":           (["learn", "learning", "self-taught", "self-learned"], 1.2),
    "artistic":        (["artistic", "art", "aesthetic", "visual storytelling"], 1.5),
    "experiment":      (["experiment", "experimented", "experimental", "prototype", "prototyping"], 1.6),
    "vision":          (["visionary", "vision", "imaginative", "imagination"], 1.7),
    "adapt":           (["adapt", "adaptable", "adaptability", "versatile", "versatility"], 1.3),
    "pioneer":         (["pioneer", "pioneering", "trailblazer", "cutting-edge", "cutting edge"], 1.7),
    "diverse":         (["diverse", "diversified", "multidisciplinary", "cross-functional"], 1.2),
    "strategy":        (["strategic", "strategy", "conceptualize", "conceptualized"], 1.3),
}

# ---------------------------------------------------------------- #
# CONSCIENTIOUSNESS
# Organization, discipline, reliability, goal-orientation
# ---------------------------------------------------------------- #
CONSCIENTIOUSNESS = {
    "organize":        (["organize", "organized", "organization", "organizing", "organizer"], 1.6),
    "detail":          (["detail-oriented", "meticulous", "thorough", "precise", "precision"], 1.8),
    "plan":            (["plan", "planned", "planning", "roadmap", "scheduled"], 1.4),
    "manage":          (["manage", "managed", "management", "managing", "manager"], 1.3),
    "achieve":         (["achieve", "achieved", "achievement", "accomplish", "accomplished"], 1.7),
    "deadline":        (["deadline", "deadlines", "on-time", "on time", "timely"], 1.5),
    "efficient":       (["efficient", "efficiency", "streamline", "streamlined", "optimize", "optimized"], 1.6),
    "discipline":      (["disciplined", "discipline", "rigorous", "diligent", "diligence"], 1.8),
    "responsible":     (["responsible", "responsibility", "accountable", "accountability", "ownership"], 1.7),
    "systematic":      (["systematic", "structured", "process-driven", "methodical", "consistent", "consistency"], 1.5),
    "quality":         (["quality assurance", "quality control", "best practices", "compliance", "standards"], 1.3),
    "goal":            (["goal-oriented", "goal-driven", "target", "targets", "objective", "objectives", "kpi", "kpis"], 1.5),
    "complete":        (["completed", "delivered", "finalized", "executed", "execution"], 1.3),
}

# ---------------------------------------------------------------- #
# EXTRAVERSION
# Sociability, assertiveness, energy, leadership visibility
# ---------------------------------------------------------------- #
EXTRAVERSION = {
    "lead":            (["lead", "led", "leader", "leadership", "leading"], 1.8),
    "present":         (["present", "presented", "presentation", "presenting", "public speaking"], 1.7),
    "collaborate":     (["collaborate", "collaborated", "collaboration", "collaborative"], 1.3),
    "team":            (["team", "teams", "teamwork", "cross-team"], 1.1),
    "communicate":     (["communicate", "communicated", "communication", "communicator"], 1.4),
    "network":         (["network", "networking", "networked", "relationship building", "client-facing"], 1.6),
    "event":           (["organized events", "hosted", "hosting", "emceed", "moderated", "moderator"], 1.7),
    "energetic":       (["energetic", "enthusiastic", "dynamic", "outgoing", "proactive"], 1.6),
    "motivate":        (["motivate", "motivated", "motivating", "inspire", "inspired", "inspiring"], 1.6),
    "negotiate":       (["negotiate", "negotiated", "negotiation", "persuade", "persuasive"], 1.5),
    "represent":       (["represented", "spokesperson", "ambassador", "liaison"], 1.5),
    "confident":       (["confident", "assertive", "outspoken", "bold"], 1.6),
}

# ---------------------------------------------------------------- #
# AGREEABLENESS
# Cooperation, empathy, support of others, community orientation
# ---------------------------------------------------------------- #
AGREEABLENESS = {
    "support":         (["support", "supported", "supportive", "supporting"], 1.5),
    "help":            (["help", "helped", "helping", "assist", "assisted", "assisting"], 1.4),
    "mentor":          (["mentor", "mentored", "mentoring", "mentorship", "coach", "coached", "coaching"], 1.8),
    "volunteer":       (["volunteer", "volunteered", "volunteering", "community service"], 1.7),
    "cooperate":       (["cooperate", "cooperative", "cooperation", "team player"], 1.6),
    "empathy":         (["empathy", "empathetic", "compassionate", "considerate"], 1.9),
    "community":       (["community", "outreach", "nonprofit", "non-profit", "charity", "social work"], 1.5),
    "listen":          (["listen", "listened", "active listening", "understanding"], 1.4),
    "care":            (["care", "caring", "nurture", "nurturing", "welfare"], 1.5),
    "friendly":        (["friendly", "approachable", "warm", "kind", "polite", "courteous"], 1.4),
    "conflict":        (["conflict resolution", "mediate", "mediation", "diplomatic", "diplomacy"], 1.6),
    "inclusive":       (["inclusive", "inclusion", "equity", "belonging"], 1.4),
}

# ---------------------------------------------------------------- #
# EMOTIONAL STABILITY  (inverse of Neuroticism)
# Composure under pressure, resilience, positive framing
# High score = calm / stable.  Low score = more stress language.
# ---------------------------------------------------------------- #
EMOTIONAL_STABILITY_POSITIVE = {
    "calm":            (["calm", "composed", "steady", "level-headed", "level headed"], 1.8),
    "resilient":       (["resilient", "resilience", "perseverance", "persevered", "persistent", "persistence"], 1.8),
    "handle_pressure": (["under pressure", "high-pressure", "tight deadlines", "fast-paced environment", "fast paced"], 1.6),
    "problem_solve":   (["problem-solving", "problem solving", "troubleshoot", "troubleshooting", "resolved"], 1.4),
    "positive":        (["positive", "optimistic", "confident", "reliable", "stable", "consistent performance"], 1.3),
    "overcome":        (["overcame", "overcome", "adapted to change", "managed change"], 1.6),
}

EMOTIONAL_STABILITY_NEGATIVE = {
    "stress":          (["stressed", "stressful", "overwhelmed", "burnout", "burned out"], 1.8),
    "struggle":        (["struggled", "struggling", "difficulty", "difficult time"], 1.5),
    "fail":            (["failed", "failure", "setback", "unable to"], 1.6),
    "anxious":         (["anxious", "anxiety", "worried", "nervous"], 1.9),
    "inconsistent":    (["inconsistent", "unreliable", "disorganized", "missed deadline", "missed deadlines"], 1.7),
}

TRAITS = {
    "Openness": OPENNESS,
    "Conscientiousness": CONSCIENTIOUSNESS,
    "Extraversion": EXTRAVERSION,
    "Agreeableness": AGREEABLENESS,
}

TRAIT_DESCRIPTIONS = {
    "Openness": "Curiosity, creativity, and openness to new ideas and experiences.",
    "Conscientiousness": "Organization, discipline, reliability, and goal-directed behavior.",
    "Extraversion": "Sociability, assertiveness, energy, and comfort in leadership/visible roles.",
    "Agreeableness": "Cooperation, empathy, and orientation toward supporting others.",
    "Emotional Stability": "Composure under pressure, resilience, and consistency (inverse of Neuroticism).",
}

TRAIT_ICONS = {
    "Openness": "🎨",
    "Conscientiousness": "🗂️",
    "Extraversion": "📣",
    "Agreeableness": "🤝",
    "Emotional Stability": "🧘",
}

# Role-fit heuristics: (trait combination) -> suggested roles
ROLE_FIT_RULES = [
    {
        "name": "Research & Development / Innovation",
        "traits": ["Openness", "Conscientiousness"],
        "roles": ["R&D Engineer", "Product Innovation", "Data Scientist", "UX Researcher"],
    },
    {
        "name": "Sales / Client-Facing / Business Development",
        "traits": ["Extraversion", "Agreeableness"],
        "roles": ["Sales Executive", "Business Development", "Customer Success", "Account Manager"],
    },
    {
        "name": "Project / Operations Management",
        "traits": ["Conscientiousness", "Emotional Stability"],
        "roles": ["Project Manager", "Operations Lead", "Program Coordinator", "QA Lead"],
    },
    {
        "name": "Leadership / People Management",
        "traits": ["Extraversion", "Conscientiousness"],
        "roles": ["Team Lead", "Engineering Manager", "Department Head"],
    },
    {
        "name": "HR / Support / Community Roles",
        "traits": ["Agreeableness", "Emotional Stability"],
        "roles": ["HR Generalist", "Customer Support Lead", "Community Manager", "Trainer/Coach"],
    },
    {
        "name": "Creative / Design / Strategy",
        "traits": ["Openness", "Extraversion"],
        "roles": ["Creative Director", "Marketing Strategist", "Brand Designer"],
    },
]

# Small, built-in stopword list (kept local so no NLTK/network download
# is required at runtime for the user).
STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "if", "then", "so", "of", "in", "on",
    "at", "to", "for", "with", "by", "from", "as", "is", "are", "was", "were",
    "be", "been", "being", "this", "that", "these", "those", "i", "you", "he",
    "she", "it", "we", "they", "my", "your", "his", "her", "its", "our", "their",
    "me", "him", "them", "us", "will", "would", "can", "could", "should", "may",
    "might", "must", "not", "no", "do", "does", "did", "have", "has", "had",
    "such", "than", "into", "over", "under", "up", "down", "out", "about",
    "who", "whom", "which", "what", "when", "where", "how", "all", "any",
    "each", "few", "more", "most", "other", "some", "own", "same", "just",
    "also", "very", "here", "there",
}
