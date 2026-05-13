import streamlit as st
import time
from services.api_client import get_ai_response
from frontend_logic.persona_config import PERSONAS, COURSES

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="RP2 AI Sales Trainer", layout="wide", page_icon="🛡️")

# 2. PROFESSIONAL HEADER
st.markdown("""
    <div style="background-color: #1E3A8A; padding: 20px; border-radius: 10px; margin-bottom: 25px;">
        <h1 style="color: white; text-align: center; margin: 0;">🛡️ RP2 Sales Training - Professional Edition</h1>
    </div>
""", unsafe_allow_html=True)

# 3. SIDEBAR: CONFIGURATION
st.sidebar.header("Configuration")
selected_p_name = st.sidebar.selectbox("Select Persona:", list(PERSONAS.keys()))
selected_course = st.sidebar.selectbox("Choose Course:", COURSES)

if st.sidebar.button("🗑️ Clear Chat History"):
    st.session_state.messages = []
    st.session_state.last_score = None
    st.rerun()

st.sidebar.divider()
st.sidebar.info(f"**Student Behavior:**\n{PERSONAS[selected_p_name]['behavior']}")

# 4. MAIN INTERFACE: AVATARS & VOICE BUTTONS
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div style="text-align: center; background-color: #f8f9fa; padding: 20px; border-radius: 15px; border: 1px solid #dee2e6;">', unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80)
    st.markdown("### Salesperson (You)")
    # Voice Input Feature
    if st.button("🎤 Record Your Pitch"):
        st.info("Listening... (Speak now)")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div style="text-align: center; background-color: #f8f9fa; padding: 20px; border-radius: 15px; border: 1px solid #dee2e6;">', unsafe_allow_html=True)
    avatars = {
        "Beginner": "https://cdn-icons-png.flaticon.com/512/3429/3429433.png",
        "Skeptical": "https://cdn-icons-png.flaticon.com/512/4712/4712035.png",
        "Price Sensitive": "https://cdn-icons-png.flaticon.com/512/2654/2654512.png",
        "Interested": "https://cdn-icons-png.flaticon.com/512/4140/4140048.png"
    }
    st.image(avatars.get(selected_p_name, avatars["Beginner"]), width=80)
    st.markdown(f"### AI Student ({selected_p_name})")
    # Voice Output Feature
    if st.button("🔈 Play Audio Response"):
        st.toast("Playing AI voice response...")
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# 5. PITCH PERFORMANCE SCORE
if "last_score" in st.session_state and st.session_state.last_score:
    st.markdown(f"""
        <div style="background-color: #E8F5E9; border: 2px solid #4CAF50; padding: 15px; border-radius: 10px; text-align: center;">
            <h3 style="color: #2E7D32; margin: 0;">Latest Pitch Score: ⭐ {st.session_state.last_score}/10</h3>
        </div>
    """, unsafe_allow_html=True)

# 6. CHAT CONVERSATION LOGIC
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Type your pitch here..."):
    # Add user message to state
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get AI response
    combined_info = {**PERSONAS[selected_p_name], "course": selected_course}
    
    with st.chat_message("assistant"):
        with st.status(f"{selected_p_name} is evaluating...", expanded=True) as status:
            # Backend call
            result = get_ai_response(prompt, combined_info)
            time.sleep(0.5)
            status.update(label="Response Ready!", state="complete", expanded=False)
            
            st.markdown(result["text"])
            if result.get("score"):
                st.session_state.last_score = result["score"]
    
    # Add assistant response to state
    st.session_state.messages.append({"role": "assistant", "content": result["text"]})
