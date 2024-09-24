import json
import tempfile
import os
from fastapi import HTTPException
from app.utils.pdf_extractor import extract_text_from_pdf
from fastapi import UploadFile

def load_document(file: UploadFile) -> str:
    try:
        if file.content_type == 'application/pdf':
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(file.file.read())
                tmp_path = tmp.name
            text = extract_text_from_pdf(tmp_path)
            os.unlink(tmp_path)  # Delete the temp file
            return text
        elif file.content_type == 'application/json':
            content = json.load(file.file)
            # Assuming the JSON has a 'content' field
            document_text = content.get('content', '')
            if not document_text:
                raise HTTPException(status_code=400, detail="JSON document must contain a 'content' field.")
            return document_text
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type. Only PDF and JSON are allowed.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")