def load_course_data():
    """Load course data from markdown file"""
    try:
        with open("ai_logic/course_data.md", "r") as f:
            return f.read()
    except:
        return ""
    

def detect_intent(message):
    msg = message.lower()
    if any(w in msg for w in ["hi", "hello", "hey"]):
        return "greeting"
    if "data science" in msg:
        return "data_science"
    if "data analytics" in msg:
        return "data_analytics"
    if "agentic" in msg or "ai agent" in msg:
        return "agentic_ai"
    if any(w in msg for w in ["fee", "price", "cost", "money"]):
        return "pricing"
    if any(w in msg for w in ["job", "career", "salary", "placement"]):
        return "career"
    return "general"


def get_section(data, keyword):
    sections = data.split("---")

    for section in sections:
        if keyword.upper() in section.upper():
            return [{"answer": section.strip()[:1200]}]
    return [{"answer": data[:500]}]
 

def search(query: str, persona: str = ""):
    """Search course data for relevant info"""
    intent = detect_intent(query)
    data = load_course_data()

    if intent == "data_science":
        return get_section(data, "DATA SCIENCE")
    elif intent == "data_analytics":
        return get_section(data, "DATA ANALYTICS")
    elif intent == "agentic_ai":
        return get_section(data, "AGENTIC AI")
    elif intent in ("pricing", "career"):
        return get_section(data, "GENERAL")
    elif intent == "greeting":
        return [{"answer": """ The student is greeting the counselor. The student is exploring courses and wants guidance. Respond naturally and continue the conversation. """}]
    else:
        return [{
            "answer": "General course inquiry. Ask the student what exactly they want to know about the course, fees, duration, placements, or syllabus."
        }]