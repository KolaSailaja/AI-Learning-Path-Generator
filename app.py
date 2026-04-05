import streamlit as st


def _phase_name(week: int, total_weeks: int) -> str:
    """Label the learning phase for this week (foundation → core → mastery)."""
    if total_weeks == 1:
        return "Intensive sprint"
    third = max(1, total_weeks // 3)
    if week <= third:
        return "Foundation"
    if week <= 2 * third:
        return "Core skills"
    return "Mastery & projects"


def _detect_profile(topic: str) -> str:
    """Pick a learning 'strand' so weekly themes match the subject area."""
    t = topic.lower()
    if any(k in t for k in ("python", "javascript", "java", "code", "programming", "software", "react", "web dev")):
        return "tech"
    if any(k in t for k in ("data", "sql", "analytics", "excel", "statistics", "machine learning", "ml ")):
        return "data"
    if any(k in t for k in ("design", "ui", "ux", "figma", "draw", "music", "photo", "video")):
        return "creative"
    if any(k in t for k in ("spanish", "french", "language", "english", "speaking", "grammar")):
        return "language"
    return "general"


# Ordered themes per profile — weeks map across this list based on duration
_THEMES: dict[str, list[str]] = {
    "general": [
        "Orientation & mindset",
        "Core vocabulary & concepts",
        "Skills in isolation",
        "Combining skills",
        "Real-world application",
        "Review, gaps & stretch",
        "Portfolio & next steps",
    ],
    "tech": [
        "Setup, toolchain & first program",
        "Syntax, types & control flow",
        "Functions, modules & debugging",
        "Data structures & APIs",
        "Testing, tooling & style",
        "Small app or feature slice",
        "Polish, docs & deployment basics",
    ],
    "data": [
        "Questions, data types & ethics",
        "Loading, cleaning & exploring",
        "Visualization & communication",
        "Models or metrics (level-appropriate)",
        "Validation & iteration",
        "Mini analysis or dashboard",
        "Storytelling & reproducibility",
    ],
    "creative": [
        "Foundations & references",
        "Core techniques",
        "Practice loops & critique",
        "Style, constraints & variation",
        "Combining elements",
        "Mini piece or study",
        "Showcase & feedback",
    ],
    "language": [
        "Sounds, script & core phrases",
        "Vocabulary themes",
        "Grammar patterns",
        "Listening & reading",
        "Speaking & writing",
        "Immersion habits",
        "Review & real situations",
    ],
}


def _theme_for_week(week: int, total_weeks: int, profile: str) -> str:
    """Map this week to one theme label, spread across the topic arc."""
    themes = _THEMES.get(profile, _THEMES["general"])
    if total_weeks == 1:
        return themes[len(themes) // 2]
    # Evenly spread week indices across the theme list
    idx = (week - 1) * (len(themes) - 1) // (total_weeks - 1)
    return themes[idx]


def _level_tone(level: str) -> dict[str, str]:
    """Short phrases that shift difficulty by level."""
    if level == "Beginner":
        return {
            "obj": "Build confidence with",
            "practice": "short, guided",
            "project": "tiny, end-to-end",
            "res": "beginner-friendly",
        }
    if level == "Intermediate":
        return {
            "obj": "Strengthen and connect",
            "practice": "focused, semi-independent",
            "project": "small but realistic",
            "res": "official docs plus one deep resource",
        }
    return {
        "obj": "Master nuances of",
        "practice": "open-ended, time-boxed",
        "project": "non-trivial and opinionated",
        "res": "primary sources, papers, or source code",
    }


def _build_week_content(
    topic: str,
    level: str,
    week: int,
    total_weeks: int,
    phase: str,
    theme: str,
    tone: dict[str, str],
) -> dict:
    """Fill objectives, practice, projects, and resources for one week."""
    t = topic.strip() or "your topic"
    w, n = week, total_weeks

    if "Foundation" in phase or phase == "Intensive sprint":
        opener = f"{tone['obj']} foundations of **{theme}** in the context of **{t}**."
    elif "Core" in phase:
        opener = f"{tone['obj']} **{theme}** by connecting ideas you already started with **{t}**."
    else:
        opener = f"{tone['obj']} **{theme}** through integration, critique, and real use of **{t}**."

    learning_objectives = [
        opener,
        f"Week {w} checkpoint: summarize what “done” looks like for this theme in one paragraph.",
        f"Tie this week to the **{phase}** phase: name one risk and one strategy to stay on track.",
    ]

    practice_tasks = [
        f"Daily {tone['practice']} blocks (25–50 min): focus only on skills that serve “{theme}”.",
        f"Log 3 short entries: win, friction, and one term to look up for **{t}**.",
        f"Repeat the toughest task once more on the last day; note what got easier.",
    ]

    mini_projects = [
        f"**Mini project:** a {tone['project']} deliverable that uses **{t}** and reflects “{theme}”.",
        f"Before you start: write a 3-bullet plan; after: write a 3-bullet retrospective.",
    ]
    if n == 1:
        mini_projects = [
            f"**Mini project:** in one day, ship one small artifact that touches setup, practice, and reflection for **{t}**.",
        ]

    recommended_resources = [
        f"Search: `{t} {theme.split()[0].lower()} tutorial {level.lower()}` — pick one source and skim the outline first.",
        f"**Community:** a forum or subreddit related to **{t}** — read solved questions, don’t post yet unless stuck.",
        f"**Reference bookmark:** one official or widely trusted glossary or cheat sheet for **{t}**.",
    ]
    if level == "Advanced":
        recommended_resources.append(
            f"**Go deeper:** one paper, RFC, repo issue thread, or conference talk linked to **{t}** this week."
        )

    return {
        "week": w,
        "phase": phase,
        "theme": theme,
        "learning_objectives": learning_objectives,
        "practice_tasks": practice_tasks,
        "mini_projects": mini_projects,
        "recommended_resources": recommended_resources,
    }


def generate_learning_plan(topic: str, level: str, duration: int) -> dict:
    """
    Build a full learning plan: topic split across weeks with objectives,
    practice, mini projects, and resources. Each week differs by topic profile,
    level, week index, and duration.
    """
    duration = max(1, int(duration))
    profile = _detect_profile(topic)
    tone = _level_tone(level)

    weeks_out: list[dict] = []
    for w in range(1, duration + 1):
        phase = _phase_name(w, duration)
        theme = _theme_for_week(w, duration, profile)
        weeks_out.append(
            _build_week_content(topic, level, w, duration, phase, theme, tone)
        )

    return {
        "topic": topic.strip() or "(your topic)",
        "level": level,
        "duration_weeks": duration,
        "profile": profile,
        "weeks": weeks_out,
    }


def plan_to_markdown(plan: dict) -> str:
    """Format the full plan as clean markdown for display and download."""
    t = plan["topic"]
    profile = plan.get("profile", "general")
    lines = [
        f"# 📚 Learning plan: {t}",
        "",
        f"- **Level:** {plan['level']}",
        f"- **Duration:** {plan['duration_weeks']} week(s)",
        f"- **Topic arc:** `{profile}` — weekly themes are spread across your timeline automatically.",
        "",
        "---",
        "",
    ]

    for block in plan["weeks"]:
        lines.append(f"## 📅 Week {block['week']} — {block['phase']}")
        lines.append(f"*Theme:* **{block['theme']}**")
        lines.append("")
        lines.append("### 🎯 Learning objectives")
        for item in block["learning_objectives"]:
            lines.append(f"- {item}")
        lines.append("")
        lines.append("### ✏️ Practice tasks")
        for item in block["practice_tasks"]:
            lines.append(f"- {item}")
        lines.append("")
        lines.append("### 🛠️ Mini projects")
        for item in block["mini_projects"]:
            lines.append(f"- {item}")
        lines.append("")
        lines.append("### 📖 Recommended resources")
        for item in block["recommended_resources"]:
            lines.append(f"- {item}")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## 🎉 Closing note")
    lines.append("")
    lines.append(
        f"Adjust weekly load to your schedule. Revisit **{t}** regularly and tweak this plan as you learn what works."
    )
    return "\n".join(lines)


def plan_to_plain_txt(markdown_text: str) -> str:
    """Strip markdown emphasis for a simple .txt download."""
    return markdown_text.replace("**", "").replace("`", "")


# --- App ---

st.set_page_config(page_title="Learning Path Generator", page_icon="📚")

st.title("📚 Learning Path Generator")
st.markdown(
    "Build a **week-by-week** roadmap for any topic. Set your choices in the sidebar, then generate."
)

with st.sidebar:
    st.header("⚙️ Your plan")
    topic = st.text_input("Topic", placeholder="e.g. Python, Data analysis, Guitar")
    level = st.selectbox("Level", ["Beginner", "Intermediate", "Advanced"])
    duration = st.number_input("Duration (weeks)", min_value=1, max_value=52, step=1)
    generate = st.button("✨ Generate roadmap", type="primary")

if generate:
    with st.spinner("Generating your roadmap…"):
        plan = generate_learning_plan(topic, level, int(duration))
        md = plan_to_markdown(plan)
        st.session_state["plan"] = plan
        st.session_state["roadmap_txt"] = plan_to_plain_txt(md)
        st.session_state["saved_topic"] = plan["topic"]
        st.session_state["saved_level"] = plan["level"]
        st.session_state["saved_weeks"] = plan["duration_weeks"]
    st.success("Roadmap ready! Scroll down to view each week.")

plan = st.session_state.get("plan")
txt_data = st.session_state.get("roadmap_txt")

if plan and txt_data:
    t_show = st.session_state.get("saved_topic", "Your topic")
    lvl_show = st.session_state.get("saved_level", "")
    dur_show = st.session_state.get("saved_weeks", 0)
    st.markdown(f"# Learning plan: {t_show}")
    st.markdown(f"- **Level:** {lvl_show}")
    st.markdown(f"- **Duration:** {dur_show} week(s)")
    st.caption(f"Topic arc profile: **{plan.get('profile', 'general')}** — themes adjust automatically.")
    st.markdown("---")
    st.subheader("📆 Weekly breakdown")

    for block in plan["weeks"]:
        title = f"Week {block['week']} — {block['phase']}"
        with st.expander(f"📌 {title}: {block['theme']}", expanded=(block["week"] == 1)):
            st.markdown(f"**Theme:** {block['theme']}")
            st.markdown("##### 🎯 Learning objectives")
            for line in block["learning_objectives"]:
                st.markdown(f"- {line}")
            st.markdown("##### ✏️ Practice tasks")
            for line in block["practice_tasks"]:
                st.markdown(f"- {line}")
            st.markdown("##### 🛠️ Mini projects")
            for line in block["mini_projects"]:
                st.markdown(f"- {line}")
            st.markdown("##### 📖 Recommended resources")
            for line in block["recommended_resources"]:
                st.markdown(f"- {line}")

    st.markdown("---")
    st.download_button(
        label="⬇️ Download roadmap as .txt",
        data=txt_data,
        file_name="learning_roadmap.txt",
        mime="text/plain",
    )
elif not generate:
    st.info("👈 Enter a topic and click **Generate roadmap** in the sidebar.")
