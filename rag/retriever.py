import os
from typing import List, Dict, Any, Optional
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_postgres.vectorstores import PGVector

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.embeddings import get_embeddings
from rag.reranker import rerank_documents
from rag.utils import setup_logger
from config import settings

logger = setup_logger("TicketRAG")

class TicketRAG:
    def __init__(self):
        self.embeddings = get_embeddings()
        self.collection_name = "ticket_knowledge"
        
        # Use sync connection string
        self.connection_string = settings.sync_database_url
        
        # Fallback to local Chroma for dev if Postgres is not set up
        self.use_pg = "sqlite" not in self.connection_string.lower()
        
        if self.use_pg:
            logger.info(f"Initializing PGVector RAG using database: {self.connection_string.split('@')[-1]}")
            self.vectorstore = PGVector(
                embeddings=self.embeddings,
                collection_name=self.collection_name,
                connection=self.connection_string,
                use_jsonb=True
            )
        else:
            # SQLite fallback uses Chroma
            logger.info("Postgres not detected, falling back to Chroma DB.")
            from langchain_community.vectorstores import Chroma
            persist_dir = os.path.abspath(settings.CHROMA_PERSIST_DIRECTORY)
            os.makedirs(persist_dir, exist_ok=True)
            self.vectorstore = Chroma(
                persist_directory=persist_dir,
                embedding_function=self.embeddings,
                collection_name=self.collection_name
            )

    def add_document(self, doc_path: str):
        """Adds a single markdown document to the vector store."""
        if not os.path.exists(doc_path):
            logger.error(f"Document not found: {doc_path}")
            return
            
        with open(doc_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        filename = os.path.basename(doc_path)
        
        category = "General"
        if "FAQ" in content or "faq" in filename: category = "FAQ"
        elif "Runbook" in content or "runbook" in filename: category = "Runbook"
        elif "SOP" in content or "sop" in filename: category = "SOP"
        elif "Ticket" in content or "ticket" in filename: category = "Past Ticket"
            
        metadata = {"source": filename, "category": category}
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_text(content)
        
        documents = [Document(page_content=chunk, metadata=metadata) for chunk in chunks]
        self.vectorstore.add_documents(documents)
        logger.info(f"Added {len(chunks)} chunks from {filename}")

    def retrieve_context(self, query: str, k: int = 8, filter_kwargs: Optional[Dict] = None) -> List[Document]:
        """Retrieve relevant context for a given query."""
        if not self.vectorstore:
            return []
            
        retriever = self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": k, "filter": filter_kwargs}
        )
        
        docs = retriever.invoke(query)
        logger.info(f"Retrieved {len(docs)} documents for query: {query}")
        
        reranked_docs = rerank_documents(query, docs)
        return reranked_docs

    def retrieve_for_ticket(self, ticket_description: str, category: Optional[str] = None) -> List[dict]:
        """Helper to retrieve specifically for ticket context."""
        query = ticket_description
        if category:
            query = f"[{category}] {query}"
            
        docs = self.retrieve_context(query, k=5)
        
        return [{"content": d.page_content, "metadata": d.metadata} for d in docs]
        
    def query_knowledge_base(self, query: str) -> List[dict]:
        docs = self.retrieve_context(query, k=5)
        return [{"content": d.page_content, "metadata": d.metadata} for d in docs]

# Expose function for LangGraph compatibility with previous stub
_rag_instance = None
def retrieve_past_solutions(query: str, k: int = 3):
    global _rag_instance
    if _rag_instance is None:
        _rag_instance = TicketRAG()
    
    results = _rag_instance.retrieve_for_ticket(query)
    # Map to the format expected by the nodes.py stub if necessary
    return [{"ticket_id": r["metadata"].get("source", "UNKNOWN"), "solution": r["content"]} for r in results]
