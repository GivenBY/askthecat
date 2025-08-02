import logging
from typing import Optional

# Assuming these are your other modules
from src.groq_llm import GroqLLM
from src.vector_store import VectorStore
from src.embedder import Embedder

# Configure logging for better diagnostics
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class QueryEngine:
    def __init__(self, llm: GroqLLM, vector_store: VectorStore, embedder: Embedder):
        if not all([llm, vector_store, embedder]):
            raise ValueError("LLM, VectorStore, and Embedder must all be provided and initialized.")
        
        self.llm = llm
        self.vector_store = vector_store
        self.embedder = embedder
        logging.info("QueryEngine initialized successfully with injected dependencies.")

    def build_context(self, query: str, k: int = 5) -> str:
        logging.info(f"Embedding query: '{query[:50]}...'")
        query_vector = self.embedder.embed([query])

        if query_vector.size == 0:
            logging.warning("Query embedding resulted in an empty vector.")
            return ""

        logging.info(f"Searching for top {k} relevant chunks.")
        search_results = self.vector_store.search(query_vector=query_vector, k=k)

        context = "\n\n---\n\n".join([text for score, text in search_results])
        return context

    def _build_prompt(self, query: str, context: str) -> tuple[str, str]:
        system_prompt = (
            "You are an expert study assistant. Your task is to answer the user's question "
            "based exclusively on the provided context. Do not use any external knowledge. "
            "Synthesize the information from the context into a clear, concise, and helpful answer. "
            "If the answer is not found within the context, state clearly that you "
            "cannot answer the question with the given information."
        )

        user_prompt = f"""
        **Context:**
        {context}

        ---

        **Question:**
        {query}
        """
        return system_prompt, user_prompt.strip()

    def ask(self, query: str) -> str:
        logging.info("Starting RAG pipeline for a new query.")
        
        context = self.build_context(query)
        if not context.strip():
            logging.warning("No context was retrieved for the query. Cannot generate an answer.")
            return "I could not find any relevant information in the uploaded documents to answer your question."

        system_prompt, user_prompt = self._build_prompt(query, context)
        
        logging.info("Sending prompt to LLM for answer generation.")
        answer = self.llm.generate(prompt=user_prompt, system_prompt=system_prompt)
        
        logging.info("Successfully generated an answer.")
        return answer