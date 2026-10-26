import requests

BASE_URL = "http://127.0.0.1:8000/api"

def upload_file_to_backend(file_name, file_bytes, file_type):
    """Sends the uploaded file to the FastAPI backend."""
    files = {"file": (file_name, file_bytes, file_type)}
    response = requests.post(f"{BASE_URL}/upload", files=files)
    
    # NEW: If the backend crashes, pass the exact error message to Streamlit
    if response.status_code != 200:
        raise Exception(response.text)
        
    return response.json()

def send_chat_query(query: str):
    """Sends the user's question to the FastAPI backend."""
    response = requests.post(f"{BASE_URL}/chat", json={"query": query})
    
    response.raise_for_status()
    return response.json()