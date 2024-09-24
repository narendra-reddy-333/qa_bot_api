# QA API Service

This project is a FastAPI-based service that provides a Question-Answer (QA) system. The API allows users to upload a document (in PDF or JSON format) and a list of questions (in JSON format), and the service responds with answers to those questions based on the content of the document.

## Features

- Accepts PDF or JSON documents.
- Accepts JSON file with a list of questions.
- Uses OpenAI's embeddings and GPT-3.5-turbo for answering questions.
- Returns answers for all questions based on the content of the uploaded document.

## Requirements

- Python 3.8+
- FastAPI
- PyPDF2
- OpenAI API Key
- LangChain (for language model and embeddings)
- FAISS (for vector similarity search)

## Project Setup

### Installation

1. **Clone the repository:**

    ```bash
    git https://github.com/narendra-reddy-333/qa_bot_api
    cd qa-api-service
    ```

2. **Install dependencies:**

    It is recommended to use a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

    Then install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

3. **Environment Variables:**

    Create a `.env` file in the root of your project and add your OpenAI API key:

    ```plaintext
    OPENAI_API_KEY=your-openai-api-key
    ```

4. **Run the application:**

    ```bash
    uvicorn app.main:app --reload
    ```

    The API should now be available at `http://127.0.0.1:8000`.

## API Endpoints

### POST `/answer-questions/`

This endpoint accepts a document and a list of questions and returns answers to those questions based on the document's content.

- **Request:**
    - `questions_file`: A JSON file containing a list of questions.
    - `document_file`: A document in PDF or JSON format.

- **Response:**
    - A JSON object containing questions as keys and the corresponding answers as values.

- **Example Request:**

    ```bash
    curl -X POST "http://127.0.0.1:8000/answer-questions/" \
    -F "questions_file=@questions.json" \
    -F "document_file=@document.pdf"
    ```

- **Example Response:**

    ```json
    {
      "results": {
        "What is the purpose of the document?": "The purpose of the document is to explain...",
        "Who is the author?": "The author of the document is John Doe."
      }
    }
    ```

### Request File Formats

- **Questions File (JSON):**
  
  The `questions_file` should be a JSON file containing a list of questions. For example:

    ```json
    [
      "What is the purpose of the document?",
      "Who is the author?",
      "When was it written?"
    ]
    ```

- **Document File (PDF or JSON):**

    - **PDF**: The file can be a PDF document. The text will be extracted using the `PyPDF2` library.
    - **JSON**: If the document is in JSON format, it should contain a `content` field with the text of the document. Example:

      ```json
      {
        "content": "This is the content of the document."
      }
      ```

## Project Structure

```bash
qa-api-service/
│
├── app/
│   ├── __init__.py
│   ├── main.py                # FastAPI app entry point
│   ├── services/
│   │   ├── document_processor.py  # Handles document loading and processing
│   │   ├── qa_service.py      # Implements the QA logic using LangChain and OpenAI
│   ├── utils/
│   │   └── pdf_extractor.py   # Extracts text from PDF files
│   ├── models/
│   │   └── schemas.py         # Pydantic models for the API responses
│   └── config.py              # Configuration settings, including OpenAI API key
│
├── tests/                     # Unit and integration tests
│
├── .env                       # Environment variables (add your OpenAI API key here)
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation (this file)