from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

# FIXED IMPORTS
from backend.ingestion import ingest_docs
from backend.test_case_agent import generate_test_cases
from backend.script_agent import generate_script

app = FastAPI()

# Allow Streamlit frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- INGEST DOCUMENTS ----------
@app.post("/ingest")
async def ingest(files: list[UploadFile] = File(...)):
    """
    Upload and store documents into vector DB.
    """
    return await ingest_docs(files)

# ---------- GENERATE TEST CASES ----------
@app.post("/generate-test-cases")
async def gen_cases(query: str):
    """
    Generates JSON test cases based strictly on documentation.
    """
    output = generate_test_cases(query)
    return {"output": output}

# ---------- GENERATE SELENIUM SCRIPT ----------
@app.post("/generate-script")
async def gen_script(test_case: str):
    """
    Generates runnable Selenium script based on selected test case.
    """
    script = generate_script(test_case)
    return {"script": script}
