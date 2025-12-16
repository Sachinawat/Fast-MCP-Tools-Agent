import os
import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from servers.config import logger, BASE_DIR

# --- 1. RAG Setup (Simulated for now, can be connected to Chroma) ---
def get_retriever(query):
    """
    In a real system, this searches ChromaDB/FAISS.
    For now, it returns a placeholder.
    """
    # If you had a real vector DB, you would do: vector_db.similarity_search(query)
    return [] 

# --- 2. The Real Intelligence (GPT-4o-mini) ---
def execute_research(query: str):
    logger.info(f"Researching: {query}")
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "Error: OPENAI_API_KEY not found in .env file."

    # 1. Retrieve Context (Simulated)
    # We try to get documents. If none, we pass an empty list.
    retrieved_docs = get_retriever(query)
    context_str = "\n".join(retrieved_docs) if retrieved_docs else "No internal documents found."

    # 2. Setup the LLM
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

    # 3. Create the Prompt
    # This instructs the AI to use context if available, otherwise use its own knowledge.
    template = """
    You are an Enterprise Research Assistant.
    
    User Query: {query}
    
    Internal Knowledge Base Context:
    {context}
    
    Instructions:
    1. If the context contains the answer, cite it.
    2. If the context is empty or irrelevant, ANSWER using your own general knowledge (e.g., for history, science, or casual chat).
    3. Keep the tone professional and concise.
    """
    
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm | StrOutputParser()

    # 4. Execute
    try:
        response = chain.invoke({"query": query, "context": context_str})
        return {"status": "success", "data": response, "source": "LLM (gpt-4o-mini)"}
    except Exception as e:
        logger.error(f"LLM Error: {e}")
        return {"status": "error", "message": str(e)}