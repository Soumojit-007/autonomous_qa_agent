# 🚀 Autonomous QA Agent (FastAPI + Streamlit + Gemini + ChromaDB)

An end-to-end intelligent QA Automation System that:
- Builds a knowledge base using uploaded project documents
- Generates test cases grounded in real documentation using Gemini (RAG)
- Converts selected test cases into complete Selenium Python scripts
- Provides a clean UI using Streamlit and REST API backend using FastAPI

---

## 📌 Features

### ✅ Document Ingestion  
Upload `checkout.html`, product docs, or any project files and build a vector-based knowledge base using ChromaDB.

### ✅ Test Case Generation  
Generate **grounded** test cases using Gemini 2.5 Flash.  
No hallucination — strictly based on uploaded files.

### ✅ Automated Script Generation  
Convert any test case into a **fully runnable Selenium Python script**.

### ✅ Clean UI  
Streamlit frontend for:
- Uploading files
- Generating test cases
- Creating Selenium scripts

### ✅ REST API  
FastAPI backend exposes:
- `/ingest`
- `/generate-test-cases`
- `/generate-script`

---

## 📁 Project Structure

project/
│── backend/
│ ├── main.py
│ ├── ingestion.py
│ ├── script_agent.py
│ ├── test_case_agent.py
│ └── vector_store.py
│
│── ui/
│ └── app.py
│
│── requirements.txt
│── .gitignore
│── README.md
│── .env.example