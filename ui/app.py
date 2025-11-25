import streamlit as st
import requests

st.set_page_config(page_title="Autonomous QA Agent", page_icon="🧠", layout="centered")

st.markdown(
    """
    <style>
    /* Main background and green text */
    .main {
        background-color: #000000;
        color: #00FF00;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    /* Title styling */
    .css-1d391kg h1 {
        color: #00FF00;
        text-align: center;
        font-weight: 700;
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    /* File uploader container */
    .stFileUpload > div {
        background-color: #121212;
        border: 1px solid #00FF00;
        border-radius: 6px;
        padding: 12px;
    }
    /* Input box and textarea: white background with black text */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #ffffff;
        color: #000000;
        border: 1px solid #00FF00;
        border-radius: 6px;
        padding: 8px;
        transition: border-color 0.3s ease;
    }
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #00cc00;
        outline: none;
    }
    /* Buttons */
    div.stButton > button {
        background-color: #008000;
        color: #fff;
        font-weight: 600;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        border: none;
        transition: background-color 0.3s ease;
        width: 100%;
        max-width: 300px;
        cursor: pointer;
    }
    div.stButton > button:hover {
        background-color: #00cc00;
    }
    /* Success and warning messages */
    .stAlert {
        border-radius: 6px;
        padding: 1rem;
        font-weight: 600;
        color: #000;
    }
    .stAlertSuccess {
        background-color: #00ff00c9;
    }
    .stAlertWarning {
        background-color: #ffa500b8;
        color: #000;
    }
    /* JSON output box */
    .stJson {
        background-color: #121212;
        border: 1px solid #00ff00;
        border-radius: 6px;
        padding: 10px;
        color: #00ff00;
        font-family: Consolas, monospace;
        font-size: 0.9rem;
    }
    /* Code block */
    .stCodeBlock {
        background-color: #121212;
        border: 1px solid #00ff00;
        border-radius: 6px;
        padding: 10px;
        color: #00ff00;
        font-family: Consolas, monospace;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Autonomous QA Agent")

uploaded_files = st.file_uploader(
    "Upload project documents (checkout.html required)",
    accept_multiple_files=True,
)

if st.button("Build Knowledge Base"):
    if uploaded_files:
        files = [("files", (f.name, f.read())) for f in uploaded_files]
        res = requests.post("http://localhost:8000/ingest", files=files)
        st.success(res.json())
    else:
        st.warning("Upload at least one file before building the knowledge base!")

query = st.text_input("Enter feature request for test cases")

if st.button("Generate Test Cases"):
    if query.strip():
        res = requests.post(
            "http://localhost:8000/generate-test-cases",
            params={"query": query}
        )
        st.json(res.json())
    else:
        st.warning("Enter a query first")

test_case = st.text_area("Paste a test case to generate Selenium script")

if st.button("Generate Script"):
    if test_case.strip():
        res = requests.post(
            "http://localhost:8000/generate-script",
            params={"test_case": test_case}
        )
        st.code(res.json().get("script", ""), language="python")
    else:
        st.warning("Enter a test case first")
