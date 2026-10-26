import streamlit as st
from api_client import upload_file_to_backend

def render_sidebar():
    """Renders the file upload UI in the Streamlit sidebar."""
    with st.sidebar:
        st.header("1. Upload Document")
        uploaded_file = st.file_uploader("Choose a PDF or Text file", type=["pdf", "txt"])
        
        if uploaded_file is not None:
            if st.button("Process Document"):
                with st.spinner("Chunking and generating embeddings..."):
                    try:
                        # Call our isolated API client
                        data = upload_file_to_backend(
                            uploaded_file.name, 
                            uploaded_file.getvalue(), 
                            uploaded_file.type
                        )
                        st.success(f"✅ Document embedded successfully! ({data.get('chunks_created')} chunks created)")
                        
                        # Clear chat history when a new document is uploaded
                        st.session_state.messages = []
                        
                    except Exception as e:
                        st.error(f"❌ Backend Error: {e}")