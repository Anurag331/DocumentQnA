import streamlit as st
from components.sidebar import render_sidebar
from api_client import send_chat_query

# Configure the page layout
st.set_page_config(page_title="AI Document QA", page_icon="📄", layout="centered")

st.title("📄 AI Document Q&A")
st.markdown("Upload a document in the sidebar, then ask questions about it!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render the sidebar (this calls the function from components/sidebar.py)
render_sidebar()

# ==========================================
# MAIN PAGE: Chat Interface
# ==========================================
st.header("2. Ask Questions")

# Display existing chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept new user input
if prompt := st.chat_input("Ask a question about your document..."):
    # Display user's message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Searching document and thinking..."):
            try:
                # Call our isolated API client
                data = send_chat_query(prompt)
                answer = data.get("answer", "No answer found.")
                
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
                
            except Exception as e:
                st.error(f"⚠️ Failed to connect to FastAPI backend. Error: {e}")