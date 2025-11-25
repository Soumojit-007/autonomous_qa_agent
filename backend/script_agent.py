import google.generativeai as genai
from backend.config import GEMINI_API_KEY, MODEL_NAME
from backend.vector_store import query_text

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(MODEL_NAME)

def generate_script(test_case: str):
    """
    Generates a runnable Selenium script based on a selected test case.
    Retrieval ensures scripts are grounded in context from the ingested documents.
    """

    # Retrieve context from vector DB
    results = query_text(test_case)

    if not results or not results.get("documents"):
        return "No relevant context found. Make sure documents are ingested first."

    # Chroma returns nested docs → flatten
    docs = results["documents"][0]
    context_text = "\n".join(docs)

    prompt = f"""
You are a senior QA automation engineer specializing in Python + Selenium.

STRICT RULES:
- Only output RAW Python code (no markdown, no commentary)
- The code MUST run without manual fixes
- Use correct selectors that exist in checkout.html
- Assume Chrome WebDriver
- Script must end with driver.quit()
- Include necessary imports
- Handle form filling, clicks, assertions, success verification

CONTEXT FROM PROJECT DOCUMENTS (GROUND TRUTH):
{context_text}

TEST CASE TO AUTOMATE:
{test_case}

Now generate the full executable script:
"""

    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.1,    # deterministic output
            "top_p": 0.9,
            "top_k": 40
        }
    )

    script = response.text

    # Remove markdown fences if model adds them
    script = script.replace("```python", "").replace("```", "").strip()

    return script
