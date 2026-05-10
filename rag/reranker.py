from typing import List
from langchain_core.documents import Document

def rerank_documents(query: str, documents: List[Document]) -> List[Document]:
    """
    Basic reranker stub. 
    In an advanced scenario, use CohereRerank or cross-encoders.
    Currently returns the similarity-based order from Chroma.
    """
    return documents
