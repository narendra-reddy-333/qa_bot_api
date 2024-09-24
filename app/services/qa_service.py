
from langchain.chains.qa_with_sources.base import QAWithSourcesChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain_community.llms import OpenAI
from langchain_community.vectorstores import FAISS

from app.config import settings


class QABot:
    def __init__(self, document_text: str):
        self.document_text = document_text
        self.qa_chain = self.setup_langchain()

    def setup_langchain(self):
        # Split the document into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        texts = text_splitter.split_text(self.document_text)

        # Initialize OpenAI embeddings
        embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)

        # Create FAISS vector store
        vector_store = FAISS.from_texts(texts, embeddings)

        # Initialize OpenAI LLM
        llm = OpenAI(openai_api_key=settings.OPENAI_API_KEY, model="gpt-3.5-turbo")

        # Create QA chain
        qa_chain = QAWithSourcesChain(
            llm=llm,
            vectorstore=vector_store,
            return_source_documents=False
        )

        return qa_chain

    def answer_question(self, question: str) -> str:
        try:
            answer = self.qa_chain.run(question)
            return answer
        except Exception as e:
            return f"Error answering question: {str(e)}"
