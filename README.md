# 🧠 AI Learning Gap Assistant

### Bloom-Aware Conceptual Tutor with Reflective Analytics and Learning Refinement

An AI-powered conceptual learning assistant that helps students bridge learning gaps through:

* Bloom learning levels
* Progressive refinement explanations
* Confidence-based reflection
* Revision-priority insights
* Structured learning summaries
* Lightweight learning analytics dashboard

Instead of only answering questions, the assistant supports:

✔ understanding  
✔ reflection  
✔ progressive clarity  
✔ learning reinforcement  

This project aligns with SDG-4 Quality Education by enabling reflective, feedback-driven learning.

---

## 📌 Project Overview

Traditional AI chat responses provide answers — but they do not:

✘ assess learning depth  
✘ support cognitive learning levels  
✘ provide refinement-based explanations  
✘ capture confidence signals  
✘ identify weak topics  

This system shifts AI from:

"Answer provider" → "Learning facilitator"

by encouraging:

* conceptual clarity  
* repeated scaffolding  
* reflective thinking  
* insight-driven revision  

---

# 🧩 Visual Learning Flow

### How a Learning Session Works

```mermaid
flowchart TD

A["Student asks question"] --> B["AI main explanation v1"]
B --> C{"Student feedback"}

C -->|"Needs simpler form"| D["Refinement v2 - simpler explanation"]
C -->|"Needs more examples"| E["Refinement v2 - example based"]
C -->|"Understood"| F["Confidence recorded"]

D --> G["Confidence check"]
E --> G

G --> H["Confidence trend logged"]
H --> I["Revision priority evaluated"]

I --> J["Learning analytics dashboard"]
J --> K["Reflection based learning summary export"]
