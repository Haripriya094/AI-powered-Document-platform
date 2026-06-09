import streamlit as st
import requests

st.set_page_config(
    page_title="AI Knowledge Assistant"
)

st.title("AI Knowledge Assistant")

st.write("Welcome to the AI Knowledge Assistant")

BACKEND_URL = "http://localhost:8015"

try:
    response = requests.get(f"{BACKEND_URL}")

    if response.status_code == 200:
        st.success("Backend Connected Successfully")
        st.json(response.json())
    else:
        st.error(f"Backend Error: {response.status_code}")

except Exception as e:
    st.error(f"Unable to connect to backend: {str(e)}")