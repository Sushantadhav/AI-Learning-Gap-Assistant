import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv
import datetime
import csv

# -----------------------------
#  LOAD API KEY
# -----------------------------

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("Groq API key not found. Add it to your .env file as GROQ_API_KEY")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)


# -----------------------------
#  SYSTEM PROMPT
# -----------------------------

SYSTEM_PROMPT = """
You are an AI-powered Learning Gap Doubt-Solving Assistant for students.

Always answer using this format:

1) Concept Explanation — simple, clear, student-friendly
2) Real-World Example — short & relatable
3) Key-Point Summary — 3 to 5 bullet points
4) Common Misconceptions — clarify mistakes students usually make
5) Quick Practice Questions — 2 conceptual questions (no answers)
6) Follow-up Support — ask if they want simpler explanation or more examples

Focus on conceptual clarity and learning improvement.
Avoid direct exam or cheating help.
"""


# -----------------------------
#  SESSION MEMORY
# -----------------------------

if "chat" not in st.session_state:
    st.session_state.chat = []

if "session_log" not in st.session_state:
    st.session_state.session_log = []


# -----------------------------
#  AI CALL FUNCTION
# -----------------------------

def ask_ai(question, subject, depth, style):

    user_prompt = f"""
Subject: {subject}
Learning Depth: {depth}
Explanation Style: {style}

Student Question:
{question}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]
    )

    answer = response.choices[0].message.content

    st.session_state.chat.append(("Student", question))
    st.session_state.chat.append(("AI Assistant", answer))

    st.session_state.session_log.append({
        "timestamp": datetime.datetime.now(),
        "subject": subject,
        "depth": depth,
        "style": style,
        "question": question,
        "response": answer
    })

    return answer


# -----------------------------
#  EXPORT CSV (optional)
# -----------------------------

def export_csv():
    filename = "learning_session_log.csv"

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(["Timestamp","Subject","Depth","Style","Question","Response"])

        for row in st.session_state.session_log:
            writer.writerow([
                row["timestamp"],
                row["subject"],
                row["depth"],
                row["style"],
                row["question"],
                row["response"]
            ])

    return filename


# -----------------------------
#  STREAMLIT UI
# -----------------------------

st.title("AI Learning Gap Assistant (Groq + Streamlit)")
st.caption("Concept-focused learning support for students.")

st.divider()

# Selection Controls

subject = st.selectbox(
    "Select Subject",
    ["General","Math","Science","Computer Science","Economics"]
)

depth = st.selectbox(
    "Learning Depth",
    ["Basic","Intermediate","Detailed"]
)

style = st.selectbox(
    "Explanation Style",
    ["Simple","Step-by-Step","Concept Breakdown"]
)


# Question input

question = st.text_area("Enter your question")

if st.button("Ask AI"):

    if question.strip() == "":
        st.warning("Enter a question first.")
    else:
        ask_ai(question, subject, depth, style)


# -----------------------------
#  CHAT DISPLAY
# -----------------------------

st.divider()
st.subheader("Conversation History")

for speaker, text in st.session_state.chat:
    if speaker == "Student":
        st.markdown(f"**🧑 Student:** {text}")
    else:
        st.markdown(f"**🤖 AI Assistant:**\n\n{text}")


# -----------------------------
#  EXPORT OPTION
# -----------------------------

st.divider()
st.subheader("Export Session Log")

if st.button("Download CSV"):
    file = export_csv()
    st.success(f"Saved: {file}")
