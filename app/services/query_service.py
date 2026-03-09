import google.generativeai as genai
from app.core.config import settings


genai.configure(api_key=settings.GEMINI_API_KEY)


class QueryService:

    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.model = genai.GenerativeModel("gemini-2.5-flash")
        self.chat_history = []

    def ask_question(self, question):

        results = self.vector_store.similarity_search(question)

        context = "\n\n".join(
            [doc.page_content for doc in results]
        )

        sources = list(set(
            [doc.metadata["path"] for doc in results]
        ))

        history_text = "\n".join(
            [f"{msg['role']}: {msg['content']}" for msg in self.chat_history]
        )

        prompt = f"""
You are an expert software engineer.

Use the following code context to answer the question.

Previous conversation:
{history_text}

CODE CONTEXT:
{context}

QUESTION:
{question}

Explain clearly and mention file paths if relevant.
"""

        response = self.model.generate_content(prompt)

        answer = response.text

        self.chat_history.append({"role": "user", "content": question})
        self.chat_history.append({"role": "assistant", "content": answer})

        return {
            "answer": answer,
            "sources": sources
        }