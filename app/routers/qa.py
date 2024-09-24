from fastapi import APIRouter, File, UploadFile, HTTPException
import json
from app.services.document_processor import load_document
from app.services.qa_service import QABot
from app.models.schemas import QAResponse

router = APIRouter()

@router.post("/answer-questions/", response_model=QAResponse)
async def answer_questions(
    questions_file: UploadFile = File(..., description="JSON file containing list of questions."),
    document_file: UploadFile = File(..., description="PDF or JSON file containing the document.")
):
    # Validate and load questions
    if questions_file.content_type != 'application/json':
        raise HTTPException(status_code=400, detail="Questions file must be a JSON.")
    try:
        questions_content = json.load(questions_file.file)
        if not isinstance(questions_content, list):
            raise ValueError("Questions JSON must be a list of questions.")
        questions = questions_content
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid questions file: {str(e)}")

    # Load and process document
    document_text = load_document(document_file)

    if not document_text.strip():
        raise HTTPException(status_code=400, detail="Document content is empty.")

    # Setup QA Bot
    try:
        qa_bot = QABot(document_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to setup QA bot: {str(e)}")

    # Answer questions
    results = {}
    for question in questions:
        answer = qa_bot.answer_question(question)
        results[question] = answer

    return QAResponse(results=results)