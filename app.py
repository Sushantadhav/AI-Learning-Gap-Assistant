import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv
import datetime
import json
import io

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


# ---------------------------------
#  APP & API SETUP
# ---------------------------------
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("Groq API key missing. Add it in .env or Streamlit Secrets.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

st.set_page_config(
    page_title="AI Learning Gap Assistant",
    page_icon="🎓",
    layout="centered"
)

st.markdown("""
<style>
html, body, [class*="css"] {
    background:#0b0e17 !important;
    color:#e8e8ea !important;
}
section.main > div {max-width: 950px}
.stChatMessage, .stMarkdown, .stTextInput, .stSelectbox {
    background:#111729 !important;
    border-radius:16px !important;
    padding:12px !important;
    border:1px solid #1c2545;
}
.stButton>button {
    background:#3d5afe !important;
    color:#ffffff !important;
    border-radius:12px;
    border:0px;
}
.stButton>button:hover {background:#5e73ff !important;}
</style>
""", unsafe_allow_html=True)


# ---------------------------------
#  LOCAL SESSION STORAGE
# ---------------------------------
DATA_FILE = "student_sessions.json"

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

def load_sessions():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_session(entry):
    data = load_sessions()
    data.append(entry)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


# ---------------------------------
#  SUBJECT & BLOOM PRESETS
# ---------------------------------
SUBJECT_PRESETS = {
    "General": "Explain simply using relatable daily-life examples.",
    "Math": "Explain step-by-step with conceptual breakdown.",
    "Science": "Explain like a real-world process with analogies.",
    "Computer Science": "Explain concept first, then small example.",
    "Economics": "Explain with real-life decision-making scenarios."
}

BLOOM_GUIDE = {
    "Remember": "Recall, define, identify basic concepts.",
    "Understand": "Explain meaning, interpret ideas clearly.",
    "Apply": "Use concepts in real-world or practical examples.",
    "Analyze": "Compare, reason, break down relationships."
}

SYSTEM_PROMPT = """
You are an AI-Powered Learning Gap Assistant.

Focus on conceptual clarity and understanding.
Avoid cheating or direct exam-type solutions.

Always respond in this structure:

1) Concept Explanation
2) Real-World Example
3) Key Points Summary (3–5 bullets)
4) Common Misconceptions
5) Quick Practice Questions (no answers)
6) Ask if student wants simpler explanation or more examples
"""


# ---------------------------------
#  SESSION STATE
# ---------------------------------
for k, v in {
    "chat_history": [],
    "meta_log": [],
    "confidence_log": [],
    "last_answer": None,
    "session_topic": "",
    "session_active": True,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ---------------------------------
#  AI RESPONSE ENGINE
# ---------------------------------
def generate_response(question, subject, bloom_level, style, mode="primary"):

    refinement_map = {
        "simpler": "Explain this again in simpler scaffolded form.",
        "more_examples": "Provide more real-world examples and analogies."
    }

    refinement_text = refinement_map.get(mode, "")

    user_prompt = f"""
Session Topic: {st.session_state.session_topic}

Subject: {subject}
Bloom Learning Level: {bloom_level}
Explanation Style: {style}

Subject Guidance:
{SUBJECT_PRESETS.get(subject, "")}

Bloom Style:
{BLOOM_GUIDE.get(bloom_level, "")}

Refinement Mode:
{refinement_text}

Student Question:
{question}
"""

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    for speaker, msg in st.session_state.chat_history:
        messages.append({
            "role": "user" if speaker == "Student" else "assistant",
            "content": msg
        })

    messages.append({"role": "user", "content": user_prompt})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )

    answer = response.choices[0].message.content

    # Response label
    if mode == "primary":
        tag = "(v1 — Main Explanation)"
    elif mode == "simpler":
        tag = "(v2 — Simpler Explanation)"
    else:
        tag = "(v2 — More Real-World Examples)"

    # --------------------------
    # IMPORTANT FIX:
    # Only add Student message for PRIMARY question
    # --------------------------
    if mode == "primary":
        st.session_state.chat_history.append(("Student", question))

    # Always add AI reply
    st.session_state.chat_history.append(("AI Assistant", f"{tag}\n\n{answer}"))
    st.session_state.last_answer = answer

    # --------------------------
    # LOG — PRIMARY ENTRY
    # --------------------------
    if mode == "primary":

        entry = {
            "timestamp": str(datetime.datetime.now()),
            "topic": st.session_state.session_topic,
            "subject": subject,
            "bloom_level": bloom_level,
            "style": style,
            "question": question,
            "response": answer,
            "refinement_count": 0,
            "refinements": []
        }

        st.session_state.meta_log.append(entry)
        save_session(entry)

    # --------------------------
    # LOG — REFINEMENTS
    # --------------------------
    else:

        if st.session_state.meta_log:

            st.session_state.meta_log[-1]["refinement_count"] += 1

            st.session_state.meta_log[-1]["refinements"].append({
                "timestamp": str(datetime.datetime.now()),
                "mode": mode,
                "response": answer
            })

    return answer


# ---------------------------------
#  REVISION PRIORITY
# ---------------------------------
def get_revision_priority(ref_count, conf_trend):

    if ref_count >= 2 or "Low" in conf_trend:
        return "HIGH ⚠ — Needs revision"

    if ref_count == 1 or "Medium" in conf_trend:
        return "MEDIUM — Review recommended"

    return "LOW — Concept understood"


# ---------------------------------
#  SUMMARY GENERATOR
# ---------------------------------
def generate_summary():

    if not st.session_state.meta_log:
        return "No questions asked yet."

    conf_trend = " → ".join(st.session_state.confidence_log) or "No feedback submitted"

    text = f"""
AI Learning Session Summary

Session Topic: {st.session_state.session_topic}
Date: {datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}

Total Questions: {len(st.session_state.meta_log)}
Confidence Trend: {conf_trend}
"""

    text += "\n\nQuestions & Learning Attempts:\n"

    for entry in st.session_state.meta_log:

        priority = get_revision_priority(
            entry["refinement_count"],
            st.session_state.confidence_log
        )

        text += f"""
• Question: {entry['question']}
  Subject: {entry['subject']}
  Bloom Level: {entry['bloom_level']}

  Revision Priority: {priority}

  Answer Version 1 (Main Explanation):
  {entry['response']}
"""

        for i, ref in enumerate(entry["refinements"], start=2):
            label = "Simpler Explanation" if ref["mode"] == "simpler" else "More Examples"

            text += f"""
  Answer Version {i} — {label}:
  {ref['response']}
"""

    text += """
Reflection Notes:
• Revise HIGH-priority topics first
• Use simpler mode when confidence is low
• Use examples mode when concepts feel abstract
• Attempt practice questions after revision
"""

    return text


# ---------------------------------
#  PDF EXPORT
# ---------------------------------
def export_pdf_buffer():

    buffer = io.BytesIO()

    filename = (
        f"Session_{st.session_state.session_topic or 'Learning'}_"
        f"{datetime.datetime.now().strftime('%d-%m-%Y_%H%M')}.pdf"
    )

    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    body = styles["BodyText"]

    story = []

    for line in generate_summary().split("\n"):
        if line.strip() == "":
            story.append(Spacer(1, 8))
        else:
            story.append(Paragraph(line, body))

    doc.build(story)

    buffer.seek(0)
    return buffer, filename


def section_header(title):
    st.markdown(
        f"<h4 style='margin-top:18px; margin-bottom:6px'>{title}</h4>",
        unsafe_allow_html=True
    )


# ---------------------------------
#  HEADER
# ---------------------------------
st.title("AI Learning Gap Assistant")
st.caption("Bloom-aware conceptual learning • Refinement support • Reflective analytics")
st.markdown("---")


# ---------------------------------
#  SESSION CONTEXT
# ---------------------------------
section_header("Session Context")

c1, c2 = st.columns([3, 1])

with c1:
    st.session_state.session_topic = st.text_input(
        "Session Topic (optional)",
        value=st.session_state.session_topic,
        placeholder="e.g., Fractions, Loops, Demand Elasticity"
    )

with c2:

    if st.button("Start New Session", key="reset_session"):
        st.session_state.chat_history = []
        st.session_state.meta_log = []
        st.session_state.confidence_log = []
        st.session_state.last_answer = None
        st.session_state.session_active = True
        st.success("Session cleared — start fresh.")

    if st.button("Exit Session", key="exit_session"):
        st.session_state.session_active = False
        st.success("Session ended — download your report below.")


# ---------------------------------
#  LEARNING PREFERENCE
# ---------------------------------
section_header("Learning Preference")

p1, p2 = st.columns(2)

with p1:
    subject = st.selectbox(
        "Subject",
        ["General", "Math", "Science", "Computer Science", "Economics"]
    )

    bloom_level = st.selectbox(
        "Bloom Learning Level",
        ["Remember", "Understand", "Apply", "Analyze"]
    )

with p2:
    style = st.selectbox(
        "Explanation Style",
        ["Simple", "Step-by-Step", "Concept Breakdown"]
    )


# ---------------------------------
#  QUESTION INPUT
# ---------------------------------
if st.session_state.session_active:
    question = st.chat_input("Ask your question...")
else:
    question = None

if question:
    generate_response(
        question=question,
        subject=subject,
        bloom_level=bloom_level,
        style=style,
        mode="primary"
    )


# ---------------------------------
#  CHAT VIEW
# ---------------------------------
st.divider()
section_header("Conversation")

for speaker, msg in st.session_state.chat_history:
    with st.chat_message("user" if speaker == "Student" else "assistant"):
        st.markdown(msg)


# ---------------------------------
#  CONFIDENCE FEEDBACK
# ---------------------------------
if st.session_state.last_answer and st.session_state.session_active:

    section_header("Confidence Check")

    c1, c2, c3 = st.columns(3)

    if c1.button("👍 High Confidence", key="conf_high"):
        st.session_state.confidence_log.append("High")
        st.success("Great — move forward!")

    if c2.button("⚠ Medium Confidence", key="conf_mid"):
        st.session_state.confidence_log.append("Medium")
        st.info("Consider revising once.")

    if c3.button("❌ Low Confidence", key="conf_low"):
        st.session_state.confidence_log.append("Low")
        st.warning("Try simpler or example-based explanation.")


# ---------------------------------
#  FOLLOW-UP LEARNING SUPPORT
# ---------------------------------
if st.session_state.session_active and st.session_state.last_answer:

    section_header("Follow-Up Learning Support")

    f1, f2 = st.columns(2)

    with f1:
        if st.button("🧩 Explain in Simpler Words", key="simpler_explain"):
            generate_response(
                st.session_state.last_answer,
                subject, bloom_level, style, "simpler"
            )

    with f2:
        if st.button("📌 Give More Real-World Examples", key="more_examples"):
            generate_response(
                st.session_state.last_answer,
                subject, bloom_level, style, "more_examples"
            )


# ---------------------------------
#  ANALYTICS DASHBOARD
# ---------------------------------
if st.session_state.meta_log:

    st.divider()
    section_header("Learning Analytics Dashboard")

    total_questions = len(st.session_state.meta_log)
    total_refinements = sum(q["refinement_count"] for q in st.session_state.meta_log)

    avg_refinements = (
        round(total_refinements / total_questions, 2)
        if total_questions else 0
    )

    st.write(f"**Total Questions:** {total_questions}")
    st.write(f"**Total Refinements:** {total_refinements}")
    st.write(f"**Average Refinements per Question:** {avg_refinements}")

    bloom_counts = {}
    for q in st.session_state.meta_log:
        b = q["bloom_level"]
        bloom_counts[b] = bloom_counts.get(b, 0) + 1

    st.write("**Bloom Learning Distribution:**")
    for b, c in bloom_counts.items():
        st.write(f"- {b}: {c}")

    if st.session_state.confidence_log:
        st.write("**Confidence Trend:**", " → ".join(st.session_state.confidence_log))


# ---------------------------------
#  SUMMARY + DOWNLOADS
# ---------------------------------
st.divider()
section_header("Reflection-Based Learning Summary")

summary_text = generate_summary()
st.text_area("Summary Preview", summary_text, height=240)

if st.session_state.meta_log:

    txt_filename = (
        f"Session_{st.session_state.session_topic or 'Learning'}_"
        f"{datetime.datetime.now().strftime('%d-%m-%Y_%H%M')}.txt"
    )

    st.download_button(
        "Download as TXT",
        data=summary_text,
        file_name=txt_filename
    )

    pdf_buffer, pdf_filename = export_pdf_buffer()

    st.download_button(
        "Download as PDF",
        data=pdf_buffer,
        file_name=pdf_filename,
        mime="application/pdf"
    )

    st.download_button(
        "Download Session Log (JSON)",
        data=json.dumps(st.session_state.meta_log, indent=4),
        file_name="session_log.json"
    )

else:
    st.info("Ask at least one question to generate a learning summary.")
