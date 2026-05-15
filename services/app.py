
import streamlit as st
import os
import sys
from gtts import gTTS
from streamlit_mic_recorder import speech_to_text

# 1. PATH SETUP (వేరే ఫోల్డర్లలో ఉన్న AI logic కోసం)
# ఇది app.py ఉన్న ఫోల్డర్ నుండి రెండు మెట్లు వెనక్కి వెళ్లి మెయిన్ ఫోల్డర్‌ని వెతుకుతుంది
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
root_dir = os.path.dirname(parent_dir)

for path in [current_dir, parent_dir, root_dir]:
    if path not in sys.path:
        sys.path.append(path)

# 2. MODULE IMPORTS
try:
    from ai_logic.llm import get_llm_response, evaluate_salespitch
    # ఇక్కడ నేరుగా persona_config ని ఇంపోర్ట్ చేస్తున్నాం (అది పక్కనే ఉండాలి)
    from persona_config import PERSONAS, COURSES
except ImportError as e:
    st.error(f"Module Error: {e}. Please ensure persona_config.py is in the same folder as app.py")
    st.stop()

# 3. PAGE CONFIGURATION
st.set_page_config(page_title="RP2 Sales AI Trainer", layout="wide")

# --- CSS FOR UI ---
st.markdown("""
<style>
    .chat-container { display: flex; flex-direction: column; }
    .user-msg {
        align-self: flex-end;
        background-color: #0078FF;
        color: white;
        padding: 10px 15px;
        border-radius: 18px 18px 2px 18px;
        margin: 5px;
        max-width: 75%;
    }
    .ai-msg {
        align-self: flex-start;
        background-color: #F1F1F2;
        color: black;
        padding: 10px 15px;
        border-radius: 18px 18px 18px 2px;
        margin: 5px;
        max-width: 75%;
    }
</style>
""", unsafe_allow_html=True)

# 4. AUDIO FUNCTION
def speak_text(text, i):
    try:
        tts = gTTS(text=text, lang='en')
        filename = f"temp_voice_{i}.mp3"
        tts.save(filename)
        st.audio(filename)
        os.remove(filename)
    except Exception:
        pass

# 5. SIDEBAR
st.sidebar.header("⚙️ Configuration")
selected_p_name = st.sidebar.selectbox("Select Persona:", list(PERSONAS.keys()))
selected_course = st.sidebar.selectbox("Choose Course:", COURSES)

st.sidebar.divider()
if st.sidebar.button("📊 End Conversation & Get Report", type="primary"):
    if "messages" in st.session_state and len(st.session_state.messages) > 0:
        report = evaluate_salespitch(st.session_state.messages)
        st.session_state.show_report = report
    else:
        st.sidebar.error("Please start the conversation first!")

# 6. MAIN INTERFACE
st.title("🛡️ RP2 Sales Training Professional")
col1, col2 = st.columns(2)
with col1:
    st.info("### 🎙️ Salesperson (You)")
    if "mic_counter" not in st.session_state:
        st.session_state.mic_counter = 0
        
    text_input = speech_to_text(
        start_prompt="Speak Now", 
        stop_prompt="Stop", 
        language='en', 
        key=f"mic_{st.session_state.mic_counter}" 
    )
    if text_input:
        st.session_state.user_voice_text = text_input

with col2:
    st.info(f"### 🤖 AI Student ({selected_p_name})")

st.divider()

# 7. CHAT DISPLAY
if "messages" not in st.session_state:
    st.session_state.messages = []

chat_display = st.container()
with chat_display:
    for i, msg in enumerate(st.session_state.messages):
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-container"><div class="user-msg">{msg["content"]}</div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-container"><div class="ai-msg">{msg["content"]}</div></div>', unsafe_allow_html=True)
            if i == len(st.session_state.messages) - 1:
                speak_text(msg["content"], i)

# 8. INPUT HANDLING
user_input = None
if prompt := st.chat_input("Type your message here..."):
    user_input = prompt
elif "user_voice_text" in st.session_state and st.session_state.user_voice_text:
    user_input = st.session_state.user_voice_text
    del st.session_state.user_voice_text
    st.session_state.mic_counter += 1 

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.status("AI is thinking..."):
        ai_response = get_llm_response(user_input, selected_p_name, selected_course, st.session_state.messages)
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
    st.rerun()

if "show_report" in st.session_state:
    st.success("### 🏆 Performance Evaluation")
    st.markdown(st.session_state.show_report)