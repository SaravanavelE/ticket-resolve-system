import os
import sys
import glob

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rag.retriever import TicketRAG
from rag.utils import get_documents_dir

def main():
    rag = TicketRAG()
    docs_dir = get_documents_dir()
    
    md_files = glob.glob(os.path.join(docs_dir, "*.md"))
    
    if not md_files:
        print(f"No markdown files found in {docs_dir}. Please run generate_docs.py first.")
        return
        
    print(f"Found {len(md_files)} documents. Ingesting...")
    
    for file_path in md_files:
        print(f"Ingesting {os.path.basename(file_path)}...")
        rag.add_document(file_path)
        
    print("Ingestion complete. Vectorstore is ready.")

if __name__ == "__main__":
    main()
