import ollama


class QueryService:

    def __init__(self, vector_store):
        self.vector_store = vector_store

    def ask_question(self, question):

        # Retrieve relevant code chunks
        results = self.vector_store.similarity_search(question)

        context = "\n\n".join(
            [doc.page_content for doc in results]
        )

        prompt = f"""
You are an expert software engineer.

Use the provided code context to answer the question.

CODE CONTEXT:
{context}

QUESTION:
{question}

Provide a clear explanation and mention file paths if possible.
"""

        response = ollama.chat(
            model="phi3",
            messages=[{"role": "user", "content": prompt}]
        )

        return response["message"]["content"]