from langchain_huggingface import HuggingFaceEmbeddings
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import settings

def get_embeddings():
    """Returns the default embedding model."""
    # Using HuggingFace sentence-transformers
    return HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)
