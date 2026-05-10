import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from langchain_groq import ChatGroq

class Settings(BaseSettings):
    GROQ_API_KEY: str = ""
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "ticket_db"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # RAG Settings
    CHROMA_PERSIST_DIRECTORY: str = "./rag/vectorstore"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def database_url(self) -> str:
        # Check for cloud deployment DATABASE_URL (Railway/Render)
        env_url = os.environ.get("DATABASE_URL")
        if env_url:
            # SQLAlchemy needs postgresql:// instead of postgres://
            if env_url.startswith("postgres://"):
                env_url = env_url.replace("postgres://", "postgresql://", 1)
            return env_url
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    @property
    def sync_database_url(self) -> str:
        # Needed for psycopg3 / PostgresSaver checkpointer
        url = self.database_url
        if url.startswith("postgresql://"):
            url = url.replace("postgresql://", "postgresql+psycopg://", 1)
        return url
    
    @property
    def sqlite_url(self) -> str:
        return "sqlite:///./ticket_db.sqlite"

settings = Settings()

def get_llm():
    model_name = "llama-3.3-70b-versatile"
    api_key = settings.GROQ_API_KEY
    
    return ChatGroq(
        model=model_name,
        temperature=0.1,
        max_tokens=1024,
        api_key=api_key if api_key else "dummy_key_to_avoid_init_error"
    )
