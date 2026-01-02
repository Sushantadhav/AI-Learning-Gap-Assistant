# 🧠 AI Learning Gap Assistant

### Bloom-Aware Conceptual Tutor with Reflective Analytics & Learning Refinement

An AI-powered conceptual learning assistant that helps students bridge learning gaps through:

* Bloom Learning Levels
* Progressive refinement explanations
* Confidence-based reflection
* Revision-priority insights
* Structured learning summaries
* Lightweight learning analytics dashboard

Instead of only *answering questions*, the assistant supports:

✔ understanding
✔ reflection
✔ progressive clarity
✔ learning reinforcement

This project aligns with **SDG-4 — Quality Education** by enabling reflective, feedback-driven learning.

---

## 📌 Project Overview

Traditional AI chat responses provide answers — but they do not:

✘ assess learning depth
✘ support cognitive learning levels
✘ provide refinement-based explanations
✘ capture confidence signals
✘ identify weak topics

This system shifts AI from:

> “Answer provider” → “Learning facilitator”

by encouraging:

* conceptual clarity
* repeated scaffolding
* reflective thinking
* insight-driven revision

---

# 🧩 Visual Learning Flow

### **How a Learning Session Works**

```mermaid
flowchart TD

A[Student Asks Question] --> B[AI Generates Main Explanation (v1)]
B --> C{Student Feedback?}

C -->|Needs Simpler Form| D[Refinement Mode — Simpler Explanation (v2)]
C -->|Needs More Examples| E[Refinement Mode — Example-Based Explanation (v2)]
C -->|Understood| F[Confidence Recorded]

D --> G[Confidence Check]
E --> G[Confidence Check]

G --> H[Confidence Trend Logged]
H --> I[Revision Priority Evaluated]

I --> J[Learning Analytics Dashboard]
J --> K[Reflection-Based Learning Summary Export]
```

The system treats learning as a **process**, not a single response.

---

# 🎚 Bloom Learning Level Support

Learner selects cognitive depth:

| Level      | Meaning                | Focus                   |
| ---------- | ---------------------- | ----------------------- |
| Remember   | Recall / definition    | Basic concepts          |
| Understand | Concept clarity        | Meaning & explanation   |
| Apply      | Real-world use         | Context & examples      |
| Analyze    | Reasoning & comparison | Insight & relationships |

This encourages progression from **recall → understanding → application → analysis**.

---

# 🔁 Progressive Refinement Loop

Students can request:

🧩 *Explain in simpler words*
📌 *Give more real-world examples*

The assistant then:

✔ preserves version-1 explanation
✔ adds refinement versions
✔ logs learning attempt history

Examples:

* v1 — main conceptual explanation
* v2 — simpler scaffolded form
* v3 — example-driven understanding

All versions are saved in the session log.

---

# 👍 Confidence-Based Reflection

After each explanation, learner provides:

* High confidence
* Medium confidence
* Low confidence

Confidence signals enable:

✔ metacognitive awareness
✔ learning reflection
✔ revision recommendations

Confidence trends are factored into:

* analytics dashboard
* learning summary export
* revision-priority evaluation

---

# 📊 Learning Analytics Dashboard

The dashboard surfaces:

| Metric                       | Meaning                          |
| ---------------------------- | -------------------------------- |
| Total Questions              | Cognitive engagement             |
| Refinement Attempts          | Struggle / clarity signals       |
| Avg Refinements per Question | Concept difficulty trend         |
| Bloom Level Distribution     | Thinking depth mapping           |
| Confidence Trend             | Learning self-reflection pattern |

This makes learning **insight-oriented** rather than chat-based.

---

# 📝 Reflection-Based Learning Summary (Exportable)

Each session generates a structured report:

Includes:

✔ session topic
✔ questions asked
✔ Bloom level
✔ refinement attempts
✔ multiple explanation versions
✔ confidence-trend insight
✔ revision-priority tag

Export options:

* TXT
* PDF *(wrapped & multi-page safe)*
* JSON session log *(research-friendly)*

---

# 🏗 System Architecture Flow

```mermaid
flowchart LR

A[Student Input] 
--> B[Chat Context Memory]
--> C[Groq LLM Response Engine]
--> D[Primary Answer v1]

D --> E{Refinement Trigger?}
E -->|Simpler| F[Refinement v2 — Simplified]
E -->|Examples| G[Refinement v2 — Example-Based]

F --> H[Chat History]
G --> H[Chat History]

H --> I[Meta Log Store (JSON)]
I --> J[Analytics Engine]
J --> K[Reflection Summary Export]
```

The system treats each doubt as a **learning event**.

---

# 🧩 Key Features

✔ Bloom-aware conceptual answering
✔ Multi-version refinement explanations
✔ Confidence-based learning reflection
✔ Revision-priority inference
✔ Persistent session logging
✔ Downloadable learning summaries
✔ JSON logs for research / ML use
✔ Modern Streamlit Indigo dashboard theme

All features are implemented in `app.py` 

---

# 🏗 Tech Stack

* Python
* Streamlit
* Groq API (LLM inference)
* ReportLab (PDF export)
* JSON-based session persistence

---

# 💻 Run Locally

### Create venv

```
python -m venv .venv
```

Activate:

```
.venv\Scripts\activate   # Windows
```

### Install dependencies

```
pip install -r requirements.txt
```

### Create `.env`

```
GROQ_API_KEY=your_api_key
```

### Run app

```
streamlit run app.py
```

---

# ☁ Deployment (Streamlit Cloud)

Add secret:

```
GROQ_API_KEY="your_api_key"
```

Deploy and run.

---

# 🎓 Pedagogical Value

Supports:

✔ conceptual understanding
✔ scaffolding-based clarity
✔ reflective self-assessment
✔ insight-driven revision
✔ SDG-4 learning equity goals

This system is built as a **learning facilitator — not a shortcut answer tool**.

---

# 🛠 Future Enhancements

* per-question confidence intelligence
* learner progress timeline
* recommendation engine for revision topics
* teacher / mentor dashboard
* concept difficulty heat-mapping

---

# 👤 Author

**Sushant Adhav**
CSRBOX — IBM SkillsBuild Applied AI Internship (2025)
