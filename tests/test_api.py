# tests/test_api.py

from fastapi.testclient import TestClient
from main import app
import json

client = TestClient(app)

def test_answer_questions_success():
    # Sample questions
    questions = [
        "What is the main topic of the document?",
        "How does the system work?"
    ]
    # Sample document content
    document = {
        "content": "This document explains how the QA bot system works. It leverages Langchain and FastAPI to answer user queries based on provided documents."
    }

    # Create temporary files
    questions_json = json.dumps(questions)
    document_json = json.dumps(document)

    files = {
        "questions_file": ("questions.json", questions_json, "application/json"),
        "document_file": ("document.json", document_json, "application/json")
    }

    response = client.post("/answer-questions/", files=files)
    assert response.status_code == 200
    json_response = response.json()
    assert isinstance(json_response, dict)
    assert len(json_response) == 2
    assert "What is the main topic of the document?" in json_response
    assert "How does the system work?" in json_response

def test_answer_questions_invalid_questions_file():
    # Invalid questions file (not a list)
    questions = {
        "question": "What is the main topic?"
    }
    document = {
        "content": "Sample content."
    }

    questions_json = json.dumps(questions)
    document_json = json.dumps(document)

    files = {
        "questions_file": ("questions.json", questions_json, "application/json"),
        "document_file": ("document.json", document_json, "application/json")
    }

    response = client.post("/answer-questions/", files=files)
    assert response.status_code == 400
    assert "Questions JSON must be a list of questions." in response.json()["detail"]

def test_answer_questions_unsupported_file_type():
    # Unsupported document file type
    questions = [
        "What is the main topic?"
    ]
    document_content = "This is a plain text document."

    questions_json = json.dumps(questions)

    files = {
        "questions_file": ("questions.json", questions_json, "application/json"),
        "document_file": ("document.txt", document_content, "text/plain")
    }

    response = client.post("/answer-questions/", files=files)
    assert response.status_code == 400
    assert "Unsupported file type" in response.json()["detail"]