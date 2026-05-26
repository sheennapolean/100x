import streamlit as st
import requests
from streamlit_mic_recorder import speech_to_text



from chatBot import chat









# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(
    page_title="AI Interview Assistant",
    layout="centered"
)

# -----------------------------------
# CUSTOM CSS
# -----------------------------------
st.markdown("""
<style>

/* -----------------------------------
   HIDE STREAMLIT DEFAULT ELEMENTS
----------------------------------- */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

/* -----------------------------------
   MAIN PAGE STYLING
----------------------------------- */

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0f172a;
    color: #f8fafc;
}

/* Main container */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 950px;
}

/* -----------------------------------
   HEADER
----------------------------------- */

.chat-title {
    font-size: 38px;
    font-weight: 700;
    color: white;
    margin-bottom: 6px;
    letter-spacing: -0.5px;
}

.chat-subtitle {
    color: #94a3b8;
    font-size: 15px;
    margin-bottom: 30px;
}

/* -----------------------------------
   CHAT MESSAGES
----------------------------------- */

[data-testid="stChatMessage"] {
    padding: 14px 18px;
    border-radius: 16px;
    margin-bottom: 14px;
    border: 1px solid rgba(255,255,255,0.06);
    backdrop-filter: blur(10px);
}

/* User message */
[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) {
    background-color: #1e293b;
}

/* Assistant message */
[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"]) {
    background-color: #111827;
}

/* Chat text */
[data-testid="stMarkdownContainer"] p {
    font-size: 15px;
    line-height: 1.7;
    color: #f8fafc;
}

/* -----------------------------------
   INPUT BOX
----------------------------------- */

.stChatInputContainer {
    background-color: #0f172a;
    border-top: 1px solid rgba(255,255,255,0.08);
    padding-top: 12px;
}

/* Input field */
textarea {
    background-color: #1e293b !important;
    color: white !important;
    border-radius: 14px !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    padding: 12px !important;
    font-size: 15px !important;
}

/* Remove ugly focus outline */
textarea:focus {
    border: 1px solid #3b82f6 !important;
    box-shadow: 0 0 0 1px #3b82f6 !important;
}

/* -----------------------------------
   BUTTONS
----------------------------------- */

button {
    border-radius: 12px !important;
    border: none !important;
    transition: all 0.2s ease;
}

/* Hover effect */
button:hover {
    transform: translateY(-1px);
}

/* -----------------------------------
   MICROPHONE BUTTON
----------------------------------- */

.stButton button {
    background-color: #1e293b;
    color: white;
    height: 50px;
    width: 100%;
}

.stButton button:hover {
    background-color: #334155;
}

/* -----------------------------------
   SCROLLBAR
----------------------------------- */

::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: transparent;
}

::-webkit-scrollbar-thumb {
    background: #334155;
    border-radius: 10px;
}

/* -----------------------------------
   DIVIDER
----------------------------------- */

hr {
    border-color: rgba(255,255,255,0.08);
}

/* -----------------------------------
   SPINNER
----------------------------------- */

[data-testid="stSpinner"] {
    color: white;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------
# HEADER
# -----------------------------------
st.markdown(
    """
    <div class="chat-title">
        AI Interview Assistant
    </div>

    <div class="chat-subtitle">
        Ask interview questions naturally
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------------
# SESSION STATE
# -----------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------------
# CHAT CONTAINER
# -----------------------------------
chat_container = st.container()

with chat_container:

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# -----------------------------------
# INPUT AREA
# -----------------------------------
st.markdown("---")

col1, col2 = st.columns([8, 1])

with col1:
    text_prompt = st.chat_input(
        "Type your interview question..."
    )

with col2:
    voice_prompt = speech_to_text(
        language="en",
        start_prompt="Speak",
        stop_prompt="Stop",
        just_once=True,
        use_container_width=True,
        key="voice_input",
    )

# -----------------------------------
# PRIORITIZE VOICE INPUT
# -----------------------------------
prompt = voice_prompt if voice_prompt else text_prompt

# -----------------------------------
# HANDLE INPUT
# -----------------------------------
if prompt:

    # Store user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # Display user message
    with chat_container:

        with st.chat_message("user"):
            st.markdown(prompt)

    # -----------------------------------
    # API CALL
    # -----------------------------------
    with chat_container:

        with st.chat_message("assistant"):

            with st.spinner("Generating response..."):

                try:

                    response = chat(prompt)

        

                    reply = response.get(
                        "reply",
                        "No response received."
                    )

                    st.markdown(reply)

                    # Store assistant response
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": reply
                    })

                except Exception as e:

                    error_message = f"Error: {str(e)}"

                    st.error(error_message)

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_message
                    })