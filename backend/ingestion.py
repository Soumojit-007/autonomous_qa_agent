from fastapi import UploadFile
from backend.vector_store import add_embedded_text


async def ingest_docs(files: list[UploadFile]):
    """
    Reads uploaded files, extracts text, and stores them in the vector database.
    Works only for text-based files. PDF/JSON handling can be added later.
    """

    if not files or len(files) == 0:
        return {"error": "No files uploaded"}

    for f in files:
        raw = await f.read()

        # Skip empty files
        if not raw:
            print(f"[WARN] Skipped empty file: {f.filename}")
            continue

        try:
            # Default text decode
            content = raw.decode("utf-8")
        except Exception:
            # If binary or invalid encoding
            print(f"[WARN] Could not decode {f.filename} as UTF-8")
            continue

        # Store in vector DB
        add_embedded_text(content, f.filename)
        print(f"[INFO] Indexed: {f.filename}")

    return {"status": "Knowledge Base Built Successfully"}
