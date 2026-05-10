import os
import sys
import shutil

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rag.retriever import TicketRAG
from config import settings

def migrate():
    print("🚀 Starting Migration to PGVector...")
    
    # Check if Postgres is configured
    if "sqlite" in settings.sync_database_url.lower():
        print("⚠️ Warning: Your DATABASE_URL seems to point to SQLite.")
        print("Please set a valid Postgres DATABASE_URL in .env before migrating.")
        print(f"Current URL: {settings.sync_database_url}")
        return
        
    print(f"Connecting to: {settings.sync_database_url}")
    
    # Initialize RAG (will auto-connect to PGVector based on config.py)
    try:
        rag = TicketRAG()
    except Exception as e:
        print(f"❌ Failed to initialize PGVector: {e}")
        return
        
    # Re-ingest documents from local documents folder
    docs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "rag", "documents")
    if not os.path.exists(docs_dir):
        print(f"❌ Documents directory not found at {docs_dir}")
        return
        
    import glob
    md_files = glob.glob(os.path.join(docs_dir, "*.md"))
    
    if not md_files:
        print(f"No markdown files found in {docs_dir}")
        return
        
    print(f"Found {len(md_files)} documents. Ingesting into PGVector...")
    
    for file_path in md_files:
        print(f"Ingesting {os.path.basename(file_path)}...")
        try:
            rag.add_document(file_path)
        except Exception as e:
            print(f"Failed to ingest {file_path}: {e}")
            
    print("✅ Migration complete. PGVector database is populated.")
    
    # Optional: Delete old Chroma vectorstore
    chroma_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "rag", "vectorstore")
    if os.path.exists(chroma_dir):
        print("🗑️ Removing old Chroma vectorstore directory...")
        shutil.rmtree(chroma_dir, ignore_errors=True)
        print("Chroma directory removed.")

if __name__ == "__main__":
    migrate()
