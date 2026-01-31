# 1. Import necessary libraries
import streamlit as st
import google.generativeai as genai

# --- STEP 1: GET API KEY FROM USER ---
# Sidebar la input box veikkom. type='password' nala key veliya theriyathu.
api_key = st.sidebar.text_input("Enter Google API Key:", type="password")

# Key illana, app ingaye stop aagidum.
if not api_key:
    st.warning("⚠️ Please enter your API Key in the sidebar to start!")
    st.stop()  # Stops the code here until key is entered

# Key irundha matum inga varum
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

st.title("🐍 Python Tutor (With Memory)")
st.caption("I remember what we talked about previously!")

# 2. INITIALIZE MEMORY (Session State)
# If we don't have a history yet, create an empty list.
if "history" not in st.session_state:
    st.session_state.history = []

# 3. DISPLAY HISTORY
# Before asking for new input, we must print all old messages on the screen.
for message in st.session_state.history:
    # "role" can be 'user' or 'model' (AI)
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. CHAT INPUT (This creates the chat bar at the bottom)
# ... (Previous code remains same) ...

# 4. CHAT INPUT
if prompt := st.chat_input("Ask me a Python question..."):
    
    # A. Display User's message (Clean version)
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # B. Save User's message to memory (Clean version)
    st.session_state.history.append({"role": "user", "content": prompt})

    # --- SECRET INSTRUCTION PART ---
    # Namma AI ki strict ah rule solrom
    restriction = """
    You are a specialized Python Tutor AI.
    Rule 1: Answer ONLY questions related to Python, Coding, or Data Science.
    Rule 2: If the user asks about movies, cooking, politics, or general life, politely refuse.
    Rule 3: Say "I can only answer Python questions" for off-topic queries.
    
    User Question: 
    """
    
    # AI ki anuppa vendiya final message (Rule + User Question)
    final_prompt_for_ai = restriction + prompt

    # C. Get AI Response
    # History load pannum pothu pazhaya conversation context edukum
    chat = model.start_chat(history=[
        {"role": m["role"], "parts": [m["content"]]} 
        for m in st.session_state.history 
        if m["role"] in ["user", "model"]
    ])
    
    # D. Send the STRICT message
    # Note: Namma 'final_prompt_for_ai' anupurom, verum 'prompt' illa
    response = chat.send_message(final_prompt_for_ai)
    
    # E. Display AI Response
    with st.chat_message("model"):
        st.markdown(response.text)
    
    # F. Save AI Response to memory
    st.session_state.history.append({"role": "model", "content": response.text})