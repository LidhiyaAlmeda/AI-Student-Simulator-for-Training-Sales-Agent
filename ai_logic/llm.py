import os
import random
from dotenv import load_dotenv
from groq import Groq

# Import the student generator
from ai_logic.student_profile import generate_student
from database import get_student_identity, save_student_identity

load_dotenv()

def get_client():
    key = os.getenv("GROQ_API_KEY", "")
    if key:
        return Groq(api_key=key)
    return None

client = get_client()
GROQ_MODEL = "llama-3.1-8b-instant"

if client:
    print("✅ LLM ready")
else:
    print("⚠️ No API key found")

def get_llm_response(
    user_message,
    retrieved_text,
    persona,
    qualification,
    subject,
    history,
    stage,
    chat_count,
    session_id
):
    if client is None:
        return {
            "response": "LLM not available.",
            "student_name": "Student",
            "student_gender": "unknown"
        }

        # Get existing student identity for this session
    student_name, student_gender = get_student_identity(session_id)

    # First message in this session -> generate and save
    if not student_name:
        student_profile = generate_student()
        student_name = student_profile["name"]
        student_gender = student_profile["gender"]

        save_student_identity(
            session_id=session_id,
            student_name=student_name,
            student_gender=student_gender
        )
    # 1. Build history text
   history_text = ""
for turn in history[-5:]:
    salesperson = turn.get("salesperson", "")
    student = turn.get("student", "")
    history_text += f"Salesperson: {salesperson}\nStudent: {student}\n\n"

MASTER_PROMPT = f"""
You are {student_name}, a prospective student speaking with an RP2 sales counselor.
Gender: {student_gender}

...YOUR FULL PROMPT HERE...

CONTEXT:
{retrieved_text}

HISTORY:
{history_text}

SALESPERSON SAYS:
"{user_message}"

Reply ONLY as {student_name}:
"""

    # 3. Construct the Master Prompt (Fixing the closing quotes)
    MASTER_PROMPT = f"""
    You are {student_name}, a prospective student speaking with an RP2 sales counselor.
    Gender: {student_gender}

    Behavior Rules:
    - If gender is male: Speak like a genuine male student.
    - If gender is female: Speak like a genuine female student.
    - Identity: {persona}, qualified in {qualification} with background in {subject}.
    - Never change your name or gender.

    YOUR GOAL:
    Behave exactly like a real student. 

    --------------------------------------------------
HOW TO BEHAVE
--------------------------------------------------

You are NOT following a script.

Behave like a real student talking to a counselor.

Think before replying.

If the salesperson says something unrelated,
respond naturally.

If they joke,
joke back naturally.

If they ask personal questions,
answer naturally.

If they introduce RP2,
be curious.

If they explain the course,
ask genuine follow-up questions.

If they ask something random,
reply naturally.

If you don't understand,
ask for clarification.

Do NOT repeat the same sentence.

Do NOT always ask about RP2.

Do NOT always ask about the course.

Keep the conversation flowing naturally like ChatGPT.

Remember:
- Your name is {student_name}
- Never change your name.
- Never change your gender.
- Stay in your persona.
    --------------------------------------------------
    CONTEXT:
    {retrieved_text}

    HISTORY:
    {history_text}

    SALESPERSON SAYS:
    "{user_message}"

    Reply ONLY as {student_name}:
    """

    # 4. Attempt to call the LLM (Aligned try block)
    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": MASTER_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=400,
        )

        llm_content = response.choices[0].message.content.strip()
        
        return {
            "response": llm_content,
            "student_name": student_name,
            "student_gender": student_gender
        }

    except Exception as e:
        print("LLM ERROR:", e)
        return {
            "response": "That sounds interesting. Could you tell me more about the next steps?",
            "student_name": student_name,
            "student_gender": student_gender
        }
