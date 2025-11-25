import google.generativeai as genai
from backend.config import GEMINI_API_KEY, MODEL_NAME
from backend.vector_store import query_text

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(MODEL_NAME)

def generate_test_cases(query: str):
    """
    Generates grounded test cases using retrieved documentation.
    Output is strictly JSON array format.
    """

    results = query_text(query)

    # If nothing returned
    if not results or not results.get("documents"):
        return "No matching documentation found. Upload + ingest files first."

    # Chroma returns: {"documents": [["doc1", "doc2", ...]]}
    # Flatten properly
    docs = results["documents"][0] if isinstance(results["documents"], list) else []
    context = "\n".join(docs)

    prompt = f"""
You are a senior QA engineer. Your task is to generate test cases based *strictly* on the provided documentation.

CONTEXT (GROUND TRUTH):
{context}

REQUIREMENTS:
- DO NOT invent features that are not present in the context.
- Ground each test case by referencing the correct document file name.
- Output only a JSON array (no markdown, no explanations).
- Include BOTH positive and negative test cases.

EACH OBJECT MUST CONTAIN:
- Test_ID (format: TC-XXX)
- Feature
- Test_Scenario
- Expected_Result
- Grounded_In (document name)

Return ONLY the JSON array:
"""

    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.1,
            "top_p": 0.9,
            "top_k": 40
        }
    )

    output = response.text.strip()

    # Clean markdown formatting if present
    output = output.replace("```json", "").replace("```", "").strip()

    return output
