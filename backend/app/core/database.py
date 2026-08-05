from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

Base = declarative_base()

def get_db_engine():
    try:
        engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
        return engine
    except Exception as e:
        print(f"Aviso: Não foi possível conectar ao PostgreSQL ({e}). Usando SQLite fallback.")
        return create_engine("sqlite:///storage.db", connect_args={"check_same_thread": False})

engine = get_db_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
